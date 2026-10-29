"use client";

import Link from "next/link";
import { DifficultyBadge } from "@/components/ui/Badge";
import type { ProblemSummary } from "@/lib/content/schema";
import { useToday } from "@/lib/hooks/use-today";
import { addDays } from "@/lib/progress/dates";
import { useProgress } from "@/lib/progress/ProgressProvider";
import { DailyChallengeCard, dailyChallengeFor } from "./DailyChallengeCard";

export function DailyPage({ pool, trackTitles }: { pool: ProblemSummary[]; trackTitles: Record<string, string> }) {
  const today = useToday();
  const { store, ready } = useProgress();
  const past = today
    ? Array.from({ length: 6 }, (_, i) => {
        const date = addDays(today, -(i + 1));
        return { date, problem: dailyChallengeFor(pool, date) };
      })
    : [];

  return (
    <div className="mx-auto max-w-3xl space-y-6 px-4 py-8">
      <header>
        <h1 className="text-2xl font-bold tracking-tight">Daily challenge</h1>
        <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
          One problem a day, picked from the whole pool. Everyone gets the same problem on the same calendar date.
        </p>
      </header>
      <DailyChallengeCard pool={pool} trackTitles={trackTitles} />
      <section aria-labelledby="past-h">
        <h2 id="past-h" className="mb-2 text-sm font-semibold uppercase tracking-wide text-zinc-500">
          Previous days
        </h2>
        <ul className="divide-y divide-zinc-200 rounded-lg border border-zinc-200 dark:divide-zinc-800 dark:border-zinc-800">
          {past.map(({ date, problem }) =>
            problem ? (
              <li key={date} className="flex items-center gap-3 px-4 py-2.5 text-sm">
                <span className="w-24 font-mono text-xs text-zinc-500">{date}</span>
                <Link href={`/problems/${problem.slug}`} className="flex-1 font-medium hover:underline">
                  {problem.title}
                </Link>
                <DifficultyBadge difficulty={problem.difficulty} />
                {ready && store.getProblemStatus(problem.slug) === "solved" && (
                  <span className="text-emerald-600 dark:text-emerald-400">
                    <span aria-hidden="true">✓</span>
                    <span className="sr-only">Solved</span>
                  </span>
                )}
              </li>
            ) : null,
          )}
        </ul>
      </section>
    </div>
  );
}
