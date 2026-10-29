---
id: filtering
title: Filtering rows with WHERE
order: 2
datasetId: employees
exerciseSlugs: [high-earners, recent-engineering-hires, missing-department]
---

`WHERE` keeps only the rows for which a condition is true.

## Comparisons

The usual operators work: `=`, `<>` (or `!=`), `<`, `<=`, `>`, `>=`.

```sql-run
SELECT first_name, salary FROM employees WHERE salary >= 150000;
```

Text values go in **single quotes**:

```sql-run
SELECT name FROM departments WHERE location = 'Berlin';
```

## Combining conditions

Use `AND`, `OR` and `NOT`. Parentheses make the intent explicit:

```sql-run
SELECT first_name, department_id, salary
FROM employees
WHERE department_id = 2 AND (salary > 95000 OR title = 'Sales Associate');
```

## Ranges and lists

`BETWEEN` is inclusive at both ends, and `IN` tests membership in a list:

```sql-run
SELECT first_name, hire_date FROM employees WHERE hire_date BETWEEN '2019-01-01' AND '2020-12-31';
```

```sql-run
SELECT first_name, title FROM employees WHERE title IN ('CTO', 'CFO');
```

## Pattern matching

`LIKE` matches text patterns: `%` is any sequence of characters, `_` is a single character.

```sql-run
SELECT first_name, last_name FROM employees WHERE last_name LIKE 'T%';
```

## NULL is special

`NULL` means "unknown". Comparing anything to `NULL` with `=` gives unknown, not true, so use `IS NULL` / `IS NOT NULL`:

```sql-run
SELECT first_name, manager_id FROM employees WHERE manager_id IS NULL;
```

## Key points

- `WHERE` filters rows before anything is returned.
- Dates stored as `YYYY-MM-DD` text compare correctly as strings.
- Never write `= NULL`; always `IS NULL`.
