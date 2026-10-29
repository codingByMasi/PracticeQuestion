import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import SqlSet

S = SqlSet("employees", ["employees", "departments"])
p = S.p

p("Employee contact list", "E", "select", "List every employee's first name, last name and email address.",
  ["Name the three columns you want after `SELECT`."], "SELECT first_name, last_name, email FROM employees;")
p("Sales team roster", "E", "where", "List the first and last names of everyone in the Sales department (`department_id = 2`).",
  ["Filter with `WHERE department_id = 2`."], "SELECT first_name, last_name FROM employees WHERE department_id = 2;")
p("Outside Engineering", "E", "where", "Find employees who are **not** in the Engineering department (`department_id = 1`) but do belong to some department.",
  ["`<>` means not equal, but NULL never compares as unequal.", "Add `department_id IS NOT NULL`."],
  "SELECT first_name, last_name, department_id FROM employees WHERE department_id <> 1 AND department_id IS NOT NULL;",
  why="A NULL department makes `department_id <> 1` unknown, so those rows drop out anyway; the explicit test just documents the intent.")
p("Mid-range salaries", "E", "where", "Return employees earning between 90,000 and 110,000 inclusive.",
  ["`BETWEEN a AND b` includes both ends."], "SELECT first_name, last_name, salary FROM employees WHERE salary BETWEEN 90000 AND 110000;")
p("Engineers by title", "E", "like", "Find employees whose title contains the word `Engineer` anywhere (for example Staff Engineer or Junior Engineer).",
  ["`LIKE '%text%'` matches the text anywhere."], "SELECT first_name, title FROM employees WHERE title LIKE '%Engineer%';")
p("First names starting with M", "E", "like", "List the first names that start with the letter M.",
  ["`LIKE 'M%'` matches a prefix."], "SELECT first_name, last_name FROM employees WHERE first_name LIKE 'M%';")
p("Hired before 2017", "E", "where", "List employees hired before 2017-01-01, with their hire date.",
  ["ISO date strings compare chronologically."], "SELECT first_name, hire_date FROM employees WHERE hire_date < '2017-01-01';")
p("Last names A to Z", "E", "order-by", "List the last names of all employees in alphabetical order.",
  ["`ORDER BY last_name`."], "SELECT last_name FROM employees ORDER BY last_name;", ordered=True)
p("Three newest hires", "E", "order-by", "Who are the three most recently hired employees? Newest first.",
  ["Sort by `hire_date DESC` and `LIMIT 3`."], "SELECT first_name, hire_date FROM employees ORDER BY hire_date DESC LIMIT 3;", ordered=True)
p("Distinct job titles", "E", "distinct", "List each job title that appears among employees, once.",
  ["`SELECT DISTINCT` removes duplicate rows."], "SELECT DISTINCT title FROM employees;")
p("Monthly pay", "E", "expressions", "Show each employee's first name and monthly salary (annual salary divided by 12), rounded to 2 decimals.",
  ["`ROUND(x, 2)`.", "Use `salary / 12.0` to avoid integer division."],
  "SELECT first_name, ROUND(salary / 12.0, 2) AS monthly_salary FROM employees;")
p("Pay bands", "E", "case", "Label each employee's pay band: `low` below 90,000, `mid` from 90,000 up to (not including) 130,000, and `high` from 130,000. Show first name and band.",
  ["`CASE WHEN ... THEN ... ELSE ... END` evaluates conditions in order."],
  "SELECT first_name, CASE WHEN salary < 90000 THEN 'low' WHEN salary < 130000 THEN 'mid' ELSE 'high' END AS band FROM employees;")
p("Total payroll", "E", "aggregate", "What is the total of all salaries?",
  ["`SUM(salary)`."], "SELECT SUM(salary) AS total_payroll FROM employees;")
p("Average pay by department", "E", "group-by", "For each department name, show the average salary rounded to 2 decimals. Include only departments that have employees.",
  ["Join to `departments` for the name.", "Group by department."],
  "SELECT d.name AS department, ROUND(AVG(e.salary), 2) AS avg_salary FROM employees e JOIN departments d ON d.id = e.department_id GROUP BY d.id, d.name;")
p("Titles in Engineering", "E", "group-by", "In Engineering (`department_id = 1`), how many employees hold each title?",
  ["Filter first, then `GROUP BY title`."], "SELECT title, COUNT(*) AS n FROM employees WHERE department_id = 1 GROUP BY title;")
p("Payroll ranking of departments", "M", "group-by", "Rank departments by total salary, highest first. Show the department name and total.",
  ["Sum salaries per department and sort by the sum."],
  "SELECT d.name AS department, SUM(e.salary) AS payroll FROM employees e JOIN departments d ON d.id = e.department_id GROUP BY d.id, d.name ORDER BY payroll DESC;", ordered=True)
p("Staff per office city", "M", "join", "How many employees work in each department location (city)? Show the city and the count.",
  ["Group by `d.location`; two departments can share a city."],
  "SELECT d.location, COUNT(*) AS staff FROM employees e JOIN departments d ON d.id = e.department_id GROUP BY d.location;")
p("People who manage others", "M", "subquery", "List employees who have at least one direct report.",
  ["`id IN (SELECT manager_id FROM employees WHERE manager_id IS NOT NULL)`."],
  "SELECT first_name, last_name FROM employees WHERE id IN (SELECT manager_id FROM employees WHERE manager_id IS NOT NULL);")
p("Individual contributors", "M", "exists", "List employees who have **no** direct reports.",
  ["`NOT EXISTS` with a correlated subquery is NULL-safe."],
  "SELECT e.first_name, e.last_name FROM employees e WHERE NOT EXISTS (SELECT 1 FROM employees r WHERE r.manager_id = e.id);")
p("Employee and manager full names", "M", "self-join", "For employees with a manager, show the employee's full name and the manager's full name (first and last separated by a space).",
  ["Concatenate with `||`.", "Join the table to itself."],
  "SELECT e.first_name || ' ' || e.last_name AS employee, m.first_name || ' ' || m.last_name AS manager FROM employees e JOIN employees m ON m.id = e.manager_id;")
p("Direct report counts", "M", "group-by", "For each manager, show their first name and how many direct reports they have.",
  ["Group the employees by `manager_id`, then join back for the name."],
  "SELECT m.first_name, COUNT(*) AS reports FROM employees e JOIN employees m ON m.id = e.manager_id GROUP BY m.id, m.first_name;")
p("Above their own department average", "M", "correlated-subquery", "List employees who earn more than the average salary of their own department. Show first name, department id and salary.",
  ["Compare with a correlated `(SELECT AVG(...) WHERE department_id = e.department_id)`."],
  "SELECT e.first_name, e.department_id, e.salary FROM employees e WHERE e.salary > (SELECT AVG(e2.salary) FROM employees e2 WHERE e2.department_id = e.department_id);")
p("Second highest salary", "M", "subquery", "What is the second highest distinct salary?",
  ["Find the maximum salary strictly below the overall maximum."],
  "SELECT MAX(salary) AS second_highest FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);")
p("Hires per year", "M", "dates", "How many people were hired in each calendar year? Show year and count, oldest year first.",
  ["`strftime('%Y', hire_date)` extracts the year."],
  "SELECT strftime('%Y', hire_date) AS year, COUNT(*) AS hires FROM employees GROUP BY year ORDER BY year;", ordered=True)
p("Whole years of service", "M", "dates", "For each employee show first name and completed years of service as of 2024-06-30 (round down).",
  ["`julianday(a) - julianday(b)` gives days.", "Divide by 365.25 and `CAST(... AS INTEGER)`."],
  "SELECT first_name, CAST((julianday('2024-06-30') - julianday(hire_date)) / 365.25 AS INTEGER) AS years FROM employees;")
p("Pay as a share of manager pay", "M", "self-join", "For every employee who has a manager, show their first name and their salary as a percentage of their manager's salary, rounded to 1 decimal.",
  ["Join employees to their managers and divide.", "Multiply by 100.0 to get a percentage."],
  "SELECT e.first_name, ROUND(100.0 * e.salary / m.salary, 1) AS pct_of_manager FROM employees e JOIN employees m ON m.id = e.manager_id;")
p("Gap to the department head", "M", "join", "For each employee with a department, show how much less they earn than the head of their department (the department member whose `manager_id` is NULL). Exclude the heads themselves. Show first name and the gap.",
  ["Join employees to employees of the same department where `manager_id IS NULL`."],
  "SELECT e.first_name, h.salary - e.salary AS gap FROM employees e JOIN employees h ON h.department_id = e.department_id AND h.manager_id IS NULL WHERE e.manager_id IS NOT NULL;")
p("Big departments", "E", "having", "Which departments have more than three employees? Show the department name and headcount.",
  ["`HAVING COUNT(*) > 3`."],
  "SELECT d.name, COUNT(*) AS headcount FROM employees e JOIN departments d ON d.id = e.department_id GROUP BY d.id, d.name HAVING COUNT(*) > 3;")
p("People and places in one list", "M", "set-ops", "Produce a single list of text values containing every employee's first name and every department name. Show the column once and keep duplicates out.",
  ["`UNION` removes duplicates; `UNION ALL` keeps them."],
  "SELECT first_name AS label FROM employees UNION SELECT name FROM departments;")
p("Raise Engineering by 10 percent", "M", "dml", "Give every Engineering employee (`department_id = 1`) a 10% raise with an `UPDATE`, then report the new total payroll of the whole company rounded to 2 decimals. (Each run starts from a fresh copy of the data.)",
  ["Run the `UPDATE` first, then a `SELECT` in the same script."],
  "UPDATE employees SET salary = salary * 1.10 WHERE department_id = 1; SELECT ROUND(SUM(salary), 2) AS total_payroll FROM employees;")
p("Running payroll by hire date", "M", "running-total", "In order of hire date, show each employee's first name, hire date and the running total of salaries of everyone hired up to and including them.",
  ["`SUM(salary) OVER (ORDER BY hire_date)`."],
  "SELECT first_name, hire_date, SUM(salary) OVER (ORDER BY hire_date) AS running_payroll FROM employees ORDER BY hire_date;", ordered=True)
p("Salary quartiles", "H", "window-functions", "Split employees into four salary quartiles with `NTILE(4)` (1 = lowest paid). Show first name, salary and quartile.",
  ["`NTILE(4) OVER (ORDER BY salary)`."],
  "SELECT first_name, salary, NTILE(4) OVER (ORDER BY salary) AS quartile FROM employees ORDER BY salary;", ordered=True)
p("Top two earners per department", "H", "ranking", "For each department, list its two highest-paid employees with their rank within the department (1 or 2). Show department id, first name, salary and rank.",
  ["`ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC)` in a CTE, then filter."],
  "WITH ranked AS (SELECT department_id, first_name, salary, ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rnk FROM employees WHERE department_id IS NOT NULL) SELECT department_id, first_name, salary, rnk FROM ranked WHERE rnk <= 2;")
p("Pay change versus previous hire", "H", "window-functions", "Ordering employees by hire date, show each person's first name, salary, and the difference from the salary of the person hired just before them (NULL for the first hire).",
  ["`LAG(salary) OVER (ORDER BY hire_date)`."],
  "SELECT first_name, salary, salary - LAG(salary) OVER (ORDER BY hire_date) AS diff_from_previous FROM employees ORDER BY hire_date;", ordered=True)
p("Org chart levels", "H", "recursive", "Compute each employee's level in the reporting tree: top managers (no manager) are level 1, their direct reports level 2, and so on. Show first name and level.",
  ["A recursive CTE starts from employees with `manager_id IS NULL` and joins children each step."],
  "WITH RECURSIVE tree(id, first_name, level) AS (SELECT id, first_name, 1 FROM employees WHERE manager_id IS NULL UNION ALL SELECT e.id, e.first_name, t.level + 1 FROM employees e JOIN tree t ON e.manager_id = t.id) SELECT first_name, level FROM tree;")
p("Everyone under Grace", "H", "recursive", "List all employees who report to Grace Hopper (id 1), directly or indirectly. Show first name only.",
  ["Start the recursion at Grace's direct reports."],
  "WITH RECURSIVE under_grace(id, first_name) AS (SELECT id, first_name FROM employees WHERE manager_id = 1 UNION ALL SELECT e.id, e.first_name FROM employees e JOIN under_grace u ON e.manager_id = u.id) SELECT first_name FROM under_grace;")
p("Chain of command for Barbara", "H", "recursive", "List Barbara Liskov's management chain: her manager, that manager's manager, and so on up to the top. Show first name and distance (1 = direct manager).",
  ["Recurse upward by joining `employees.id = chain.manager_id`."],
  "WITH RECURSIVE chain(id, manager_id, first_name, dist) AS (SELECT m.id, m.manager_id, m.first_name, 1 FROM employees b JOIN employees m ON m.id = b.manager_id WHERE b.first_name = 'Barbara' UNION ALL SELECT m.id, m.manager_id, m.first_name, c.dist + 1 FROM chain c JOIN employees m ON m.id = c.manager_id) SELECT first_name, dist FROM chain ORDER BY dist;", ordered=True)
p("Cumulative headcount by hire year", "H", "window-functions", "For each hire year show the number hired that year and the cumulative number of employees hired up to that year.",
  ["Aggregate by year in a CTE, then apply a running `SUM` window over the counts."],
  "WITH yearly AS (SELECT strftime('%Y', hire_date) AS year, COUNT(*) AS hires FROM employees GROUP BY year) SELECT year, hires, SUM(hires) OVER (ORDER BY year) AS cumulative FROM yearly ORDER BY year;", ordered=True)
p("Largest team by direct reports", "M", "subquery", "Which manager has the most direct reports? Show their first name and the count. (There is no tie.)",
  ["Group by manager, order by count descending, take one."],
  "SELECT m.first_name, COUNT(*) AS reports FROM employees e JOIN employees m ON m.id = e.manager_id GROUP BY m.id, m.first_name ORDER BY reports DESC LIMIT 1;")
p("Department share of payroll", "H", "window-functions", "For each department with employees, show its payroll and its share of total company payroll as a percentage rounded to 1 decimal. Employees without a department count in the company total.",
  ["Total payroll can be a scalar subquery over all employees."],
  "SELECT d.name AS department, SUM(e.salary) AS payroll, ROUND(100.0 * SUM(e.salary) / (SELECT SUM(salary) FROM employees), 1) AS pct FROM employees e JOIN departments d ON d.id = e.department_id GROUP BY d.id, d.name;")
