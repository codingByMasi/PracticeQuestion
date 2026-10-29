CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  country TEXT NOT NULL,
  signup_date TEXT NOT NULL
);

CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  price REAL NOT NULL
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(id),
  order_date TEXT NOT NULL,
  status TEXT NOT NULL
);

CREATE TABLE order_items (
  order_id INTEGER NOT NULL REFERENCES orders(id),
  product_id INTEGER NOT NULL REFERENCES products(id),
  quantity INTEGER NOT NULL,
  unit_price REAL NOT NULL,
  PRIMARY KEY (order_id, product_id)
);

INSERT INTO customers (id, name, email, country, signup_date) VALUES
  (1, 'Olivia Chen', 'olivia@example.com', 'USA', '2023-01-15'),
  (2, 'Liam Novak', 'liam@example.com', 'Germany', '2023-02-03'),
  (3, 'Sofia Rossi', 'sofia@example.com', 'Italy', '2023-03-21'),
  (4, 'Noah Smith', 'noah@example.com', 'USA', '2023-04-10'),
  (5, 'Emma Dubois', 'emma@example.com', 'France', '2023-05-05'),
  (6, 'Lucas Silva', 'lucas@example.com', 'Brazil', '2023-06-18'),
  (7, 'Mia Tanaka', 'mia@example.com', 'Japan', '2023-08-30'),
  (8, 'Ethan Brown', 'ethan@example.com', 'USA', '2023-10-12'),
  (9, 'Ava Müller', 'ava@example.com', 'Germany', '2024-01-07'),
  (10, 'Leo Garcia', 'leo@example.com', 'Spain', '2024-02-14');

INSERT INTO products (id, name, category, price) VALUES
  (1, 'Mechanical Keyboard', 'Electronics', 89.99),
  (2, 'Wireless Mouse', 'Electronics', 24.50),
  (3, '27in Monitor', 'Electronics', 229.00),
  (4, 'USB-C Hub', 'Electronics', 39.95),
  (5, 'Desk Lamp', 'Home', 34.00),
  (6, 'Office Chair', 'Home', 189.00),
  (7, 'Coffee Mug', 'Home', 12.00),
  (8, 'Notebook Set', 'Stationery', 9.50),
  (9, 'Fountain Pen', 'Stationery', 45.00),
  (10, 'Sticky Notes', 'Stationery', 4.25),
  (11, 'Standing Desk', 'Home', 399.00),
  (12, 'Webcam', 'Electronics', 59.00),
  (13, 'Laptop Stand', 'Electronics', 49.00),
  (14, 'Desk Mat', 'Home', 19.99);

INSERT INTO orders (id, customer_id, order_date, status) VALUES
  (1, 1, '2024-01-05', 'delivered'),
  (2, 2, '2024-01-12', 'delivered'),
  (3, 1, '2024-01-20', 'delivered'),
  (4, 3, '2024-02-02', 'delivered'),
  (5, 4, '2024-02-11', 'cancelled'),
  (6, 5, '2024-02-18', 'delivered'),
  (7, 2, '2024-03-01', 'delivered'),
  (8, 6, '2024-03-09', 'shipped'),
  (9, 1, '2024-03-15', 'delivered'),
  (10, 7, '2024-03-28', 'delivered'),
  (11, 4, '2024-04-04', 'delivered'),
  (12, 8, '2024-04-19', 'shipped'),
  (13, 3, '2024-05-02', 'delivered'),
  (14, 9, '2024-05-16', 'delivered'),
  (15, 5, '2024-05-30', 'cancelled'),
  (16, 2, '2024-06-08', 'delivered'),
  (17, 7, '2024-06-21', 'shipped'),
  (18, 1, '2024-06-29', 'pending');

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
  (1, 1, 1, 89.99), (1, 2, 1, 24.50),
  (2, 3, 2, 229.00),
  (3, 8, 3, 9.50), (3, 10, 5, 4.25),
  (4, 6, 1, 189.00), (4, 5, 1, 34.00),
  (5, 11, 1, 399.00),
  (6, 9, 2, 45.00), (6, 8, 2, 9.50),
  (7, 4, 1, 39.95), (7, 12, 1, 59.00),
  (8, 7, 4, 12.00),
  (9, 3, 1, 219.00), (9, 4, 2, 39.95),
  (10, 1, 1, 89.99), (10, 6, 1, 189.00),
  (11, 2, 2, 24.50),
  (12, 11, 1, 399.00), (12, 5, 2, 34.00),
  (13, 7, 2, 12.00),
  (14, 12, 1, 59.00), (14, 1, 1, 84.99),
  (15, 9, 1, 45.00),
  (16, 10, 10, 4.25), (16, 8, 4, 9.50),
  (17, 3, 1, 229.00),
  (18, 6, 2, 189.00);
