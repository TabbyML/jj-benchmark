"use client";

import * as React from "react";
import { Check, Monitor, Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";

import { Button } from "@/components/ui/button";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { cn } from "@/lib/utils";

type ThemeMode = "light" | "dark" | "system";

const themeOptions: Array<{ value: ThemeMode; label: string }> = [
  { value: "light", label: "Light" },
  { value: "dark", label: "Dark" },
  { value: "system", label: "System" },
];

function ThemeIcon({ theme }: { theme: ThemeMode }) {
  if (theme === "light") {
    return <Sun className="h-4 w-4" />;
  }
  if (theme === "dark") {
    return <Moon className="h-4 w-4" />;
  }
  return <Monitor className="h-4 w-4" />;
}

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  const [open, setOpen] = React.useState(false);
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
  }, []);

  const activeTheme = (mounted ? theme : "dark") as ThemeMode;

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          type="button"
          variant="outline"
          size="icon-sm"
          aria-label="Switch theme"
          className="size-8 rounded-full border-border/70 bg-background/90 shadow-sm backdrop-blur supports-backdrop-filter:bg-background/70"
        >
          <ThemeIcon theme={activeTheme} />
          <span className="sr-only">Current theme: {activeTheme}</span>
        </Button>
      </PopoverTrigger>
      <PopoverContent align="end" className="w-48 rounded-xl border-border/70 bg-popover/95 p-2 shadow-xl">
        <div className="flex flex-col gap-1">
          {themeOptions.map((option) => {
            const active = mounted && activeTheme === option.value;
            return (
              <button
                key={option.value}
                type="button"
                onClick={() => {
                  setTheme(option.value);
                  setOpen(false);
                }}
                className={cn(
                  "flex items-center justify-between rounded-lg border px-2.5 py-2 text-sm transition-colors",
                  active
                    ? "border-primary/30 bg-primary/10 text-foreground"
                    : "border-transparent hover:border-border/70 hover:bg-accent/70 hover:text-accent-foreground"
                )}
                aria-label={`Use ${option.label} theme`}
              >
                <span className="flex items-center gap-2">
                  <ThemeIcon theme={option.value} />
                  <span>{option.label}</span>
                </span>
                <Check className={cn("h-4 w-4", active ? "opacity-100" : "opacity-0")} />
              </button>
            );
          })}
        </div>
      </PopoverContent>
    </Popover>
  );
}
