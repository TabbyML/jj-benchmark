import type { CSSProperties } from "react";
import tasksData from "@/tasks.json";
import { TrajectoryPage } from "./components/trajectory-page";
import zealtConfig from "@/../zealt.json";
import { redirect } from "next/navigation";
import { AlertTriangle, Check, HelpCircle, X as XIcon } from "lucide-react";


type RouteParams = {
  name: string;
  jobId: string;
};

type TrialEntry = {
  trial_name: string;
  job_name: string;
  agent: string;
  passed?: boolean;
  error?: boolean;
  latency_sec?: number | null;
  latency_breakdown?: {
    env_setup?: number | null;
    agent_setup?: number | null;
    agent_exec?: number | null;
    verifier?: number | null;
  };
  trajectory_id?: string;
  stderr_text?: string | null;
  stderr_line_count?: number;
  verifier_text?: string | null;
  verifier_line_count?: number;
};

function formatStartTime(jobName: string): string {
  const match = jobName.match(/^(\d{4})-(\d{2})-(\d{2})__(\d{2})-(\d{2})-(\d{2})$/);
  if (!match) {
    return "Unknown";
  }

  const [, year, month, day, hour, minute, second] = match;
  const localDate = new Date(Number(year), Number(month) - 1, Number(day), Number(hour), Number(minute), Number(second));
  if (Number.isNaN(localDate.getTime())) {
    return "Unknown";
  }

  return localDate.toLocaleString();
}

function formatStartTimeShort(jobName: string): string {
  const match = jobName.match(/^(\d{4})-(\d{2})-(\d{2})__(\d{2})-(\d{2})-(\d{2})$/);
  if (!match) {
    return "Unknown";
  }

  const [, year, month, day, hour, minute, second] = match;
  const localDate = new Date(Number(year), Number(month) - 1, Number(day), Number(hour), Number(minute), Number(second));
  if (Number.isNaN(localDate.getTime())) {
    return "Unknown";
  }

  const monthLabel = String(localDate.getMonth() + 1);
  const dayLabel = String(localDate.getDate());
  const hourLabel = String(localDate.getHours()).padStart(2, "0");
  const minuteLabel = String(localDate.getMinutes()).padStart(2, "0");
  return `${monthLabel}/${dayLabel} ${hourLabel}:${minuteLabel}`;
}

function formatDuration(durationSec: number | null | undefined): string {
  if (durationSec == null || Number.isNaN(durationSec)) {
    return "Unknown";
  }

  if (durationSec < 60) {
    return `${durationSec.toFixed(1)}s`;
  }

  const minutes = Math.floor(durationSec / 60);
  const seconds = durationSec % 60;
  return `${minutes}m ${seconds.toFixed(1)}s`;
}

function getTrialStatus(trial: TrialEntry | null): "error" | "passed" | "failed" | "unknown" {
  if (!trial) {
    return "unknown";
  }

  if (trial.error) {
    return "error";
  }

  if (trial.passed) {
    return "passed";
  }

  if (trial.passed === false) {
    return "failed";
  }

  return "unknown";
}

function getStatusMeta(status: "error" | "passed" | "failed" | "unknown") {
  if (status === "error") {
    return {
      label: "Error",
      className: "text-red-400",
      Icon: AlertTriangle,
    };
  }

  if (status === "passed") {
    return {
      label: "Passed",
      className: "text-emerald-400",
      Icon: Check,
    };
  }

  if (status === "failed") {
    return {
      label: "Failed",
      className: "text-amber-400",
      Icon: XIcon,
    };
  }

  return {
    label: "Unknown",
    className: "text-muted-foreground",
    Icon: HelpCircle,
  };
}

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

function getGithubOwnerRepo(): string {
  const repoUrl = zealtConfig.github_repo;
  const match = repoUrl.match(/github\.com\/(.+?\/[^/]+)/);
  return match ? match[1] : repoUrl;
}

function buildClipUrl(jobName: string, trialName: string, title: string): string {
  const ownerRepo = getGithubOwnerRepo();
  const url = new URL(`/f/raw.githubusercontent.com/${ownerRepo}/refs/heads/main/jobs/${jobName}/${trialName}/agent/pochi/trajectory.jsonl`, getServerBaseUrl());
  url.searchParams.set("title", title);
  url.searchParams.set("theme", "dark");
  return url.toString();
}

function isTrialEntry(value: unknown): value is TrialEntry {
  if (typeof value !== "object" || value === null) {
    return false;
  }

  const trial = value as Record<string, unknown>;
  if (
    typeof trial.trial_name !== "string" ||
    typeof trial.job_name !== "string" ||
    typeof trial.agent !== "string"
  ) {
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
  const headerTitle = `${resolvedParams.name}__${resolvedParams.jobId}`;
  const startedAt = trialEntry ? formatStartTime(trialEntry.job_name) : "Unknown";
  const startedAtShort = trialEntry ? formatStartTimeShort(trialEntry.job_name) : "Unknown";
  const executionDurationLabel = formatDuration(trialEntry?.latency_breakdown?.agent_exec ?? null);
  const verifyDurationLabel = formatDuration(trialEntry?.latency_breakdown?.verifier ?? null);
  const trialStatus = getTrialStatus(trialEntry);
  const statusMeta = getStatusMeta(trialStatus);
  const StatusIcon = statusMeta.Icon;
  const contentTopOffsetClassName = "top-36 sm:top-32 lg:top-28";
  
  const trajectoryUrl = clipId && trialEntry
    ? buildClipUrl(trialEntry.job_name, trialEntry.trial_name, resolvedParams.name)
    : null;
  
  // FIXME
  if (!trajectoryUrl) {
    redirect(fallbackUrl ?? '/tasks');
  }
  const stderrText = trialEntry?.stderr_text ?? null;
  const verifierText = trialEntry?.verifier_text ?? null;
  const pageThemeVars = {
    "--background": "oklch(0.268 0.004 106.643)",
    "--border": "oklch(0.362 0.01 106.893)",
  } as CSSProperties;

  return (
    <div style={pageThemeVars} className="w-full h-screen bg-background text-foreground font-sans selection:bg-primary/20 overflow-hidden">
      <div className="fixed inset-0 -z-10 h-full w-full bg-background bg-[radial-gradient(#2a2a2a_1px,transparent_1px)] [background-size:16px_16px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_70%,transparent_100%)] opacity-20 dark:opacity-40"></div>
      <div className="fixed inset-x-0 top-0 z-40 border-b border-border/50 bg-background/85 backdrop-blur-sm">
        <div className="mx-auto w-full max-w-[1400px] px-4 py-4 sm:px-7 lg:px-10">
          <div className="flex flex-col gap-1">
            <h1 className="truncate whitespace-nowrap font-bold text-2xl">
              {headerTitle}
            </h1>
            <div className="mt-2 text-xs sm:text-sm">
              <div className="grid grid-cols-2 gap-x-4 gap-y-1.5 sm:hidden">
                <div className={`font-medium ${statusMeta.className}`}>
                  Status: {statusMeta.label}
                </div>
                <div className="text-muted-foreground">Started: {startedAtShort}</div>
                <div className="text-muted-foreground">Execution: {executionDurationLabel}</div>
                <div className="text-muted-foreground">Test: {verifyDurationLabel}</div>
              </div>

              <div className="hidden items-center gap-4 sm:flex">
                <span className={`inline-flex shrink-0 items-center gap-1.5 font-medium ${statusMeta.className}`}>
                  <StatusIcon className="h-3.5 w-3.5" />
                  <span>Status: {statusMeta.label}</span>
                </span>
                <span className="text-muted-foreground">Started: {startedAt}</span>
                <span className="text-muted-foreground truncate">Execution: {executionDurationLabel}</span>
                <span className="text-muted-foreground truncate">Test: {verifyDurationLabel}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <TrajectoryPage
        trajectoryUrl={trajectoryUrl}
        fallbackUrl={fallbackUrl ?? ''}
        stderrText={stderrText}
        verifierText={verifierText}
        topOffsetClassName={contentTopOffsetClassName}
      />
    </div>
  );
}