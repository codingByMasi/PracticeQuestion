---
id: ctes-and-windows
title: CTEs and window functions
order: 8
datasetId: ecommerce
exerciseSlugs: [monthly-revenue, salary-rank-in-department, running-revenue]
---

Two tools make complex queries readable and powerful: **common table expressions** and **window functions**.

## WITH: common table expressions

A CTE names a subquery so you can use it like a table. Queries read top to bottom:

```sql-run
WITH order_totals AS (
  SELECT order_id, SUM(quantity * unit_price) AS total
  FROM order_items
  GROUP BY order_id
)
SELECT o.id, o.order_date, ROUND(t.total, 2) AS total
FROM orders o
JOIN order_totals t ON t.order_id = o.id
ORDER BY t.total DESC
LIMIT 5;
```

You can define several CTEs separated by commas, and each can use the previous ones.

## Window functions

A window function computes a value **for each row** from a set of related rows, without collapsing them like `GROUP BY` does.

```sql-run
SELECT name, category, price,
  RANK() OVER (PARTITION BY category ORDER BY price DESC) AS price_rank
FROM products;
```

- `PARTITION BY` splits rows into independent groups.
- `ORDER BY` inside `OVER` defines the order within each partition.

## Ranking functions

`ROW_NUMBER()` numbers rows uniquely, `RANK()` leaves gaps after ties, `DENSE_RANK()` doesn't.

## Running totals

Aggregates become cumulative with `OVER (ORDER BY ...)`:

```sql-run
SELECT id, order_date,
  COUNT(*) OVER (ORDER BY order_date) AS orders_so_far
FROM orders
ORDER BY order_date;
```

## Comparing with neighbours

`LAG` and `LEAD` read the previous or next row:

```sql-run
SELECT id, order_date, LAG(order_date) OVER (ORDER BY order_date) AS previous_order
FROM orders
WHERE customer_id = 1;
```

## Key points

- CTEs (`WITH name AS (...)`) break big queries into named steps.
- Window functions keep every row and add a computed column.
- `PARTITION BY` is to windows what `GROUP BY` is to aggregates.
