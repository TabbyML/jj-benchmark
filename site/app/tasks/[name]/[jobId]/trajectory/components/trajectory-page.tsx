"use client";

import { useEffect, useRef, useState } from "react";
import { Loader2 } from "lucide-react";

type TrajectoryPageProps = {
  title: string;
  trajectoryUrl: string | null;
  fallbackUrl: string;
};

export function TrajectoryPage({ title, trajectoryUrl, fallbackUrl }: TrajectoryPageProps) {
  const [iframeLoading, setIframeLoading] = useState(true);
  const iframeRef = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    if (!trajectoryUrl) {
      if (fallbackUrl) {
        window.location.replace(fallbackUrl);
      }
      return;
    }

    setIframeLoading(true);
  }, [trajectoryUrl, fallbackUrl]);

  const handleIframeLoad = () => {
    setIframeLoading(false);
    setTimeout(() => {
      if (iframeRef.current) {
        iframeRef.current.style.opacity = "1";
      }
    }, 300);
  };

  const handleIframeError = () => {
    if (fallbackUrl) {
      window.location.replace(fallbackUrl);
    }
  }

  if (trajectoryUrl) {
    return (
      <div className="fixed inset-0 w-full h-full">
        {iframeLoading && (
          <div className="flex flex-col items-center justify-center h-full space-y-6">
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
          className="fixed inset-0 w-full h-full border-0 opacity-0"
          title={title || "Trial Details"}
          onLoad={handleIframeLoad}
          onError={handleIframeError}
        />
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center h-screen space-y-6">
      <div className="relative flex items-center justify-center">
        <Loader2 className="w-12 h-12 text-primary animate-spin relative z-10" />
      </div>
      <div className="space-y-2 text-center">
        <h2 className="text-lg font-semibold tracking-tight text-foreground">Loading</h2>
      </div>
    </div>
  );
}