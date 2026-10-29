"""Builds content/problems/python/*.json from tools/content-gen/py/*.py, executing every reference in CPython.
Usage: python3 tools/content-gen/build_py.py"""
import copy, glob, importlib.util, json, os, random, sys, textwrap, zlib
from collections import Counter
from common import slugify, DIFF_RANK

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
OUT = os.path.join(ROOT, "content", "problems", "python")
SQL_DIR = os.path.join(ROOT, "content", "problems", "sql")
originals = set(open(os.path.join(HERE, "original_python.txt")).read().split())

PY_CONCEPTS = ["basics", "functions", "conditionals", "numbers", "math", "loops", "strings", "lists", "tuples", "sets", "dicts", "counting",
               "sorting", "comprehensions", "searching", "recursion", "two-pointers", "sliding-window", "stacks", "queues", "intervals",
               "matrix", "bit-manipulation", "number-theory", "parsing", "simulation", "greedy", "dynamic-programming", "backtracking",
               "combinatorics", "graphs", "trees", "heaps", "design", "regex"]
RANK = {c: i for i, c in enumerate(PY_CONCEPTS)}


def strict_json(v, path="value"):
    """Reject anything that would not survive the JSON round trip unchanged (tuples, sets, non-str keys, NaN)."""
    if v is None or isinstance(v, (bool, str)): return
    if isinstance(v, int): return
    if isinstance(v, float):
        if v != v or v in (float("inf"), float("-inf")): raise ValueError(f"{path}: non-finite float")
        return
    if isinstance(v, list):
        for i, x in enumerate(v): strict_json(x, f"{path}[{i}]")
        return
    if isinstance(v, dict):
        for k, x in v.items():
            if not isinstance(k, str): raise ValueError(f"{path}: non-string dict key {k!r}")
            strict_json(x, f"{path}.{k}")
        return
    raise ValueError(f"{path}: unsupported type {type(v).__name__}")


def load_modules():
    mods = []
    for f in sorted(glob.glob(os.path.join(HERE, "py", "*.py"))):
        spec = importlib.util.spec_from_file_location("py_" + os.path.basename(f)[:-3], f)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); mods.append(m)
    return mods


def short(v, n=90):
    s = json.dumps(v, ensure_ascii=False)
    return s if len(s) <= n else s[: n - 1] + "…"


def main():
    taken = set(originals)
    for f in glob.glob(os.path.join(SQL_DIR, "*.json")): taken.add(os.path.basename(f)[:-5])
    taken_titles = set()
    problems, errors = [], []
    seq = 0
    for m in load_modules():
        for it in m.P.items:
            seq += 1
            slug = slugify(it["title"])
            if slug in taken or it["title"].lower() in taken_titles:
                errors.append(f"duplicate slug/title: {it['title']}"); continue
            taken.add(slug); taken_titles.add(it["title"].lower())
            ref = textwrap.dedent(it["ref"]).strip() + "\n"
            ns = {}
            try:
                exec(compile(ref, slug, "exec"), ns)
                f = ns[it["fn"]]
            except Exception as e:
                errors.append(f"{slug}: reference does not compile: {e!r}"); continue
            rng = random.Random(zlib.crc32(slug.encode()))
            vis = [tuple(a) for a in it["vis"]]
            hid = [tuple(a) for a in it["hid"]]
            if it["rand"]:
                for _ in range(it["extra"]): hid.append(tuple(it["rand"](rng)))
            if len(vis) < 2 or len(hid) < 3: errors.append(f"{slug}: needs >=2 visible and >=3 hidden tests (has {len(vis)}/{len(hid)})"); continue
            tests, seen, ok = [], set(), True
            for args, hidden in [(a, False) for a in vis] + [(a, True) for a in hid]:
                try:
                    strict_json(list(args), "args")
                    snapshot = copy.deepcopy(list(args))
                    val = f(*copy.deepcopy(list(args)))
                    strict_json(val, "result")
                    if json.loads(json.dumps(val)) != val: raise ValueError("result changes in JSON round trip")
                    val2 = f(*copy.deepcopy(snapshot))
                    if val2 != val: raise ValueError("non-deterministic")
                except Exception as e:
                    errors.append(f"{slug}: test {short(args)} failed: {e!r}"); ok = False; break
                k = json.dumps(list(args), sort_keys=True)
                if k in seen: errors.append(f"{slug}: duplicate test input {short(args)}"); ok = False; break
                seen.add(k)
                tests.append({"args": list(args), "expected": val, "hidden": hidden})
            if not ok: continue
            if len({json.dumps(t["expected"], sort_keys=True) for t in tests}) < 2:
                errors.append(f"{slug}: all tests have the same expected value (trivially hard-codable)"); continue
            first = tests[0]
            call = f"{it['fn']}({', '.join(short(a, 60) for a in first['args'])})"
            statement = f"{textwrap.dedent(it['statement']).strip()}\n\n**Example:** `{call}` returns `{short(first['expected'], 80)}`."
            problem = {
                "slug": slug, "track": "python", "title": it["title"], "difficulty": it["diff"], "tags": it["tags"],
                "statementMd": statement, "hints": it["hints"],
                "solutionMd": f"```python\n{ref}```\n\n{it['why']}",
                "starterCode": f"def {it['fn']}({it['sig']}):\n    # Write your code here\n    pass\n",
                "functionName": it["fn"], "referenceSolution": ref, "tests": tests,
                "_k": (DIFF_RANK[it["diff"]], RANK.get(it["tags"][0], 99), seq),
            }
            if not it["hints"]: errors.append(f"{slug}: needs at least one hint")
            problems.append(problem)
    if errors:
        print("\n".join(errors)); print(f"\n{len(errors)} problems with errors"); sys.exit(1)
    for f in glob.glob(os.path.join(OUT, "*.json")):
        if os.path.basename(f)[:-5] not in originals: os.remove(f)
    allp = problems[:]
    for slug in originals:
        d = json.load(open(os.path.join(OUT, slug + ".json")))
        d["_k"] = (DIFF_RANK[d["difficulty"]], RANK.get(d["tags"][0], 99), 0)
        allp.append(d)
    allp.sort(key=lambda d: d["_k"])
    for i, d in enumerate(allp, 1):
        d.pop("_k"); d["order"] = i
        with open(os.path.join(OUT, d["slug"] + ".json"), "w") as fh:
            json.dump(d, fh, indent=2, ensure_ascii=False); fh.write("\n")
    print(len(allp), "python problems", dict(Counter(d["difficulty"] for d in allp)))
    print("tags:", dict(Counter(d["tags"][0] for d in allp)))


if __name__ == "__main__":
    main()
