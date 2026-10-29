/// <reference lib="webworker" />
import initSqlJs, { type SqlJsStatic } from "sql.js";
import { serveRunner } from "../worker-host";
import { executeSql } from "./engine";

let SQL: SqlJsStatic | undefined;

serveRunner({
  async init(report) {
    report("Loading SQLite…");
    SQL = await initSqlJs({ locateFile: () => "/vendor/sql-wasm.wasm" });
  },
  async run(input) {
    if (!SQL) throw new Error("SQLite is not loaded");
    return executeSql(SQL, input);
  },
});
