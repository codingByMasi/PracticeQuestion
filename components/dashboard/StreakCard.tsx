"use client";

import { useProgress } from "@/lib/progress/ProgressProvider";
import { useStreak } from "@/lib/progress/use-streak";

export function StreakCard() {
  const { ready } = useProgress();
  const { current, longest } = useStreak();
  return (
    <section aria-labelledby="streak-h" className="rounded-xl border border-zinc-200 p-5 dark:border-zinc-800">
      <h2 id="streak-h" className="text-sm font-semibold uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
        Streak
      </h2>
      <p className="mt-1 text-3xl font-bold">
        <span aria-hidden="true">🔥</span> {ready ? current : "–"}
        <span className="text-base font-normal text-zinc-500 dark:text-zinc-400"> day{current === 1 ? "" : "s"}</span>
      </p>
      <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">Longest: {ready ? longest : "–"} days. Submit an answer or finish a lesson to keep it going.</p>
    </section>
  );
}
