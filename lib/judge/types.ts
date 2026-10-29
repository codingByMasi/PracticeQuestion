import type { Table } from "../runners/types";
import type { SqlDiff } from "./sql-compare";

export type JudgeMode = "run" | "submit";

export type CaseReport = {
  label: string;
  hidden: boolean;
  passed: boolean;
  /** Omitted for hidden tests. */
  input?: string;
  expected?: string;
  actual?: string;
  stdout?: string;
  error?: string;
};

export type JudgeReport = {
  mode: JudgeMode;
  passed: boolean;
  durationMs: number;
  /** Compile/runtime error that stopped judging. */
  error?: string;
  stdout?: string;
  cases?: CaseReport[];
  /** SQL: the user's result and the expected result. */
  table?: Table;
  expectedTable?: Table;
  diff?: SqlDiff;
};
