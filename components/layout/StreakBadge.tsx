"use client";

import Link from "next/link";
import { useProgress } from "@/lib/progress/ProgressProvider";
import { useStreak } from "@/lib/progress/use-streak";

export function StreakBadge() {
  const { ready } = useProgress();
  const streak = useStreak();
  if (!ready) return null;
  return (
    <Link
      href="/progress"
      className="rounded-md px-2 py-1 text-sm font-medium text-amber-700 hover:bg-amber-50 dark:text-amber-400 dark:hover:bg-zinc-800"
      aria-label={`Current streak: ${streak.current} day${streak.current === 1 ? "" : "s"}`}
    >
      <span aria-hidden="true">🔥</span> {streak.current}
    </Link>
  );
}
