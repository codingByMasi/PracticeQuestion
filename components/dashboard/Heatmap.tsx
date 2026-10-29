"use client";

import { useMemo } from "react";
import { useToday } from "@/lib/hooks/use-today";
import { buildHeatmap, intensity } from "@/lib/progress/heatmap";
import { useProgress } from "@/lib/progress/ProgressProvider";

const LEVELS = [
  "bg-zinc-100 dark:bg-zinc-800",
  "bg-emerald-200 dark:bg-emerald-900",
  "bg-emerald-400 dark:bg-emerald-700",
  "bg-emerald-500 dark:bg-emerald-500",
  "bg-emerald-700 dark:bg-emerald-300",
];

export function Heatmap({ weeks = 53 }: { weeks?: number }) {
  const { store, ready } = useProgress();
  const today = useToday();
  const counts = ready ? store.getActivityCounts() : {};
  const key = JSON.stringify(counts);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const grid = useMemo(() => (today ? buildHeatmap(counts, today, weeks) : []), [key, today, weeks]);
  const activeDays = Object.keys(counts).length;

  if (!today) return <div className="h-28" aria-hidden="true" />;
  return (
    <figure className="space-y-2">
      <div className="overflow-x-auto pb-1">
        <div className="flex w-max gap-[3px]" role="img" aria-label={`Activity heatmap: ${activeDays} active days in the last year`}>
          {grid.map((col, i) => (
            <div key={i} className="flex flex-col gap-[3px]">
              {col.map((cell) => (
                <div
                  key={cell.date}
                  title={cell.inRange ? `${cell.date}: ${cell.count} activit${cell.count === 1 ? "y" : "ies"}` : undefined}
                  className={`h-3 w-3 rounded-sm ${cell.inRange ? LEVELS[intensity(cell.count)] : "bg-transparent"}`}
                />
              ))}
            </div>
          ))}
        </div>
      </div>
      <figcaption className="flex items-center gap-1 text-xs text-zinc-500">
        Less
        {LEVELS.map((c, i) => (
          <span key={i} className={`h-3 w-3 rounded-sm ${c}`} aria-hidden="true" />
        ))}
        More
      </figcaption>
    </figure>
  );
}
