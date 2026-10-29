import type { Runner } from "../types";
import { WorkerRunner } from "../worker-runner";

/** The worker is prebuilt to public/workers by scripts/build-workers.mjs. */
export function createPythonRunner(): Runner {
  return new WorkerRunner("python", () => new Worker("/workers/python.worker.js", { type: "module", name: "codedrill-python" }), {
    loadingMessage: "Loading Python…",
  });
}
