---
id: dictionaries
title: Dictionaries
order: 5
exerciseSlugs: [word-frequency, merge-counts, two-sum]
---

A dictionary maps **keys** to **values** with fast lookup.

## Basics

```python-run
ages = {"ada": 36, "alan": 41}
ages["grace"] = 85
print(ages["ada"], len(ages), "alan" in ages)
ages
```

Looking up a missing key raises `KeyError`. `.get` returns a default instead:

```python-run
ages = {"ada": 36}
print(ages.get("bob"), ages.get("bob", 0))
```

## Iterating

```python-run
prices = {"apple": 1.2, "pear": 0.8, "fig": 2.5}
for fruit, price in prices.items():
    print(fruit, price)
print(list(prices.keys()), list(prices.values()))
```

## Counting

A classic pattern: count occurrences with `.get(key, 0) + 1`:

```python-run
counts = {}
for word in "the cat and the hat".split():
    counts[word] = counts.get(word, 0) + 1
counts
```

The standard library has a helper for exactly this:

```python-run
from collections import Counter
Counter("mississippi").most_common(2)
```

## Grouping

`setdefault` creates a missing entry and returns it:

```python-run
groups = {}
for word in ["apple", "avocado", "banana", "blueberry", "cherry"]:
    groups.setdefault(word[0], []).append(word)
groups
```

## Lookups to avoid nested loops

Remembering what you've seen in a dict often turns an O(n²) search into O(n):

```python-run
def has_pair_with_sum(nums, target):
    seen = set()
    for x in nums:
        if target - x in seen:
            return True
        seen.add(x)
    return False

has_pair_with_sum([2, 7, 11, 15], 9)
```

## Key points

- Keys must be immutable (strings, numbers, tuples).
- `.get`, `.items()` and `setdefault` cover most everyday needs.
