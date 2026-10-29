import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import SqlSet
S = SqlSet("employees", ["employees", "departments"])
p = S.p

p("Employee count by department including empty ones", "M", "left-join", "List every department with its employee count, including departments with none (count 0).", ["Count a column from the employees side after a `LEFT JOIN`."],
  "SELECT d.name, COUNT(e.id) AS employees FROM departments d LEFT JOIN employees e ON e.department_id = d.id GROUP BY d.id, d.name;")
p("Salary spread per department", "M", "aggregate", "For each department with employees show the gap between its highest and lowest salary.", ["`MAX(salary) - MIN(salary)`."],
  "SELECT d.name, MAX(e.salary) - MIN(e.salary) AS spread FROM employees e JOIN departments d ON d.id = e.department_id GROUP BY d.id, d.name;")
p("Total team payroll per manager", "H", "recursive", "For each manager with reports, compute the total salary of everyone who reports to them directly or indirectly (not including the manager). Show first name and team payroll, highest first.", ["Recursive CTE listing (ancestor, descendant) pairs."],
  "WITH RECURSIVE tree(root, id) AS (SELECT manager_id, id FROM employees WHERE manager_id IS NOT NULL UNION ALL SELECT t.root, e.id FROM tree t JOIN employees e ON e.manager_id = t.id) SELECT m.first_name, SUM(e.salary) AS team_payroll FROM tree t JOIN employees m ON m.id = t.root JOIN employees e ON e.id = t.id GROUP BY m.id, m.first_name ORDER BY team_payroll DESC;", ordered=True)
p("Depth of each branch", "H", "recursive", "Report the maximum depth (number of management levels below the top) of the reporting tree as `max_depth`, where a top manager is depth 0.", ["Recursive CTE tracking depth, then `MAX`."],
  "WITH RECURSIVE t(id, depth) AS (SELECT id, 0 FROM employees WHERE manager_id IS NULL UNION ALL SELECT e.id, t.depth + 1 FROM employees e JOIN t ON e.manager_id = t.id) SELECT MAX(depth) AS max_depth FROM t;")
p("Salary percentile within department", "H", "window-functions", "For each employee with a department show the percentage rank (`PERCENT_RANK`) of their salary within the department rounded to 2 decimals. Order by department then salary.", ["`PERCENT_RANK() OVER (PARTITION BY department_id ORDER BY salary)`."],
  "SELECT department_id, first_name, salary, ROUND(PERCENT_RANK() OVER (PARTITION BY department_id ORDER BY salary), 2) AS pct_rank FROM employees WHERE department_id IS NOT NULL ORDER BY department_id, salary;", ordered=True)
p("Employees with the same title", "M", "self-join", "Find pairs of different employees with the same job title. List each pair once (first names alphabetical inside the pair) with the title.", ["Self-join on title with `a.id < b.id`."],
  "SELECT a.first_name AS employee_a, b.first_name AS employee_b, a.title FROM employees a JOIN employees b ON a.title = b.title AND a.id < b.id;")
p("Hire date gaps", "H", "window-functions", "Order employees by hire date and show, for each, the number of days since the previous hire. List the five largest gaps (ties by name).", ["`LAG(hire_date)`."],
  "WITH g AS (SELECT first_name, CAST(julianday(hire_date) - julianday(LAG(hire_date) OVER (ORDER BY hire_date)) AS INTEGER) AS gap FROM employees) SELECT first_name, gap FROM g WHERE gap IS NOT NULL ORDER BY gap DESC, first_name LIMIT 5;", ordered=True)
p("Lowest paid in each department", "M", "correlated-subquery", "List the lowest-paid employee of each department (first name, department id, salary).", ["Compare to `MIN(salary)` of the same department."],
  "SELECT e.first_name, e.department_id, e.salary FROM employees e WHERE e.department_id IS NOT NULL AND e.salary = (SELECT MIN(e2.salary) FROM employees e2 WHERE e2.department_id = e.department_id);")
p("Salary ranges per title level", "E", "case", "Count employees whose title contains `Head`, `Senior` or `Junior`, labelled by that keyword (use `other` for the rest).", ["`CASE WHEN title LIKE '%Head%' ...`."],
  "SELECT CASE WHEN title LIKE '%Head%' THEN 'Head' WHEN title LIKE '%Senior%' THEN 'Senior' WHEN title LIKE '%Junior%' THEN 'Junior' ELSE 'other' END AS level, COUNT(*) AS employees FROM employees GROUP BY level;")
p("Email username", "E", "strings", "Show each employee's email username (the part before `@`) in upper case.", ["`substr(email, 1, instr(email, '@') - 1)`."],
  "SELECT UPPER(substr(email, 1, instr(email, '@') - 1)) AS username FROM employees;")
p("Departments with above-average payroll", "M", "subquery", "List departments whose total payroll is above the average department payroll. Show name and payroll.", ["Aggregate in a CTE first."],
  "WITH p AS (SELECT department_id, SUM(salary) AS payroll FROM employees WHERE department_id IS NOT NULL GROUP BY department_id) SELECT d.name, p.payroll FROM p JOIN departments d ON d.id = p.department_id WHERE p.payroll > (SELECT AVG(payroll) FROM p);")
