import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { ProblemWorkspace } from "@/components/problem/ProblemWorkspace";
import { getContent, toSummary } from "@/lib/content/loader";
import { getNextTarget } from "@/lib/content/next-problem";

type Params = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return getContent().problems.map((p) => ({ slug: p.slug }));
}

export const dynamicParams = false;

export async function generateMetadata({ params }: Params): Promise<Metadata> {
  const { slug } = await params;
  const problem = getContent().problems.find((p) => p.slug === slug);
  return { title: problem?.title ?? "Problem" };
}

export default async function ProblemPage({ params }: Params) {
  const { slug } = await params;
  const content = getContent();
  const problem = content.problems.find((p) => p.slug === slug);
  if (!problem) notFound();
  const track = content.tracks.find((t) => t.id === problem.track);
  if (!track) notFound();
  const datasetSql = problem.kind === "sql" ? content.datasets.find((d) => d.id === problem.datasetId)?.sql : undefined;
  const next = getNextTarget(content.problems.map(toSummary), content.lessons, slug);
  return (
    <ProblemWorkspace
      problem={problem}
      runnerId={track.runnerId}
      editorLanguage={track.editorLanguage}
      datasetSql={datasetSql}
      next={next}
    />
  );
}
