---
id: select-basics
title: SELECT basics
order: 1
datasetId: employees
exerciseSlugs: [select-all-departments, london-departments]
---

SQL (Structured Query Language) is how you ask a relational database questions. Data lives in **tables**: named collections of **rows**, where every row has the same **columns**.

This lesson uses a small company database with two tables, `departments` and `employees`. Every code block marked **Run** is live: edit it and press the button (or **Ctrl/⌘ + Enter**).

## Selecting everything

`SELECT` chooses columns and `FROM` names the table. `*` means "all columns":

```sql-run
SELECT * FROM departments;
```

## Choosing columns

List the columns you want, separated by commas. They come back in the order you write them:

```sql-run
SELECT first_name, last_name, title FROM employees;
```

## Renaming with AS

`AS` gives a column a new name in the result (an **alias**). You can also compute new columns:

```sql-run
SELECT first_name AS name, salary / 12 AS monthly_salary FROM employees;
```

## Unique values

`DISTINCT` removes duplicate rows from the result:

```sql-run
SELECT DISTINCT location FROM departments;
```

## Key points

- `SELECT columns FROM table` is the core of every query.
- `*` selects all columns; prefer explicit columns in real code.
- `AS` renames output columns; expressions like `salary / 12` are allowed.
- SQL keywords are case-insensitive, but upper case makes queries easier to read.
