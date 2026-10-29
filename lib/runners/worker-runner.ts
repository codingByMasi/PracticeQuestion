import type { Runner, RunInput, RunResult, RunnerStatus } from "./types";
import type { WorkerRequest, WorkerResponse } from "./worker-protocol";

export const DEFAULT_TIMEOUT_MS = 10_000;

type Options = {
  /** Max execution time per run. The worker is terminated and recreated on timeout. */
  timeoutMs?: number;
  /** Max time to load the runtime (downloads can be large on first visit). */
  initTimeoutMs?: number;
  loadingMessage?: string;
};

type Pending = { resolve: (r: WorkerResponse & { type: "done" }) => void };

/** Generic Runner backed by a Web Worker speaking the worker-protocol. */
export class WorkerRunner implements Runner {
  private worker: Worker | null = null;
  private initPromise: Promise<void> | null = null;
  private pending = new Map<number, Pending>();
  private nextId = 1;
  private queue: Promise<unknown> = Promise.resolve();
  private status: RunnerStatus = { state: "idle" };
  private listeners = new Set<(s: RunnerStatus) => void>();
  private readonly timeoutMs: number;
  private readonly initTimeoutMs: number;

  constructor(
    public readonly id: string,
    private readonly createWorker: () => Worker,
    private readonly options: Options = {},
  ) {
    this.timeoutMs = options.timeoutMs ?? DEFAULT_TIMEOUT_MS;
    this.initTimeoutMs = options.initTimeoutMs ?? 120_000;
  }

  getStatus(): RunnerStatus {
    return this.status;
  }

  onStatus(listener: (status: RunnerStatus) => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  private setStatus(status: RunnerStatus): void {
    this.status = status;
    for (const l of this.listeners) l(status);
  }

  private getWorker(): Worker {
    if (this.worker) return this.worker;
    const worker = this.createWorker();
    worker.onmessage = (event: MessageEvent<WorkerResponse>) => {
      const msg = event.data;
      if (msg.type === "status") {
        if (this.status.state === "loading" || this.status.state === "running")
          this.setStatus({ state: this.status.state, message: msg.message });
        return;
      }
      const p = this.pending.get(msg.id);
      if (p) {
        this.pending.delete(msg.id);
        p.resolve(msg);
      }
    };
    worker.onerror = (event) => {
      event.preventDefault();
      this.failAll(event.message || "The runner crashed.");
    };
    this.worker = worker;
    return worker;
  }

  private failAll(error: string): void {
    for (const [id, p] of this.pending) p.resolve({ id, type: "done", error });
    this.pending.clear();
    this.reset();
  }

  private request(req: { type: "init" } | { type: "run"; input: RunInput }, timeoutMs: number) {
    const id = this.nextId++;
    const worker = this.getWorker();
    return new Promise<(WorkerResponse & { type: "done" }) | "timeout">((resolve) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        resolve("timeout");
      }, timeoutMs);
      this.pending.set(id, {
        resolve: (r) => {
          clearTimeout(timer);
          resolve(r);
        },
      });
      worker.postMessage({ ...req, id } as WorkerRequest);
    });
  }

  /** Terminates the worker; the next call starts a fresh one. */
  private reset(): void {
    this.worker?.terminate();
    this.worker = null;
    this.initPromise = null;
  }

  init(): Promise<void> {
    this.initPromise ??= (async () => {
      this.setStatus({ state: "loading", message: this.options.loadingMessage });
      const res = await this.request({ type: "init" }, this.initTimeoutMs);
      if (res === "timeout" || res.error) {
        const message = res === "timeout" ? "Timed out loading the runtime." : res.error;
        this.reset();
        this.setStatus({ state: "error", message });
        throw new Error(message);
      }
      this.setStatus({ state: "ready" });
    })();
    return this.initPromise;
  }

  run(input: RunInput): Promise<RunResult> {
    const job = this.queue.then(() => this.runNow(input));
    this.queue = job.catch(() => undefined);
    return job;
  }

  private async runNow(input: RunInput): Promise<RunResult> {
    try {
      await this.init();
    } catch (e) {
      return { ok: false, error: `Could not start the ${this.id} runner: ${(e as Error).message}`, durationMs: 0 };
    }
    this.setStatus({ state: "running" });
    const start = performance.now();
    const res = await this.request({ type: "run", input }, this.timeoutMs);
    const durationMs = Math.round(performance.now() - start);
    if (res === "timeout") {
      this.reset();
      this.setStatus({ state: "idle" });
      return { ok: false, error: `Time limit exceeded (${this.timeoutMs / 1000}s). Check for infinite loops.`, durationMs };
    }
    this.setStatus({ state: "ready" });
    if (res.error || !res.result) return { ok: false, error: res.error ?? "No result", durationMs };
    return res.result;
  }

  dispose(): void {
    this.failAll("Runner disposed.");
    this.setStatus({ state: "idle" });
  }
}
