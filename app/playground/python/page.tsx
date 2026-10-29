import type { Metadata } from "next";
import { PythonPlayground } from "@/components/playground/PythonPlayground";

export const metadata: Metadata = { title: "Python playground" };

export default function PythonPlaygroundPage() {
  return <PythonPlayground />;
}
