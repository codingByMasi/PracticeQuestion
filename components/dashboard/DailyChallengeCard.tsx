"use client";

import Link from "next/link";
import { DifficultyBadge } from "@/components/ui/Badge";
import type { ProblemSummary } from "@/lib/content/schema";
import { pickDailyChallenge } from "@/lib/daily";
import { useToday } from "@/lib/hooks/use-today";
import { useProgress } from "@/lib/progress/ProgressProvider";

export function dailyChallengeFor(pool: ProblemSummary[], date: string | null): ProblemSummary | null {
  if (!date) return null;
  const slug = pickDailyChallenge(
    pool.map((p) => p.slug),
    date,
  );
  return pool.find((p) => p.slug === slug) ?? null;
}

export function DailyChallengeCard({ pool, trackTitles }: { pool: ProblemSummary[]; trackTitles: Record<string, string> }) {
  const today = useToday();
  const problem = dailyChallengeFor(pool, today);
  const { store, ready } = useProgress();
  const solved = !!problem && ready && store.getProblemStatus(problem.slug) === "solved";

  return (
    <section aria-labelledby="daily-h" className="flex flex-col gap-3 rounded-xl border border-indigo-200 bg-indigo-50/60 p-5 dark:border-indigo-900 dark:bg-indigo-950/30">
      <h2 id="daily-h" className="text-sm font-semibold uppercase tracking-wide text-indigo-700 dark:text-indigo-300">
        Daily challenge {today && <span className="font-normal normal-case text-zinc-500 dark:text-zinc-400">· {today}</span>}
      </h2>
      {problem ? (
        <>
          <p className="text-lg font-semibold">{problem.title}</p>
          <div className="flex items-center gap-2 text-sm">
            <DifficultyBadge difficulty={problem.difficulty} />
            <span className="text-zinc-600 dark:text-zinc-400">{trackTitles[problem.track] ?? problem.track}</span>
            {solved && <span className="font-medium text-emerald-600 dark:text-emerald-400">✓ Done today</span>}
          </div>
          <Link
            href={`/problems/${problem.slug}`}
            className="mt-1 inline-flex w-fit rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-indigo-500"
          >
            {solved ? "Review" : "Solve it"}
          </Link>
        </>
      ) : (
        <p className="h-20 text-sm text-zinc-500 dark:text-zinc-400">Picking today&apos;s challenge…</p>
      )}
    </section>
  );
}
