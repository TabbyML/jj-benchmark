import fs from 'fs/promises';
import path from 'path';

type TrialEntry = {
  jobName: string;
  trialName: string;
  trialDir: string;
  trajectoryJsonlPath: string;
  trajectoryIdPath: string;
};

type TaskTrialEntry = {
  job_name: string;
  trial_name: string;
  trajectory_id?: string;
  [key: string]: unknown;
};

const RETRY_ATTEMPTS = 3;
const RETRY_BASE_DELAY_MS = 700;

function getServerBaseUrl() {
  return process.env.CLIPS_BASE_URL || 'https://cc.getpochi.com';
}

function parseJsonLines(content: string): unknown[] {
  const lines = content.split(/\r?\n/).filter((line) => line.trim().length > 0);
  if (lines.length === 0) {
    throw new Error('Empty JSONL payload');
  }

  const parsed: unknown[] = [];
  for (const [index, line] of lines.entries()) {
    try {
      parsed.push(JSON.parse(line));
    } catch (_e) {
      throw new Error(`Invalid JSONL at line ${index + 1}`);
    }
  }

  return parsed;
}

function formatErrorMessage(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}

async function sleep(ms: number) {
  await new Promise((resolve) => setTimeout(resolve, ms));
}

async function postClipWithRetry(
  baseUrl: string,
  messages: unknown[],
  authorizationHeaderValue: string
): Promise<string> {
  const endpoint = `${baseUrl}/api/clips`;
  let lastError: string | null = null;

  for (let attempt = 1; attempt <= RETRY_ATTEMPTS; attempt++) {
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'authorization': authorizationHeaderValue,
        },
        body: JSON.stringify({ data: { messages } }),
      });
      if (!response.ok) {
        const text = await response.text();
        throw new Error(`HTTP ${response.status}: ${text || response.statusText}`);
      }

      const json = await response.json() as { id?: string };
      if (!json.id) {
        throw new Error('Response missing clip id');
      }

      return json.id;
    } catch (e) {
      const errorText = e instanceof Error ? e.message : String(e);
      lastError = errorText;
      console.error(`POST failed (attempt ${attempt}/${RETRY_ATTEMPTS}): ${errorText}`);
      if (attempt < RETRY_ATTEMPTS) {
        await sleep(RETRY_BASE_DELAY_MS * attempt);
      }
    }
  }

  throw new Error(lastError || 'Unknown error when posting clip');
}

async function getTrialEntries(jobsDir: string): Promise<TrialEntry[]> {
  const entries: TrialEntry[] = [];

  const jobs = await fs.readdir(jobsDir, { withFileTypes: true });
  for (const job of jobs) {
    if (!job.isDirectory()) continue;

    const jobName = job.name;
    const jobDir = path.join(jobsDir, jobName);
    const trials = await fs.readdir(jobDir, { withFileTypes: true });

    for (const trial of trials) {
      if (!trial.isDirectory()) continue;

      const trialName = trial.name;
      const trialDir = path.join(jobDir, trialName, 'agent', 'pochi');
      const trajectoryJsonlPath = path.join(trialDir, 'trajectory.jsonl');
      const trajectoryIdPath = path.join(trialDir, 'trajectory-id.txt');

      try {
        await fs.access(trajectoryJsonlPath);
      } catch (_e) {
        continue;
      }

      entries.push({
        jobName,
        trialName,
        trialDir,
        trajectoryJsonlPath,
        trajectoryIdPath,
      });
    }
  }

  // Keep ordering deterministic for repeatable runs.
  entries.sort((a, b) => a.trajectoryJsonlPath.localeCompare(b.trajectoryJsonlPath));
  return entries;
}

function getAuthorizationHeaderValue(): string {
  const internalApiKey = process.env.INTERNAL_API_KEY?.trim();
  if (internalApiKey) {
    return `x-api-key: ${internalApiKey}`;
  }

  throw new Error('Missing environment variable INTERNAL_API_KEY');
}

async function readTrajectoryId(idPath: string): Promise<string | null> {
  try {
    const content = await fs.readFile(idPath, 'utf-8');
    const id = content.trim();
    return id.length > 0 ? id : null;
  } catch (_e) {
    return null;
  }
}

async function writeTrajectoryId(idPath: string, clipId: string): Promise<void> {
  await fs.writeFile(idPath, `${clipId}\n`, 'utf-8');
}

function buildTrialKey(jobName: string, trialName: string): string {
  return `${jobName}::${trialName}`;
}

async function updateTasksJson(tasksPath: string, trajectoryIdByTrial: Map<string, string>): Promise<number> {
  const tasksRaw = await fs.readFile(tasksPath, 'utf-8');
  const parsed = JSON.parse(tasksRaw) as unknown;

  if (typeof parsed !== 'object' || parsed === null) {
    throw new Error(`Invalid tasks.json format: expected object at ${tasksPath}`);
  }

  const tasks = parsed as Record<string, unknown>;
  let updatedCount = 0;

  for (const taskEntries of Object.values(tasks)) {
    if (!Array.isArray(taskEntries)) {
      continue;
    }

    for (const item of taskEntries) {
      if (typeof item !== 'object' || item === null) {
        continue;
      }

      const trial = item as TaskTrialEntry;
      if (typeof trial.job_name !== 'string' || typeof trial.trial_name !== 'string') {
        continue;
      }

      const key = buildTrialKey(trial.job_name, trial.trial_name);
      const trajectoryId = trajectoryIdByTrial.get(key);
      if (!trajectoryId) {
        continue;
      }

      if (trial.trajectory_id !== trajectoryId) {
        trial.trajectory_id = trajectoryId;
        updatedCount++;
      }
    }
  }

  await fs.writeFile(tasksPath, `${JSON.stringify(tasks, null, 2)}\n`, 'utf-8');
  return updatedCount;
}

async function main() {
  const isForceMode = process.argv.includes('--force');
  const jobsDir = path.join(process.cwd(), '..', 'jobs');
  const tasksPath = path.join(process.cwd(), 'tasks.json');
  const baseUrl = getServerBaseUrl();
  console.log(`Post clips to ${baseUrl}`);
  let authorizationHeaderValue: string | null = null;

  let entries: TrialEntry[] = [];
  try {
    entries = await getTrialEntries(jobsDir);
  } catch (e) {
    console.error(`Error scanning jobs dir ${jobsDir}:`, e);
    process.exit(1);
  }

  let processed = 0;
  const trajectoryIdByTrial = new Map<string, string>();

  for (const entry of entries) {
    const existingTrajectoryId = isForceMode ? null : await readTrajectoryId(entry.trajectoryIdPath);
    const shouldSkip = !isForceMode && !!existingTrajectoryId;

    if (shouldSkip) {
      trajectoryIdByTrial.set(buildTrialKey(entry.jobName, entry.trialName), existingTrajectoryId);
      continue;
    }

    const content = await fs.readFile(entry.trajectoryJsonlPath, 'utf-8');
    let messages: unknown[];
    try {
      messages = parseJsonLines(content);
    } catch (error) {
      throw new Error(`${entry.jobName}/${entry.trialName}: ${formatErrorMessage(error)}`);
    }
    if (!authorizationHeaderValue) {
      authorizationHeaderValue = getAuthorizationHeaderValue();
    }
    const clipId = await postClipWithRetry(baseUrl, messages, authorizationHeaderValue);
    await fs.mkdir(entry.trialDir, { recursive: true });
    await writeTrajectoryId(entry.trajectoryIdPath, clipId);
    trajectoryIdByTrial.set(buildTrialKey(entry.jobName, entry.trialName), clipId);

    processed++;
  }

  const updatedTasksCount = await updateTasksJson(tasksPath, trajectoryIdByTrial);

  console.log(`Processed ${processed} trial(s).`);
  console.log(`Updated ${updatedTasksCount} trial(s) in ${tasksPath}.`);
}

main().catch((e) => {
  const errorText = formatErrorMessage(e);
  console.error(`Failed to compute trajectory id: ${errorText}`);
  process.exit(1);
});
