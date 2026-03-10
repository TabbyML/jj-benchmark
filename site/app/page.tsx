import { Github, ChevronDown, Trophy, Search, Filter, ArrowUpRight, Terminal, ListTree } from "lucide-react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import Link from "next/link";
import resultData from "./result-data";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface LeaderboardEntry {
  id: string;
  model: string;
  agent: string;
  passedEvals: number;
  successRate: number;
  isNew?: boolean;
}

function ProgressBar({ value, colorClass }: { value: number; colorClass: string }) {
  return (
    <div className="h-2 w-24 bg-secondary rounded-full overflow-hidden">
      <div
        className={cn("h-full transition-all duration-500 ease-out", colorClass)}
        style={{ width: `${value}%` }}
      />
    </div>
  );
}

function ScoreCell({ value }: { value: number }) {
  let colorClass = "bg-primary";
  let textClass = "text-muted-foreground";

  if (value >= 90) {
    colorClass = "bg-emerald-500";
    textClass = "text-emerald-500 font-bold";
  } else if (value >= 75) {
    colorClass = "bg-blue-500";
    textClass = "text-blue-500 font-medium";
  } else if (value >= 60) {
    colorClass = "bg-amber-500";
    textClass = "text-amber-500";
  } else {
    colorClass = "bg-red-500";
    textClass = "text-red-500";
  }

  return (
    <div className="flex items-center gap-3">
      <span className={cn("w-12 text-right", textClass)}>{value}%</span>
      <ProgressBar value={value} colorClass={colorClass} />
    </div>
  );
}

export default async function Home() {
  const data = Object.entries(resultData.evals)
    .map(([key, val], index) => {
      let parts = key.split("__");
      let agentRaw = parts[0] || "Unknown";
      let model = parts[1] || "Unknown";

      if (parts.length === 2) {
        agentRaw = "Codex";
        model = parts[0];
      }

      const agent = agentRaw.charAt(0).toUpperCase() + agentRaw.slice(1);

      return {
        id: String(index + 1),
        model: model,
        agent: agent,
        passedEvals: Math.round(val.metrics[0].mean * val.n_trials),
        successRate: Math.round(val.metrics[0].mean * 100),
        isNew: index === 0,
      };
    })
    .sort((a, b) => b.successRate - a.successRate);

  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/20">
      {/* Background Gradient Effect */}
      <div className="fixed inset-0 -z-10 h-full w-full bg-background bg-[radial-gradient(#2a2a2a_1px,transparent_1px)] [background-size:16px_16px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_70%,transparent_100%)] opacity-20 dark:opacity-40"></div>

      <div className="container mx-auto px-4 py-16 max-w-6xl">
        {/* Header Section */}
        <div className="text-center mb-16 space-y-6">
          <div className="inline-flex items-center justify-center p-1.5 rounded-full bg-secondary/50 backdrop-blur-sm border border-border mb-4">
            <span className="flex h-2 w-2 rounded-full bg-emerald-500 mx-2 animate-pulse"></span>
            <span className="text-xs font-medium px-2">Live Benchmarks</span>
          </div>

          <h1 className="text-5xl md:text-7xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-b from-foreground to-foreground/50 pb-2">
            JJ Benchmark
          </h1>

          <p className="text-lg text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            Performance results of AI coding agents on Jujutsu tasks,
            measuring success rate and execution time with high precision.
          </p>

          <div className="flex items-center justify-center gap-6 text-sm text-muted-foreground pt-4">
            <a href="https://github.com/TabbyML/jj-benchmark" target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 hover:text-primary transition-colors">
              <Github className="w-4 h-4" />
              <span>View on GitHub</span>
            </a>
            <div className="h-4 w-px bg-border"></div>
            <span className="flex items-center gap-2">
              <Terminal className="w-4 h-4" />
              <span>Last run: {new Date(resultData.startedAt).toLocaleDateString()}</span>
            </span>
          </div>
        </div>

        {/* Controls & Filters */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
          <h2 className="text-2xl font-semibold flex items-center gap-2">
            Agent Performance
          </h2>

          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 w-full md:w-auto">
            <Link 
              href="/tasks" 
              className="flex items-center justify-center gap-2 px-4 py-2 border border-border bg-card/50 hover:bg-secondary/50 text-foreground rounded-lg text-sm font-medium transition-colors shadow-sm backdrop-blur-sm whitespace-nowrap"
            >
              <ListTree className="w-4 h-4" />
              View Tasks Details
            </Link>
            
            <div className="relative w-full sm:w-auto">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search agents..."
                className="pl-9 pr-4 py-2 bg-card border border-border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 w-full sm:w-64 transition-all"
              />
            </div>
          </div>
        </div>

        {/* Leaderboard Table */}
        <div className="rounded-xl border border-border bg-card/50 backdrop-blur-sm shadow-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="bg-secondary/50 text-muted-foreground font-medium border-b border-border">
                <tr>
                  <th className="px-6 py-4 w-[30%]">Model</th>
                  <th className="px-6 py-4 w-[20%]">Agent</th>
                  <th className="px-6 py-4 w-[15%] text-center">Passed</th>
                  <th className="px-6 py-4 w-[35%]">Success Rate</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/50">
                {data.map((row, index) => (
                  <tr
                    key={row.id}
                    className="group hover:bg-secondary/30 transition-colors duration-200"
                  >
                    <td className="px-6 py-4 font-medium text-foreground flex items-center gap-3">
                      <span className="w-6 text-muted-foreground/50 text-xs">#{index + 1}</span>
                      <div className="flex flex-col">
                        <span className="flex items-center gap-2">
                          {row.model}
                          {index === 0 && <Trophy className="w-3 h-3 text-yellow-500" />}
                          {row.isNew && (
                            <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-blue-500/10 text-blue-500 border border-blue-500/20">
                              NEW
                            </span>
                          )}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-muted-foreground">
                      <div className="flex items-center gap-2">
                        <div className="w-6 h-6 rounded-full bg-secondary flex items-center justify-center text-[10px] font-bold border border-border">
                          {row.agent.substring(0, 1).toUpperCase()}
                        </div>
                        {row.agent}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-center text-muted-foreground font-mono">
                      {row.passedEvals}
                    </td>
                    <td className="px-6 py-4">
                      <Link href={`/tasks?model=${encodeURIComponent(row.model)}&agent=${encodeURIComponent(row.agent.toLowerCase())}`} className="block w-full hover:opacity-80 transition-opacity">
                        <ScoreCell value={row.successRate} />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
