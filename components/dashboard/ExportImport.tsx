"use client";

import { useRef, useState } from "react";
import { Button } from "@/components/ui/Button";
import { toLocalDateKey } from "@/lib/progress/dates";
import { useProgress } from "@/lib/progress/ProgressProvider";

export function ExportImport() {
  const { store } = useProgress();
  const fileRef = useRef<HTMLInputElement>(null);
  const [message, setMessage] = useState<{ ok: boolean; text: string } | null>(null);

  const doExport = () => {
    const blob = new Blob([store.export()], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `codedrill-progress-${toLocalDateKey(new Date())}.json`;
    a.click();
    URL.revokeObjectURL(url);
    setMessage({ ok: true, text: "Progress exported." });
  };

  const doImport = async (file: File) => {
    try {
      const text = await file.text();
      if (!window.confirm("Importing replaces all progress on this device. Continue?")) return;
      store.import(text);
      setMessage({ ok: true, text: "Progress imported." });
    } catch {
      setMessage({ ok: false, text: "That file isn't a valid CodeDrill progress export." });
    } finally {
      if (fileRef.current) fileRef.current.value = "";
    }
  };

  return (
    <section aria-labelledby="backup-h" className="space-y-3 rounded-xl border border-zinc-200 p-5 dark:border-zinc-800">
      <h2 id="backup-h" className="text-sm font-semibold uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
        Backup
      </h2>
      <p className="text-sm text-zinc-600 dark:text-zinc-400">
        Progress is stored in this browser only. Export it to move to another device or browser, then import it there.
      </p>
      <div className="flex flex-wrap gap-2">
        <Button variant="primary" onClick={doExport}>
          Export progress
        </Button>
        <Button onClick={() => fileRef.current?.click()}>Import progress…</Button>
        <input
          ref={fileRef}
          type="file"
          accept="application/json,.json"
          className="sr-only"
          aria-label="Import progress file"
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) void doImport(f);
          }}
        />
      </div>
      {message && (
        <p role="status" className={`text-sm ${message.ok ? "text-emerald-600 dark:text-emerald-400" : "text-rose-600"}`}>
          {message.text}
        </p>
      )}
    </section>
  );
}
