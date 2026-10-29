---
id: functions-recursion
title: Functions and recursion
order: 6
exerciseSlugs: [factorial, fibonacci, flatten-list]
---

## Recursion

A recursive function calls itself on a smaller version of the problem. It needs a **base case** that stops the recursion:

```python-run
def countdown(n):
    if n == 0:          # base case
        return ["liftoff"]
    return [n] + countdown(n - 1)

countdown(3)
```

## Thinking recursively

Sum of a list = first element + sum of the rest:

```python-run
def total(nums):
    if not nums:
        return 0
    return nums[0] + total(nums[1:])

total([1, 2, 3, 4])
```

## Recursion on nested data

Recursion shines when the data itself is recursive, like nested lists:

```python-run
def depth(item):
    if not isinstance(item, list):
        return 0
    return 1 + max((depth(x) for x in item), default=0)

depth([1, [2, [3, [4]]]])
```

## The cost of repeated work

Naive recursive Fibonacci recomputes the same values many times. Memoization caches results:

```python-run
from functools import lru_cache

calls = 0

@lru_cache(maxsize=None)
def fib(n):
    global calls
    calls += 1
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(60), "computed with", calls, "calls")
```

## Functions are values

Functions can be passed around like any other value:

```python-run
def apply_twice(f, x):
    return f(f(x))

print(apply_twice(lambda v: v * 3, 2))
print(sorted(["bb", "a", "ccc"], key=len))
```

## Key points

- Every recursive function needs a base case.
- Python's default recursion limit is around 1000 calls deep.
- Cache results (`lru_cache`) or iterate when subproblems repeat.
