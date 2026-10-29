import { describe, expect, it } from "vitest";
import { compareResultSets } from "@/lib/judge/sql-compare";

const t = (columns: string[], rows: unknown[][]) => ({ columns, rows });

describe("compareResultSets", () => {
  const expected = t(["name", "total"], [
    ["Ann", 10],
    ["Bob", 5.5],
  ]);

  it("passes identical results", () => {
    expect(compareResultSets(expected, expected, { orderMatters: true }).pass).toBe(true);
  });

  it("normalizes column names case-insensitively", () => {
    const actual = t(["NAME", "Total"], expected.rows);
    expect(compareResultSets(actual, expected, { orderMatters: true }).pass).toBe(true);
  });

  it("accepts the same columns in a different order", () => {
    const actual = t(["total", "name"], [
      [10, "Ann"],
      [5.5, "Bob"],
    ]);
    expect(compareResultSets(actual, expected, { orderMatters: true }).pass).toBe(true);
  });

  it("reports column mismatches", () => {
    const r = compareResultSets(t(["name"], [["Ann"], ["Bob"]]), expected, { orderMatters: false });
    expect(r).toEqual({ pass: false, diff: { kind: "columns", expected: ["name", "total"], actual: ["name"] } });
    expect(compareResultSets(t(["name", "sum"], expected.rows), expected, { orderMatters: false }).pass).toBe(false);
  });

  it("reports row count mismatches", () => {
    const r = compareResultSets(t(["name", "total"], [["Ann", 10]]), expected, { orderMatters: false });
    expect(r).toEqual({ pass: false, diff: { kind: "rowCount", expected: 2, actual: 1 } });
  });

  it("ignores row order unless orderMatters", () => {
    const reversed = t(["name", "total"], [...expected.rows].reverse());
    expect(compareResultSets(reversed, expected, { orderMatters: false }).pass).toBe(true);
    const r = compareResultSets(reversed, expected, { orderMatters: true });
    expect(r.pass).toBe(false);
    if (!r.pass) expect(r.diff).toMatchObject({ kind: "row", index: 0, expected: ["Ann", 10], actual: ["Bob", 5.5] });
  });

  it("compares numbers with tolerance", () => {
    const actual = t(["name", "total"], [
      ["Ann", 10.0000000001],
      ["Bob", 5.5],
    ]);
    expect(compareResultSets(actual, expected, { orderMatters: true }).pass).toBe(true);
    const off = t(["name", "total"], [
      ["Ann", 10.01],
      ["Bob", 5.5],
    ]);
    expect(compareResultSets(off, expected, { orderMatters: true }).pass).toBe(false);
  });

  it("treats integers and equal floats as equal", () => {
    expect(compareResultSets(t(["x"], [[3]]), t(["x"], [[3.0]]), { orderMatters: true }).pass).toBe(true);
  });

  it("does not equate numbers with numeric strings", () => {
    expect(compareResultSets(t(["x"], [["3"]]), t(["x"], [[3]]), { orderMatters: true }).pass).toBe(false);
  });

  it("handles NULLs, including when sorting", () => {
    const e = t(["x"], [[null], [1], ["a"]]);
    const a = t(["x"], [["a"], [null], [1]]);
    expect(compareResultSets(a, e, { orderMatters: false }).pass).toBe(true);
    expect(compareResultSets(t(["x"], [[0]]), t(["x"], [[null]]), { orderMatters: true }).pass).toBe(false);
  });

  it("handles duplicate rows as a multiset", () => {
    const e = t(["x"], [[1], [1], [2]]);
    expect(compareResultSets(t(["x"], [[1], [2], [2]]), e, { orderMatters: false }).pass).toBe(false);
    expect(compareResultSets(t(["x"], [[2], [1], [1]]), e, { orderMatters: false }).pass).toBe(true);
  });

  it("passes empty result sets with matching columns", () => {
    expect(compareResultSets(t(["x"], []), t(["X"], []), { orderMatters: false }).pass).toBe(true);
  });
});
