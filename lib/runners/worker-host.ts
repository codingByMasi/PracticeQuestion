/// <reference lib="webworker" />
import type { RunInput, RunResult } from "./types";
import type { WorkerRequest, WorkerResponse } from "./worker-protocol";

type Engine = {
  init(report: (message: string) => void): Promise<void>;
  /** Optional slow setup for a specific input (e.g. downloading packages). Not counted in the run timeout. */
  prepare?(input: RunInput, report: (message: string) => void): Promise<void>;
  run(input: RunInput, report: (message: string) => void): Promise<RunResult>;
};

/** Wires an execution engine to the worker message protocol. Call from a worker file. */
export function serveRunner(engine: Engine): void {
  const scope = self as unknown as DedicatedWorkerGlobalScope;
  const post = (msg: WorkerResponse) => scope.postMessage(msg);
  const report = (message: string) => post({ type: "status", message });
  let ready: Promise<void> | null = null;
  const ensureInit = () => {
    ready ??= engine.init(report).catch((e: unknown) => {
      ready = null;
      throw e;
    });
    return ready;
  };

  scope.onmessage = async (event: MessageEvent<WorkerRequest>) => {
    const req = event.data;
    try {
      await ensureInit();
      if (req.type === "init") post({ id: req.id, type: "done" });
      else if (req.type === "prepare") {
        await engine.prepare?.(req.input, report);
        post({ id: req.id, type: "done" });
      } else post({ id: req.id, type: "done", result: await engine.run(req.input, report) });
    } catch (e) {
      post({ id: req.id, type: "done", error: e instanceof Error ? e.message : String(e) });
    }
  };
}
