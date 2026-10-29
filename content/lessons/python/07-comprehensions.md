---
id: comprehensions
title: Comprehensions
order: 7
exerciseSlugs: [even-squares, transpose-matrix]
---

Comprehensions build lists, sets and dicts in a single readable expression.

## List comprehensions

`[expression for item in iterable]`:

```python-run
[x * x for x in range(6)]
```

Add a filter with `if`:

```python-run
[x for x in range(20) if x % 3 == 0]
```

It's equivalent to this loop:

```python-run
result = []
for x in range(20):
    if x % 3 == 0:
        result.append(x)
result
```

## Conditional expressions

`a if condition else b` chooses a value; it goes **before** the `for`:

```python-run
["even" if x % 2 == 0 else "odd" for x in range(5)]
```

## Nested comprehensions

Loops read left to right, like nested `for` statements:

```python-run
pairs = [(r, c) for r in range(2) for c in range(3)]
grid = [[r * 3 + c for c in range(3)] for r in range(3)]
print(pairs)
grid
```

## Dict and set comprehensions

```python-run
words = ["sql", "python", "pandas", "sql"]
lengths = {w: len(w) for w in words}
unique_first_letters = {w[0] for w in words}
print(lengths)
unique_first_letters
```

## zip

`zip` walks several iterables in parallel, which pairs nicely with comprehensions:

```python-run
names = ["ada", "alan"]
years = [1815, 1912]
{name: year for name, year in zip(names, years)}
```

## Key points

- Prefer comprehensions for simple transform-and-filter steps.
- If it gets hard to read, a plain loop is fine.
