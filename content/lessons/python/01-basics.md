---
id: basics
title: Values, variables and functions
order: 1
exerciseSlugs: [add-two-numbers, celsius-to-fahrenheit]
---

Python runs here in your browser. The first run downloads the Python runtime (about 10 MB); after that it's cached. Edit any **Run** block and press the button or **Ctrl/⌘ + Enter**. Like a REPL, the value of the last line is shown.

## Values and variables

Variables are names that point at values. No declarations needed:

```python-run
name = "Ada"
year = 1843
pi = 3.14159
print(name, year, pi)
type(pi)
```

## Arithmetic

`/` always gives a float, `//` is floor division, `%` is the remainder and `**` is exponentiation:

```python-run
print(7 / 2, 7 // 2, 7 % 2, 2 ** 10)
```

## Defining functions

`def` defines a function. Indentation (four spaces) marks the body. `return` sends a value back:

```python-run
def area(width, height):
    return width * height

area(3, 4)
```

## print vs return

`print` only displays text. Practice problems check what your function **returns**, so always `return` the answer:

```python-run
def shout(word):
    print(word.upper())   # displays, returns None

result = shout("hi")
print("result is", result)
```

## Default arguments

```python-run
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Grace"))
print(greet("Alan", greeting="Hi"))
```

`f"..."` strings (f-strings) insert expressions inside `{}`.

## Key points

- Indentation is syntax in Python.
- Functions `return` values; problems are judged on return values.
