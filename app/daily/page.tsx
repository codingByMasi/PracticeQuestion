import type { Metadata } from "next";
import { DailyPage } from "@/components/dashboard/DailyPage";
import { getContent, toSummary } from "@/lib/content/loader";

export const metadata: Metadata = { title: "Daily challenge" };

export default function Daily() {
  const { problems, tracks } = getContent();
  return <DailyPage pool={problems.map(toSummary)} trackTitles={Object.fromEntries(tracks.map((t) => [t.id, t.title]))} />;
}
