---
id: sorting-limiting
title: Sorting and limiting
order: 3
datasetId: ecommerce
exerciseSlugs: [top-five-salaries, products-by-category-price]
---

Without `ORDER BY`, a database may return rows in **any** order. If order matters, ask for it. This lesson uses the e-commerce dataset (`customers`, `products`, `orders`, `order_items`).

## ORDER BY

Sort ascending (`ASC`, the default) or descending (`DESC`):

```sql-run
SELECT name, price FROM products ORDER BY price DESC;
```

## Several sort keys

Later keys only break ties in earlier ones:

```sql-run
SELECT name, category, price FROM products ORDER BY category, price;
```

## LIMIT and OFFSET

`LIMIT n` keeps the first `n` rows; `OFFSET k` skips `k` rows first (useful for pagination):

```sql-run
SELECT name, price FROM products ORDER BY price DESC LIMIT 3;
```

```sql-run
SELECT name, price FROM products ORDER BY price DESC LIMIT 3 OFFSET 3;
```

## Sorting by expressions

You can sort by a computed value, or by an alias defined in `SELECT`:

```sql-run
SELECT order_id, product_id, quantity * unit_price AS line_total
FROM order_items
ORDER BY line_total DESC
LIMIT 5;
```

## Key points

- Only `ORDER BY` guarantees order.
- `LIMIT` without `ORDER BY` returns an arbitrary subset.
- Add a tie-breaker column when you need fully deterministic results.
