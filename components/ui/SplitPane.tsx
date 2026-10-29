"use client";

import { useRef, useState, type KeyboardEvent, type PointerEvent, type ReactNode } from "react";
import { useMediaQuery } from "@/lib/hooks/use-media-query";

type Props = {
  first: ReactNode;
  second: ReactNode;
  orientation?: "horizontal" | "vertical";
  /** Initial size of the first pane, in percent. */
  initial?: number;
  min?: number;
  label: string;
  /** Below the `lg` breakpoint panes stack and aren't resizable. */
  stackOnMobile?: boolean;
  className?: string;
};

export function SplitPane({ first, second, orientation = "horizontal", initial = 50, min = 20, label, stackOnMobile = true, className = "" }: Props) {
  const wide = useMediaQuery("(min-width: 1024px)", true);
  const [pct, setPct] = useState(initial);
  const ref = useRef<HTMLDivElement>(null);
  const horizontal = orientation === "horizontal";
  const clamp = (v: number) => Math.min(100 - min, Math.max(min, v));

  if (stackOnMobile && !wide) {
    return (
      <div className={`flex flex-col ${className}`}>
        <div>{first}</div>
        <div>{second}</div>
      </div>
    );
  }

  const onPointerDown = (e: PointerEvent<HTMLDivElement>) => {
    e.currentTarget.setPointerCapture(e.pointerId);
  };
  const onPointerMove = (e: PointerEvent<HTMLDivElement>) => {
    if (!e.currentTarget.hasPointerCapture(e.pointerId) || !ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    const v = horizontal ? ((e.clientX - rect.left) / rect.width) * 100 : ((e.clientY - rect.top) / rect.height) * 100;
    setPct(clamp(v));
  };
  const onKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
    const dec = horizontal ? "ArrowLeft" : "ArrowUp";
    const inc = horizontal ? "ArrowRight" : "ArrowDown";
    if (e.key === dec) setPct((p) => clamp(p - 5));
    else if (e.key === inc) setPct((p) => clamp(p + 5));
    else if (e.key === "Home") setPct(min);
    else if (e.key === "End") setPct(100 - min);
    else return;
    e.preventDefault();
  };

  return (
    <div ref={ref} className={`flex min-h-0 min-w-0 ${horizontal ? "flex-row" : "flex-col"} ${className}`}>
      <div className="min-h-0 min-w-0 overflow-hidden" style={{ flexBasis: `${pct}%`, flexGrow: 0, flexShrink: 0 }}>
        {first}
      </div>
      <div
        role="separator"
        aria-orientation={horizontal ? "vertical" : "horizontal"}
        aria-label={label}
        aria-valuenow={Math.round(pct)}
        aria-valuemin={min}
        aria-valuemax={100 - min}
        tabIndex={0}
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onKeyDown={onKeyDown}
        className={`group relative shrink-0 touch-none bg-zinc-200 hover:bg-indigo-400 focus-visible:bg-indigo-500 dark:bg-zinc-800 ${
          horizontal ? "w-1 cursor-col-resize" : "h-1 cursor-row-resize"
        }`}
      />
      <div className="min-h-0 min-w-0 flex-1 overflow-hidden">{second}</div>
    </div>
  );
}
