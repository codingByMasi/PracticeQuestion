---
id: group-by-having
title: GROUP BY and HAVING
order: 5
datasetId: movies
exerciseSlugs: [headcount-by-department, prolific-reviewers, well-paid-departments]
---

`GROUP BY` splits rows into groups and computes aggregates **per group**.

## One row per group

```sql-run
SELECT genre, COUNT(*) AS movies FROM movies GROUP BY genre;
```

Every column in `SELECT` must either be in `GROUP BY` or be inside an aggregate.

```sql-run
SELECT genre, ROUND(AVG(runtime_minutes), 1) AS avg_runtime, MAX(gross_millions) AS best_gross
FROM movies
GROUP BY genre
ORDER BY avg_runtime DESC;
```

## Grouping by several columns

```sql-run
SELECT reviewer, rating, COUNT(*) AS times FROM reviews GROUP BY reviewer, rating ORDER BY reviewer, rating;
```

## HAVING filters groups

`WHERE` filters rows **before** grouping; `HAVING` filters groups **after**:

```sql-run
SELECT movie_id, COUNT(*) AS reviews, AVG(rating) AS avg_rating
FROM reviews
GROUP BY movie_id
HAVING COUNT(*) >= 3;
```

Both can appear in the same query:

```sql-run
SELECT reviewer, COUNT(*) AS high_ratings
FROM reviews
WHERE rating >= 9
GROUP BY reviewer
HAVING COUNT(*) > 1;
```

## Order of evaluation

`FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY` → `LIMIT`. This is why `WHERE` can't use aggregates but `HAVING` can.

## Key points

- `GROUP BY` produces one output row per distinct group.
- `HAVING` is `WHERE` for groups.
