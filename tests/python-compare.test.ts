import { describe, expect, it } from "vitest";
import { formatPython, jsonEqual } from "@/lib/judge/python-compare";

describe("jsonEqual", () => {
  it("compares primitives strictly", () => {
    expect(jsonEqual("a", "a")).toBe(true);
    expect(jsonEqual("1", 1)).toBe(false);
    expect(jsonEqual(true, 1)).toBe(false);
    expect(jsonEqual(null, null)).toBe(true);
  });
  it("uses float tolerance", () => {
    expect(jsonEqual(0.1 + 0.2, 0.3)).toBe(true);
    expect(jsonEqual(2, 2.0)).toBe(true);
    expect(jsonEqual(2.01, 2)).toBe(false);
  });
  it("compares nested structures", () => {
    expect(jsonEqual({ a: [1, { b: 2 }] }, { a: [1, { b: 2 }] })).toBe(true);
    expect(jsonEqual({ a: 1, b: 2 }, { a: 1 })).toBe(false);
    expect(jsonEqual([1, 2], [2, 1])).toBe(false);
    expect(jsonEqual([1, 2], { 0: 1, 1: 2 })).toBe(false);
  });
});

describe("formatPython", () => {
  it("renders Python literals", () => {
    expect(formatPython([true, null, "x", { k: 1.5 }])).toBe("[True, None, 'x', {'k': 1.5}]");
    expect(formatPython("it's")).toBe(`"it's"`);
  });
});
