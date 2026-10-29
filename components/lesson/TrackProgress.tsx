"use client";

import { lessonKey } from "@/lib/content/schema";
import { useProgress } from "@/lib/progress/ProgressProvider";

/** Progress bar for lessons completed in a track. */
export function TrackProgress({ trackId, lessonIds }: { trackId: string; lessonIds: string[] }) {
  const { store, ready } = useProgress();
  const done = ready ? lessonIds.filter((id) => store.getLessonDone(lessonKey(trackId, id))).length : 0;
  const pct = lessonIds.length ? Math.round((done / lessonIds.length) * 100) : 0;
  return (
    <div className="space-y-1">
      <div
        className="h-2 overflow-hidden rounded-full bg-zinc-200 dark:bg-zinc-800"
        role="progressbar"
        aria-valuenow={pct}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label="Lessons completed"
      >
        <div className="h-full rounded-full bg-indigo-600 transition-all" style={{ width: `${pct}%` }} />
      </div>
      <p className="text-xs text-zinc-500 dark:text-zinc-400">
        {done} of {lessonIds.length} lessons complete
      </p>
    </div>
  );
}

export function LessonDoneMark({ trackId, lessonId }: { trackId: string; lessonId: string }) {
  const { store, ready } = useProgress();
  const done = ready && store.getLessonDone(lessonKey(trackId, lessonId));
  return (
    <span className={done ? "text-emerald-600 dark:text-emerald-400" : "text-zinc-300 dark:text-zinc-700"}>
      <span aria-hidden="true">✓</span>
      <span className="sr-only">{done ? "Completed" : "Not completed"}</span>
    </span>
  );
}
