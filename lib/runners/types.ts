export type Table = { columns: string[]; rows: unknown[][] };

/** Output of one function call when a harness is used (Python-style judging). */
export type CaseOutcome = {
  ok: boolean;
  /** JSON-compatible return value. */
  value?: unknown;
  stdout: string;
  error?: string;
};

export type RunInput = {
  code: string;
  /** Runs before `code` in the same fresh environment (e.g. dataset SQL). */
  setup?: string;
  /** Call `functionName` once per case after running `code`. */
  harness?: { functionName: string; cases: { args: unknown[] }[] };
  /** Playground mode: echo the value of a trailing expression, REPL style. */
  echoLastExpression?: boolean;
};

export type RunResult = {
  ok: boolean;
  stdout?: string;
  stderr?: string;
  table?: { columns: string[]; rows: unknown[][] };
  error?: string;
  durationMs: number;
  cases?: CaseOutcome[];
};

export type RunnerStatus = {
  state: "idle" | "loading" | "ready" | "running" | "error";
  message?: string;
};

export interface Runner {
  id: "sql" | "python" | string;
  init(): Promise<void>;
  /** Executes in a worker. Never throws: failures come back as `ok: false`. */
  run(input: RunInput): Promise<RunResult>;
  dispose(): void;
  getStatus(): RunnerStatus;
  onStatus(listener: (status: RunnerStatus) => void): () => void;
}

export type Execute = (input: RunInput) => Promise<RunResult>;
