---
id: algorithms
title: Simple algorithms
order: 8
exerciseSlugs: [binary-search, balanced-brackets, run-length-encoding]
---

A few patterns solve a surprising number of problems.

## Big-O in one minute

Big-O describes how work grows with input size `n`. A single loop is O(n); a loop inside a loop is O(n²); halving the problem each step is O(log n).

```python-run
import time

def time_it(f, *args):
    start = time.perf_counter()
    f(*args)
    return round((time.perf_counter() - start) * 1000, 2)

nums = list(range(200_000))
print("linear search ms:", time_it(lambda: 199_999 in nums))
print("set lookup ms:   ", time_it(lambda s: 199_999 in s, set(nums)))
```

## Binary search

On **sorted** data, compare with the middle element and discard half:

```python-run
def contains(sorted_nums, target):
    lo, hi = 0, len(sorted_nums) - 1
    steps = 0
    while lo <= hi:
        steps += 1
        mid = (lo + hi) // 2
        if sorted_nums[mid] == target:
            return True, steps
        if sorted_nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False, steps

contains(list(range(1_000_000)), 765_432)
```

## Stacks

A list used with `append` and `pop` is a stack: last in, first out. Stacks are perfect for matching things like brackets or undo history:

```python-run
stack = []
for token in ["open A", "open B", "close", "open C", "close", "close"]:
    if token.startswith("open"):
        stack.append(token.split()[1])
    else:
        print("closing", stack.pop())
stack
```

## Two pointers

Walk a sequence from both ends (or with two cursors) to avoid nested loops:

```python-run
def is_sorted_palindrome(seq):
    i, j = 0, len(seq) - 1
    while i < j:
        if seq[i] != seq[j]:
            return False
        i += 1
        j -= 1
    return True

is_sorted_palindrome([1, 2, 3, 2, 1])
```

## Scanning runs

Track the "current" item and a count while you scan once:

```python-run
from itertools import groupby
[(ch, len(list(group))) for ch, group in groupby("aaabccdddd")]
```

## Key points

- Choose the right data structure first: sets and dicts make lookups O(1).
- Binary search needs sorted input and runs in O(log n).
- Stacks match nested structure.
