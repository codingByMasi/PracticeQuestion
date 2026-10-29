import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import SqlSet

S = SqlSet("school", ["teachers", "courses", "students", "enrollments"])
p = S.p
GRADE = "CASE WHEN score >= 90 THEN 'A' WHEN score >= 80 THEN 'B' WHEN score >= 70 THEN 'C' WHEN score >= 60 THEN 'D' ELSE 'F' END"

p("Student roster", "E", "select", "List every student's name and grade level.", ["Select two columns."], "SELECT name, grade_level FROM students;")
p("Seniors", "E", "where", "List the names of students in grade level 12.", ["`grade_level = 12`."], "SELECT name FROM students WHERE grade_level = 12;")
p("Students from Lakeside or Hillview", "E", "where", "List students living in Lakeside or Hillview with their city.", ["`IN ('Lakeside', 'Hillview')`."], "SELECT name, city FROM students WHERE city IN ('Lakeside', 'Hillview');")
p("Heavy courses", "E", "where", "List courses worth 4 credits.", ["`credits = 4`."], "SELECT title, department FROM courses WHERE credits = 4;")
p("Courses without a teacher", "E", "null", "Find courses that currently have no teacher assigned.", ["`teacher_id IS NULL`."], "SELECT title FROM courses WHERE teacher_id IS NULL;")
p("Ungraded enrollments", "E", "null", "How many enrollments have no score yet?", ["Count rows where `score IS NULL`."], "SELECT COUNT(*) AS ungraded FROM enrollments WHERE score IS NULL;")
p("Perfect-ish scores", "E", "where", "List enrollments (student id, course id) with a score of at least 98.", ["Numeric comparison."], "SELECT student_id, course_id, score FROM enrollments WHERE score >= 98;")
p("Teachers by seniority", "E", "order-by", "List teachers with the year they were hired, longest-serving first (ties by name).", ["Sort by `hired_year` then `name`."],
  "SELECT name, hired_year FROM teachers ORDER BY hired_year, name;", ordered=True)
p("Youngest five students", "E", "order-by", "The five youngest students by birth date (most recent birth date first). Break ties by name.", ["`ORDER BY birth_date DESC, name`."],
  "SELECT name, birth_date FROM students ORDER BY birth_date DESC, name LIMIT 5;", ordered=True)
p("Department names", "E", "distinct", "List each department that offers courses, once.", ["`DISTINCT department`."], "SELECT DISTINCT department FROM courses;")
p("Total credits offered", "E", "aggregate", "What is the total number of credits across all courses?", ["`SUM(credits)`."], "SELECT SUM(credits) AS total_credits FROM courses;")
p("Score summary", "E", "aggregate", "Show the lowest, highest and average score among graded enrollments (average rounded to 2 decimals).", ["Aggregates skip NULL."],
  "SELECT MIN(score) AS lowest, MAX(score) AS highest, ROUND(AVG(score), 2) AS average FROM enrollments;")
p("Students per grade level", "E", "group-by", "Count students in each grade level.", ["`GROUP BY grade_level`."], "SELECT grade_level, COUNT(*) AS students FROM students GROUP BY grade_level;")
p("Courses per department", "E", "group-by", "How many courses does each department offer, and how many credits in total?", ["Two aggregates."],
  "SELECT department, COUNT(*) AS courses, SUM(credits) AS credits FROM courses GROUP BY department;")
p("Courses with their teachers", "E", "join", "List each course title with its teacher's name (courses without a teacher are omitted).", ["Inner join on `teacher_id`."],
  "SELECT c.title, t.name AS teacher FROM courses c JOIN teachers t ON t.id = c.teacher_id;")
p("All courses, teacher or TBA", "E", "left-join", "List every course with its teacher's name, or `TBA` if none.", ["`LEFT JOIN` and `COALESCE`."],
  "SELECT c.title, COALESCE(t.name, 'TBA') AS teacher FROM courses c LEFT JOIN teachers t ON t.id = c.teacher_id;")
p("Letter grades", "M", "case", "Convert each graded enrollment of student 1 into a letter grade: A (90+), B (80-89), C (70-79), D (60-69), F (below 60). Show course id, score and letter, ordered by course id.", ["`CASE WHEN score >= 90 ...`."],
  f"SELECT course_id, score, {GRADE} AS letter FROM enrollments WHERE student_id = 1 AND score IS NOT NULL ORDER BY course_id, semester;", ordered=True)
p("Grade distribution", "M", "case", "How many graded enrollments earned each letter grade (A 90+, B 80+, C 70+, D 60+, otherwise F)?", ["Group by the CASE expression."],
  f"SELECT {GRADE} AS letter, COUNT(*) AS n FROM enrollments WHERE score IS NOT NULL GROUP BY letter;")
p("Average score per course", "M", "join", "For each course with graded enrollments show its title and average score rounded to 1 decimal. Highest first (ties by title).", ["Join and group."],
  "SELECT c.title, ROUND(AVG(e.score), 1) AS avg_score FROM enrollments e JOIN courses c ON c.id = e.course_id GROUP BY c.id, c.title ORDER BY avg_score DESC, c.title;", ordered=True)
p("Class sizes", "M", "join", "How many enrollments does each course have? Show title and count, largest first (ties by title).", ["Count enrollment rows per course."],
  "SELECT c.title, COUNT(*) AS enrolled FROM enrollments e JOIN courses c ON c.id = e.course_id GROUP BY c.id, c.title ORDER BY enrolled DESC, c.title;", ordered=True)
p("Students without enrollments", "M", "left-join", "Count students with fewer than 4 enrollments (zero counts).", ["Left join and `HAVING COUNT(e.course_id) < 4`."],
  "SELECT COUNT(*) AS students FROM (SELECT s.id FROM students s LEFT JOIN enrollments e ON e.student_id = s.id GROUP BY s.id HAVING COUNT(e.course_id) < 4);")
p("Student grade point average", "M", "join", "Compute each student's average score (graded enrollments), rounded to 1 decimal. Show the top five students; break ties by name.", ["Group by student."],
  "SELECT s.name, ROUND(AVG(e.score), 1) AS avg_score FROM students s JOIN enrollments e ON e.student_id = s.id GROUP BY s.id, s.name ORDER BY avg_score DESC, s.name LIMIT 5;", ordered=True)
p("Teacher workload", "M", "join", "For each teacher show the number of courses they teach and the total credits. Include teachers with no courses (zero).", ["`LEFT JOIN` and `COALESCE(SUM(...), 0)`."],
  "SELECT t.name, COUNT(c.id) AS courses, COALESCE(SUM(c.credits), 0) AS credits FROM teachers t LEFT JOIN courses c ON c.teacher_id = t.id GROUP BY t.id, t.name;")
p("Teachers across departments", "M", "multi-join", "Show the average score of students in each teacher's courses. Show teacher name and average rounded to 1 decimal.", ["Join teachers, courses, enrollments."],
  "SELECT t.name, ROUND(AVG(e.score), 1) AS avg_score FROM teachers t JOIN courses c ON c.teacher_id = t.id JOIN enrollments e ON e.course_id = c.id GROUP BY t.id, t.name;")
p("Cross-department students", "M", "having", "List students enrolled in courses from at least four different departments.", ["`COUNT(DISTINCT c.department)`."],
  "SELECT s.name, COUNT(DISTINCT c.department) AS departments FROM students s JOIN enrollments e ON e.student_id = s.id JOIN courses c ON c.id = e.course_id GROUP BY s.id, s.name HAVING COUNT(DISTINCT c.department) >= 4;")
p("Semester comparison", "M", "group-by", "Average score per semester, rounded to 2 decimals.", ["`GROUP BY semester`."],
  "SELECT semester, ROUND(AVG(score), 2) AS avg_score FROM enrollments GROUP BY semester;")
p("Students above the class average", "M", "subquery", "List students whose average score exceeds the average of all scores. Show name and average rounded to 1 decimal.", ["Compare `AVG(score)` per student with a scalar subquery."],
  "SELECT s.name, ROUND(AVG(e.score), 1) AS avg_score FROM students s JOIN enrollments e ON e.student_id = s.id GROUP BY s.id, s.name HAVING AVG(e.score) > (SELECT AVG(score) FROM enrollments);")
p("Honor roll", "M", "having", "List students who have at least three graded enrollments and an average of at least 85. Show name, count and average rounded to 1 decimal.", ["Two aggregate conditions in `HAVING`."],
  "SELECT s.name, COUNT(e.score) AS graded, ROUND(AVG(e.score), 1) AS avg_score FROM students s JOIN enrollments e ON e.student_id = s.id GROUP BY s.id, s.name HAVING COUNT(e.score) >= 3 AND AVG(e.score) >= 85;")
p("Failing grades by department", "M", "group-by", "Count scores below 60 per course department. Show departments with at least one.", ["Filter in `WHERE`, join courses."],
  "SELECT c.department, COUNT(*) AS failing FROM enrollments e JOIN courses c ON c.id = e.course_id WHERE e.score < 60 GROUP BY c.department;")
p("Age of students", "M", "dates", "Show each student's age in whole years as of 2024-09-01. List the five oldest (ties by name).", ["Days difference / 365.25."],
  "SELECT name, CAST((julianday('2024-09-01') - julianday(birth_date)) / 365.25 AS INTEGER) AS age FROM students ORDER BY age DESC, name LIMIT 5;", ordered=True)
p("Birthdays by month", "M", "dates", "How many students were born in each calendar month (01-12)? Show the month number and count.", ["`strftime('%m', birth_date)`."],
  "SELECT strftime('%m', birth_date) AS month, COUNT(*) AS students FROM students GROUP BY month;")
p("Top score per course", "M", "correlated-subquery", "For each course show the highest score and the student id who earned it (all students if tied).", ["Compare to `MAX(score)` of the course."],
  "SELECT e.course_id, e.student_id, e.score FROM enrollments e WHERE e.score = (SELECT MAX(e2.score) FROM enrollments e2 WHERE e2.course_id = e.course_id);")
p("Best student per department", "H", "ranking", "For each course department find the student with the highest average score in that department's courses. Show department, student name and average rounded to 1 decimal. Break ties by name.", ["Aggregate by department and student, then `ROW_NUMBER`."],
  "WITH a AS (SELECT c.department, s.name, AVG(e.score) AS avg_score FROM enrollments e JOIN courses c ON c.id = e.course_id JOIN students s ON s.id = e.student_id GROUP BY c.department, s.id), r AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY department ORDER BY avg_score DESC, name) AS rn FROM a) SELECT department, name, ROUND(avg_score, 1) AS avg_score FROM r WHERE rn = 1;")
p("Class rank within grade level", "H", "ranking", "Rank students within their grade level by average score (1 = best) using `RANK()`. Show grade level, rank, name and average rounded to 1 decimal. Keep ranks 1 to 3, ordered by grade level, rank, name.", ["Average per student, then `RANK() OVER (PARTITION BY grade_level ...)`."],
  "WITH a AS (SELECT s.grade_level, s.name, AVG(e.score) AS avg_score FROM students s JOIN enrollments e ON e.student_id = s.id GROUP BY s.id), r AS (SELECT *, RANK() OVER (PARTITION BY grade_level ORDER BY avg_score DESC) AS rk FROM a) SELECT grade_level, rk, name, ROUND(avg_score, 1) AS avg_score FROM r WHERE rk <= 3 ORDER BY grade_level, rk, name;", ordered=True)
p("Score percentile per course", "H", "window-functions", "For each enrollment in course 1 with a score, show student id, score and `PERCENT_RANK` among course 1 scores rounded to 3 decimals. Order by score, student id.", ["`PERCENT_RANK() OVER (ORDER BY score)`."],
  "SELECT student_id, score, ROUND(PERCENT_RANK() OVER (ORDER BY score), 3) AS pct_rank FROM enrollments WHERE course_id = 1 AND score IS NOT NULL ORDER BY score, student_id;", ordered=True)
p("Distance from course average", "H", "window-functions", "For every graded enrollment of course 2 show student id, score and the difference from that course's average score (rounded to 1 decimal). Order by student id and semester.", ["`AVG(score) OVER ()`."],
  "SELECT student_id, semester, score, ROUND(score - AVG(score) OVER (), 1) AS vs_avg FROM enrollments WHERE course_id = 2 AND score IS NOT NULL ORDER BY student_id, semester;", ordered=True)
p("Running enrollment per course", "H", "running-total", "For course 3, list enrollments ordered by semester and student id with a running count of enrolled students.", ["`COUNT(*) OVER (ORDER BY ...)` with a unique tie-breaker."],
  "SELECT semester, student_id, ROW_NUMBER() OVER (ORDER BY semester, student_id) AS running_count FROM enrollments WHERE course_id = 3 ORDER BY semester, student_id;", ordered=True)
p("Students taking all three Math courses", "H", "having", "List students enrolled (any semester) in at least three different Math courses.", ["`COUNT(DISTINCT c.id)` for Math."],
  "SELECT s.name, COUNT(DISTINCT c.id) AS math_courses FROM students s JOIN enrollments e ON e.student_id = s.id JOIN courses c ON c.id = e.course_id WHERE c.department = 'Math' GROUP BY s.id, s.name HAVING COUNT(DISTINCT c.id) >= 3;")
p("Teacher with the highest average", "M", "subquery", "Which teacher's students score the highest on average? Show the teacher and the average rounded to 2 decimals. No tie.", ["Group, sort, limit 1."],
  "SELECT t.name, ROUND(AVG(e.score), 2) AS avg_score FROM teachers t JOIN courses c ON c.teacher_id = t.id JOIN enrollments e ON e.course_id = c.id GROUP BY t.id, t.name ORDER BY avg_score DESC LIMIT 1;")
p("Credit load per student", "H", "expressions", "Compute each student's total credits across their distinct course enrollments (a course counted once even if taken twice). List the five highest, ties by name.", ["Deduplicate student-course pairs first."],
  "SELECT s.name, SUM(c.credits) AS credits FROM students s JOIN (SELECT DISTINCT student_id, course_id FROM enrollments) x ON x.student_id = s.id JOIN courses c ON c.id = x.course_id GROUP BY s.id, s.name ORDER BY credits DESC, s.name LIMIT 5;", ordered=True)
p("Pivot grades by semester", "H", "pivot", "For each department show the average score in `2023-fall` and `2024-spring` as two columns rounded to 1 decimal.", ["Conditional `AVG(CASE WHEN ... THEN score END)`."],
  "SELECT c.department, ROUND(AVG(CASE WHEN e.semester = '2023-fall' THEN e.score END), 1) AS fall, ROUND(AVG(CASE WHEN e.semester = '2024-spring' THEN e.score END), 1) AS spring FROM enrollments e JOIN courses c ON c.id = e.course_id GROUP BY c.department;")
p("Teacher hire cohorts", "E", "group-by", "How many teachers were hired in each decade (2000s, 2010s, 2020s)? Show the decade start year and count.", ["`hired_year / 10 * 10`."],
  "SELECT hired_year / 10 * 10 AS decade, COUNT(*) AS teachers FROM teachers GROUP BY decade;")
p("Update a score", "M", "dml", "A teacher re-graded: add 5 points (capped at 100) to every score in course 1 using `MIN(100, score + 5)`, then show the new average for course 1 rounded to 2 decimals.", ["`UPDATE enrollments SET score = MIN(100, score + 5) WHERE course_id = 1`."],
  "UPDATE enrollments SET score = MIN(100, score + 5) WHERE course_id = 1; SELECT ROUND(AVG(score), 2) AS new_avg FROM enrollments WHERE course_id = 1;")
p("Assign the orphan course", "M", "dml", "Assign teacher 5 to every course that has no teacher, then list the courses taught by teacher 5.", ["`UPDATE courses SET teacher_id = 5 WHERE teacher_id IS NULL`."],
  "UPDATE courses SET teacher_id = 5 WHERE teacher_id IS NULL; SELECT title FROM courses WHERE teacher_id = 5;")
p("Name length buckets", "E", "strings", "How many students have a name shorter than 12 characters, from 12 to 15, and longer than 15? Show a `bucket` label (`short`, `medium`, `long`) and the count.", ["`LENGTH(name)` in a `CASE`."],
  "SELECT CASE WHEN LENGTH(name) < 12 THEN 'short' WHEN LENGTH(name) <= 15 THEN 'medium' ELSE 'long' END AS bucket, COUNT(*) AS students FROM students GROUP BY bucket;")
p("Teachers and students directory", "M", "set-ops", "Create one combined directory with columns `name` and `role` (`teacher` or `student`) for all teachers and all students in grade level 12.", ["`UNION ALL` with a literal role column."],
  "SELECT name, 'teacher' AS role FROM teachers UNION ALL SELECT name, 'student' FROM students WHERE grade_level = 12;")
p("Distinct classmates of student 1", "H", "self-join", "List students who share at least one course in the same semester with student 1 (excluding student 1). Show student id and how many shared course-semesters.", ["Self-join enrollments on course and semester."],
  "SELECT b.student_id, COUNT(*) AS shared FROM enrollments a JOIN enrollments b ON a.course_id = b.course_id AND a.semester = b.semester AND b.student_id <> a.student_id WHERE a.student_id = 1 GROUP BY b.student_id;")
p("Consecutive high scorers", "H", "gaps-islands", "Look at student 2's graded enrollments in order of semester then course id. Mark each row whether the score is at least 80 and report the longest run of consecutive rows that are at least 80 as `longest_run`.", ["Number the rows and the 'good' rows separately; difference identifies runs."],
  "WITH r AS (SELECT score >= 80 AS good, ROW_NUMBER() OVER (ORDER BY semester, course_id) AS rn FROM enrollments WHERE student_id = 2 AND score IS NOT NULL), g AS (SELECT rn - ROW_NUMBER() OVER (ORDER BY rn) AS grp, rn FROM r WHERE good = 1) SELECT COALESCE(MAX(c), 0) AS longest_run FROM (SELECT COUNT(*) AS c FROM g GROUP BY grp);")
p("Median score", "H", "window-functions", "Compute the median score of all graded enrollments (average the two middle values if the count is even).", ["Number the sorted scores and pick the middle row(s)."],
  "WITH r AS (SELECT score, ROW_NUMBER() OVER (ORDER BY score) AS rn, COUNT(*) OVER () AS n FROM enrollments WHERE score IS NOT NULL) SELECT AVG(score) AS median_score FROM r WHERE rn IN ((n + 1) / 2, (n + 2) / 2);")
