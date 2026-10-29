import re

DIFF = {"E": "Easy", "M": "Medium", "H": "Hard"}
DIFF_RANK = {"Easy": 0, "Medium": 1, "Hard": 2}

# Teaching order of concepts, used to give problems a beginner -> advanced `order` within each difficulty.
CONCEPTS = [
    "basics", "select", "where", "null", "like", "order-by", "limit", "distinct", "case", "expressions",
    "math", "strings", "dates", "aggregate", "group-by", "having", "join", "left-join", "self-join", "multi-join",
    "subquery", "exists", "set-ops", "correlated-subquery", "cte", "window-functions", "ranking", "running-total",
    "pivot", "recursive", "gaps-islands", "dml", "optimization",
    # python
    "functions", "conditionals", "loops", "numbers", "lists", "tuples", "sets", "dicts", "sorting", "comprehensions",
    "recursion", "searching", "two-pointers", "sliding-window", "stacks", "queues", "matrix", "bit-manipulation",
    "dynamic-programming", "greedy", "backtracking", "graphs", "trees", "heaps", "intervals", "design", "classes",
    "generators", "iterators", "decorators", "regex", "parsing", "simulation", "number-theory", "combinatorics",
]
CONCEPT_RANK = {c: i for i, c in enumerate(CONCEPTS)}


def slugify(title):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s


class SqlSet:
    def __init__(self, dataset, tables):
        self.dataset, self.tables, self.items = dataset, tables, []

    def p(self, title, diff, tags, statement, hints, query, ordered=False, why="", setup=None, allow_empty=False):
        self.items.append(dict(title=title, diff=DIFF[diff], tags=tags if isinstance(tags, list) else tags.split(), statement=statement.strip(), hints=hints, query=query.strip(),
                               ordered=ordered, why=why.strip(), setup=setup, allow_empty=allow_empty, dataset=self.dataset, tables=self.tables))


class PySet:
    def __init__(self):
        self.items = []

    def p(self, title, diff, tags, fn, sig, statement, hints, ref, why, vis, hid, rand=None, extra=3):
        self.items.append(dict(title=title, diff=DIFF[diff], tags=tags if isinstance(tags, list) else tags.split(), fn=fn, sig=sig, statement=statement,
                               hints=hints, ref=ref, why=why.strip(), vis=vis, hid=hid, rand=rand, extra=extra))
