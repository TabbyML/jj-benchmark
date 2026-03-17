import fs from 'fs/promises';
import path from 'path';

type StdoutFileEntry = {
  trialName: string;
  relativePath: string;
};

async function getStdoutFiles(dir: string): Promise<StdoutFileEntry[]> {
  const files: StdoutFileEntry[] = [];
  try {
    const jobs = await fs.readdir(dir, { withFileTypes: true });
    for (const job of jobs) {
      if (!job.isDirectory()) continue;
      const jobDir = path.join(dir, job.name);
      const trials = await fs.readdir(jobDir, { withFileTypes: true });
      for (const trial of trials) {
        if (!trial.isDirectory()) continue;
        const relativePath = path.join(job.name, trial.name, 'agent', 'pochi', 'stdout.txt');
        try {
          await fs.access(path.join(dir, relativePath));
          files.push({ trialName: trial.name, relativePath });
        } catch (e) {
          // stdout.txt doesn't exist in this trial dir
        }
      }
    }
  } catch (e) {
    console.error(`Error reading ${dir}:`, e);
  }
  return files;
}

function parseJsonLines(content: string, filePath: string): any[] {
  const lines = content.split(/\r?\n/).filter((line) => line.trim().length > 0);
  const parsed: any[] = [];
  for (const line of lines) {
    try {
      parsed.push(JSON.parse(line));
    } catch (e) {
      console.error(`Error parsing JSONL line in ${filePath}:`);
      // Any invalid line invalidates the whole JSONL payload
      return [];
    }
  }
  return parsed;
}

async function main() {
  const jobsDir = path.join(process.cwd(), '..', 'jobs');
  const stdoutFiles = await getStdoutFiles(jobsDir);

  const messages: Record<string, any[]> = {};

  for (const { trialName, relativePath } of stdoutFiles) {
    const fullPath = path.join(jobsDir, relativePath);
    let content = '';
    try {
      content = await fs.readFile(fullPath, 'utf-8');
    } catch (e) {
      console.error(`Error reading ${fullPath}:`, e);
      continue;
    }

    const parsed = parseJsonLines(content, fullPath);
    if (parsed.length === 0) {
      continue;
    }

    if (!messages[trialName]) {
      messages[trialName] = [];
    }

    messages[trialName].push(...parsed);
  }

  const outputPath = path.join(process.cwd(), 'messages.json');

  await fs.writeFile(outputPath, JSON.stringify(messages, null, 2));
  console.log(`Computed ${Object.keys(messages).length} trials into ${outputPath}`);
}

main().catch(console.error);
