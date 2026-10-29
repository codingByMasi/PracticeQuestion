"""Builds content/problems/sql/*.json from tools/content-gen/sql/*.py, running every reference in SQLite.
Usage: python3 tools/content-gen/build_sql.py"""
import glob, importlib.util, json, os, sqlite3, sys, textwrap
from common import slugify, DIFF_RANK, CONCEPT_RANK

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
OUT = os.path.join(ROOT, "content", "problems", "sql")
originals = set(open(os.path.join(os.path.dirname(__file__), "original_sql.txt")).read().split())
originals_py = set(open(os.path.join(os.path.dirname(__file__), "original_python.txt")).read().split())


def split_statements(sql):
    out, cur, q = [], [], None
    for ch in sql:
        if q:
            cur.append(ch)
            if ch == q: q = None
        elif ch in "'\"":
            q = ch; cur.append(ch)
        elif ch == ";":
            s = "".join(cur).strip()
            if s: out.append(s)
            cur = []
        else:
            cur.append(ch)
    s = "".join(cur).strip()
    if s: out.append(s)
    return out


def run(dataset_sql, setup, query, reverse=False):
    db = sqlite3.connect(":memory:")
    if reverse: db.execute("PRAGMA reverse_unordered_selects=ON")
    db.executescript(dataset_sql)
    if setup: db.executescript(setup)
    cols, rows = None, []
    for st in split_statements(query):
        cur = db.execute(st)
        if cur.description:
            cols, rows = [d[0] for d in cur.description], cur.fetchall()
    db.close()
    return cols, rows


def norm(rows):
    return [tuple(round(v, 6) if isinstance(v, float) else v for v in r) for r in rows]


def key(r):
    return [(0, "") if v is None else (1, v) if isinstance(v, (int, float)) else (2, v) for v in r]


def load_modules():
    mods = []
    for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "sql", "*.py"))):
        spec = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); mods.append(m)
    return mods


def main():
    datasets = {os.path.basename(f)[:-4]: open(f).read() for f in glob.glob(os.path.join(ROOT, "content", "datasets", "*.sql"))}
    taken = set(originals) | set(originals_py)
    problems, errors = [], []
    seq = 0
    for m in load_modules():
        for it in [i for st in [m.S] + list(getattr(m, "EXTRA", [])) for i in st.items]:
            seq += 1
            slug = slugify(it["title"])
            if slug in taken:
                errors.append(f"duplicate slug/title: {it['title']}"); continue
            taken.add(slug)
            ds = datasets[it["dataset"]]
            try:
                cols, rows = run(ds, it["setup"], it["query"])
                cols2, rows2 = run(ds, it["setup"], it["query"], reverse=True)
            except Exception as e:
                errors.append(f"{slug}: SQL error {e}"); continue
            if cols is None: errors.append(f"{slug}: query returns no result set"); continue
            if len({c.lower() for c in cols}) != len(cols): errors.append(f"{slug}: duplicate column names {cols}")
            if not rows and not it["allow_empty"]: errors.append(f"{slug}: empty result")
            if len(rows) > 120: errors.append(f"{slug}: {len(rows)} rows (too many to inspect, add LIMIT/filter)")
            a, b = norm(rows), norm(rows2)
            if it["ordered"]:
                if a != b: errors.append(f"{slug}: ORDER not deterministic (ties)")
            else:
                if sorted(a, key=key) != sorted(b, key=key): errors.append(f"{slug}: result set not deterministic (LIMIT ties?)")
            if it["ordered"] and len(rows) < 2: errors.append(f"{slug}: ordered but <2 rows")
            blurb = "Tables: " + ", ".join(f"`{t}`" for t in it["tables"]) + "."
            colline = "Expected columns: " + ", ".join(f"`{c}`" for c in cols) + "."
            order = "**Row order matters** for this problem." if it["ordered"] else "Row order does not matter."
            statement = f"{it['statement']}\n\n{colline}\n\n{blurb}\n\n{order}"
            if it["setup"]: statement = statement  # setup is applied silently to the dataset
            why = it["why"] or "Compare with your own query; the result sets must match."
            problem = {
                "slug": slug, "track": "sql", "title": it["title"], "difficulty": it["diff"], "tags": it["tags"],
                "statementMd": statement, "hints": it["hints"],
                "solutionMd": f"```sql\n{it['query']}\n```\n\n{why}",
                "starterCode": f"-- {blurb[:-1].replace('`', '')}\nSELECT\n",
                "datasetId": it["dataset"],
                "expected": {"query": it["query"], "orderMatters": it["ordered"]},
                "_seq": seq,
            }
            if it["setup"]: problem["setupSql"] = it["setup"].strip()
            problems.append(problem)
    if errors:
        print("\n".join(errors)); print(f"\n{len(errors)} problems with errors"); sys.exit(1)
    # clear previously generated files
    for f in glob.glob(os.path.join(OUT, "*.json")):
        if os.path.basename(f)[:-5] not in originals: os.remove(f)
    for p in problems:
        seq = p.pop("_seq")
        p["_k"] = (DIFF_RANK[p["difficulty"]], CONCEPT_RANK.get(p["tags"][0], 99), seq)
    # beginner -> advanced ordering over all sql problems (originals included)
    allp = problems[:]
    for slug in originals:
        d = json.load(open(os.path.join(OUT, slug + ".json")))
        d["_k"] = (DIFF_RANK[d["difficulty"]], CONCEPT_RANK.get(d["tags"][0], 99), 0)
        allp.append(d)
    allp.sort(key=lambda d: d["_k"])
    for i, d in enumerate(allp, 1):
        d.pop("_k"); d["order"] = i
        json.dump(d, open(os.path.join(OUT, d["slug"] + ".json"), "w"), indent=2, ensure_ascii=False); open(os.path.join(OUT, d["slug"] + ".json"), "a").write("\n")
    from collections import Counter
    print(len(allp), "sql problems", dict(Counter(d["difficulty"] for d in allp)))


if __name__ == "__main__":
    main()
