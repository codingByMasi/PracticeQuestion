import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import SqlSet

S = SqlSet("ecommerce", ["customers", "products", "orders", "order_items"])
p = S.p
REV = "oi.quantity * oi.unit_price"

p("Product catalogue", "E", "select", "List the name and price of every product.", ["Select two columns from `products`."], "SELECT name, price FROM products;")
p("Customers from the USA", "E", "where", "List the names of customers whose country is `USA`.", ["Strings use single quotes."], "SELECT name FROM customers WHERE country = 'USA';")
p("Budget electronics", "E", "where", "Find Electronics products priced under 50. Show name and price.", ["Combine two conditions with `AND`."],
  "SELECT name, price FROM products WHERE category = 'Electronics' AND price < 50;")
p("Not yet delivered", "E", "where", "List order ids whose status is either `shipped` or `pending`.", ["`IN ('shipped', 'pending')`."],
  "SELECT id, status FROM orders WHERE status IN ('shipped', 'pending');")
p("Orders in spring 2024", "E", "dates", "List orders placed from 2024-03-01 to 2024-05-31 inclusive.", ["`BETWEEN` works on ISO date strings."],
  "SELECT id, order_date FROM orders WHERE order_date BETWEEN '2024-03-01' AND '2024-05-31';")
p("Customers sorted by signup", "E", "order-by", "List customer names with their signup date, earliest signup first.", ["`ORDER BY signup_date`."],
  "SELECT name, signup_date FROM customers ORDER BY signup_date;", ordered=True)
p("Three priciest products", "E", "order-by", "Which three products have the highest price? Highest first.", ["`ORDER BY price DESC LIMIT 3`."],
  "SELECT name, price FROM products ORDER BY price DESC LIMIT 3;", ordered=True)
p("Countries we sell to", "E", "distinct", "List each customer country once.", ["`SELECT DISTINCT country`."], "SELECT DISTINCT country FROM customers;")
p("Gmail-style email domains", "E", "strings", "Show each customer's name and the part of their email after the `@` sign.", ["`substr(email, instr(email, '@') + 1)`."],
  "SELECT name, substr(email, instr(email, '@') + 1) AS domain FROM customers;")
p("Price with tax", "E", "expressions", "Show each product name and its price with 20% tax added, rounded to 2 decimals.", ["`ROUND(price * 1.2, 2)`."],
  "SELECT name, ROUND(price * 1.2, 2) AS price_with_tax FROM products;")
p("Product price tiers", "E", "case", "Classify products: `cheap` under 20, `standard` from 20 to under 100, `premium` from 100. Show name and tier.", ["Use a `CASE` expression."],
  "SELECT name, CASE WHEN price < 20 THEN 'cheap' WHEN price < 100 THEN 'standard' ELSE 'premium' END AS tier FROM products;")
p("Number of orders", "E", "aggregate", "How many orders exist in total?", ["`COUNT(*)`."], "SELECT COUNT(*) AS order_count FROM orders;")
p("Catalogue price range", "E", "aggregate", "Show the cheapest price, the most expensive price and the average price (rounded to 2 decimals) across all products.", ["`MIN`, `MAX`, `AVG`."],
  "SELECT MIN(price) AS cheapest, MAX(price) AS priciest, ROUND(AVG(price), 2) AS avg_price FROM products;")
p("Orders per status", "E", "group-by", "Count orders in each status.", ["`GROUP BY status`."], "SELECT status, COUNT(*) AS orders FROM orders GROUP BY status;")
p("Customers per country", "E", "group-by", "How many customers are in each country?", ["`GROUP BY country`."], "SELECT country, COUNT(*) AS customers FROM customers GROUP BY country;")
p("Products per category", "E", "group-by", "For each category, show the number of products and the average price rounded to 2 decimals.", ["Two aggregates in one query."],
  "SELECT category, COUNT(*) AS products, ROUND(AVG(price), 2) AS avg_price FROM products GROUP BY category;")
p("Items with product names", "E", "join", "For each order line show the order id, the product name and the quantity.", ["Join `order_items` to `products`."],
  "SELECT oi.order_id, p.name, oi.quantity FROM order_items oi JOIN products p ON p.id = oi.product_id;")
p("Orders with customer names", "E", "join", "List each order id with the name of the customer who placed it.", ["Join `orders` to `customers`."],
  "SELECT o.id, c.name FROM orders o JOIN customers c ON c.id = o.customer_id;")
p("Categories with more than three products", "E", "having", "Which categories contain more than three products?", ["`HAVING COUNT(*) > 3`."],
  "SELECT category, COUNT(*) AS products FROM products GROUP BY category HAVING COUNT(*) > 3;")
p("Units sold per product", "M", "join", "For every product that has been ordered, show its name and total units sold across all orders (cancelled included).", ["Join, then `SUM(quantity)` per product."],
  "SELECT p.name, SUM(oi.quantity) AS units FROM order_items oi JOIN products p ON p.id = oi.product_id GROUP BY p.id, p.name;")
p("Order totals", "M", "join", "Compute the total value of each order (quantity times unit price summed over its lines), rounded to 2 decimals. Show order id and total.", ["Group `order_items` by `order_id`."],
  f"SELECT oi.order_id, ROUND(SUM({REV}), 2) AS total FROM order_items oi GROUP BY oi.order_id;")
p("Revenue by country", "M", "multi-join", "Total revenue per customer country, excluding cancelled orders, rounded to 2 decimals. Highest first.", ["Join customers, orders and order items."],
  f"SELECT c.country, ROUND(SUM({REV}), 2) AS revenue FROM customers c JOIN orders o ON o.customer_id = c.id JOIN order_items oi ON oi.order_id = o.id WHERE o.status <> 'cancelled' GROUP BY c.country ORDER BY revenue DESC;", ordered=True)
p("Customers without orders", "M", "left-join", "List customers who have never placed an order.", ["`LEFT JOIN orders` and test for NULL."],
  "SELECT c.name FROM customers c LEFT JOIN orders o ON o.customer_id = c.id WHERE o.id IS NULL;")
p("Orders per customer including zero", "M", "left-join", "Show every customer and how many orders they placed (zero if none).", ["Count a column from the right table, not `*`."],
  "SELECT c.name, COUNT(o.id) AS orders FROM customers c LEFT JOIN orders o ON o.customer_id = c.id GROUP BY c.id, c.name;")
p("Cheapest product per category", "M", "correlated-subquery", "For each category show the cheapest product (name and price).", ["Compare to `MIN(price)` in the same category."],
  "SELECT p.category, p.name, p.price FROM products p WHERE p.price = (SELECT MIN(p2.price) FROM products p2 WHERE p2.category = p.category);")
p("Products above average price", "M", "subquery", "List products priced above the average product price.", ["Scalar subquery for the average."],
  "SELECT name, price FROM products WHERE price > (SELECT AVG(price) FROM products);")
p("Customers who bought electronics", "M", "exists", "List the names of customers who have ordered at least one Electronics product (any status).", ["`EXISTS` with a join inside."],
  "SELECT c.name FROM customers c WHERE EXISTS (SELECT 1 FROM orders o JOIN order_items oi ON oi.order_id = o.id JOIN products p ON p.id = oi.product_id WHERE o.customer_id = c.id AND p.category = 'Electronics');")
p("Customers who never bought stationery", "M", "exists", "List customers who have **not** ordered any Stationery product (customers with no orders count).", ["`NOT EXISTS`."],
  "SELECT c.name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o JOIN order_items oi ON oi.order_id = o.id JOIN products p ON p.id = oi.product_id WHERE o.customer_id = c.id AND p.category = 'Stationery');")
p("Orders over 200", "M", "having", "List orders whose total value exceeds 200. Show order id and total rounded to 2 decimals.", ["Aggregate, then filter with `HAVING`."],
  f"SELECT oi.order_id, ROUND(SUM({REV}), 2) AS total FROM order_items oi GROUP BY oi.order_id HAVING SUM({REV}) > 200;")
p("Average order value", "M", "cte", "What is the average value of an order (over orders that have items), rounded to 2 decimals?", ["Compute per-order totals in a CTE first."],
  f"WITH totals AS (SELECT order_id, SUM({REV}) AS total FROM order_items oi GROUP BY order_id) SELECT ROUND(AVG(total), 2) AS avg_order_value FROM totals;")
p("Price drift from list price", "M", "join", "Find order lines where the customer paid a different unit price than the product's current list price. Show order id, product name, list price and unit price.", ["Join items to products and compare."],
  "SELECT oi.order_id, p.name, p.price AS list_price, oi.unit_price FROM order_items oi JOIN products p ON p.id = oi.product_id WHERE oi.unit_price <> p.price;")
p("Customer signup months", "M", "dates", "How many customers signed up in each month (format YYYY-MM)? Earliest month first.", ["`strftime('%Y-%m', signup_date)`."],
  "SELECT strftime('%Y-%m', signup_date) AS month, COUNT(*) AS signups FROM customers GROUP BY month ORDER BY month;", ordered=True)
p("Cancellation rate", "M", "aggregate", "What percentage of orders were cancelled? Round to 1 decimal.", ["Average a 0/1 flag, or divide counts."],
  "SELECT ROUND(100.0 * SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*), 1) AS cancelled_pct FROM orders;")
p("Revenue per order status", "M", "group-by", "Total value of order lines per order status, rounded to 2 decimals.", ["Join orders to items."],
  f"SELECT o.status, ROUND(SUM({REV}), 2) AS value FROM orders o JOIN order_items oi ON oi.order_id = o.id GROUP BY o.status;")
p("Repeat customers", "M", "having", "List customers with at least two non-cancelled orders. Show name and order count.", ["Filter cancelled orders before grouping."],
  "SELECT c.name, COUNT(*) AS orders FROM customers c JOIN orders o ON o.customer_id = c.id WHERE o.status <> 'cancelled' GROUP BY c.id, c.name HAVING COUNT(*) >= 2;")
p("Biggest single line", "M", "order-by", "Which order line has the highest value (quantity times unit price)? Show order id, product id and value.", ["Sort by the computed value, take one."],
  f"SELECT oi.order_id, oi.product_id, {REV} AS value FROM order_items oi ORDER BY value DESC LIMIT 1;")
p("Products never sold in January", "M", "subquery", "List products that do not appear in any order placed in January 2024.", ["Subquery on orders in January, `NOT IN`."],
  "SELECT name FROM products WHERE id NOT IN (SELECT oi.product_id FROM order_items oi JOIN orders o ON o.id = oi.order_id WHERE o.order_date LIKE '2024-01-%');")
p("Two-category shoppers", "H", "having", "Find customers who bought products from at least two different categories (non-cancelled orders). Show name and category count.", ["`COUNT(DISTINCT p.category)`."],
  "SELECT c.name, COUNT(DISTINCT p.category) AS categories FROM customers c JOIN orders o ON o.customer_id = c.id AND o.status <> 'cancelled' JOIN order_items oi ON oi.order_id = o.id JOIN products p ON p.id = oi.product_id GROUP BY c.id, c.name HAVING COUNT(DISTINCT p.category) >= 2;")
p("Products bought together", "H", "self-join", "Find pairs of different products that appear in the same order. List each pair once (smaller product id first) together with the number of orders that contain both.", ["Self-join `order_items` on `order_id` with `a.product_id < b.product_id`."],
  "SELECT a.product_id AS product_a, b.product_id AS product_b, COUNT(*) AS together FROM order_items a JOIN order_items b ON a.order_id = b.order_id AND a.product_id < b.product_id GROUP BY a.product_id, b.product_id;")
p("Category share of revenue", "H", "window-functions", "Each category's revenue (non-cancelled orders) and its percentage of total revenue, rounded to 1 decimal. Highest share first.", ["Window `SUM(...) OVER ()` gives the grand total beside each group."],
  f"WITH rev AS (SELECT p.category, SUM({REV}) AS revenue FROM order_items oi JOIN orders o ON o.id = oi.order_id JOIN products p ON p.id = oi.product_id WHERE o.status <> 'cancelled' GROUP BY p.category) SELECT category, ROUND(revenue, 2) AS revenue, ROUND(100.0 * revenue / SUM(revenue) OVER (), 1) AS pct FROM rev ORDER BY pct DESC;", ordered=True)
p("Latest order per customer", "H", "window-functions", "For each customer who ordered, show their name and the id and date of their most recent order.", ["`ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC)`."],
  "WITH ranked AS (SELECT o.*, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn FROM orders o) SELECT c.name, r.id AS order_id, r.order_date FROM ranked r JOIN customers c ON c.id = r.customer_id WHERE r.rn = 1;")
p("Days between orders", "H", "window-functions", "For each customer's orders, show the customer id, order id, date and the number of days since their previous order (NULL for the first).", ["`LAG(order_date)` and `julianday`."],
  "SELECT customer_id, id AS order_id, order_date, CAST(julianday(order_date) - julianday(LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)) AS INTEGER) AS days_since_previous FROM orders ORDER BY customer_id, order_date;", ordered=True)
p("Running customer spend", "H", "running-total", "For each customer, list their non-cancelled orders in date order with the order total and the customer's cumulative spend so far (both rounded to 2 decimals).", ["Per-order totals in a CTE, then `SUM() OVER (PARTITION BY ... ORDER BY ...)`."],
  f"WITH t AS (SELECT o.customer_id, o.id AS order_id, o.order_date, SUM({REV}) AS total FROM orders o JOIN order_items oi ON oi.order_id = o.id WHERE o.status <> 'cancelled' GROUP BY o.id) SELECT customer_id, order_id, ROUND(total, 2) AS total, ROUND(SUM(total) OVER (PARTITION BY customer_id ORDER BY order_date, order_id), 2) AS cumulative FROM t ORDER BY customer_id, order_date, order_id;", ordered=True)
p("Top product per category by revenue", "H", "ranking", "For each category, show the product with the highest revenue (non-cancelled lines). Show category, product name and revenue rounded to 2 decimals.", ["Rank products within category with `RANK()`."],
  f"WITH r AS (SELECT p.category, p.name, SUM({REV}) AS revenue FROM order_items oi JOIN orders o ON o.id = oi.order_id JOIN products p ON p.id = oi.product_id WHERE o.status <> 'cancelled' GROUP BY p.id), k AS (SELECT *, RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rk FROM r) SELECT category, name, ROUND(revenue, 2) AS revenue FROM k WHERE rk = 1;")
p("Quarterly revenue pivot", "H", "pivot", "Revenue of non-cancelled orders per quarter of 2024 as columns `q1` and `q2` (Jan-Mar, Apr-Jun), rounded to 2 decimals, in one row.", ["Conditional aggregation: `SUM(CASE WHEN ... THEN value END)`."],
  f"SELECT ROUND(SUM(CASE WHEN o.order_date < '2024-04-01' THEN {REV} END), 2) AS q1, ROUND(SUM(CASE WHEN o.order_date >= '2024-04-01' THEN {REV} END), 2) AS q2 FROM orders o JOIN order_items oi ON oi.order_id = o.id WHERE o.status <> 'cancelled';")
p("Category columns per customer", "H", "pivot", "For each customer who ordered anything (non-cancelled), show how many units they bought in each category as three columns `electronics`, `home` and `stationery` (0 when none).", ["Conditional `SUM(CASE ...)` per category."],
  "SELECT c.name, COALESCE(SUM(CASE WHEN p.category = 'Electronics' THEN oi.quantity END), 0) AS electronics, COALESCE(SUM(CASE WHEN p.category = 'Home' THEN oi.quantity END), 0) AS home, COALESCE(SUM(CASE WHEN p.category = 'Stationery' THEN oi.quantity END), 0) AS stationery FROM customers c JOIN orders o ON o.customer_id = c.id AND o.status <> 'cancelled' JOIN order_items oi ON oi.order_id = o.id JOIN products p ON p.id = oi.product_id GROUP BY c.id, c.name;")
p("Customers above their country average", "H", "correlated-subquery", "Among customers with non-cancelled orders, list those whose total spend exceeds the average total spend of customers in their own country. Show name, country and total rounded to 2 decimals.", ["Build per-customer totals in a CTE and compare with a window average per country."],
  f"WITH s AS (SELECT c.id, c.name, c.country, SUM({REV}) AS total FROM customers c JOIN orders o ON o.customer_id = c.id AND o.status <> 'cancelled' JOIN order_items oi ON oi.order_id = o.id GROUP BY c.id) SELECT name, country, ROUND(total, 2) AS total FROM (SELECT *, AVG(total) OVER (PARTITION BY country) AS country_avg FROM s) WHERE total > country_avg;")
p("Orders per month with gaps filled", "H", "recursive", "For each month from 2024-01 to 2024-06 show the number of orders (0 for empty months). Use a recursive CTE for the month list. Earliest first.", ["`LEFT JOIN` orders onto the generated months."],
  "WITH RECURSIVE months(m) AS (SELECT '2024-01' UNION ALL SELECT strftime('%Y-%m', date(m || '-01', '+1 month')) FROM months WHERE m < '2024-06') SELECT m AS month, COUNT(o.id) AS orders FROM months LEFT JOIN orders o ON strftime('%Y-%m', o.order_date) = m GROUP BY m ORDER BY m;", ordered=True)
p("Cancel an order and recount", "M", "dml", "Delete all items of cancelled orders with a `DELETE`, then report how many order lines remain.", ["`DELETE FROM order_items WHERE order_id IN (SELECT id FROM orders WHERE status = 'cancelled')`."],
  "DELETE FROM order_items WHERE order_id IN (SELECT id FROM orders WHERE status = 'cancelled'); SELECT COUNT(*) AS lines FROM order_items;")
p("Price increase simulation", "M", "dml", "Raise the price of every Home product by 5%, then list the Home products with their new prices rounded to 2 decimals.", ["`UPDATE` first, then `SELECT`."],
  "UPDATE products SET price = price * 1.05 WHERE category = 'Home'; SELECT name, ROUND(price, 2) AS price FROM products WHERE category = 'Home';")
p("Add a new customer", "M", "dml", "Insert a customer named `Zed Park` from `Korea` (email `zed@example.com`, signup date `2024-07-01`, id 11), then list all customers from Korea or Japan.", ["`INSERT INTO customers (...) VALUES (...)`."],
  "INSERT INTO customers (id, name, email, country, signup_date) VALUES (11, 'Zed Park', 'zed@example.com', 'Korea', '2024-07-01'); SELECT name, country FROM customers WHERE country IN ('Korea', 'Japan');")
p("Order status summary string", "M", "strings", "For each status, produce one text value like `delivered: 10` using `||`. Name the column `summary`.", ["Concatenate with `||`; cast the count as needed."],
  "SELECT status || ': ' || COUNT(*) AS summary FROM orders GROUP BY status;")
p("Average days to ship placeholder", "M", "dates", "How many days are there between each customer's signup and their first order? Show customer name and days, customers with orders only.", ["`MIN(order_date)` per customer, then `julianday` difference."],
  "SELECT c.name, CAST(julianday(MIN(o.order_date)) - julianday(c.signup_date) AS INTEGER) AS days_to_first_order FROM customers c JOIN orders o ON o.customer_id = c.id GROUP BY c.id, c.name;")
p("Expensive lines per order", "M", "join", "For each order, count the lines where the unit price is at least 50. Show only orders with at least one such line.", ["Filter lines with `WHERE`, then group."],
  "SELECT order_id, COUNT(*) AS expensive_lines FROM order_items WHERE unit_price >= 50 GROUP BY order_id;")
p("Customer lifetime value ranking", "H", "ranking", "Rank customers by lifetime value (non-cancelled revenue) with `DENSE_RANK`. Show rank, name and value rounded to 2 decimals. Order by rank then name.", ["`DENSE_RANK() OVER (ORDER BY total DESC)`."],
  f"WITH s AS (SELECT c.id, c.name, SUM({REV}) AS total FROM customers c JOIN orders o ON o.customer_id = c.id AND o.status <> 'cancelled' JOIN order_items oi ON oi.order_id = o.id GROUP BY c.id) SELECT DENSE_RANK() OVER (ORDER BY total DESC) AS rank, name, ROUND(total, 2) AS ltv FROM s ORDER BY rank, name;", ordered=True)
p("Second order of each customer", "H", "window-functions", "For customers with at least two orders (any status), show the id and date of their second order.", ["`ROW_NUMBER()` partitioned by customer, filter 2."],
  "WITH r AS (SELECT customer_id, id, order_date, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, id) AS rn FROM orders) SELECT customer_id, id AS order_id, order_date FROM r WHERE rn = 2;")
p("Median product price", "H", "window-functions", "Compute the median product price. With an even number of products, average the two middle prices.", ["Order by price, number the rows, and keep the middle one or two."],
  "WITH r AS (SELECT price, ROW_NUMBER() OVER (ORDER BY price) AS rn, COUNT(*) OVER () AS n FROM products) SELECT AVG(price) AS median_price FROM r WHERE rn IN ((n + 1) / 2, (n + 2) / 2);")
p("Best selling product by month", "H", "ranking", "For each month of 2024 that has non-cancelled sales, show the product with the most units sold (month, product name, units). Break ties by product name.", ["Group by month and product, rank with `ROW_NUMBER` ordered by units desc then name."],
  "WITH m AS (SELECT strftime('%Y-%m', o.order_date) AS month, p.name, SUM(oi.quantity) AS units FROM orders o JOIN order_items oi ON oi.order_id = o.id JOIN products p ON p.id = oi.product_id WHERE o.status <> 'cancelled' GROUP BY month, p.id), r AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY month ORDER BY units DESC, name) AS rn FROM m) SELECT month, name, units FROM r WHERE rn = 1 ORDER BY month;", ordered=True)
