import { useMemo } from "react";

interface Style {
  color?: string;
  bold?: boolean;
}

function parseAnsi(text: string): { text: string; style: Style }[] {
  const ansiRegex = /[\u001b\x1b]\[([0-9;]*)m/g;
  const segments: { text: string; style: Style }[] = [];
  
  let match;
  let lastIndex = 0;
  let currentStyle: Style = {};

  const codeToStyle = (code: number, style: Style): Style => {
    const newStyle = { ...style };
    if (code === 0) {
      return {};
    }
    if (code === 1) {
      newStyle.bold = true;
    } else if (code === 22) {
      newStyle.bold = false;
    } else if (code >= 30 && code <= 37) {
      const colors = [
        "text-black dark:text-white", // 30
        "text-red-500 dark:text-red-400", // 31
        "text-emerald-500 dark:text-emerald-400", // 32
        "text-amber-500 dark:text-amber-400", // 33
        "text-blue-500 dark:text-blue-400", // 34
        "text-magenta-500 dark:text-magenta-400", // 35
        "text-cyan-500 dark:text-cyan-400", // 36
        "text-gray-500 dark:text-gray-400", // 37
      ];
      newStyle.color = colors[code - 30];
    } else if (code === 39) {
      delete newStyle.color;
    } else if (code >= 90 && code <= 97) {
      const brightColors = [
        "text-gray-400 dark:text-gray-500", // 90
        "text-red-400 dark:text-red-300", // 91
        "text-emerald-400 dark:text-emerald-300", // 92
        "text-amber-400 dark:text-amber-300", // 93
        "text-blue-400 dark:text-blue-300", // 94
        "text-magenta-400 dark:text-magenta-300", // 95
        "text-cyan-400 dark:text-cyan-300", // 96
        "text-white dark:text-black", // 97
      ];
      newStyle.color = brightColors[code - 90];
    }
    return newStyle;
  };

  while ((match = ansiRegex.exec(text)) !== null) {
    const textSegment = text.slice(lastIndex, match.index);
    if (textSegment) {
      segments.push({ text: textSegment, style: { ...currentStyle } });
    }

    const codesStr = match[1];
    const codes = codesStr ? codesStr.split(";").map(Number) : [0];
    for (const code of codes) {
      currentStyle = codeToStyle(code, currentStyle);
    }

    lastIndex = ansiRegex.lastIndex;
  }

  const remainingText = text.slice(lastIndex);
  if (remainingText) {
    segments.push({ text: remainingText, style: { ...currentStyle } });
  }

  return segments;
}

export function AnsiLog({ text }: { text: string }) {
  const segments = useMemo(() => parseAnsi(text), [text]);

  return (
    <pre className="w-max min-w-full whitespace-pre font-mono text-xs leading-5 text-foreground/95">
      {segments.map((seg, i) => {
        const classes = [];
        if (seg.style.bold) classes.push("font-bold");
        if (seg.style.color) classes.push(seg.style.color);
        
        if (classes.length > 0) {
          return (
            <span key={i} className={classes.join(" ")}>
              {seg.text}
            </span>
          );
        }
        return seg.text;
      })}
    </pre>
  );
}
