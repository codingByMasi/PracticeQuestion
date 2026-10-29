import type { Metadata } from "next";
import { ProblemList } from "@/components/problem/ProblemList";
import { getContent, toSummary } from "@/lib/content/loader";

export const metadata: Metadata = { title: "Problems" };

export default function ProblemsPage() {
  const { problems, tracks } = getContent();
  return (
    <div className="mx-auto max-w-7xl px-4 py-8">
      <h1 className="text-2xl font-bold tracking-tight">Problems</h1>
      <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
        {problems.length} problems across {tracks.length} tracks. Your code runs entirely in your browser.
      </p>
      <ProblemList problems={problems.map(toSummary)} tracks={tracks.map((t) => ({ id: t.id, title: t.title }))} />
    </div>
  );
}
