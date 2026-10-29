"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { DifficultyBadge, Tag } from "@/components/ui/Badge";
import { DIFFICULTIES, type ProblemSummary } from "@/lib/content/schema";
import { useProgress } from "@/lib/progress/ProgressProvider";
import type { Status } from "@/lib/progress/types";

type StatusFilter = "all" | "solved" | "unsolved";

const PAGE_SIZE = 50;

const selectClass =
  "rounded-md border border-zinc-300 bg-white px-2 py-1.5 text-sm dark:border-zinc-700 dark:bg-zinc-900";

const STATUS_ICON: Record<Status, { icon: string; label: string; className: string }> = {
  solved: { icon: "✓", label: "Solved", className: "text-emerald-600 dark:text-emerald-400" },
  attempted: { icon: "◐", label: "Attempted", className: "text-amber-600 dark:text-amber-400" },
  unsolved: { icon: "", label: "Not attempted", className: "" },
};

export function ProblemList({ problems, tracks }: { problems: ProblemSummary[]; tracks: { id: string; title: string }[] }) {
  const { store, ready } = useProgress();
  const [track, setTrack] = useState("all");
  const [difficulty, setDifficulty] = useState("all");
  const [tag, setTag] = useState("all");
  const [status, setStatus] = useState<StatusFilter>("all");
  const [query, setQuery] = useState("");

  const tags = useMemo(
    () => [...new Set(problems.filter((p) => track === "all" || p.track === track).flatMap((p) => p.tags))].sort(),
    [problems, track],
  );
  const difficultyRank = (d: string) => DIFFICULTIES.indexOf(d as (typeof DIFFICULTIES)[number]);

  const statusOf = (slug: string): Status => (ready ? store.getProblemStatus(slug) : "unsolved");
  const filtered = problems
    .filter((p) => track === "all" || p.track === track)
    .filter((p) => difficulty === "all" || p.difficulty === difficulty)
    .filter((p) => tag === "all" || p.tags.includes(tag))
    .filter((p) => status === "all" || (status === "solved") === (statusOf(p.slug) === "solved"))
    .filter((p) => !query || p.title.toLowerCase().includes(query.toLowerCase()))
    .sort(
      (a, b) =>
        a.track.localeCompare(b.track) ||
        (a.order ?? Number.MAX_SAFE_INTEGER) - (b.order ?? Number.MAX_SAFE_INTEGER) ||
        difficultyRank(a.difficulty) - difficultyRank(b.difficulty) ||
        a.title.localeCompare(b.title),
    );

  // The page size resets whenever a filter changes (the pager remembers which filters it was grown for).
  const filterKey = [track, difficulty, tag, status, query].join("|");
  const [pager, setPager] = useState({ key: filterKey, count: PAGE_SIZE });
  const visible = pager.key === filterKey ? pager.count : PAGE_SIZE;
  const shown = filtered.slice(0, visible);

  return (
    <div className="mt-6 space-y-4">
      <form className="flex flex-wrap items-end gap-3" onSubmit={(e) => e.preventDefault()} aria-label="Filter problems">
        <label className="flex flex-col gap-1 text-xs font-medium text-zinc-600 dark:text-zinc-400">
          Search
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Title…"
            className={selectClass}
          />
        </label>
        <label className="flex flex-col gap-1 text-xs font-medium text-zinc-600 dark:text-zinc-400">
          Track
          <select
            className={selectClass}
            value={track}
            onChange={(e) => {
              setTrack(e.target.value);
              setTag("all");
            }}
          >
            <option value="all">All tracks</option>
            {tracks.map((t) => (
              <option key={t.id} value={t.id}>
                {t.title}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs font-medium text-zinc-600 dark:text-zinc-400">
          Difficulty
          <select className={selectClass} value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
            <option value="all">Any difficulty</option>
            {DIFFICULTIES.map((d) => (
              <option key={d}>{d}</option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs font-medium text-zinc-600 dark:text-zinc-400">
          Tag
          <select className={selectClass} value={tag} onChange={(e) => setTag(e.target.value)}>
            <option value="all">Any tag</option>
            {tags.map((t) => (
              <option key={t}>{t}</option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs font-medium text-zinc-600 dark:text-zinc-400">
          Status
          <select className={selectClass} value={status} onChange={(e) => setStatus(e.target.value as StatusFilter)}>
            <option value="all">Any status</option>
            <option value="solved">Solved</option>
            <option value="unsolved">Unsolved</option>
          </select>
        </label>
        <p className="ml-auto text-sm text-zinc-500 dark:text-zinc-400" aria-live="polite">
          {shown.length} of {filtered.length} shown
        </p>
      </form>

      <div className="overflow-hidden rounded-lg border border-zinc-200 dark:border-zinc-800">
        <table className="w-full text-sm">
          <thead className="bg-zinc-50 text-left text-xs uppercase tracking-wide text-zinc-500 dark:text-zinc-400 dark:bg-zinc-900">
            <tr>
              <th scope="col" className="w-10 px-3 py-2">
                <span className="sr-only">Status</span>
              </th>
              <th scope="col" className="px-3 py-2">
                Title
              </th>
              <th scope="col" className="hidden px-3 py-2 sm:table-cell">
                Track
              </th>
              <th scope="col" className="px-3 py-2">
                Difficulty
              </th>
              <th scope="col" className="hidden px-3 py-2 md:table-cell">
                Tags
              </th>
            </tr>
          </thead>
          <tbody>
            {shown.map((p) => {
              const s = STATUS_ICON[statusOf(p.slug)];
              return (
                <tr key={p.slug} className="border-t border-zinc-100 hover:bg-zinc-50 dark:border-zinc-800 dark:hover:bg-zinc-900/60">
                  <td className={`px-3 py-2 text-center ${s.className}`}>
                    <span aria-hidden="true">{s.icon}</span>
                    <span className="sr-only">{s.label}</span>
                  </td>
                  <td className="px-3 py-2">
                    <Link href={`/problems/${p.slug}`} className="font-medium hover:text-indigo-600 hover:underline dark:hover:text-indigo-400">
                      {p.title}
                    </Link>
                  </td>
                  <td className="hidden px-3 py-2 text-zinc-600 sm:table-cell dark:text-zinc-400">
                    {tracks.find((t) => t.id === p.track)?.title ?? p.track}
                  </td>
                  <td className="px-3 py-2">
                    <DifficultyBadge difficulty={p.difficulty} />
                  </td>
                  <td className="hidden px-3 py-2 md:table-cell">
                    <div className="flex flex-wrap gap-1">
                      {p.tags.map((t) => (
                        <Tag key={t}>{t}</Tag>
                      ))}
                    </div>
                  </td>
                </tr>
              );
            })}
            {filtered.length === 0 && (
              <tr>
                <td colSpan={5} className="px-3 py-8 text-center text-zinc-500 dark:text-zinc-400">
                  No problems match these filters.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      {filtered.length > shown.length && (
        <div className="flex justify-center">
          <button
            type="button"
            onClick={() => setPager({ key: filterKey, count: visible + PAGE_SIZE })}
            className="rounded-md border border-zinc-300 bg-white px-4 py-2 text-sm font-medium hover:bg-zinc-50 dark:border-zinc-700 dark:bg-zinc-900 dark:hover:bg-zinc-800"
          >
            Show {Math.min(PAGE_SIZE, filtered.length - shown.length)} more
          </button>
        </div>
      )}
    </div>
  );
}
