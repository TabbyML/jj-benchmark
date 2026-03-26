import fs from 'fs/promises';
import path from 'path';

type TaskTrial = {
  job_name: string;
  trial_name: string;
  agent: string;
  model: string;
  provider: string;
  passed: boolean;
  reward: number | null;
  error: boolean;
  latency_sec: number | null;
  latency_breakdown: {
    env_setup: number | null;
    agent_setup: number | null;
    agent_exec: number | null;
    verifier: number | null;
  };
  tokens: {
    input: number;
    output: number;
    cache: number;
  };
};

type TaskRecord = {
  instruction: string;
  trials: TaskTrial[];
};

type ParsedResult = {
  task_name?: string;
  started_at?: string;
  finished_at?: string;
  environment_setup?: { started_at?: string; finished_at?: string };
  agent_setup?: { started_at?: string; finished_at?: string };
  agent_execution?: { started_at?: string; finished_at?: string };
  verifier?: { started_at?: string; finished_at?: string };
  verifier_result?: { rewards?: { reward?: number } };
  exception_info?: unknown;
  config?: { agent?: { model_name?: string; name?: string } };
  agent_info?: { model_info?: { name?: string; provider?: string }; name?: string };
  trial_name?: string;
  agent_result?: {
    n_input_tokens?: number;
    n_output_tokens?: number;
    n_cache_tokens?: number;
  };
};

async function getResultFiles(dir: string): Promise<string[]> {
  const files: string[] = [];
  try {
    const jobs = await fs.readdir(dir, { withFileTypes: true });
    for (const job of jobs) {
      if (!job.isDirectory()) continue;
      const jobDir = path.join(dir, job.name);
      const trials = await fs.readdir(jobDir, { withFileTypes: true });
      for (const trial of trials) {
        if (!trial.isDirectory()) continue;
        const resultPath = path.join(job.name, trial.name, 'result.json');
        try {
          await fs.access(path.join(dir, resultPath));
          files.push(resultPath);
        } catch {
          // result.json doesn't exist in this trial dir
        }
      }
    }
  } catch (e) {
    console.error(`Error reading ${dir}:`, e);
  }
  return files;
}

async function readTaskInstruction(repoRoot: string, taskName: string): Promise<string> {
  const instructionPath = path.join(repoRoot, 'tasks', taskName, 'instruction.md');
  try {
    return await fs.readFile(instructionPath, 'utf-8');
  } catch (_e) {
    return '';
  }
}

async function countPendingSampleCases(repoRoot: string): Promise<number> {
  const pendingTasksDir = path.join(repoRoot, 'scratchpad', 'pending-tasks');
  try {
    const entries = await fs.readdir(pendingTasksDir, { withFileTypes: true });
    return entries.filter((entry) => entry.isDirectory()).length;
  } catch (_e) {
    return 0;
  }
}

async function main() {
  const siteRoot = process.cwd();
  const repoRoot = path.join(siteRoot, '..');
  const jobsDir = path.join(repoRoot, 'jobs');
  const resultFiles = await getResultFiles(jobsDir);
  const pendingSampleCases = await countPendingSampleCases(repoRoot);

  const tasks: Record<string, TaskRecord> = {};

  for (const file of resultFiles) {
    const fullPath = path.join(jobsDir, file);
    const content = await fs.readFile(fullPath, 'utf-8');
    let data: ParsedResult;
    try {
      data = JSON.parse(content) as ParsedResult;
    } catch (e) {
      console.error(`Error parsing ${fullPath}:`, e);
      continue;
    }

    const taskName = data.task_name;
    if (!taskName) continue;

    if (!tasks[taskName]) {
      tasks[taskName] = {
        instruction: await readTaskInstruction(repoRoot, taskName),
        trials: [],
      };
    }

    const startedAt = data.started_at ? new Date(data.started_at).getTime() : 0;
    const finishedAt = data.finished_at ? new Date(data.finished_at).getTime() : 0;
    const latencySec = startedAt && finishedAt ? (finishedAt - startedAt) / 1000 : null;

    const getDuration = (start?: string, end?: string) => {
      if (!start || !end) return null;
      return (new Date(end).getTime() - new Date(start).getTime()) / 1000;
    };

    const envSetup = getDuration(data.environment_setup?.started_at, data.environment_setup?.finished_at);
    const agentSetup = getDuration(data.agent_setup?.started_at, data.agent_setup?.finished_at);
    const agentExec = getDuration(data.agent_execution?.started_at, data.agent_execution?.finished_at);
    const verifierExec = getDuration(data.verifier?.started_at, data.verifier?.finished_at);

    const reward = data.verifier_result?.rewards?.reward;
    const passed = reward === 1.0;
    const hasError = !!data.exception_info;

    const model = data.config?.agent?.model_name || data.agent_info?.model_info?.name || 'unknown';
    const provider = data.agent_info?.model_info?.provider || 'unknown';
    
    const agentName = data.config?.agent?.name || data.agent_info?.name || 'unknown';

    // Extract job directory name (e.g., 2026-03-08__16-54-33)
    const jobName = file.split('/')[0] || file.split('\\')[0];
    const trialName = data.trial_name || 'unknown-trial';

    tasks[taskName].trials.push({
      job_name: jobName,
      trial_name: trialName,
      agent: agentName,
      model: model,
      provider: provider,
      passed,
      reward: reward !== undefined ? reward : null,
      error: hasError,
      latency_sec: latencySec,
      latency_breakdown: {
        env_setup: envSetup,
        agent_setup: agentSetup,
        agent_exec: agentExec,
        verifier: verifierExec
      },
      tokens: {
        input: data.agent_result?.n_input_tokens || 0,
        output: data.agent_result?.n_output_tokens || 0,
        cache: data.agent_result?.n_cache_tokens || 0,
      },
    });
  }

  const outputPath = path.join(siteRoot, '../.zealt/tasks.json');
  const pendingTasksOutputPath = path.join(siteRoot, '../.zealt/pending-tasks.json');
  
  await fs.writeFile(outputPath, JSON.stringify(tasks, null, 2));
  await fs.writeFile(
    pendingTasksOutputPath,
    JSON.stringify({ 'pending-tasks': pendingSampleCases }, null, 2),
  );
  console.log(`Computed ${Object.keys(tasks).length} tasks into ${outputPath}`);
  console.log(`Computed ${pendingSampleCases} pending sample cases into ${pendingTasksOutputPath}`);
}

main().catch(console.error);
