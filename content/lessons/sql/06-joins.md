---
id: joins
title: Joining tables
order: 6
datasetId: employees
exerciseSlugs: [employee-departments, empty-departments, employee-managers]
---

Relational data is split across tables linked by **keys**. `employees.department_id` refers to `departments.id`. A `JOIN` puts matching rows side by side.

## INNER JOIN

Keeps only rows with a match on both sides:

```sql-run
SELECT e.first_name, d.name AS department
FROM employees e
JOIN departments d ON d.id = e.department_id;
```

`e` and `d` are **table aliases**; they keep column references short and unambiguous.

## LEFT JOIN

Keeps every row from the left table; missing matches become NULL:

```sql-run
SELECT d.name, e.first_name
FROM departments d
LEFT JOIN employees e ON e.department_id = d.id
ORDER BY d.name;
```

Notice *Research* appears with a NULL employee. Filtering on that NULL finds rows **without** a match (an anti-join):

```sql-run
SELECT d.name FROM departments d
LEFT JOIN employees e ON e.department_id = d.id
WHERE e.id IS NULL;
```

## Self-joins

A table can be joined to itself. Here each employee is matched with their manager:

```sql-run
SELECT e.first_name AS employee, m.first_name AS manager
FROM employees e
LEFT JOIN employees m ON m.id = e.manager_id;
```

## Joins with aggregates

```sql-run
SELECT d.name, COUNT(e.id) AS headcount
FROM departments d
LEFT JOIN employees e ON e.department_id = d.id
GROUP BY d.id, d.name;
```

`COUNT(e.id)` counts 0 for departments without employees, while `COUNT(*)` would count 1.

## Key points

- `JOIN ... ON` matches rows by a condition, usually key equality.
- `INNER JOIN` drops unmatched rows; `LEFT JOIN` keeps every left row.
