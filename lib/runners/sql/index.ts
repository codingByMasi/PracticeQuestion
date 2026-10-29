import type { Runner } from "../types";
import { WorkerRunner } from "../worker-runner";

export function createSqlRunner(): Runner {
  return new WorkerRunner("sql", () => new Worker(new URL("./sql.worker.ts", import.meta.url), { type: "module" }), {
    loadingMessage: "Loading SQLite…",
  });
}
