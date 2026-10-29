---
id: aggregates
title: Aggregate functions
order: 4
datasetId: movies
exerciseSlugs: [count-employees, salary-stats, box-office-totals]
---

Aggregate functions collapse many rows into one value. The movies dataset has `movies`, `directors` and `reviews`.

## COUNT, SUM, AVG, MIN, MAX

```sql-run
SELECT COUNT(*) AS movies, MIN(release_year) AS oldest, MAX(release_year) AS newest FROM movies;
```

```sql-run
SELECT AVG(runtime_minutes) AS avg_runtime, SUM(gross_millions) AS total_gross FROM movies;
```

## Rounding

`ROUND(value, digits)` tidies up averages:

```sql-run
SELECT ROUND(AVG(rating), 2) AS avg_rating FROM reviews;
```

## Aggregates and NULL

Aggregates **skip NULLs**. `COUNT(*)` counts rows, while `COUNT(column)` counts non-NULL values:

```sql-run
SELECT COUNT(*) AS all_movies, COUNT(budget_millions) AS with_budget FROM movies;
```

## Filtering first

`WHERE` runs before aggregation, so you can aggregate a subset:

```sql-run
SELECT COUNT(*) AS sci_fi_movies, AVG(runtime_minutes) AS avg_runtime
FROM movies
WHERE genre = 'Sci-Fi';
```

## COUNT DISTINCT

```sql-run
SELECT COUNT(DISTINCT reviewer) AS reviewers FROM reviews;
```

## Key points

- Without `GROUP BY`, an aggregate query returns exactly one row.
- NULLs are ignored by every aggregate except `COUNT(*)`.
- Use `ROUND` when a problem asks for a fixed number of decimals.
