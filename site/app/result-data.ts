import resultData from "@/jobs/2026-03-08__16-54-33/result.json"

export default {
  startedAt: resultData.started_at,
  evals: {
    ...resultData.stats.evals,
  }
}
