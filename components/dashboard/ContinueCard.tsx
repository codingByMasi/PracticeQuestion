"use client";

import Link from "next/link";
import { useProgress } from "@/lib/progress/ProgressProvider";

export function ContinueCard({ fallbackHref, fallbackTitle }: { fallbackHref: string; fallbackTitle: string }) {
  const { store, ready } = useProgress();
  const last = ready ? store.getLastVisited() : null;
  return (
    <section aria-labelledby="continue-h" className="flex flex-col gap-2 rounded-xl border border-zinc-200 p-5 dark:border-zinc-800">
      <h2 id="continue-h" className="text-sm font-semibold uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
        {last ? "Continue where you left off" : "Start here"}
      </h2>
      <p className="text-lg font-semibold">{last?.title ?? fallbackTitle}</p>
      <Link
        href={last?.href ?? fallbackHref}
        className="inline-flex w-fit rounded-md border border-zinc-300 px-3 py-1.5 text-sm font-medium hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-900"
      >
        {last ? "Continue" : "Begin"} →
      </Link>
    </section>
  );
}
