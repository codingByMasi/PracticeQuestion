import type { RunInput, RunResult } from "./types";

export type WorkerRequest =
  | { id: number; type: "init" }
  | { id: number; type: "prepare"; input: RunInput }
  | { id: number; type: "run"; input: RunInput };

export type WorkerResponse =
  | { id: number; type: "done"; result?: RunResult; error?: string }
  | { type: "status"; message: string };
