import Link from "next/link";
import { ContinueCard } from "@/components/dashboard/ContinueCard";
import { DailyChallengeCard } from "@/components/dashboard/DailyChallengeCard";
import { Heatmap } from "@/components/dashboard/Heatmap";
import { SolvedStats } from "@/components/dashboard/SolvedStats";
import { StreakCard } from "@/components/dashboard/StreakCard";
import { TrackProgress } from "@/components/lesson/TrackProgress";
import { getContent, toSummary } from "@/lib/content/loader";

export default function DashboardPage() {
  const { problems, tracks, lessons } = getContent();
  const summaries = problems.map(toSummary);
  const firstLesson = lessons[0];
  const trackTitles = Object.fromEntries(tracks.map((t) => [t.id, t.title]));

  return (
    <div className="mx-auto max-w-7xl space-y-6 px-4 py-8">
      <header>
        <h1 className="text-3xl font-bold tracking-tight">Welcome to CodeDrill</h1>
        <p className="mt-1 text-zinc-600 dark:text-zinc-400">Practice SQL and Python in your browser. Your progress stays on this device.</p>
      </header>

      <div className="grid gap-4 md:grid-cols-3">
        <ContinueCard
          fallbackHref={firstLesson ? `/learn/${firstLesson.track}/${firstLesson.id}` : "/problems"}
          fallbackTitle={firstLesson ? `${trackTitles[firstLesson.track]}: ${firstLesson.title}` : "Browse problems"}
        />
        <DailyChallengeCard pool={summaries} trackTitles={trackTitles} />
        <StreakCard />
      </div>

      <div className="grid gap-4 lg:grid-cols-[1fr_1fr]">
        <SolvedStats problems={summaries} tracks={tracks.map((t) => ({ id: t.id, title: t.title }))} />
        <section aria-labelledby="lessons-h" className="space-y-4 rounded-xl border border-zinc-200 p-5 dark:border-zinc-800">
          <h2 id="lessons-h" className="text-sm font-semibold uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
            Lessons
          </h2>
          {tracks.map((t) => (
            <div key={t.id} className="space-y-1">
              <Link href={`/learn/${t.id}`} className="font-medium hover:underline">
                {t.title}
              </Link>
              <TrackProgress trackId={t.id} lessonIds={lessons.filter((l) => l.track === t.id).map((l) => l.id)} />
            </div>
          ))}
        </section>
      </div>

      <section aria-labelledby="activity-h" className="rounded-xl border border-zinc-200 p-5 dark:border-zinc-800">
        <h2 id="activity-h" className="mb-3 text-sm font-semibold uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
          Activity
        </h2>
        <Heatmap />
      </section>
    </div>
  );
}
