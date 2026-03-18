import fs from 'fs/promises';
import path from 'path';

async function readTrajectoryId(jobsDir: string, jobName: string, trialName: string): Promise<string | null> {
  const trajectoryIdPath = path.join(jobsDir, jobName, trialName, 'agent', 'pochi', 'trajectory-id.txt');
  try {
    const content = await fs.readFile(trajectoryIdPath, 'utf-8');
    const id = content.trim();
    return id.length > 0 ? id : null;
  } catch (_e) {
    return null;
  }
}

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
        } catch (e) {
          // result.json doesn't exist in this trial dir
        }
      }
    }
  } catch (e) {
    console.error(`Error reading ${dir}:`, e);
  }
  return files;
}

async function main() {
  const jobsDir = path.join(process.cwd(), '..', 'jobs');
  const resultFiles = await getResultFiles(jobsDir);

  const tasks: Record<string, any[]> = {};

  for (const file of resultFiles) {
    const fullPath = path.join(jobsDir, file);
    const content = await fs.readFile(fullPath, 'utf-8');
    let data: any;
    try {
      data = JSON.parse(content);
    } catch (e) {
      console.error(`Error parsing ${fullPath}:`, e);
      continue;
    }

    const taskName = data.task_name;
    if (!taskName) continue;

    if (!tasks[taskName]) {
      tasks[taskName] = [];
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
    const provider = data.agent_info?.model_info?.provider;
    
    const agentName = data.config?.agent?.name || data.agent_info?.name || 'unknown';

    // Extract job directory name (e.g., 2026-03-08__16-54-33)
    const jobName = file.split('/')[0] || file.split('\\')[0];
    const trialName = data.trial_name;
    const trajectoryId = trialName ? await readTrajectoryId(jobsDir, jobName, trialName) : null;

    tasks[taskName].push({
      job_name: jobName,
      trial_name: trialName,
      ...(trajectoryId ? { trajectory_id: trajectoryId } : {}),
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
      }
    });
  }

  const outputPath = path.join(process.cwd(), 'tasks.json');
  
  await fs.writeFile(outputPath, JSON.stringify(tasks, null, 2));
  console.log(`Computed ${Object.keys(tasks).length} tasks into ${outputPath}`);
}

main().catch(console.error);
