"use client";

import { useState, useMemo } from "react";
import { Search, Trophy, ListTree } from "lucide-react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import Link from "next/link";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export interface LeaderboardEntry {
  id: string;
  model: string;
  agent: string;
  passedEvals: number;
  successRate: number;
  avgLatency: number;
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

export default function LeaderboardTable({ data }: { data: LeaderboardEntry[] }) {
  const [searchQuery, setSearchQuery] = useState("");

  const filteredData = useMemo(() => {
    let processedData = data;

    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      processedData = processedData.filter(item => 
        item.model.toLowerCase().includes(query) || 
        item.agent.toLowerCase().includes(query)
      );
    }

    return processedData;
  }, [data, searchQuery]);

  return (
    <>
      {/* Controls & Filters */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
        <h2 className="text-2xl font-semibold flex items-center gap-2">
          Agent Performance
        </h2>

        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 w-full md:w-auto">
          <Link 
            href="./tasks" 
            className="flex items-center justify-center gap-2 px-4 py-2 border border-border bg-card/50 hover:bg-secondary/50 text-foreground rounded-lg text-sm font-medium transition-colors shadow-sm backdrop-blur-sm whitespace-nowrap"
          >
            <ListTree className="w-4 h-4" />
            View Tasks
          </Link>
          
          <div className="relative w-full sm:w-auto">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search models or agents..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
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
                <th className="px-6 py-4 w-[25%]">Model</th>
                <th className="px-6 py-4 w-[15%]">Agent</th>
                <th className="px-6 py-4 w-[15%] text-center">Passed</th>
                <th className="px-6 py-4 w-[15%] text-right">Avg Duration</th>
                <th className="px-6 py-4 w-[30%]">Success Rate</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/50">
              {filteredData.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-muted-foreground">
                    No results found matching your search.
                  </td>
                </tr>
              ) : (
                filteredData.map((row, index) => (
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
                  <td className="px-6 py-4 text-right text-muted-foreground font-mono">
                    {row.avgLatency > 0 ? `${row.avgLatency.toFixed(1)}s` : '-'}
                  </td>
                  <td className="px-6 py-4">
                    <Link href={`./tasks?model=${encodeURIComponent(row.model)}&agent=${encodeURIComponent(row.agent.toLowerCase())}`} className="block w-full hover:opacity-80 transition-opacity">
                      <ScoreCell value={row.successRate} />
                    </Link>
                  </td>
                </tr>
              )))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
