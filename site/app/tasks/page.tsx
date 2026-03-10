"use client";

import { useState, useMemo, useEffect, Suspense } from "react";
import { CheckCircle2, XCircle, Search, AlertTriangle, ArrowUpDown, ArrowUp, ArrowDown, Filter, X } from "lucide-react";
import Link from "next/link";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import tasksDataRaw from "../../tasks.json";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Convert object to array and sort by task name
const tasksData = Object.entries(tasksDataRaw).map(([taskName, trials]) => {
  return {
    taskName,
    trials: (trials as any[]).map(t => ({ 
      ...t, 
      model: t.model.split('/').pop() || t.model,
      agent: t.agent.charAt(0).toUpperCase() + t.agent.slice(1)
    })),
  };
}).sort((a, b) => a.taskName.localeCompare(b.taskName));

const allModels = Array.from(new Set(tasksData.flatMap(t => t.trials.map(tr => tr.model))));
const allAgents = Array.from(new Set(tasksData.flatMap(t => t.trials.map(tr => tr.agent))));

function TasksContent() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const queryQ = searchParams.get("q") || "";
  const queryStatus = searchParams.get("status") || "all";
  const queryModel = searchParams.get("model") || "all";
  const queryAgent = searchParams.get("agent") || "all";
  const querySort = searchParams.get("sort") || "default";
  const queryOrder = searchParams.get("order") || "asc";

  const [searchQuery, setSearchQuery] = useState(queryQ);

  const hasActiveFilters = queryStatus !== "all" || queryModel !== "all" || queryAgent !== "all" || searchQuery !== "" || querySort !== "default";

  // Debounce search query to URL
  useEffect(() => {
    const timer = setTimeout(() => {
      updateParams({ q: searchQuery });
    }, 300);
    return () => clearTimeout(timer);
  }, [searchQuery]);

  const updateParams = (updates: Record<string, string | null>) => {
    const params = new URLSearchParams(searchParams.toString());
    Object.entries(updates).forEach(([key, value]) => {
      if (value === null || value === "" || value === "all" || (key === "sort" && value === "default")) {
        params.delete(key);
      } else {
        params.set(key, value);
      }
    });
    router.replace(`${pathname}?${params.toString()}`, { scroll: false });
  };

  const filteredTasks = useMemo(() => {
    return tasksData.map(task => {
      // Filter trials based on status and model
      const filteredTrials = task.trials.filter(trial => {
        if (queryStatus === "passed" && !trial.passed) return false;
        if (queryStatus === "failed" && (trial.passed || trial.error)) return false;
        if (queryStatus === "error" && !trial.error) return false;
        if (queryModel !== "all" && trial.model !== queryModel) return false;
        if (queryAgent !== "all" && trial.agent.toLowerCase() !== queryAgent.toLowerCase()) return false;
        return true;
      });

      // Sort trials
      const sortedTrials = [...filteredTrials].sort((a, b) => {
        let valA = 0;
        let valB = 0;
        if (querySort === "latency") {
          valA = a.latency_sec || 0;
          valB = b.latency_sec || 0;
        } else if (querySort === "tokens") {
          valA = (a.tokens?.input || 0) + (a.tokens?.output || 0) + (a.tokens?.cache || 0);
          valB = (b.tokens?.input || 0) + (b.tokens?.output || 0) + (b.tokens?.cache || 0);
        } else {
           // default: preserve original order
           return 0;
        }
        
        if (queryOrder === "asc") {
          return valA - valB;
        } else {
          return valB - valA;
        }
      });

      return {
        ...task,
        trials: sortedTrials
      };
    }).filter(task => {
      // Filter by search query
      if (searchQuery && !task.taskName.toLowerCase().includes(searchQuery.toLowerCase())) {
        return false;
      }
      // Hide tasks that have no trials after filtering
      if (task.trials.length === 0) {
        return false;
      }
      return true;
    });
  }, [searchQuery, queryStatus, queryModel, queryAgent, querySort, queryOrder]);

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

  return (
    <div className="container mx-auto px-4 py-16 max-w-6xl">
      {/* Header Section */}
      <div className="mb-8 space-y-4">
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
            Detailed breakdown of individual task performance across different models and agents.
          </p>
        </div>
      </div>

      {/* Filters & Search */}
      <div className="sticky top-4 z-20 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8 p-4 rounded-xl border border-border bg-card/80 backdrop-blur-md shadow-sm transition-all">
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
            <Select value={queryStatus} onValueChange={(value) => updateParams({ status: value })}>
              <SelectTrigger className="w-full sm:w-[140px] bg-background">
                <SelectValue placeholder="All Statuses" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Statuses</SelectItem>
                <SelectItem value="passed">Passed</SelectItem>
                <SelectItem value="failed">Failed</SelectItem>
                <SelectItem value="error">Error</SelectItem>
              </SelectContent>
            </Select>

            <Select value={queryModel} onValueChange={(value) => updateParams({ model: value })}>
              <SelectTrigger className="w-full sm:w-[180px] bg-background">
                <SelectValue placeholder="All Models" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Models</SelectItem>
                {allModels.map(m => (
                  <SelectItem key={m} value={m}>{m}</SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={queryAgent} onValueChange={(value) => updateParams({ agent: value })}>
              <SelectTrigger className="w-full sm:w-[140px] bg-background col-span-2 sm:col-span-1">
                <SelectValue placeholder="All Agents" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Agents</SelectItem>
                {allAgents.map(a => (
                  <SelectItem key={a} value={a.toLowerCase()}>{a}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {hasActiveFilters && (
            <button
              type="button"
              onClick={() => {
                setSearchQuery("");
                router.replace(pathname, { scroll: false });
              }}
              className="flex items-center justify-center gap-1.5 px-3 py-1.5 text-sm text-muted-foreground hover:text-foreground bg-secondary/50 hover:bg-secondary rounded-md transition-colors w-full sm:w-auto"
            >
              <X className="w-3.5 h-3.5" />
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
      <div className="space-y-6">
        {filteredTasks.length === 0 ? (
          <div className="text-center py-12 text-muted-foreground animate-in fade-in duration-300">
            No tasks found matching your filters
          </div>
        ) : (
          filteredTasks.map((task, index) => (
            <div 
              key={task.taskName} 
              className="rounded-xl border border-border bg-card/50 backdrop-blur-sm shadow-sm overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-500 fill-mode-both" 
              style={{ animationDelay: `${Math.min(index * 50, 500)}ms` }}
            >
              <div className="px-4 sm:px-6 py-4 bg-secondary/30 border-b border-border flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 sm:gap-0">
                <h3 className="text-lg font-semibold font-mono text-foreground flex items-center gap-2 w-full sm:w-auto">
                  <span className="text-muted-foreground/50 text-sm shrink-0">#{index + 1}</span>
                  <span className="truncate" title={task.taskName}>{task.taskName}</span>
                </h3>
                <div className="text-sm text-muted-foreground shrink-0">
                  {task.trials.length} trials
                </div>
              </div>
              
              <div className="overflow-x-auto pb-2">
                <table className="w-full table-fixed text-sm text-left min-w-[600px]">
                  <thead className="bg-secondary/10 text-muted-foreground font-medium border-b border-border/50 select-none">
                    <tr>
                      <th className="px-4 sm:px-6 py-3 w-[50%]">Model / Agent</th>
                      <th className="px-4 sm:px-6 py-3 w-[25%] text-center">Status</th>
                      <th 
                        className="px-4 sm:px-6 py-3 w-[25%] text-right cursor-pointer hover:bg-secondary/30 hover:text-foreground transition-colors group"
                        onClick={() => toggleSort("latency")}
                      >
                        <div className="flex items-center justify-end gap-1 sm:gap-2">
                          Latency
                          {renderSortIcon("latency")}
                        </div>
                      </th>
                      {false && (
                        <th 
                          className="px-4 sm:px-6 py-3 w-[30%] sm:w-[40%] cursor-pointer hover:bg-secondary/30 hover:text-foreground transition-colors group"
                          onClick={() => toggleSort("tokens")}
                        >
                          <div className="flex items-center gap-1 sm:gap-2">
                            <span className="hidden sm:inline">Tokens (In / Out / Cache)</span>
                            <span className="sm:hidden">Tokens</span>
                            {renderSortIcon("tokens")}
                          </div>
                        </th>
                      )}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border/30 relative">
                    {task.trials.map((trial, tIndex) => (
                      <tr 
                        key={trial.trial_name || tIndex} 
                        className="hover:bg-secondary/20 transition-all duration-300 ease-in-out"
                        style={{
                          transform: "translateY(0)",
                          animation: "fadeIn 0.3s ease-in-out",
                        }}
                      >
                        <td className="px-4 sm:px-6 py-3">
                          <div className="flex flex-col">
                            <span className="font-medium text-foreground truncate max-w-[150px] sm:max-w-none" title={trial.model}>{trial.model}</span>
                            <span className="text-xs text-muted-foreground">{trial.agent}</span>
                          </div>
                        </td>
                        <td className="px-4 sm:px-6 py-3">
                          <div className="flex items-center justify-center gap-2">
                            {trial.error ? (
                              <div className="flex items-center gap-1 sm:gap-1.5 px-1.5 sm:px-2 py-1 rounded-md bg-red-500/10 text-red-500 border border-red-500/20 w-fit mx-auto">
                                <AlertTriangle className="w-3 h-3 sm:w-4 sm:h-4" />
                                <span className="text-[10px] sm:text-xs font-medium">Error</span>
                              </div>
                            ) : trial.passed ? (
                              <div className="flex items-center gap-1 sm:gap-1.5 px-1.5 sm:px-2 py-1 rounded-md bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 w-fit mx-auto">
                                <CheckCircle2 className="w-3 h-3 sm:w-4 sm:h-4" />
                                <span className="text-[10px] sm:text-xs font-medium">Passed</span>
                              </div>
                            ) : (
                              <div className="flex items-center gap-1 sm:gap-1.5 px-1.5 sm:px-2 py-1 rounded-md bg-amber-500/10 text-amber-500 border border-amber-500/20 w-fit mx-auto">
                                <XCircle className="w-3 h-3 sm:w-4 sm:h-4" />
                                <span className="text-[10px] sm:text-xs font-medium">Failed</span>
                              </div>
                            )}
                          </div>
                        </td>
                        <td className="px-4 sm:px-6 py-3 text-muted-foreground text-right">
                          {trial.latency_breakdown ? (
                            <HoverCard openDelay={200} closeDelay={100}>
                              <HoverCardTrigger asChild>
                                <button type="button" className="flex items-center justify-end gap-2 w-full cursor-help hover:text-foreground transition-colors">
                                  <span className="font-mono text-xs sm:text-sm">{trial.latency_sec ? `${trial.latency_sec.toFixed(1)}s` : '-'}</span>
                                </button>
                              </HoverCardTrigger>
                              <HoverCardContent side="top" align="center" className="w-48 p-3 bg-popover shadow-xl border-border z-50">
                                <div className="space-y-1.5 text-xs text-popover-foreground text-left">
                                  <div className="flex justify-between">
                                    <span className="text-muted-foreground">Env Setup:</span>
                                    <span className="font-mono">{trial.latency_breakdown.env_setup?.toFixed(1) || '-'}s</span>
                                  </div>
                                  <div className="flex justify-between">
                                    <span className="text-muted-foreground">Agent Setup:</span>
                                    <span className="font-mono">{trial.latency_breakdown.agent_setup?.toFixed(1) || '-'}s</span>
                                  </div>
                                  <div className="flex justify-between font-medium">
                                    <span className="text-foreground">Agent Exec:</span>
                                    <span className="font-mono text-primary">{trial.latency_breakdown.agent_exec?.toFixed(1) || '-'}s</span>
                                  </div>
                                  <div className="flex justify-between">
                                    <span className="text-muted-foreground">Verifier:</span>
                                    <span className="font-mono">{trial.latency_breakdown.verifier?.toFixed(1) || '-'}s</span>
                                  </div>
                                </div>
                              </HoverCardContent>
                            </HoverCard>
                          ) : (
                            <div className="flex items-center justify-end gap-2 w-full">
                              <span className="font-mono text-xs sm:text-sm">{trial.latency_sec ? `${trial.latency_sec.toFixed(1)}s` : '-'}</span>
                            </div>
                          )}
                        </td>
                        {false && (
                          <td className="px-4 sm:px-6 py-3 text-muted-foreground">
                            <div className="flex items-center gap-2">
                              <div className="flex flex-wrap gap-1 sm:gap-2 font-mono text-[10px] sm:text-[11px]">
                                <span className="bg-secondary/50 text-foreground/80 px-1 sm:px-1.5 py-0.5 rounded border border-border whitespace-nowrap" title="Input Tokens">
                                  In: {trial.tokens?.input?.toLocaleString() || 0}
                                </span>
                                <span className="bg-secondary/50 text-foreground/80 px-1 sm:px-1.5 py-0.5 rounded border border-border whitespace-nowrap" title="Output Tokens">
                                  Out: {trial.tokens?.output?.toLocaleString() || 0}
                                </span>
                                {trial.tokens?.cache > 0 && (
                                  <span className="bg-secondary/50 text-foreground/80 px-1 sm:px-1.5 py-0.5 rounded border border-border whitespace-nowrap" title="Cache Tokens">
                                    Cache: {trial.tokens?.cache?.toLocaleString()}
                                  </span>
                                )}
                              </div>
                            </div>
                          </td>
                        )}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ))
        )}
      </div>

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

function BackToTop() {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const toggleVisibility = () => {
      if (window.scrollY > 300) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };

    window.addEventListener("scroll", toggleVisibility);
    return () => window.removeEventListener("scroll", toggleVisibility);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  };

  if (!isVisible) return null;

  return (
    <button
      type="button"
      onClick={scrollToTop}
      className="fixed bottom-8 right-8 p-3 bg-secondary text-foreground rounded-full shadow-lg border border-border hover:bg-secondary/80 transition-all z-50 flex items-center justify-center group backdrop-blur-sm"
      aria-label="Back to top"
    >
      <ArrowUp className="w-5 h-5 group-hover:-translate-y-1 transition-transform" />
    </button>
  );
}
