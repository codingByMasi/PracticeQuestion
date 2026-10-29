/// <reference lib="webworker" />
import type { PyodideAPI } from "pyodide";
import { serveRunner } from "../worker-host";
import { PYODIDE_BASE_URL } from "./config";
import { executePython, installHarness } from "./engine";

let pyodide: PyodideAPI | undefined;

type LoadPyodide = (options: { indexURL: string }) => Promise<PyodideAPI>;

/** Loads Pyodide from the CDN (this file is bundled as a module worker by scripts/build-workers.mjs). */
async function importPyodide(): Promise<LoadPyodide> {
  const mod = (await import(/* webpackIgnore: true */ `${PYODIDE_BASE_URL}pyodide.mjs`)) as {
    loadPyodide: LoadPyodide;
  };
  return mod.loadPyodide;
}

serveRunner({
  async init(report) {
    report("Downloading Python runtime (~10 MB, cached after the first visit)…");
    const loadPyodide = await importPyodide();
    report("Starting Python…");
    pyodide = await loadPyodide({ indexURL: PYODIDE_BASE_URL });
    installHarness(pyodide);
  },
  async prepare(input, report) {
    if (!pyodide) throw new Error("Python is not loaded");
    // Load numpy, pandas, etc. on demand from the Pyodide distribution.
    await pyodide.loadPackagesFromImports(input.code, {
      messageCallback: (msg: string) => report(msg),
      errorCallback: (msg: string) => report(msg),
    });
  },
  async run(input) {
    if (!pyodide) throw new Error("Python is not loaded");
    return executePython(pyodide, input);
  },
});
