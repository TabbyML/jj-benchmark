import fs from 'fs/promises';
import path from 'path';

type TrialEntry = {
  jobName: string;
  trialName: string;
  trajectoryJsonlPath: string;
};

type CheckError = {
  jobName: string;
  trialName: string;
  reason: string;
};

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

      try {
        await fs.access(trajectoryJsonlPath);
      } catch (_e) {
        continue;
      }

      entries.push({ jobName, trialName, trajectoryJsonlPath });
    }
  }

  entries.sort((a, b) => a.trajectoryJsonlPath.localeCompare(b.trajectoryJsonlPath));
  return entries;
}

function checkTrajectory(content: string): string | null {
  const lines = content.split(/\r?\n/).filter((line) => line.trim().length > 0);
  if (lines.length === 0) {
    return 'Empty JSONL file';
  }

  for (const [index, line] of lines.entries()) {
    try {
      JSON.parse(line);
    } catch (_e) {
      return `Invalid JSON on line ${index + 1}`;
    }
  }

  return null;
}

async function main() {
  const jobsDir = path.join(process.cwd(), '..', 'jobs');

  let entries: TrialEntry[] = [];
  try {
    entries = await getTrialEntries(jobsDir);
  } catch (e) {
    console.error(`Error scanning jobs dir ${jobsDir}:`, e);
    process.exit(1);
  }

  const errors: CheckError[] = [];

  for (const entry of entries) {
    let content: string;
    try {
      content = await fs.readFile(entry.trajectoryJsonlPath, 'utf-8');
    } catch (e) {
      errors.push({
        jobName: entry.jobName,
        trialName: entry.trialName,
        reason: e instanceof Error ? e.message : String(e),
      });
      continue;
    }

    const reason = checkTrajectory(content);
    if (reason !== null) {
      errors.push({ jobName: entry.jobName, trialName: entry.trialName, reason });
    }
  }

  const total = entries.length;
  const errorCount = errors.length;

  console.log(`Total: ${total}, Errored: ${errorCount}`);

  if (errorCount > 0) {
    const shown = errors.slice(0, 10);
    console.log(`\nErrored trajectories (showing ${shown.length} of ${errorCount}):`);
    for (const err of shown) {
      console.log(`  ${err.jobName}/${err.trialName}: ${err.reason}`);
    }
  }

  if (errorCount > 0) {
    process.exit(1);
  }
}

main().catch((e) => {
  console.error('Unexpected error:', e instanceof Error ? e.message : String(e));
  process.exit(1);
});
