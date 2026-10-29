// Copies the sql.js WebAssembly binary into public/ so the SQL worker can load it
// from the same origin. Runs on postinstall.
import { copyFileSync, mkdirSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";

const require = createRequire(import.meta.url);
const src = require.resolve("sql.js/dist/sql-wasm-browser.wasm");
const destDir = path.resolve("public", "vendor");
mkdirSync(destDir, { recursive: true });
copyFileSync(src, path.join(destDir, "sql-wasm.wasm"));
console.log("copied sql-wasm.wasm to public/vendor");
