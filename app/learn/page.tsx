import type { Metadata } from "next";
import Link from "next/link";
import { TrackProgress } from "@/components/lesson/TrackProgress";
import { getContent } from "@/lib/content/loader";

export const metadata: Metadata = { title: "Learn" };

export default function LearnPage() {
  const { tracks, lessons, problems } = getContent();
  return (
    <div className="mx-auto max-w-5xl px-4 py-8">
      <h1 className="text-2xl font-bold tracking-tight">Learn</h1>
      <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">Guided lessons with runnable examples, each followed by exercises.</p>
      <ul className="mt-6 grid gap-4 sm:grid-cols-2">
        {tracks.map((t) => {
          const trackLessons = lessons.filter((l) => l.track === t.id);
          return (
            <li key={t.id} className="flex flex-col gap-3 rounded-xl border border-zinc-200 p-5 dark:border-zinc-800">
              <h2 className="text-lg font-semibold">
                <Link href={`/learn/${t.id}`} className="hover:underline">
                  {t.title}
                </Link>
              </h2>
              <p className="flex-1 text-sm text-zinc-600 dark:text-zinc-400">{t.description}</p>
              <p className="text-xs text-zinc-500">
                {trackLessons.length} lessons · {problems.filter((p) => p.track === t.id).length} problems
              </p>
              <TrackProgress trackId={t.id} lessonIds={trackLessons.map((l) => l.id)} />
            </li>
          );
        })}
      </ul>
    </div>
  );
}
