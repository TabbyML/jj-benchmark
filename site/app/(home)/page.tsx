import { Github, Terminal } from "lucide-react";
import tasksData from "../../tasks.json";
import LeaderboardTable, { type LeaderboardEntry } from "./components/leaderboard-table";

export default function Home() {
  // Process tasks.json to compute leaderboard stats directly on the server
  const statsMap = new Map<string, {
    passed: number;
    total: number;
    totalLatency: number;
    latencyCount: number;
    model: string;
    agent: string;
  }>();

  Object.values(tasksData).forEach((trials: any[]) => {
    trials.forEach(trial => {
      // Simplify model name
      const modelName = trial.model.split('/').pop() || trial.model;
      const agentName = trial.agent.charAt(0).toUpperCase() + trial.agent.slice(1);
      
      const key = `${modelName}-${agentName}`;
      
      if (!statsMap.has(key)) {
        statsMap.set(key, {
          passed: 0,
          total: 0,
          totalLatency: 0,
          latencyCount: 0,
          model: modelName,
          agent: agentName
        });
      }
      
      const stats = statsMap.get(key)!;
      stats.total += 1;
      if (trial.passed) {
        stats.passed += 1;
      }
      if (trial.latency_sec) {
        stats.totalLatency += trial.latency_sec;
        stats.latencyCount += 1;
      }
    });
  });

  const data: LeaderboardEntry[] = Array.from(statsMap.values())
    .map((stats, index) => {
      const successRate = stats.total > 0 ? Math.round((stats.passed / stats.total) * 100) : 0;
      const avgLatency = stats.latencyCount > 0 ? stats.totalLatency / stats.latencyCount : 0;
      return {
        id: String(index + 1),
        model: stats.model,
        agent: stats.agent,
        passedEvals: stats.passed,
        successRate: successRate,
        avgLatency: avgLatency,
      };
    })
    .sort((a, b) => b.successRate - a.successRate);

  // Re-assign IDs based on sorted order and adjust isNew
  data.forEach((item, index) => {
    item.id = String(index + 1);
    item.isNew = index === 0; // Keeping the original visual effect for the top item
  });

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
              <span>Last run: {new Date().toLocaleDateString()}</span>
            </span>
          </div>
        </div>

        {/* Client Component for Interactive Table */}
        <LeaderboardTable data={data} />
      </div>
    </div>
  );
}
