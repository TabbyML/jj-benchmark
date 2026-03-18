#!/usr/bin/env bun

import fs from 'fs/promises';
import path from 'path';

type TaskTrialEntry = {
  job_name?: unknown;
  trial_name?: unknown;
  trajectory_id?: unknown;
};

async function main() {
  const tasksPath = path.join(process.cwd(), 'site', 'tasks.json');
  const raw = await fs.readFile(tasksPath, 'utf-8');
  const parsed = JSON.parse(raw) as unknown;

  if (typeof parsed !== 'object' || parsed === null) {
    throw new Error(`Invalid tasks.json format: ${tasksPath}`);
  }

  const tasks = parsed as Record<string, unknown>;
  const missing: Array<{ taskName: string; jobName: string; trialName: string }> = [];

  for (const [taskName, entries] of Object.entries(tasks)) {
    if (!Array.isArray(entries)) {
      continue;
    }

    for (const entry of entries) {
      if (typeof entry !== 'object' || entry === null) {
        continue;
      }

      const trial = entry as TaskTrialEntry;
      const jobName = typeof trial.job_name === 'string' ? trial.job_name : 'unknown-job';
      const trialName = typeof trial.trial_name === 'string' ? trial.trial_name : 'unknown-trial';
      const trajectoryId = typeof trial.trajectory_id === 'string' ? trial.trajectory_id.trim() : '';

      if (!trajectoryId) {
        missing.push({ taskName, jobName, trialName });
      }
    }
  }

  if (missing.length > 0) {
    console.error(`Missing trajectory_id in ${missing.length} trial(s):`);
    const maxLines = 100;
    for (const item of missing.slice(0, maxLines)) {
      console.error(`- ${item.taskName}: ${item.jobName}/${item.trialName}`);
    }
    if (missing.length > maxLines) {
      console.error(`... and ${missing.length - maxLines} more`);
    }
    process.exit(1);
  }

  console.log('All trials have trajectory_id.');
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
