"use client";

import { DIFFICULTIES, type ProblemSummary } from "@/lib/content/schema";
import { useProgress } from "@/lib/progress/ProgressProvider";

export function SolvedStats({ problems, tracks }: { problems: ProblemSummary[]; tracks: { id: string; title: string }[] }) {
  const { store, ready } = useProgress();
  const solved = (p: ProblemSummary) => ready && store.getProblemStatus(p.slug) === "solved";
  const total = problems.filter(solved).length;

  return (
    <section aria-labelledby="solved-h" className="rounded-xl border border-zinc-200 p-5 dark:border-zinc-800">
      <h2 id="solved-h" className="text-sm font-semibold uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
        Solved
      </h2>
      <p className="mt-1 text-3xl font-bold">
        {total}
        <span className="text-base font-normal text-zinc-500 dark:text-zinc-400"> / {problems.length}</span>
      </p>
      <div className="mt-4 overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-xs text-zinc-500 dark:text-zinc-400">
              <th scope="col" className="py-1 pr-3 font-medium">
                Track
              </th>
              {DIFFICULTIES.map((d) => (
                <th key={d} scope="col" className="py-1 pr-3 font-medium">
                  {d}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {tracks.map((t) => (
              <tr key={t.id} className="border-t border-zinc-100 dark:border-zinc-800">
                <th scope="row" className="py-1.5 pr-3 text-left font-medium">
                  {t.title}
                </th>
                {DIFFICULTIES.map((d) => {
                  const pool = problems.filter((p) => p.track === t.id && p.difficulty === d);
                  return (
                    <td key={d} className="py-1.5 pr-3 tabular-nums">
                      {pool.filter(solved).length}
                      <span className="text-zinc-500 dark:text-zinc-400">/{pool.length}</span>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
