import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import SqlSet
S = SqlSet("ecommerce", ["customers", "products", "orders", "order_items"])
p = S.p
REV = "oi.quantity * oi.unit_price"

p("Average items per order", "M", "aggregate", "On average how many units does an order contain? Round to 2 decimals (orders with items only).", ["Sum quantity per order first."],
  "WITH o AS (SELECT order_id, SUM(quantity) AS units FROM order_items GROUP BY order_id) SELECT ROUND(AVG(units), 2) AS avg_units FROM o;")
p("Second most expensive product per category", "H", "ranking", "For each category with at least two products show the second most expensive product (category, name, price).", ["`DENSE_RANK() OVER (PARTITION BY category ORDER BY price DESC)` = 2."],
  "WITH r AS (SELECT category, name, price, DENSE_RANK() OVER (PARTITION BY category ORDER BY price DESC) AS rk FROM products) SELECT category, name, price FROM r WHERE rk = 2;")
p("Order sizes compared with the customer average", "H", "window-functions", "For each customer's orders with items, show order id, order total and the customer's average order total (both rounded to 2 decimals) for customers with at least two orders.", ["Window `AVG` over per-order totals partitioned by customer."],
  f"WITH t AS (SELECT o.customer_id, o.id AS order_id, SUM({REV}) AS total FROM orders o JOIN order_items oi ON oi.order_id = o.id GROUP BY o.id) SELECT customer_id, order_id, ROUND(total, 2) AS total, ROUND(AVG(total) OVER (PARTITION BY customer_id), 2) AS customer_avg FROM t WHERE customer_id IN (SELECT customer_id FROM t GROUP BY customer_id HAVING COUNT(*) >= 2) ORDER BY customer_id, order_id;", ordered=True)
p("Unit price discounts", "M", "expressions", "For lines where the paid unit price is below the list price, show order id, product name and the discount percentage rounded to 1 decimal.", ["`100 * (price - unit_price) / price`."],
  "SELECT oi.order_id, p.name, ROUND(100.0 * (p.price - oi.unit_price) / p.price, 1) AS discount_pct FROM order_items oi JOIN products p ON p.id = oi.product_id WHERE oi.unit_price < p.price;")
p("Basket with the most distinct products", "M", "group-by", "Which order contains the most distinct products? Show order id and the count (no tie).", ["Count lines per order."],
  "SELECT order_id, COUNT(DISTINCT product_id) AS products FROM order_items GROUP BY order_id ORDER BY products DESC, order_id LIMIT 1;")
p("Products ordered by every customer who ordered", "H", "having", "List products that were ordered (any status) by at least 3 different customers. Show name and customer count.", ["`COUNT(DISTINCT o.customer_id)`."],
  "SELECT p.name, COUNT(DISTINCT o.customer_id) AS customers FROM products p JOIN order_items oi ON oi.product_id = p.id JOIN orders o ON o.id = oi.order_id GROUP BY p.id, p.name HAVING COUNT(DISTINCT o.customer_id) >= 3;")
p("Median order total", "H", "window-functions", "Compute the median order total (orders with items), rounded to 2 decimals.", ["Rank totals and pick the middle row(s)."],
  f"WITH t AS (SELECT SUM({REV}) AS total FROM order_items oi GROUP BY order_id), r AS (SELECT total, ROW_NUMBER() OVER (ORDER BY total) AS rn, COUNT(*) OVER () AS n FROM t) SELECT ROUND(AVG(total), 2) AS median_total FROM r WHERE rn IN ((n + 1) / 2, (n + 2) / 2);")
p("Country with the biggest basket", "M", "group-by", "Which customer country has the highest average order value (orders with items, non-cancelled)? Show country and the average rounded to 2 decimals.", ["Per-order totals, then average by country."],
  f"WITH t AS (SELECT o.customer_id, SUM({REV}) AS total FROM orders o JOIN order_items oi ON oi.order_id = o.id WHERE o.status <> 'cancelled' GROUP BY o.id) SELECT c.country, ROUND(AVG(t.total), 2) AS avg_order FROM t JOIN customers c ON c.id = t.customer_id GROUP BY c.country ORDER BY AVG(t.total) DESC LIMIT 1;")
p("Percent of customers who ordered", "M", "subquery", "What percentage of customers have placed at least one order? Round to 1 decimal.", ["Count distinct ordering customers over all customers."],
  "SELECT ROUND(100.0 * (SELECT COUNT(DISTINCT customer_id) FROM orders) / (SELECT COUNT(*) FROM customers), 1) AS pct;")
