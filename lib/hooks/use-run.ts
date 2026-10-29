"use client";

import { useCallback, useState } from "react";
import type { RunInput, RunResult } from "@/lib/runners/types";
import { useRunner } from "./use-runner";

/** Run arbitrary code with a runner, tracking the latest result and busy state. */
export function useRun(runnerId: string, { eager = false } = {}) {
  const { runner, status } = useRunner(runnerId, { eager });
  const [result, setResult] = useState<RunResult | null>(null);
  const [busy, setBusy] = useState(false);
  const run = useCallback(
    async (input: RunInput) => {
      setBusy(true);
      try {
        setResult(await runner.run(input));
      } finally {
        setBusy(false);
      }
    },
    [runner],
  );
  return { run, result, busy, status };
}
