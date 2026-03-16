import tasksData from "@/tasks.json";
import { TrajectoryPage } from "./components/trajectory-page";

type RouteParams = {
  name: string;
  jobName: string;
};

type TrialEntry = {
  trial_name: string;
  job_name: string;
};

function isTrialEntry(value: unknown): value is TrialEntry {
  if (typeof value !== "object" || value === null) {
    return false;
  }

  const trial = value as Record<string, unknown>;
  return typeof trial.trial_name === "string" && typeof trial.job_name === "string";
}

export const dynamicParams = false;

export function generateStaticParams(): RouteParams[] {
  const params: RouteParams[] = [];

  for (const trials of Object.values(tasksData as Record<string, unknown>)) {
    if (!Array.isArray(trials)) {
      continue;
    }

    for (const trial of trials) {
      if (!isTrialEntry(trial)) {
        continue;
      }

      params.push({
        name: trial.trial_name,
        jobName: trial.job_name,
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

  return (
    <div className="w-full h-screen bg-background text-foreground font-sans selection:bg-primary/20 overflow-hidden">
      <div className="fixed inset-0 -z-10 h-full w-full bg-background bg-[radial-gradient(#2a2a2a_1px,transparent_1px)] [background-size:16px_16px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_70%,transparent_100%)] opacity-20 dark:opacity-40"></div>
      <TrajectoryPage
        name={resolvedParams.name}
        jobName={resolvedParams.jobName}
      />
    </div>
  );
}