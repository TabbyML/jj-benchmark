"use client";

import { useEffect, useRef, useState } from "react";
import { Loader2 } from "lucide-react";
import zealtConfig from "../../../../../../../zealt.json";

type TrajectoryPageProps = {
  name: string;
  jobName: string;
};

let messagesCachePromise: Promise<Record<string, unknown>> | null = null;

async function loadMessages() {
  if (!messagesCachePromise) {
    messagesCachePromise = import("@/messages.json").then((module) => {
      const data = module.default || module;
      return data as Record<string, unknown>;
    });
  }

  return messagesCachePromise;
}

function getServerBaseUrl() {
  const isDev = process.env.NODE_ENV === "development";
  return isDev ? "http://localhost:4113" : "https://cc.getpochi.com";
}

export function TrajectoryPage({ name, jobName }: TrajectoryPageProps) {
  const [error, setError] = useState<string | null>(null);
  const [redirectUrl, setRedirectUrl] = useState<string | null>(null);
  const [iframeLoading, setIframeLoading] = useState(false);
  const [showIframe, setShowIframe] = useState(false);
  const fallbackUrlRef = useRef<string>("");
  const iframeRef = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    if (!name || !jobName) {
      setError("Missing name or jobName parameters.");
      return;
    }

    const fallback = `${zealtConfig.github_repo}/blob/main/jobs/${jobName}/${name}/result.json`;
    fallbackUrlRef.current = fallback;

    const processRedirect = async () => {
      try {
        const messagesData = await loadMessages();
        const trialMessages = messagesData[name];

        if (trialMessages) {
          const baseUrl = getServerBaseUrl();
          const response = await fetch(`${baseUrl}/api/clips`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ data: { messages: trialMessages } }),
          });

          if (!response.ok) {
            throw new Error(`Failed to post clip: ${response.statusText}`);
          }

          const { id } = await response.json();
          if (id) {
            const url = new URL(`/e/${id}`, baseUrl);
            url.searchParams.set("embed", "true");
            url.searchParams.set("title", name);
            url.searchParams.set("theme", "dark")
            setRedirectUrl(url.toString());
            setIframeLoading(true);
            setShowIframe(true);
            return;
          }
        }

        window.location.replace(fallback);
      } catch (_err) {
        window.location.replace(fallback);
      }
    };

    processRedirect();
  }, [name, jobName]);

  const handleIframeLoad = () => {
    setIframeLoading(false);
    setTimeout(() => {
      if (iframeRef.current) {
        iframeRef.current.style.opacity = "1";
      }
    }, 200);
  };

  const handleIframeError = () => {
    window.location.replace(fallbackUrlRef.current);
  };

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-[50vh] space-y-4">
        <div className="text-red-500 font-medium">{error}</div>
      </div>
    );
  }

  if (redirectUrl) {
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
        {showIframe && (
          <iframe
            ref={iframeRef}
            src={redirectUrl}
            className="fixed inset-0 w-full h-full border-0 opacity-0"
            title={name || "Trial Details"}
            onLoad={handleIframeLoad}
            onError={handleIframeError}
          />
        )}
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