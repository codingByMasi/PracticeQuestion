import { formatValue } from "@/lib/judge/values";
import type { SqlDiff } from "@/lib/judge/sql-compare";

export function SqlDiffView({ diff }: { diff: SqlDiff }) {
  switch (diff.kind) {
    case "columns":
      return (
        <p>
          Column mismatch. Expected <code>{diff.expected.join(", ")}</code> but got <code>{diff.actual.join(", ") || "(none)"}</code>.
        </p>
      );
    case "rowCount":
      return (
        <p>
          Row count mismatch: expected {diff.expected} row{diff.expected === 1 ? "" : "s"}, got {diff.actual}.
        </p>
      );
    case "row":
      return (
        <div className="space-y-1">
          <p>
            First mismatch at row {diff.index + 1}
            {diff.orderMatters ? "" : " (after sorting both results, since order doesn't matter)"}:
          </p>
          <p className="font-mono text-xs">
            expected: {diff.expected.map(formatValue).join(" | ")}
            <br />
            yours:&nbsp;&nbsp;&nbsp; {diff.actual.map(formatValue).join(" | ")}
          </p>
        </div>
      );
  }
}
