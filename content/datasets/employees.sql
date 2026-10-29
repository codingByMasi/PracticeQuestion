CREATE TABLE departments (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  location TEXT NOT NULL
);

CREATE TABLE employees (
  id INTEGER PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT NOT NULL,
  department_id INTEGER REFERENCES departments(id),
  manager_id INTEGER REFERENCES employees(id),
  title TEXT NOT NULL,
  salary INTEGER NOT NULL,
  hire_date TEXT NOT NULL
);

INSERT INTO departments (id, name, location) VALUES
  (1, 'Engineering', 'Berlin'),
  (2, 'Sales', 'London'),
  (3, 'Marketing', 'London'),
  (4, 'Finance', 'New York'),
  (5, 'Research', 'Toronto');

INSERT INTO employees (id, first_name, last_name, email, department_id, manager_id, title, salary, hire_date) VALUES
  (1, 'Grace', 'Hopper', 'grace@codedrill.dev', 1, NULL, 'CTO', 185000, '2015-03-01'),
  (2, 'Alan', 'Turing', 'alan@codedrill.dev', 1, 1, 'Staff Engineer', 152000, '2016-07-15'),
  (3, 'Ada', 'Lovelace', 'ada@codedrill.dev', 1, 1, 'Senior Engineer', 138000, '2017-01-09'),
  (4, 'Linus', 'Torvalds', 'linus@codedrill.dev', 1, 2, 'Engineer', 112000, '2019-05-20'),
  (5, 'Margaret', 'Hamilton', 'margaret@codedrill.dev', 1, 2, 'Senior Engineer', 141000, '2018-02-12'),
  (6, 'Ken', 'Thompson', 'ken@codedrill.dev', 1, 3, 'Engineer', 109000, '2021-09-01'),
  (7, 'Barbara', 'Liskov', 'barbara@codedrill.dev', 1, 3, 'Junior Engineer', 84000, '2023-04-17'),
  (8, 'Steve', 'Jobs', 'steve@codedrill.dev', 2, NULL, 'Head of Sales', 160000, '2014-11-03'),
  (9, 'Mary', 'Barra', 'mary@codedrill.dev', 2, 8, 'Account Executive', 97000, '2018-06-25'),
  (10, 'Jack', 'Ma', 'jack@codedrill.dev', 2, 8, 'Account Executive', 93000, '2020-01-13'),
  (11, 'Indra', 'Nooyi', 'indra@codedrill.dev', 2, 8, 'Sales Associate', 68000, '2022-08-08'),
  (12, 'Sheryl', 'Sandberg', 'sheryl@codedrill.dev', 3, NULL, 'Head of Marketing', 150000, '2016-02-29'),
  (13, 'David', 'Ogilvy', 'david@codedrill.dev', 3, 12, 'Brand Manager', 99000, '2019-10-07'),
  (14, 'Mary', 'Wells', 'mwells@codedrill.dev', 3, 12, 'Content Writer', 72000, '2021-03-22'),
  (15, 'Warren', 'Buffett', 'warren@codedrill.dev', 4, NULL, 'CFO', 178000, '2013-05-06'),
  (16, 'Abigail', 'Johnson', 'abigail@codedrill.dev', 4, 15, 'Financial Analyst', 101000, '2017-12-11'),
  (17, 'Ray', 'Dalio', 'ray@codedrill.dev', 4, 15, 'Accountant', 88000, '2020-07-30'),
  (18, 'Tim', 'Berners-Lee', 'tim@codedrill.dev', NULL, 1, 'Contractor', 95000, '2024-02-05');
