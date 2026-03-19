"use client";

import { useState, useMemo, useEffect, Suspense, useCallback } from "react";
import {
  Check,
  X as XIcon,
  Search,
  AlertTriangle,
  ArrowUpDown,
  ArrowUp,
  ArrowDown,
  Filter,
  X,
  ExternalLink,
} from "lucide-react";
import Link from "next/link";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import tasksDataRaw from "../../tasks.json";
import zealtConfig from "../../../zealt.json";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import {
  Drawer,
  DrawerContent,
  DrawerDescription,
  DrawerHeader,
  DrawerTitle,
} from "@/components/ui/drawer";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { MultiSelect } from "./components/multi-select";
import { BackToTop } from "./components/back-to-top";


function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Convert object to array and sort by task name
const tasksData = Object.entries(tasksDataRaw).map(([taskName, { trials, instruction }]) => {
  return {
    taskName,
    instruction,
    trials: (trials as any[]).map(t => {
      const trialNameParts = String(t.trial_name ?? "").split("__");
      const taskName = trialNameParts[0] || "";
      const jobId = trialNameParts[trialNameParts.length - 1] || "";

      return {
        ...t,
        model: t.model.split('/').pop() || t.model,
        agent: t.agent.charAt(0).toUpperCase() + t.agent.slice(1),
        exec_duration: t.latency_breakdown?.agent_exec || t.latency_sec || 0,
        taskName,
        jobId,
      };
    }),
  };
}).sort((a, b) => a.taskName.localeCompare(b.taskName));

const allTrialsFlat = tasksData.flatMap(task =>
  task.trials.map(trial => ({
    taskName: task.taskName,
    ...trial
  }))
);

const allModels = Array.from(new Set(allTrialsFlat.map(tr => tr.model)));
const allCombos = Array.from(new Set(allTrialsFlat.map(tr => `${tr.model} (${tr.agent})`))).sort();

function useMediaQuery(query: string) {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    setMatches(media.matches);

    const listener = (event: MediaQueryListEvent) => setMatches(event.matches);
    media.addEventListener("change", listener);

    return () => media.removeEventListener("change", listener);
  }, [query]);

  return matches;
}

function TasksContent() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const queryQ = searchParams.get("q") || "";
  const queryStatusStr = searchParams.get("status") || "";
  const queryModelStr = searchParams.get("model") || "";
  const queryAgentStr = searchParams.get("agent") || "";
  const querySort = searchParams.get("sort") || "default";
  const queryOrder = searchParams.get("order") || "asc";

  const selectedStatuses = queryStatusStr ? queryStatusStr.split(",") : [];
  const selectedModels = queryModelStr ? queryModelStr.split(",") : [];
  const selectedAgents = queryAgentStr ? queryAgentStr.split(",") : [];

  const [searchQuery, setSearchQuery] = useState(queryQ);
  const [selectedTask, setSelectedTask] = useState<string | null>(null);
  const [isInstructionOpen, setIsInstructionOpen] = useState(false);
  const isDesktop = useMediaQuery("(min-width: 1024px)");

  const hasActiveFilters = selectedStatuses.length > 0 || selectedModels.length > 0 || selectedAgents.length > 0 || searchQuery !== "" || querySort !== "default";

  const updateParams = useCallback((updates: Record<string, string | null>) => {
    const params = new URLSearchParams(searchParams.toString());
    Object.entries(updates).forEach(([key, value]) => {
      if (value === null || value === "" || value === "all" || (key === "sort" && value === "default")) {
        params.delete(key);
      } else {
        params.set(key, value);
      }
    });
    const nextQuery = params.toString();
    const currentQuery = searchParams.toString();
    if (nextQuery === currentQuery) {
      return;
    }

    const nextUrl = nextQuery ? `${pathname}?${nextQuery}` : pathname;
    router.replace(nextUrl, { scroll: false });
  }, [pathname, router, searchParams]);

  // Debounce search query to URL
  useEffect(() => {
    if (searchQuery === queryQ) {
      return;
    }

    const timer = setTimeout(() => {
      updateParams({ q: searchQuery });
    }, 300);
    return () => clearTimeout(timer);
  }, [queryQ, searchQuery, updateParams]);

  const activeCombos = useMemo(() => {
    const combos = allCombos.filter(combo => {
      const [model, agentStr] = combo.split(" (");
      const agent = agentStr.slice(0, -1);

      if (selectedModels.length !== 1) {
        if (selectedModels.length > 0 && !selectedModels.includes(model)) return false;
      }

      if (selectedAgents.length > 0 && !selectedAgents.includes(agent.toLowerCase())) return false;
      return true;
    });

    if (selectedModels.length === 1) {
      const selectedModel = selectedModels[0];
      combos.sort((a, b) => {
        const aModel = a.split(" (")[0];
        const bModel = b.split(" (")[0];
        const aIsSelected = aModel === selectedModel;
        const bIsSelected = bModel === selectedModel;
        if (aIsSelected && !bIsSelected) return -1;
        if (!aIsSelected && bIsSelected) return 1;
        return a.localeCompare(b);
      });
    }

    return combos;
  }, [selectedModels.join(","), selectedAgents.join(",")]);

  const filteredAndSortedTasks = useMemo(() => {
    const result = tasksData.map(task => {
      const comboMap: Record<string, any> = {};
      let hasMatchingTrial = false;
      let selectedModelMatchesStatus = false;
      let hasSelectedModelTrial = false;

      task.trials.forEach(trial => {
        const comboKey = `${trial.model} (${trial.agent})`;
        if (!activeCombos.includes(comboKey)) return;

        let matchesStatus = true;
        if (selectedStatuses.length > 0) {
          if (selectedStatuses.includes("passed") && trial.passed) {
            matchesStatus = true;
          } else if (selectedStatuses.includes("failed") && !trial.passed && !trial.error) {
            matchesStatus = true;
          } else if (selectedStatuses.includes("error") && trial.error) {
            matchesStatus = true;
          } else {
            matchesStatus = false;
          }
        }

        if (selectedModels.length === 1 && trial.model === selectedModels[0]) {
          hasSelectedModelTrial = true;
          if (matchesStatus) {
            selectedModelMatchesStatus = true;
          }
        }

        if (selectedModels.length === 1) {
          comboMap[comboKey] = trial;
        } else {
          if (matchesStatus) {
            comboMap[comboKey] = trial;
            hasMatchingTrial = true;
          }
        }
      });

      if (selectedModels.length === 1) {
        if (selectedStatuses.length > 0) {
          hasMatchingTrial = selectedModelMatchesStatus;
        } else {
          hasMatchingTrial = hasSelectedModelTrial;
        }
      }

      const avgDuration = Object.values(comboMap).length > 0
        ? Object.values(comboMap).reduce((sum, t) => sum + t.exec_duration, 0) / Object.values(comboMap).length
        : 0;

      return {
        taskName: task.taskName,
        comboMap,
        hasMatchingTrial,
        avgDuration
      };
    }).filter(task => {
      if (!task.hasMatchingTrial) return false;
      if (searchQuery && !task.taskName.toLowerCase().includes(searchQuery.toLowerCase())) return false;
      return true;
    });

    result.sort((a, b) => {
      if (querySort === "latency") {
        return queryOrder === "asc" ? a.avgDuration - b.avgDuration : b.avgDuration - a.avgDuration;
      } else {
        // default sort by taskName
        return queryOrder === "asc"
          ? a.taskName.localeCompare(b.taskName)
          : b.taskName.localeCompare(a.taskName);
      }
    });

    return result;
  }, [searchQuery, selectedStatuses.join(","), activeCombos, querySort, queryOrder, selectedModels.join(",")]);

  const toggleSort = (field: string) => {
    if (querySort === field) {
      if (queryOrder === "asc") {
        updateParams({ order: "desc" });
      } else {
        updateParams({ sort: "default", order: null });
      }
    } else {
      updateParams({ sort: field, order: "asc" });
    }
  };

  const renderSortIcon = (field: string) => {
    if (querySort !== field) return <ArrowUpDown className="w-3 h-3 opacity-30" />;
    return queryOrder === "asc" ? <ArrowUp className="w-3 h-3" /> : <ArrowDown className="w-3 h-3" />;
  };

  const selectedTaskInstructionUrl = selectedTask
    ? `${zealtConfig.github_repo}/tree/main/tasks/${selectedTask}/instruction.md`
    : "";

  const selectedTaskInstruction = selectedTask
    ? tasksData.find(task => task.taskName === selectedTask)?.instruction || ""
    : "";

  const instructionBody = (
    <>
      <div className="min-h-0 flex-1 overflow-y-auto overflow-x-hidden px-5 sm:px-7 py-4 sm:py-5">
        {selectedTask ? (
          selectedTaskInstruction ? (
            <pre className="m-0 p-0 text-xs sm:text-sm leading-6 sm:leading-7 text-foreground/95 whitespace-pre-wrap wrap-break-word font-mono">
              {selectedTaskInstruction}
            </pre>
          ) : (
            <div className="rounded-lg border border-border/60 bg-secondary/20 px-4 py-3 text-sm text-muted-foreground">
              This task has no instruction content.
            </div>
          )
        ) : (
          <Skeleton className="h-28 w-full" />
        )}
      </div>

      <div className="shrink-0 border-t border-border/60 px-5 sm:px-7 py-3 bg-card/80">
        <Button variant="outline" asChild className="h-8 w-full text-xs sm:h-9 sm:w-auto sm:text-sm">
          <a
            href={selectedTaskInstructionUrl}
            target="_blank"
            rel="noopener noreferrer"
          >
            <ExternalLink className="h-4 w-4" />
            Open instruction.md
          </a>
        </Button>
      </div>
    </>
  );

  return (
    <div className="container mx-auto px-4 sm:px-8 lg:px-12 py-8 max-w-screen-2xl h-[100dvh] flex flex-col overflow-hidden">
      {/* Header Section */}
      <div className="mb-6 space-y-4 shrink-0">
        <div className="flex items-center gap-4">
          <Link href="/" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
            &larr; Back to Leaderboard
          </Link>
        </div>
        <div>
          <h1 className="text-4xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-b from-foreground to-foreground/50">
            Task
          </h1>
          <p className="text-muted-foreground max-w-2xl leading-relaxed mt-2">
            Detailed breakdown of individual task performance across different models.
          </p>
        </div>
      </div>

      {/* Filters & Search */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 p-4 rounded-xl border border-border bg-card/50 backdrop-blur-sm shadow-sm transition-all shrink-0">
        <div className="flex flex-wrap items-center gap-4 w-full md:w-auto">
          <div
            className={cn(
              "flex items-center justify-center w-9 h-9 rounded-lg transition-colors shrink-0",
              hasActiveFilters ? "bg-primary/10 text-primary" : "bg-secondary/50 text-muted-foreground"
            )}
            title="Filters"
          >
            <Filter className="w-4 h-4" />
          </div>

          <div className="flex-1 grid grid-cols-2 sm:flex sm:flex-wrap gap-2 sm:gap-4">
            <MultiSelect
              title="Status"
              options={["passed", "failed", "error"]}
              selected={selectedStatuses}
              onChange={(vals) => updateParams({ status: vals.length > 0 ? vals.join(",") : null })}
              className="w-full sm:w-[140px]"
            />

            <MultiSelect
              title="Models"
              options={allModels}
              selected={selectedModels}
              onChange={(vals) => updateParams({ model: vals.length > 0 ? vals.join(",") : null })}
              className="w-full sm:min-w-[180px] sm:w-auto"
            />
          </div>

          {hasActiveFilters && (
            <button
              type="button"
              onClick={() => {
                setSearchQuery("");
                router.replace(pathname, { scroll: false });
              }}
              className="flex h-9 items-center justify-center gap-1.5 px-4 text-sm font-medium text-foreground bg-secondary hover:bg-secondary/80 border border-border shadow-sm rounded-md transition-colors w-full sm:w-auto ml-auto md:ml-0 cursor-pointer"
            >
              <X className="w-4 h-4" />
              Clear Filters
            </button>
          )}
        </div>

        <div className="relative w-full md:w-72">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search tasks..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-background border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
          />
        </div>
      </div>

      {/* Task List */}
      <div className="rounded-xl border border-border bg-card/50 backdrop-blur-sm shadow-sm overflow-hidden animate-in fade-in duration-500 relative flex flex-col max-h-full pb-1">
        {filteredAndSortedTasks.length === 0 ? (
          <div className="text-center py-12 text-muted-foreground flex-1 flex items-center justify-center">
            No tasks found matching your filters
          </div>
        ) : (
          <div className="overflow-auto relative custom-scrollbar">
            <table className="w-full text-sm text-left border-collapse">
              <thead className="sticky top-0 z-30 bg-secondary/95 backdrop-blur text-muted-foreground font-medium border-b border-border select-none shadow-sm">
                <tr>
                  <th
                    className="md:sticky left-0 z-40 bg-transparent md:bg-[#f6f6f6] dark:md:bg-[#0f0f0f] border-r border-border/50 px-3 sm:px-6 py-3 w-[200px] min-w-[200px] max-w-[200px] md:w-[350px] md:min-w-[350px] md:max-w-[350px] cursor-pointer hover:bg-secondary/50 hover:text-foreground transition-colors group md:shadow-[1px_0_0_rgba(0,0,0,0.05)]"
                    onClick={() => toggleSort("taskName")}
                  >
                    <div className="flex items-center gap-1 sm:gap-2">
                      <span className="truncate">Task Name ({filteredAndSortedTasks.length} tasks)</span>
                      {renderSortIcon("taskName")}
                    </div>
                  </th>
                  {activeCombos.map(combo => (
                    <th key={combo} className="px-3 sm:px-6 py-3 min-w-[120px] md:min-w-[150px] text-left border-l border-border/50">
                      <div className="flex flex-col items-start">
                        <span className="text-foreground font-medium truncate max-w-[100px] md:max-w-[130px]" title={combo.split(' (')[0]}>
                          {combo.split(' (')[0]}
                        </span>
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-border/30">
                {filteredAndSortedTasks.map((task) => (
                  <tr
                    key={task.taskName}
                    className="hover:bg-secondary/30 even:bg-secondary/5 transition-colors duration-200 group"
                  >
                    <td className="md:sticky left-0 z-20 bg-background border-r border-border/50 p-0 font-mono w-[200px] min-w-[200px] max-w-[200px] md:w-[350px] md:min-w-[350px] md:max-w-[350px] md:shadow-[1px_0_0_rgba(0,0,0,0.05)]">
                      <button
                        type="button"
                        onClick={() => {
                          setSelectedTask(task.taskName);
                          setIsInstructionOpen(true);
                        }}
                        className="group/task flex items-center gap-2 px-3 sm:px-6 py-2 w-full h-full text-foreground hover:text-primary transition-colors focus:outline-none bg-transparent group-even:bg-secondary/5 group-hover:bg-secondary/30 cursor-pointer text-left"
                        title={`View ${task.taskName} instruction`}
                      >
                        <span className="truncate w-full block group-hover/task:underline text-xs md:text-sm">
                          {task.taskName}
                        </span>
                      </button>
                    </td>
                    {activeCombos.map(combo => {
                      const trial = task.comboMap[combo];
                      return (
                        <td key={combo} className="p-0 border-l border-border/50 h-full relative min-w-[120px] md:min-w-[150px] z-10">
                          {trial ? (
                            <HoverCard openDelay={200} closeDelay={0}>
                              <HoverCardTrigger asChild>
                                <Link 
                                  href={`/tasks/${encodeURIComponent(trial.taskName)}/${encodeURIComponent(trial.jobId)}/trajectory`}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="absolute inset-0 flex items-center justify-start gap-1.5 md:gap-2 px-3 sm:px-6 w-full h-full cursor-pointer hover:bg-secondary/50 transition-colors group/cell focus:outline-none text-left bg-transparent border-none m-0 p-0"
                                >
                                  {trial.error ? (
                                    <AlertTriangle className="w-3.5 h-3.5 md:w-4 md:h-4 text-red-500/90 shrink-0" />
                                  ) : trial.passed ? (
                                    <Check className="w-3.5 h-3.5 md:w-4 md:h-4 text-emerald-500/90 shrink-0" strokeWidth={3} />
                                  ) : (
                                    <XIcon className="w-3.5 h-3.5 md:w-4 md:h-4 text-amber-500/90 shrink-0" strokeWidth={3} />
                                  )}
                                  <span className="font-mono text-xs md:text-sm text-muted-foreground/80 group-hover/cell:text-foreground group-hover/cell:underline transition-colors">
                                    {trial.exec_duration ? `${trial.exec_duration.toFixed(1)}s` : '-'}
                                  </span>
                                </Link>
                              </HoverCardTrigger>
                              <HoverCardContent side="top" align="center" className="w-64 p-4 bg-popover shadow-xl border-border z-50">
                                <div className="flex items-center gap-2 mb-3 pb-3 border-b border-border/50">
                                  {trial.error ? (
                                    <><AlertTriangle className="w-4 h-4 text-red-500" /><span className="font-medium text-red-500">Error</span></>
                                  ) : trial.passed ? (
                                    <><Check className="w-4 h-4 text-emerald-500" strokeWidth={3} /><span className="font-medium text-emerald-500">Passed</span></>
                                  ) : (
                                    <><XIcon className="w-4 h-4 text-amber-500" strokeWidth={3} /><span className="font-medium text-amber-500">Failed</span></>
                                  )}
                                </div>
                                {trial.latency_breakdown ? (
                                  <div className="space-y-2.5 text-xs text-popover-foreground text-left">
                                    <div className="flex justify-between items-center">
                                      <span className="text-muted-foreground">Setup Environment</span>
                                      <span className="font-mono">{trial.latency_breakdown.env_setup?.toFixed(1) || '-'}s</span>
                                    </div>
                                    <div className="flex justify-between items-center">
                                      <span className="text-muted-foreground">Setup</span>
                                      <span className="font-mono">{trial.latency_breakdown.agent_setup?.toFixed(1) || '-'}s</span>
                                    </div>
                                    <div className="flex justify-between items-center font-medium bg-secondary/40 py-1.5 px-2 -mx-2 rounded">
                                      <span className="text-foreground">Execution</span>
                                      <span className="font-mono text-primary">{trial.latency_breakdown.agent_exec?.toFixed(1) || '-'}s</span>
                                    </div>
                                    <div className="flex justify-between items-center">
                                      <span className="text-muted-foreground">Verify Result</span>
                                      <span className="font-mono">{trial.latency_breakdown.verifier?.toFixed(1) || '-'}s</span>
                                    </div>
                                  </div>
                                ) : (
                                  <div className="text-xs text-muted-foreground text-left">
                                    No detailed latency breakdown available.
                                  </div>
                                )}
                              </HoverCardContent>
                            </HoverCard>
                          ) : (
                            <div className="flex items-center justify-start pl-3 sm:pl-6 text-muted-foreground/30 font-mono text-xs md:text-sm py-2 w-full h-full">
                              -
                            </div>
                          )}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {isDesktop ? (
        <Sheet open={isInstructionOpen} onOpenChange={setIsInstructionOpen}>
          <SheetContent
            side="right"
            className="h-full min-h-0 w-[640px] lg:w-[680px] xl:w-[760px] 2xl:w-[820px] max-w-[90vw] border-l border-border/70 bg-card/80 p-0 shadow-[0_0_0_1px_rgba(255,255,255,0.04),0_24px_80px_rgba(0,0,0,0.55)] backdrop-blur-md data-[state=open]:duration-320 data-[state=closed]:duration-220 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=open]:slide-in-from-right data-[state=closed]:slide-out-to-right data-[state=open]:zoom-in-95 data-[state=closed]:zoom-out-95"
          >
            <div className="flex h-full min-h-0 flex-col">
              <SheetHeader className="border-b border-border/60 bg-card/80 px-7 py-5 pr-14">
                <SheetTitle className="text-base">{selectedTask || "Task Instruction"}</SheetTitle>
                <SheetDescription className="sr-only">{selectedTask}</SheetDescription>
              </SheetHeader>
              {instructionBody}
            </div>
          </SheetContent>
        </Sheet>
      ) : (
        <Drawer open={isInstructionOpen} onOpenChange={setIsInstructionOpen} direction="bottom">
          <DrawerContent className="inset-x-0 bottom-0 h-[76dvh] max-h-[76dvh] rounded-t-2xl border-t border-border/70 bg-card/95 p-0">
            <div className="mx-auto mt-3 h-1.5 w-14 rounded-full bg-muted-foreground/40" />
            <div className="flex h-full min-h-0 flex-col">
              <DrawerHeader className="border-b border-border/60 px-5 pb-4">
                <DrawerTitle className="text-base">
                  {selectedTask || "Task Instruction"}
                </DrawerTitle>
                <SheetDescription className="sr-only">{selectedTask}</SheetDescription>
              </DrawerHeader>
              {instructionBody}
            </div>
          </DrawerContent>
        </Drawer>
      )}

      <BackToTop />
    </div>
  );
}

export default function TasksPage() {
  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/20">
      {/* Background Gradient Effect */}
      <div className="fixed inset-0 -z-10 h-full w-full bg-background bg-[radial-gradient(#2a2a2a_1px,transparent_1px)] [background-size:16px_16px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_70%,transparent_100%)] opacity-20 dark:opacity-40"></div>

      <Suspense fallback={<div className="container mx-auto px-4 py-16 text-center text-muted-foreground">Loading tasks...</div>}>
        <TasksContent />
      </Suspense>
    </div>
  );
}
