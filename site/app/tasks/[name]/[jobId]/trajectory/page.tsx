import tasksData from "@/tasks.json";
import { TrajectoryPage } from "./components/trajectory-page";
import zealtConfig from "@/../zealt.json";


type RouteParams = {
  name: string;
  jobId: string;
};

type TrialEntry = {
  trial_name: string;
  job_name: string;
  trajectory_id?: string;
};

function buildFallbackUrl(jobName: string, trialName: string) {
  return `${zealtConfig.github_repo}/blob/main/jobs/${jobName}/${trialName}/result.json`
}

function splitTrialName(trialName: string): { taskName: string; jobId: string } | null {
  const separatorIndex = trialName.lastIndexOf("__");
  if (separatorIndex <= 0 || separatorIndex >= trialName.length - 2) {
    return null;
  }

  return {
    taskName: trialName.slice(0, separatorIndex),
    jobId: trialName.slice(separatorIndex + 2),
  };
}

function getServerBaseUrl() {
  return process.env.CLIPS_BASE_URL || 'https://cc.getpochi.com';
}

function buildClipUrl(clipId: string, title: string): string {
  const url = new URL(`/e/${clipId}`, getServerBaseUrl());
  url.searchParams.set("title", title);
  url.searchParams.set("theme", "dark");
  return url.toString();
}

function isTrialEntry(value: unknown): value is TrialEntry {
  if (typeof value !== "object" || value === null) {
    return false;
  }

  const trial = value as Record<string, unknown>;
  if (typeof trial.trial_name !== "string" || typeof trial.job_name !== "string") {
    return false;
  }

  return true;
}

function findTrialEntry(taskName: string, jobId: string): TrialEntry | null {
  for (const task of Object.values(tasksData as Record<string, unknown>)) {
    if (typeof task !== "object" || task === null) {
      continue;
    }

    const trials = (task as { trials?: unknown }).trials;
    if (!Array.isArray(trials)) {
      continue;
    }

    for (const trial of trials) {
      if (!isTrialEntry(trial)) {
        continue;
      }

      const splitName = splitTrialName(trial.trial_name);
      if (!splitName) {
        continue;
      }

      if (splitName.taskName === taskName && splitName.jobId === jobId) {
        return trial;
      }
    }
  }

  return null;
}

export const dynamicParams = false;

export function generateStaticParams(): RouteParams[] {
  const params: RouteParams[] = [];

  for (const task of Object.values(tasksData as Record<string, unknown>)) {
    if (typeof task !== "object" || task === null) {
      continue;
    }

    const trials = (task as { trials?: unknown }).trials;
    if (!Array.isArray(trials)) {
      continue;
    }

    for (const trial of trials) {
      if (!isTrialEntry(trial)) {
        continue;
      }

      const splitName = splitTrialName(trial.trial_name);
      if (!splitName) {
        continue;
      }

      params.push({
        name: splitName.taskName,
        jobId: splitName.jobId,
      });
    }
  }

  return params;
}

export default async function TrajectoryRoutePage({
  params,
}: {
  params: Promise<RouteParams>;
}) {
  const resolvedParams = await params;

  const trialEntry = findTrialEntry(resolvedParams.name, resolvedParams.jobId);
  const fallbackUrl = trialEntry
    ? buildFallbackUrl(trialEntry.job_name, trialEntry.trial_name)
    : null;
  const clipId = trialEntry?.trajectory_id?.trim() || null;
  const trajectoryUrl = clipId ? buildClipUrl(clipId, resolvedParams.name) : null;

  return (
    <div className="w-full h-screen bg-background text-foreground font-sans selection:bg-primary/20 overflow-hidden">
      <div className="fixed inset-0 -z-10 h-full w-full bg-background bg-[radial-gradient(#2a2a2a_1px,transparent_1px)] [background-size:16px_16px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_70%,transparent_100%)] opacity-20 dark:opacity-40"></div>
      <TrajectoryPage
        title={resolvedParams.name}
        trajectoryUrl={trajectoryUrl}
        fallbackUrl={fallbackUrl ?? ""}
      />
    </div>
  );
}