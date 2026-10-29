// Bundles the Python worker as a native ES module worker into public/workers/.
// Pyodide only runs in module workers, and Next's bundler emits classic workers,
// so this worker is built separately. Runs before `dev` and `build`.
import { build } from "esbuild";

await build({
  entryPoints: { "python.worker": "lib/runners/python/python.worker.ts" },
  outdir: "public/workers",
  bundle: true,
  format: "esm",
  platform: "browser",
  target: "es2022",
  minify: true,
  sourcemap: true,
  logLevel: "warning",
  define: {
    "process.env.NEXT_PUBLIC_PYODIDE_BASE_URL": JSON.stringify(process.env.NEXT_PUBLIC_PYODIDE_BASE_URL ?? null),
  },
});
console.log("built public/workers/python.worker.js");
