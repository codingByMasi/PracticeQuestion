"use client";

import { useEffect, useState } from "react";
import { getRunner } from "@/lib/runners/registry";
import type { Runner, RunnerStatus } from "@/lib/runners/types";

/** Returns the runner for `runnerId` and its live status. Starts loading on mount. */
export function useRunner(runnerId: string, { eager = true } = {}): { runner: Runner; status: RunnerStatus } {
  const [runner] = useState(() => getRunner(runnerId));
  const [status, setStatus] = useState<RunnerStatus>(() => runner.getStatus());
  useEffect(() => {
    const off = runner.onStatus(setStatus);
    if (eager) runner.init().catch(() => undefined);
    return off;
  }, [runner, eager]);
  return { runner, status };
}
