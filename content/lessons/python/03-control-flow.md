---
id: control-flow
title: Conditionals and loops
order: 3
exerciseSlugs: [fizzbuzz, sum-of-digits, valid-palindrome]
---

## if / elif / else

```python-run
def grade(score):
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    else:
        return "C"

[grade(s) for s in (95, 80, 60)]
```

Conditions are checked top to bottom; the first true branch wins.

## for loops and range

`range(stop)`, `range(start, stop)` and `range(start, stop, step)` produce numbers, with `stop` excluded:

```python-run
for i in range(1, 6):
    print(i, i * i)
```

## while loops

Repeat while a condition holds. Make sure it eventually becomes false: infinite loops hit the 10-second time limit.

```python-run
n = 1234
digits = []
while n > 0:
    digits.append(n % 10)
    n //= 10
digits
```

## break and continue

```python-run
for n in range(2, 20):
    if n % 2 == 0:
        continue      # skip even numbers
    if n > 11:
        break         # stop the loop entirely
    print(n)
```

## Truthiness

Empty containers, `0`, `""` and `None` are "falsy"; nearly everything else is "truthy":

```python-run
for value in [0, 1, "", "x", [], [0], None]:
    print(repr(value), bool(value))
```

## Key points

- Use `elif` for mutually exclusive branches.
- `range(1, n + 1)` loops from 1 to `n` inclusive.
- `%` and `//` are handy for digit manipulation.
