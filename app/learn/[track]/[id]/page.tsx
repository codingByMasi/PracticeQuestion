import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { LessonView } from "@/components/lesson/LessonView";
import { getContent, toSummary } from "@/lib/content/loader";
import type { ProblemSummary } from "@/lib/content/schema";

type Params = { params: Promise<{ track: string; id: string }> };

export function generateStaticParams() {
  return getContent().lessons.map((l) => ({ track: l.track, id: l.id }));
}

export const dynamicParams = false;

export async function generateMetadata({ params }: Params): Promise<Metadata> {
  const { track, id } = await params;
  return { title: getContent().lessons.find((l) => l.track === track && l.id === id)?.title ?? "Lesson" };
}

export default async function LessonPage({ params }: Params) {
  const { track: trackId, id } = await params;
  const { tracks, lessons, problems, datasets } = getContent();
  const track = tracks.find((t) => t.id === trackId);
  const trackLessons = lessons.filter((l) => l.track === trackId);
  const index = trackLessons.findIndex((l) => l.id === id);
  const lesson = trackLessons[index];
  if (!track || !lesson) notFound();

  const link = (i: number) => {
    const l = trackLessons[i];
    return l ? { id: l.id, title: l.title } : null;
  };
  const exercises = lesson.exerciseSlugs
    .map((slug) => problems.find((p) => p.slug === slug))
    .filter((p) => p !== undefined)
    .map(toSummary) satisfies ProblemSummary[];

  return (
    <LessonView
      track={{ id: track.id, title: track.title, runnerId: track.runnerId, editorLanguage: track.editorLanguage }}
      tracks={tracks.map((t) => ({ runnerId: t.runnerId, editorLanguage: t.editorLanguage }))}
      lesson={{ id: lesson.id, title: lesson.title, order: lesson.order, bodyMd: lesson.bodyMd }}
      total={trackLessons.length}
      datasetSql={datasets.find((d) => d.id === lesson.datasetId)?.sql}
      exercises={exercises}
      prev={link(index - 1)}
      next={link(index + 1)}
    />
  );
}
