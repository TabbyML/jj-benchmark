declare module "@/jobs/*/result.json" {
  export interface EvalMetric {
    mean: number;
  }

  export interface EvalStats {
    n_trials: number;
    n_errors: number;
    metrics: EvalMetric[];
    reward_stats?: Record<string, any>;
    exception_stats?: Record<string, any>;
  }

  export interface ResultStats {
    n_trials: number;
    n_errors: number;
    evals: Record<string, EvalStats>;
  }

  export interface BenchmarkResult {
    id: string;
    started_at: string;
    finished_at: string;
    n_total_trials: number;
    stats: ResultStats;
  }

  const value: BenchmarkResult;
  export default value;
}
