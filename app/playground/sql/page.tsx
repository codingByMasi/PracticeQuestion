import type { Metadata } from "next";
import { SqlPlayground } from "@/components/playground/SqlPlayground";
import { getContent } from "@/lib/content/loader";

export const metadata: Metadata = { title: "SQL playground" };

export default function SqlPlaygroundPage() {
  const datasets = getContent().datasets.map(({ id, title, description, sql }) => ({ id, title, description, sql }));
  return <SqlPlayground datasets={datasets} />;
}
