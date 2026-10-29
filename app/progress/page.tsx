import type { Metadata } from "next";
import { ExportImport } from "@/components/dashboard/ExportImport";
import { Heatmap } from "@/components/dashboard/Heatmap";
import { SolvedStats } from "@/components/dashboard/SolvedStats";
import { StreakCard } from "@/components/dashboard/StreakCard";
import { TrackProgress } from "@/components/lesson/TrackProgress";
import { getContent, toSummary } from "@/lib/content/loader";

export const metadata: Metadata = { title: "Progress" };

export default function ProgressPage() {
  const { problems, tracks, lessons } = getContent();
  return (
    <div className="mx-auto max-w-5xl space-y-6 px-4 py-8">
      <h1 className="text-2xl font-bold tracking-tight">Your progress</h1>
      <div className="grid gap-4 md:grid-cols-2">
        <StreakCard />
        <section aria-labelledby="lessons-h" className="space-y-3 rounded-xl border border-zinc-200 p-5 dark:border-zinc-800">
          <h2 id="lessons-h" className="text-sm font-semibold uppercase tracking-wide text-zinc-500">
            Lessons
          </h2>
          {tracks.map((t) => (
            <div key={t.id}>
              <p className="text-sm font-medium">{t.title}</p>
              <TrackProgress trackId={t.id} lessonIds={lessons.filter((l) => l.track === t.id).map((l) => l.id)} />
            </div>
          ))}
        </section>
      </div>
      <section aria-labelledby="activity-h" className="rounded-xl border border-zinc-200 p-5 dark:border-zinc-800">
        <h2 id="activity-h" className="mb-3 text-sm font-semibold uppercase tracking-wide text-zinc-500">
          Activity in the last year
        </h2>
        <Heatmap />
      </section>
      <SolvedStats problems={problems.map(toSummary)} tracks={tracks.map((t) => ({ id: t.id, title: t.title }))} />
      <ExportImport />
    </div>
  );
}
