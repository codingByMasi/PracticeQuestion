---
id: strings
title: Working with strings
order: 2
exerciseSlugs: [reverse-string, count-vowels, title-case]
---

Strings are immutable sequences of characters.

## Indexing and slicing

Indexes start at 0; negative indexes count from the end. Slices are `s[start:stop:step]`, with `stop` excluded:

```python-run
s = "CodeDrill"
print(s[0], s[-1], s[0:4], s[4:], s[::-1])
```

## Useful methods

```python-run
s = "  Hello, World  "
print(s.strip())
print(s.lower(), s.upper())
print(s.strip().replace("World", "Python"))
print("a,b,c".split(","))
print("-".join(["x", "y", "z"]))
```

## Looping over characters

```python-run
vowels = 0
for ch in "programming":
    if ch in "aeiou":
        vowels += 1
vowels
```

## Checking characters

```python-run
for ch in "a1 B!":
    print(repr(ch), ch.isalpha(), ch.isdigit(), ch.isalnum(), ch.isupper())
```

## Building strings

Strings are immutable, so build lists of pieces and `join` them at the end:

```python-run
parts = []
for word in ["sql", "and", "python"]:
    parts.append(word.capitalize())
" ".join(parts)
```

## Key points

- `s[::-1]` reverses a string.
- `split` turns a string into a list; `join` does the opposite.
- `in` checks for a substring or character.
