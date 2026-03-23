"use client";

import { useEffect, useMemo, useState } from "react";
import { useTheme } from "next-themes";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Skeleton } from "@/components/ui/skeleton";

type TrajectoryPageProps = {
  trajectoryUrl: string;
  fallbackUrl: string;
  stderrText: string | null;
  verifierText: string | null;
};

export function TrajectoryPage({
  trajectoryUrl,
  fallbackUrl,
  stderrText,
  verifierText,
}: TrajectoryPageProps) {
  const { resolvedTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const [iframeLoading, setIframeLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("trajectory");

  const iframeTheme = mounted && resolvedTheme === "light" ? "light" : "dark";

  const iframeUrl = useMemo(() => {
    const url = new URL(trajectoryUrl);
    url.searchParams.set("theme", iframeTheme);
    return url.toString();
  }, [trajectoryUrl, iframeTheme]);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!mounted) {
      return;
    }

    setIframeLoading(true);
  }, [iframeUrl, mounted]);

  const handleIframeLoad = () => {
    setIframeLoading(false);
  };

  const handleIframeError = () => {
    window.location.replace(fallbackUrl);
  };

  const renderLogContent = (text: string | null, emptyMessage: string) => {
    if (!text) {
      return <p className="text-sm text-muted-foreground">{emptyMessage}</p>;
    }

    return (
      <pre className="w-max min-w-full whitespace-pre font-mono text-xs leading-5 text-foreground/95">
        {text}
      </pre>
    );
  };

  return (
    <div className="h-full w-full pb-4 pt-4 sm:pb-6 sm:pt-5">
      <div className="mx-auto h-full w-full max-w-[1400px] px-4 sm:px-7 lg:px-10">
          <Tabs
            value={activeTab}
            onValueChange={setActiveTab}
            className="flex h-full min-h-0 flex-col gap-0 overflow-hidden rounded-xl border border-border bg-background/70 backdrop-blur-sm shadow-sm"
          >
            <div className="border-b border-border bg-background/40 px-3 py-3 sm:px-4">
              <TabsList className="grid h-11 w-[300px] max-w-full grid-cols-3 items-stretch gap-1 rounded-xl bg-muted/55 p-1">
                <TabsTrigger
                  value="trajectory"
                  className="h-full w-full cursor-pointer rounded-lg border-0 py-0 leading-none text-muted-foreground transition-colors hover:bg-primary/10 hover:text-foreground data-[state=active]:bg-primary/18 data-[state=active]:text-foreground data-[state=active]:shadow-none"
                >
                  Trajectory
                </TabsTrigger>
                <TabsTrigger
                  value="log"
                  className="h-full w-full cursor-pointer rounded-lg border-0 py-0 leading-none text-muted-foreground transition-colors hover:bg-primary/10 hover:text-foreground data-[state=active]:bg-primary/18 data-[state=active]:text-foreground data-[state=active]:shadow-none"
                >
                  Log
                </TabsTrigger>
                <TabsTrigger
                  value="test"
                  className="h-full w-full cursor-pointer rounded-lg border-0 py-0 leading-none text-muted-foreground transition-colors hover:bg-primary/10 hover:text-foreground data-[state=active]:bg-primary/18 data-[state=active]:text-foreground data-[state=active]:shadow-none"
                >
                  Test
                </TabsTrigger>
              </TabsList>
            </div>

            <TabsContent value="trajectory" className="relative min-h-0 flex-1 overflow-hidden px-2" forceMount>
              <div
                className={`absolute inset-0 z-10 overflow-auto bg-background/80 transition-opacity duration-420 ease-out delay-220 ${!mounted || iframeLoading ? "opacity-100" : "pointer-events-none opacity-0"}`}
              >
                <TrajectorySkeleton />
              </div>
              {mounted && (
                <iframe
                  src={iframeUrl}
                  className={`h-full w-full border-0 transition-opacity duration-260 ease-out ${iframeLoading ? "opacity-0" : "opacity-100"}`}
                  title="Trial Details"
                  onLoad={handleIframeLoad}
                  onError={handleIframeError}
                />
              )}
            </TabsContent>

            <TabsContent value="log" className="min-h-0 flex-1 overflow-hidden" forceMount>
              <ScrollArea className="h-full w-full">
                <div className="px-3 pb-4 pt-2 sm:px-4 sm:pb-5 sm:pt-3">
                  {renderLogContent(stderrText, "No stderr content available for this trial.")}
                </div>
              </ScrollArea>
            </TabsContent>

            <TabsContent value="test" className="min-h-0 flex-1 overflow-hidden" forceMount>
              <ScrollArea className="h-full w-full">
                <div className="px-3 pb-4 pt-2 sm:px-4 sm:pb-5 sm:pt-3">
                  {renderLogContent(verifierText, "No verifier test output available for this trial.")}
                </div>
              </ScrollArea>
            </TabsContent>
          </Tabs>
      </div>
    </div>
  );
}

function TrajectorySkeleton() {
  return (
    <div className="animate-pulse space-y-2 p-4">
      <div className="flex items-center space-x-3">
        <Skeleton className="size-6 rounded-full" />
        <Skeleton className="h-4 w-16" />
      </div>
      <div className="space-y-2 pt-1">
        <Skeleton className="h-4 w-[80%]" />
        <Skeleton className="h-4 w-[50%]" />
      </div>
      <div className="mt-8 flex items-center space-x-3">
        <div className="flex items-center space-x-3">
          <Skeleton className="size-6 rounded-full" />
          <Skeleton className="h-4 w-16" />
        </div>
      </div>
      <div className="space-y-2 pt-1">
        <Skeleton className="h-4 w-[80%]" />
        <Skeleton className="h-4 w-[80%]" />
        <Skeleton className="h-4 w-[50%]" />
      </div>
    </div>
  );
}
