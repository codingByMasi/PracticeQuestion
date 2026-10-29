import { loadPyodide, type PyodideAPI } from "pyodide";
import { beforeAll, describe, expect, it } from "vitest";
import type { PythonProblem } from "@/lib/content/schema";
import { judgePython } from "@/lib/judge/python";
import { executePython, installHarness } from "@/lib/runners/python/engine";

let py: PyodideAPI;
beforeAll(async () => {
  py = await loadPyodide();
  installHarness(py);
}, 60_000);

const run = (code: string, extra = {}) => executePython(py, { code, ...extra });

const problem: PythonProblem = {
  slug: "add",
  track: "python",
  title: "Add",
  difficulty: "Easy",
  tags: ["basics"],
  statementMd: "x",
  hints: [],
  solutionMd: "x",
  starterCode: "def add(a, b):\n    pass\n",
  functionName: "add",
  referenceSolution: "def add(a, b):\n    return a + b\n",
  tests: [
    { args: [1, 2], expected: 3, hidden: false },
    { args: [5, 5], expected: 10, hidden: true },
  ],
};

describe("python harness", () => {
  it("captures stdout and echoes the last expression in playground mode", () => {
    const r = run("print('hi')\n1 + 1", { echoLastExpression: true });
    expect(r).toMatchObject({ ok: true, stdout: "hi\n2\n" });
  });

  it("reports syntax and runtime errors with line numbers", () => {
    expect(run("def f(:\n  pass").error).toMatch(/SyntaxError/);
    const r = run("x = 1\ny = x / 0");
    expect(r.ok).toBe(false);
    expect(r.error).toMatch(/line 2/);
    expect(r.error).toMatch(/ZeroDivisionError/);
  });

  it("blocks js/pyodide imports and file writes", () => {
    expect(run("import js").error).toMatch(/not available/);
    expect(run("from pyodide import ffi").error).toMatch(/not available/);
    expect(run("open('/tmp/x', 'w')").error).toMatch(/PermissionError/);
  });

  it("isolates runs from each other", () => {
    run("leak = 42");
    expect(run("print(leak)").error).toMatch(/NameError/);
  });

  it("converts return values to JSON (tuples, sets, dict keys)", () => {
    const r = run("def f():\n    return (1, 2), {3, 1}, {1: 'a'}", { harness: { functionName: "f", cases: [{ args: [] }] } });
    expect(r.cases?.[0]).toMatchObject({ ok: true, value: [[1, 2], [1, 3], { "1": "a" }] });
  });

  it("does not let a function mutate shared test args", () => {
    const code = "def f(xs):\n    xs.append(1)\n    return len(xs)";
    const r = run(code, { harness: { functionName: "f", cases: [{ args: [[]] }, { args: [[]] }] } });
    expect(r.cases?.map((c) => c.value)).toEqual([1, 1]);
  });
});

describe("judgePython", () => {
  const exec = async (input: Parameters<typeof executePython>[1]) => executePython(py, input);

  it("runs only visible tests on run, all on submit", async () => {
    const runReport = await judgePython(problem, problem.referenceSolution, "run", exec);
    expect(runReport.cases).toHaveLength(1);
    const submit = await judgePython(problem, problem.referenceSolution, "submit", exec);
    expect(submit.passed).toBe(true);
    expect(submit.cases).toHaveLength(2);
  });

  it("hides inputs of hidden tests", async () => {
    const r = await judgePython(problem, "def add(a, b):\n    return a * b", "submit", exec);
    expect(r.passed).toBe(false);
    const hidden = r.cases?.find((c) => c.hidden);
    expect(hidden).toEqual({ label: "Hidden test 1", hidden: true, passed: false, error: undefined });
    expect(r.cases?.[0]).toMatchObject({ input: "add(1, 2)", expected: "3", actual: "2" });
  });

  it("reports a missing function", async () => {
    const r = await judgePython(problem, "def plus(a, b):\n    return a + b", "submit", exec);
    expect(r.error).toMatch(/'add' is not defined/);
  });
});
