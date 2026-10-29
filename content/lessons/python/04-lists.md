---
id: lists
title: Lists
order: 4
exerciseSlugs: [find-max, remove-duplicates, second-largest]
---

Lists are ordered, mutable collections.

## Creating and modifying

```python-run
nums = [3, 1, 4]
nums.append(1)
nums.extend([5, 9])
nums.insert(0, 2)
print(nums, len(nums))
nums.pop()
nums
```

## Indexing and slicing

Just like strings:

```python-run
nums = [10, 20, 30, 40, 50]
print(nums[0], nums[-1], nums[1:3], nums[::2])
```

## Sorting

`sorted()` returns a new list; `.sort()` sorts in place:

```python-run
words = ["pear", "Apple", "fig"]
print(sorted(words))
print(sorted(words, key=str.lower))
print(sorted(words, key=len, reverse=True))
```

## Built-ins

```python-run
nums = [4, 8, 15, 16, 23, 42]
print(sum(nums), min(nums), max(nums), 15 in nums)
```

## Looping with indexes

`enumerate` gives you index and value together:

```python-run
for i, word in enumerate(["zero", "one", "two"]):
    print(i, word)
```

## Sets for uniqueness

A `set` stores unique items and checks membership quickly:

```python-run
seen = set()
for x in [1, 2, 1, 3, 2]:
    seen.add(x)
seen, 2 in seen
```

## Copying

Assignment doesn't copy; both names point at the same list:

```python-run
a = [1, 2]
b = a
b.append(3)
c = list(a)   # a real copy
c.append(4)
print(a, b, c)
```

## Key points

- Lists are mutable; strings and tuples are not.
- `sorted(..., key=...)` sorts by any computed value.
- Use sets for "have I seen this?" checks.
