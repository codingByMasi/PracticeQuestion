/** Must match the `pyodide` devDependency (checked by validate:content). */
export const PYODIDE_VERSION = "314.0.7";

/** Override with NEXT_PUBLIC_PYODIDE_BASE_URL to self-host Pyodide. */
export const PYODIDE_BASE_URL =
  process.env.NEXT_PUBLIC_PYODIDE_BASE_URL || `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;
