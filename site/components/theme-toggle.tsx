"use client";

import * as React from "react";
import { Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";

import { Button } from "@/components/ui/button";

export function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme();
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
  }, []);

  const isDark = mounted ? resolvedTheme !== "light" : true;

  return (
    <Button
      type="button"
      variant="outline"
      size="icon-sm"
      aria-label={isDark ? "Switch to light theme" : "Switch to dark theme"}
      className="size-8 cursor-pointer rounded-full border-border/70 bg-background/90 shadow-sm backdrop-blur supports-backdrop-filter:bg-background/70"
      onClick={() => setTheme(isDark ? "light" : "dark")}
    >
      {isDark ? <Moon className="h-4 w-4" /> : <Sun className="h-4 w-4" />}
      <span className="sr-only">Current theme: {isDark ? "dark" : "light"}</span>
    </Button>
  );
}
