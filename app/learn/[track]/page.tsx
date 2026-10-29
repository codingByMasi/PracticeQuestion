import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { LessonDoneMark, TrackProgress } from "@/components/lesson/TrackProgress";
import { getContent } from "@/lib/content/loader";

type Params = { params: Promise<{ track: string }> };

export function generateStaticParams() {
  return getContent().tracks.map((t) => ({ track: t.id }));
}

export const dynamicParams = false;

export async function generateMetadata({ params }: Params): Promise<Metadata> {
  const { track } = await params;
  return { title: `${getContent().tracks.find((t) => t.id === track)?.title ?? "Track"} lessons` };
}

export default async function TrackPage({ params }: Params) {
  const { track: trackId } = await params;
  const { tracks, lessons } = getContent();
  const track = tracks.find((t) => t.id === trackId);
  if (!track) notFound();
  const trackLessons = lessons.filter((l) => l.track === track.id);

  return (
    <div className="mx-auto max-w-3xl px-4 py-8">
      <nav aria-label="Breadcrumb" className="text-sm text-zinc-500 dark:text-zinc-400">
        <Link href="/learn" className="hover:underline">
          Learn
        </Link>
      </nav>
      <h1 className="mt-2 text-2xl font-bold tracking-tight">{track.title}</h1>
      <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">{track.description}</p>
      <div className="mt-4">
        <TrackProgress trackId={track.id} lessonIds={trackLessons.map((l) => l.id)} />
      </div>
      <ol className="mt-6 divide-y divide-zinc-200 rounded-lg border border-zinc-200 dark:divide-zinc-800 dark:border-zinc-800">
        {trackLessons.map((l) => (
          <li key={l.id}>
            <Link href={`/learn/${track.id}/${l.id}`} className="flex items-center gap-4 px-4 py-3 hover:bg-zinc-50 dark:hover:bg-zinc-900">
              <span className="w-6 text-right font-mono text-sm text-zinc-500 dark:text-zinc-400">{l.order}</span>
              <span className="flex-1 font-medium">{l.title}</span>
              <span className="text-xs text-zinc-500 dark:text-zinc-400">{l.exerciseSlugs.length} exercises</span>
              <LessonDoneMark trackId={track.id} lessonId={l.id} />
            </Link>
          </li>
        ))}
      </ol>
    </div>
  );
}
