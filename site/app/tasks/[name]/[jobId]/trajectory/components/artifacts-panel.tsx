"use client";

import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { useSearchParams, useRouter, usePathname } from "next/navigation";
import { ChevronRight, File, Folder } from "lucide-react";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  fetchLogText,
  LogContentSkeleton,
  LogErrorView,
  getLogErrorMessage,
} from "./trajectory-page";

export type ArtifactNode = {
  name: string;
  type: "file" | "dir";
  path: string;
  children?: ArtifactNode[];
};

export type ArtifactNodeWithUrl =
  | { name: string; type: "file"; path: string; url: string }
  | { name: string; type: "dir"; path: string; children: ArtifactNodeWithUrl[] };

type ArtifactsPanelProps = {
  artifactTree: ArtifactNodeWithUrl[];
};

export function ArtifactsPanel({ artifactTree }: ArtifactsPanelProps) {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  const queryArtifact = searchParams.get("artifact");
  const queryPath = searchParams.get("path");

  const activeArtifact = useMemo(() => {
    if (queryArtifact) {
      const found = artifactTree.find((node) => node.name === queryArtifact);
      if (found) return found;
    }
    return artifactTree[0] ?? null;
  }, [artifactTree, queryArtifact]);

  const updateParams = (next: { artifact?: string | null; path?: string | null }) => {
    const params = new URLSearchParams(searchParams.toString());
    if (next.artifact === null) {
      params.delete("artifact");
    } else if (next.artifact !== undefined) {
      params.set("artifact", next.artifact);
    }
    if (next.path === null) {
      params.delete("path");
    } else if (next.path !== undefined) {
      params.set("path", next.path);
    }
    router.replace(`${pathname}?${params.toString()}`, { scroll: false });
  };

  const handleSelectArtifact = (name: string) => {
    updateParams({ artifact: name, path: null });
  };

  if (!activeArtifact) {
    return (
      <div className="flex h-full items-center justify-center text-sm text-muted-foreground">
        No artifacts available.
      </div>
    );
  }

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div className="bg-background/20 px-3 py-1.5 sm:px-4 mt-3 shrink-0 overflow-x-auto">
        <div className="flex gap-1.5 min-w-max">
          {artifactTree.map((node) => (
            <button
              key={node.name}
              type="button"
              onClick={() => handleSelectArtifact(node.name)}
              className={`px-2.5 py-1 text-[11px] sm:text-xs rounded-full transition-colors whitespace-nowrap border inline-flex items-center gap-1 ${
                activeArtifact.name === node.name
                  ? "bg-primary/10 text-primary border-primary/20 font-medium"
                  : "bg-transparent text-muted-foreground border-transparent hover:bg-secondary/50 hover:text-foreground"
              }`}
            >
              {node.type === "dir" ? (
                <Folder className="h-3 w-3" />
              ) : (
                <File className="h-3 w-3" />
              )}
              {node.name}
            </button>
          ))}
        </div>
      </div>

      <div className="min-h-0 flex-1 overflow-hidden">
        {activeArtifact.type === "file" ? (
          <FileViewer url={activeArtifact.url} />
        ) : (
          <DirectoryArtifactView
            artifact={activeArtifact}
            currentPath={queryPath}
            onPathChange={(path) => updateParams({ path: path ?? null })}
          />
        )}
      </div>
    </div>
  );
}

type DirectoryArtifactViewProps = {
  artifact: Extract<ArtifactNodeWithUrl, { type: "dir" }>;
  currentPath: string | null;
  onPathChange: (path: string | null) => void;
};

function DirectoryArtifactView({ artifact, currentPath, onPathChange }: DirectoryArtifactViewProps) {
  // Resolve the active path. If currentPath isn't valid for this artifact, fall back to the artifact root.
  const resolved = useMemo(() => resolvePath(artifact, currentPath), [artifact, currentPath]);
  const { folder, selectedFile, breadcrumbDirs } = resolved;

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div className="px-3 sm:px-4 mt-2 shrink-0 flex items-center flex-wrap gap-1 text-xs text-muted-foreground">
        {breadcrumbDirs.map((dir, idx) => {
          const isLast = idx === breadcrumbDirs.length - 1 && !selectedFile;
          return (
            <span key={dir.path} className="inline-flex items-center gap-1">
              <button
                type="button"
                onClick={() => onPathChange(idx === 0 ? null : dir.path)}
                className={`hover:text-foreground transition-colors ${
                  isLast ? "text-foreground font-medium" : ""
                }`}
              >
                {dir.name}
              </button>
              {(idx < breadcrumbDirs.length - 1 || selectedFile) && (
                <ChevronRight className="h-3 w-3" />
              )}
            </span>
          );
        })}
        {selectedFile && (
          <span className="text-foreground font-medium">{selectedFile.name}</span>
        )}
      </div>

      <div className="bg-background/20 px-3 py-1.5 sm:px-4 mt-2 shrink-0 overflow-x-auto">
        <div className="flex gap-1.5 min-w-max">
          {folder.children.length === 0 && (
            <span className="text-xs text-muted-foreground italic">Empty directory.</span>
          )}
          {folder.children.map((child) => {
            const isActive = child.type === "file" && selectedFile?.path === child.path;
            return (
              <button
                key={child.path}
                type="button"
                onClick={() => onPathChange(child.path)}
                className={`px-2.5 py-1 text-[11px] sm:text-xs rounded-full transition-colors whitespace-nowrap border inline-flex items-center gap-1 ${
                  isActive
                    ? "bg-primary/10 text-primary border-primary/20 font-medium"
                    : "bg-transparent text-muted-foreground border-transparent hover:bg-secondary/50 hover:text-foreground"
                }`}
              >
                {child.type === "dir" ? (
                  <Folder className="h-3 w-3" />
                ) : (
                  <File className="h-3 w-3" />
                )}
                {child.name}
              </button>
            );
          })}
        </div>
      </div>

      <div className="min-h-0 flex-1 overflow-hidden">
        {selectedFile ? (
          <FileViewer url={selectedFile.url} />
        ) : (
          <div className="flex h-full items-center justify-center px-4 text-center text-sm text-muted-foreground">
            Select a file to view its contents.
          </div>
        )}
      </div>
    </div>
  );
}

function FileViewer({ url }: { url: string }) {
  const query = useQuery({
    queryKey: ["artifact-file", url],
    queryFn: () => fetchLogText(url),
  });

  return (
    <ScrollArea className="h-full w-full">
      <div className="px-3 pb-4 pt-2 sm:px-4 sm:pb-5 sm:pt-3">
        {query.isPending || query.isFetching ? (
          <LogContentSkeleton />
        ) : query.isError ? (
          <LogErrorView
            message={getLogErrorMessage(query.error)}
            onRetry={() => void query.refetch()}
          />
        ) : query.data ? (
          <pre className="w-max min-w-full whitespace-pre font-mono text-xs leading-5 text-foreground/95">
            {query.data}
          </pre>
        ) : (
          <p className="text-sm text-muted-foreground">Empty file.</p>
        )}
      </div>
    </ScrollArea>
  );
}

type ResolvedPath = {
  folder: Extract<ArtifactNodeWithUrl, { type: "dir" }>;
  selectedFile: Extract<ArtifactNodeWithUrl, { type: "file" }> | null;
  breadcrumbDirs: { name: string; path: string }[];
};

function resolvePath(
  root: Extract<ArtifactNodeWithUrl, { type: "dir" }>,
  targetPath: string | null,
): ResolvedPath {
  const breadcrumbDirs: { name: string; path: string }[] = [{ name: root.name, path: root.path }];
  let folder = root;
  let selectedFile: Extract<ArtifactNodeWithUrl, { type: "file" }> | null = null;

  if (!targetPath || !targetPath.startsWith(`${root.path}/`)) {
    return { folder, selectedFile, breadcrumbDirs };
  }

  const remainder = targetPath.slice(root.path.length + 1);
  const segments = remainder.split("/").filter(Boolean);

  let currentPath = root.path;
  for (let i = 0; i < segments.length; i++) {
    const segment = segments[i];
    currentPath = `${currentPath}/${segment}`;
    const child = folder.children.find((c) => c.name === segment);
    if (!child) {
      // Path doesn't exist; bail and show what we resolved so far.
      return { folder, selectedFile: null, breadcrumbDirs };
    }
    if (child.type === "dir") {
      folder = child;
      breadcrumbDirs.push({ name: child.name, path: child.path });
    } else {
      // File at the end of the path.
      selectedFile = child;
      // Don't push the file as a breadcrumb dir; the caller renders it separately.
      break;
    }
  }

  return { folder, selectedFile, breadcrumbDirs };
}
