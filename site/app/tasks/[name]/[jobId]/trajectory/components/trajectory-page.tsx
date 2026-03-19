"use client";

import { useEffect, useRef, useState } from "react";
import { Check, Copy, List, ListOrdered, Loader2 } from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";

type TrajectoryPageProps = {
  trajectoryUrl: string;
  fallbackUrl: string;
  stderrText: string | null;
  verifierText: string | null;
  topOffsetClassName?: string;
};

export function TrajectoryPage({
  trajectoryUrl,
  fallbackUrl,
  stderrText,
  verifierText,
  topOffsetClassName = "top-20",
}: TrajectoryPageProps) {
  const [iframeLoading, setIframeLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("trajectory");
  const [showLineNumbers, setShowLineNumbers] = useState(false);
  const [copiedTab, setCopiedTab] = useState<"log" | "test" | null>(null);
  const iframeRef = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    setIframeLoading(true);
  }, [trajectoryUrl]);

  useEffect(() => {
    if (!copiedTab) {
      return;
    }

    const timer = window.setTimeout(() => {
      setCopiedTab(null);
    }, 1200);

    return () => window.clearTimeout(timer);
  }, [copiedTab]);

  const handleIframeLoad = () => {
    setIframeLoading(false);
    setTimeout(() => {
      if (iframeRef.current) {
        iframeRef.current.style.opacity = "1";
      }
    }, 300);
  };

  const handleIframeError = () => {
    window.location.replace(fallbackUrl);
  };

  const copyActiveLog = async () => {
    const targetText = activeTab === "log" ? stderrText : verifierText;
    if (!targetText) {
      return;
    }

    await navigator.clipboard.writeText(targetText);
    setCopiedTab(activeTab === "log" ? "log" : "test");
  };

  const getLogStats = (text: string | null) => {
    if (!text || text.length === 0) {
      return {
        chars: 0,
        lines: 0,
        nonEmptyLines: 0,
      };
    }

    const lines = text.split(/\r?\n/);
    const nonEmptyLines = lines.reduce((count, line) => {
      return line.trim().length > 0 ? count + 1 : count;
    }, 0);

    return {
      chars: text.length,
      lines: lines.length,
      nonEmptyLines,
    };
  };

  const verifierStats = getLogStats(verifierText);
  const stderrStats = getLogStats(stderrText);

  const renderLogContent = (text: string | null, emptyMessage: string, toneClassName: string) => {
    if (!text) {
      return <p className="text-sm text-muted-foreground">{emptyMessage}</p>;
    }

    if (!showLineNumbers) {
      return (
        <pre className={`whitespace-pre-wrap wrap-break-word font-mono text-xs leading-5 ${toneClassName}`}>
          {text}
        </pre>
      );
    }

    const lines = text.split(/\r?\n/);
    return (
      <div className={`font-mono text-xs leading-5 ${toneClassName}`}>
        {lines.map((line, index) => (
          <div key={`${index}-${line.length}`} className="grid grid-cols-[auto_1fr] gap-3">
            <span className="select-none text-muted-foreground/70">{index + 1}</span>
            <span className="whitespace-pre-wrap wrap-break-word">{line.length > 0 ? line : " "}</span>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="fixed inset-0 w-full h-full">
      <div className={`absolute inset-x-0 bottom-0 ${topOffsetClassName} pb-4 sm:pb-6`}>
        <div className="mx-auto h-full w-full max-w-[1400px] px-4 sm:px-7 lg:px-10">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="h-full rounded-xl border border-border/60 bg-card/40 backdrop-blur-sm shadow-sm">
            <div className="border-b border-border/50 px-3 py-3 sm:px-4">
              <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                <TabsList className="grid w-[300px] max-w-full grid-cols-3">
                <TabsTrigger value="trajectory" className="w-full">Trajectory</TabsTrigger>
                <TabsTrigger value="log" className="w-full">Log</TabsTrigger>
                <TabsTrigger value="test" className="w-full">Test</TabsTrigger>
                </TabsList>

                {activeTab !== "trajectory" && (
                  <div className="flex items-center gap-2">
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      className="h-8"
                      onClick={() => setShowLineNumbers((prev) => !prev)}
                    >
                      {showLineNumbers ? <List className="h-3.5 w-3.5" /> : <ListOrdered className="h-3.5 w-3.5" />}
                      {showLineNumbers ? "Hide Line Numbers" : "Show Line Numbers"}
                    </Button>
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      className="h-8"
                      onClick={copyActiveLog}
                      disabled={activeTab === "log" ? !stderrText : activeTab === "test" ? !verifierText : true}
                    >
                      {copiedTab === activeTab ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
                      {copiedTab === activeTab ? "Copied" : "Copy"}
                    </Button>
                  </div>
                )}
              </div>
            </div>

            <TabsContent value="trajectory" className="relative h-[calc(100%-64px)] overflow-hidden" forceMount>
              {iframeLoading && (
                <div className="absolute inset-0 z-10 flex flex-col items-center justify-center space-y-6 bg-background/80 backdrop-blur-sm">
                  <div className="relative flex items-center justify-center">
                    <Loader2 className="w-12 h-12 text-primary animate-spin relative z-10" />
                  </div>
                  <div className="space-y-2 text-center">
                    <h2 className="text-lg font-semibold tracking-tight text-foreground">Loading</h2>
                  </div>
                </div>
              )}
              <iframe
                ref={iframeRef}
                src={trajectoryUrl}
                className="h-full w-full border-0 opacity-0 transition-opacity duration-300"
                title="Trial Details"
                onLoad={handleIframeLoad}
                onError={handleIframeError}
              />
            </TabsContent>

            <TabsContent value="log" className="h-[calc(100%-64px)] overflow-auto px-3 pb-3 sm:px-4 sm:pb-4" forceMount>
              <div className="rounded-lg border border-border/50 bg-background/70 p-3 sm:p-4">
                <div className="mb-3 flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
                  <span className="rounded-md border border-border/50 px-2 py-0.5">Lines: {stderrStats.lines}</span>
                  <span className="rounded-md border border-border/50 px-2 py-0.5">Non-empty: {stderrStats.nonEmptyLines}</span>
                  <span className="rounded-md border border-border/50 px-2 py-0.5">Chars: {stderrStats.chars}</span>
                </div>
                {renderLogContent(stderrText, "No stderr content available for this trial.", "text-red-500/90")}
              </div>
            </TabsContent>

            <TabsContent value="test" className="h-[calc(100%-64px)] overflow-auto px-3 pb-3 sm:px-4 sm:pb-4" forceMount>
              <div className="rounded-lg border border-border/50 bg-background/70 p-3 sm:p-4">
                <div className="mb-3 flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
                  <span className="rounded-md border border-border/50 px-2 py-0.5">Lines: {verifierStats.lines}</span>
                  <span className="rounded-md border border-border/50 px-2 py-0.5">Non-empty: {verifierStats.nonEmptyLines}</span>
                  <span className="rounded-md border border-border/50 px-2 py-0.5">Chars: {verifierStats.chars}</span>
                </div>
                {renderLogContent(verifierText, "No verifier test output available for this trial.", "text-foreground/95")}
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
}