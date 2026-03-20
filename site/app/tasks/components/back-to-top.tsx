"use client";

import { useState, useEffect } from "react";
import { ArrowUp } from "lucide-react";

export function BackToTop() {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const toggleVisibility = () => {
      if (window.scrollY > 300) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };

    window.addEventListener("scroll", toggleVisibility);
    return () => window.removeEventListener("scroll", toggleVisibility);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  };

  if (!isVisible) return null;

  return (
    <button
      type="button"
      onClick={scrollToTop}
      className="fixed bottom-8 right-8 p-3 bg-secondary text-foreground rounded-full shadow-lg border border-border hover:bg-secondary/80 transition-all z-50 flex items-center justify-center group backdrop-blur-sm"
      aria-label="Back to top"
    >
      <ArrowUp className="w-5 h-5 group-hover:-translate-y-1 transition-transform" />
    </button>
  );
}
