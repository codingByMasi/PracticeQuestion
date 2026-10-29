---
id: subqueries
title: Subqueries
order: 7
datasetId: employees
exerciseSlugs: [above-average-salary, never-ordered-products, top-earner-per-department]
---

A **subquery** is a query inside another query, written in parentheses.

## Scalar subqueries

A subquery that returns one value can be used like a constant:

```sql-run
SELECT first_name, salary, (SELECT AVG(salary) FROM employees) AS company_avg
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

## IN and NOT IN

A subquery returning one column works as a list:

```sql-run
SELECT first_name FROM employees
WHERE department_id IN (SELECT id FROM departments WHERE location = 'London');
```

Careful: `NOT IN` returns no rows at all if the subquery contains a NULL.

## EXISTS

`EXISTS` checks whether a subquery returns any row. It is often used with a **correlated** subquery, which refers to the outer row:

```sql-run
SELECT d.name FROM departments d
WHERE NOT EXISTS (SELECT 1 FROM employees e WHERE e.department_id = d.id);
```

## Correlated subqueries

The inner query is re-evaluated per outer row. Who earns more than their department's average?

```sql-run
SELECT e.first_name, e.department_id, e.salary
FROM employees e
WHERE e.salary > (
  SELECT AVG(e2.salary) FROM employees e2 WHERE e2.department_id = e.department_id
);
```

## Subqueries in FROM

A subquery can act as a temporary table (it needs an alias):

```sql-run
SELECT department_id, avg_salary
FROM (SELECT department_id, AVG(salary) AS avg_salary FROM employees GROUP BY department_id) AS t
WHERE avg_salary > 120000;
```

## Key points

- Scalar subqueries return one value; `IN` subqueries return one column.
- Correlated subqueries reference the outer query.
- Prefer `NOT EXISTS` over `NOT IN` when NULLs might appear.
