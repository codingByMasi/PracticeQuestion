import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import SqlSet

S = SqlSet("library", ["authors", "books", "members", "loans"])
p = S.p
OVERDUE = "(l.return_date > l.due_date OR (l.return_date IS NULL AND l.due_date < '2024-07-01'))"

p("Book catalogue", "E", "select", "List the title, genre and number of pages of every book.", ["Select three columns."], "SELECT title, genre, pages FROM books;")
p("Mystery shelf", "E", "where", "List the titles of Mystery books.", ["`genre = 'Mystery'`."], "SELECT title FROM books WHERE genre = 'Mystery';")
p("Thick books", "E", "where", "List books with more than 600 pages, with their page counts.", ["Numeric comparison."], "SELECT title, pages FROM books WHERE pages > 600;")
p("Rare copies", "E", "where", "Find books of which the library owns exactly one copy.", ["`copies = 1`."], "SELECT title FROM books WHERE copies = 1;")
p("Published in the 1980s", "E", "where", "List books published from 1980 to 1989 inclusive.", ["`BETWEEN`."], "SELECT title, published_year FROM books WHERE published_year BETWEEN 1980 AND 1989;")
p("Premium members in Lyon", "E", "where", "List the names of premium-tier members who live in Lyon.", ["Two conditions with `AND`."], "SELECT name FROM members WHERE tier = 'premium' AND city = 'Lyon';")
p("Titles containing Winter", "E", "like", "Find books with `Winter` in the title.", ["`LIKE '%Winter%'`."], "SELECT title FROM books WHERE title LIKE '%Winter%';")
p("Books not yet returned", "E", "null", "List loan ids that have not been returned (no return date).", ["`return_date IS NULL`."], "SELECT id, book_id, member_id FROM loans WHERE return_date IS NULL;")
p("Oldest authors", "E", "order-by", "List the five authors born earliest, with birth year, earliest first.", ["`ORDER BY birth_year LIMIT 5`; years may tie, so also order by name."],
  "SELECT name, birth_year FROM authors ORDER BY birth_year, name LIMIT 5;", ordered=True)
p("Longest books", "E", "order-by", "The 5 longest books by page count, longest first (break ties by title).", ["Sort by pages descending, then title."],
  "SELECT title, pages FROM books ORDER BY pages DESC, title LIMIT 5;", ordered=True)
p("Author countries", "E", "distinct", "List each country that has at least one author.", ["`DISTINCT`."], "SELECT DISTINCT country FROM authors;")
p("Number of members", "E", "aggregate", "How many members does the library have?", ["`COUNT(*)`."], "SELECT COUNT(*) AS members FROM members;")
p("Total copies owned", "E", "aggregate", "How many physical copies does the library own in total?", ["`SUM(copies)`."], "SELECT SUM(copies) AS total_copies FROM books;")
p("Page statistics", "E", "aggregate", "Show the minimum, maximum and average page count across all books (average rounded to 1 decimal).", ["Three aggregates."],
  "SELECT MIN(pages) AS shortest, MAX(pages) AS longest, ROUND(AVG(pages), 1) AS average FROM books;")
p("Books per genre", "E", "group-by", "Count books per genre.", ["`GROUP BY genre`."], "SELECT genre, COUNT(*) AS books FROM books GROUP BY genre;")
p("Members per tier", "E", "group-by", "Count members per tier.", ["`GROUP BY tier`."], "SELECT tier, COUNT(*) AS members FROM members GROUP BY tier;")
p("Books and their authors", "E", "join", "List each book title with its author's name.", ["Join `books` to `authors`."],
  "SELECT b.title, a.name AS author FROM books b JOIN authors a ON a.id = b.author_id;")
p("Loans with member names", "E", "join", "For loans made in January 2024, show the loan id, member name and loan date.", ["Join `loans` to `members`, filter on the date."],
  "SELECT l.id, m.name, l.loan_date FROM loans l JOIN members m ON m.id = l.member_id WHERE l.loan_date >= '2024-01-01' AND l.loan_date < '2024-02-01';")
p("Genres with at least eight books", "E", "having", "Which genres have at least 8 books?", ["`HAVING COUNT(*) >= 8`."],
  "SELECT genre, COUNT(*) AS books FROM books GROUP BY genre HAVING COUNT(*) >= 8;")
p("Authors by number of books", "M", "group-by", "Show each author who has books and how many they wrote, most first (ties by name).", ["Join, group, sort."],
  "SELECT a.name, COUNT(*) AS books FROM authors a JOIN books b ON b.author_id = a.id GROUP BY a.id, a.name ORDER BY books DESC, a.name;", ordered=True)
p("Authors without books", "M", "left-join", "List authors who have no books in the catalogue.", ["Anti-join with `LEFT JOIN`."],
  "SELECT a.name FROM authors a LEFT JOIN books b ON b.author_id = a.id WHERE b.id IS NULL;")
p("Least borrowed books", "M", "left-join", "List books with fewer than 3 loans, including books never loaned. Show title and loan count.", ["`LEFT JOIN` and count a column of the right table.", "Filter groups with `HAVING`."],
  "SELECT b.title, COUNT(l.id) AS loans FROM books b LEFT JOIN loans l ON l.book_id = b.id GROUP BY b.id, b.title HAVING COUNT(l.id) < 3;")
p("Most borrowed books", "M", "join", "The five books with the most loans (title and loan count). Break ties by title.", ["Group loans by book."],
  "SELECT b.title, COUNT(*) AS loans FROM loans l JOIN books b ON b.id = l.book_id GROUP BY b.id, b.title ORDER BY loans DESC, b.title LIMIT 5;", ordered=True)
p("Loans per genre", "M", "multi-join", "How many loans did each genre receive? Most popular first.", ["Join loans to books."],
  "SELECT b.genre, COUNT(*) AS loans FROM loans l JOIN books b ON b.id = l.book_id GROUP BY b.genre ORDER BY loans DESC;", ordered=True)
p("Active borrowers", "M", "having", "List members who borrowed at least 10 books. Show name and loan count.", ["`HAVING COUNT(*) >= 10`."],
  "SELECT m.name, COUNT(*) AS loans FROM members m JOIN loans l ON l.member_id = m.id GROUP BY m.id, m.name HAVING COUNT(*) >= 10;")
p("Occasional members", "M", "left-join", "List members who borrowed fewer than 6 books in total (zero counts). Show name and loan count.", ["`LEFT JOIN` then `HAVING COUNT(l.id) < 6`."],
  "SELECT m.name, COUNT(l.id) AS loans FROM members m LEFT JOIN loans l ON l.member_id = m.id GROUP BY m.id, m.name HAVING COUNT(l.id) < 6;")
p("Loan duration", "M", "dates", "For returned loans show loan id and the number of days kept (return date minus loan date). Show the 5 longest, ties by loan id.", ["`julianday(return_date) - julianday(loan_date)`."],
  "SELECT id, CAST(julianday(return_date) - julianday(loan_date) AS INTEGER) AS days_kept FROM loans WHERE return_date IS NOT NULL ORDER BY days_kept DESC, id LIMIT 5;", ordered=True)
p("Late returns", "M", "dates", "Count loans returned after their due date.", ["Compare `return_date` to `due_date` (NULL returns excluded automatically)."],
  "SELECT COUNT(*) AS late_returns FROM loans WHERE return_date > due_date;")
p("Late return rate by tier", "M", "join", "For each member tier show the percentage of returned loans that were late, rounded to 1 decimal.", ["Average a 0/1 flag over returned loans."],
  "SELECT m.tier, ROUND(100.0 * SUM(CASE WHEN l.return_date > l.due_date THEN 1 ELSE 0 END) / COUNT(*), 1) AS late_pct FROM loans l JOIN members m ON m.id = l.member_id WHERE l.return_date IS NOT NULL GROUP BY m.tier;")
p("Currently overdue", "M", "dates", "As of 2024-07-01, list loans that are still out and past their due date. Show loan id and days overdue.", ["Unreturned and `due_date < '2024-07-01'`."],
  "SELECT id, CAST(julianday('2024-07-01') - julianday(due_date) AS INTEGER) AS days_overdue FROM loans WHERE return_date IS NULL AND due_date < '2024-07-01';")
p("Fines owed", "M", "expressions", "Charge 0.25 per day late for returned loans. List members with their total fine, rounded to 2 decimals, only members who owe something. Largest first (ties by name).", ["Sum the late days per member."],
  "SELECT m.name, ROUND(SUM((julianday(l.return_date) - julianday(l.due_date)) * 0.25), 2) AS fine FROM loans l JOIN members m ON m.id = l.member_id WHERE l.return_date > l.due_date GROUP BY m.id, m.name ORDER BY fine DESC, m.name;", ordered=True)
p("Average pages per author country", "M", "multi-join", "Average book length per author country, rounded to 1 decimal.", ["Join books to authors."],
  "SELECT a.country, ROUND(AVG(b.pages), 1) AS avg_pages FROM books b JOIN authors a ON a.id = b.author_id GROUP BY a.country;")
p("Books by countrymen of the member", "M", "multi-join", "Count loans where the borrowed book's author comes from the UK.", ["Join loans, books, authors."],
  "SELECT COUNT(*) AS uk_loans FROM loans l JOIN books b ON b.id = l.book_id JOIN authors a ON a.id = b.author_id WHERE a.country = 'UK';")
p("Loans per month", "M", "dates", "Number of loans started in each month (YYYY-MM), earliest first.", ["`strftime`."],
  "SELECT strftime('%Y-%m', loan_date) AS month, COUNT(*) AS loans FROM loans GROUP BY month ORDER BY month;", ordered=True)
p("Busiest weekday", "M", "dates", "Which weekday (0 = Sunday) has the most loans started? Show weekday and count; there is no tie.", ["`strftime('%w', loan_date)`."],
  "SELECT strftime('%w', loan_date) AS weekday, COUNT(*) AS loans FROM loans GROUP BY weekday ORDER BY loans DESC LIMIT 1;")
p("Books with above-average length in their genre", "M", "correlated-subquery", "List books longer than the average page count of their genre.", ["Correlated subquery on genre."],
  "SELECT b.title, b.genre, b.pages FROM books b WHERE b.pages > (SELECT AVG(b2.pages) FROM books b2 WHERE b2.genre = b.genre);")
p("Members who borrowed five or more genres", "H", "having", "List members who borrowed books from at least five different genres. Show name and genre count.", ["`COUNT(DISTINCT b.genre)`."],
  "SELECT m.name, COUNT(DISTINCT b.genre) AS genres FROM members m JOIN loans l ON l.member_id = m.id JOIN books b ON b.id = l.book_id GROUP BY m.id, m.name HAVING COUNT(DISTINCT b.genre) >= 5;")
p("Author popularity ranking", "H", "ranking", "Rank authors by total loans of their books with `DENSE_RANK` (1 = most loans). Show rank, author and loans, only the top 5 ranks, ordered by rank then author.", ["Aggregate loans per author, then rank."],
  "WITH t AS (SELECT a.name, COUNT(*) AS loans FROM loans l JOIN books b ON b.id = l.book_id JOIN authors a ON a.id = b.author_id GROUP BY a.id, a.name), r AS (SELECT name, loans, DENSE_RANK() OVER (ORDER BY loans DESC) AS rk FROM t) SELECT rk, name, loans FROM r WHERE rk <= 5 ORDER BY rk, name;", ordered=True)
p("Favourite genre per member", "H", "ranking", "For each member with loans, show their most borrowed genre and the loan count (ties: alphabetically first genre).", ["Count per member and genre, `ROW_NUMBER` ordered by count desc, genre."],
  "WITH c AS (SELECT l.member_id, b.genre, COUNT(*) AS n FROM loans l JOIN books b ON b.id = l.book_id GROUP BY l.member_id, b.genre), r AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY member_id ORDER BY n DESC, genre) AS rn FROM c) SELECT m.name, r.genre, r.n FROM r JOIN members m ON m.id = r.member_id WHERE r.rn = 1;")
p("Cumulative loans over time", "H", "running-total", "For each month show loans that month and the cumulative number of loans to date. Earliest first.", ["Monthly counts, then running sum."],
  "WITH m AS (SELECT strftime('%Y-%m', loan_date) AS month, COUNT(*) AS loans FROM loans GROUP BY month) SELECT month, loans, SUM(loans) OVER (ORDER BY month) AS cumulative FROM m ORDER BY month;", ordered=True)
p("Moving three-month average", "H", "window-functions", "For each month show loans and the average of that month and the two previous months (rounded to 1 decimal; fewer months at the start). Earliest first.", ["`ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`."],
  "WITH m AS (SELECT strftime('%Y-%m', loan_date) AS month, COUNT(*) AS loans FROM loans GROUP BY month) SELECT month, loans, ROUND(AVG(loans) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 1) AS moving_avg FROM m ORDER BY month;", ordered=True)
p("Month over month change", "H", "window-functions", "For each month show loans and the percentage change from the previous month (rounded to 1 decimal, NULL for the first).", ["`LAG(loans)`."],
  "WITH m AS (SELECT strftime('%Y-%m', loan_date) AS month, COUNT(*) AS loans FROM loans GROUP BY month) SELECT month, loans, ROUND(100.0 * (loans - LAG(loans) OVER (ORDER BY month)) / LAG(loans) OVER (ORDER BY month), 1) AS pct_change FROM m ORDER BY month;", ordered=True)
p("Members' first and last loan", "M", "aggregate", "For each member with loans show their first and last loan date and how many days separate them.", ["`MIN`, `MAX` and `julianday`."],
  "SELECT m.name, MIN(l.loan_date) AS first_loan, MAX(l.loan_date) AS last_loan, CAST(julianday(MAX(l.loan_date)) - julianday(MIN(l.loan_date)) AS INTEGER) AS span_days FROM members m JOIN loans l ON l.member_id = m.id GROUP BY m.id, m.name;")
p("Demand per copy", "H", "expressions", "For the 5 books with the highest loans-per-copy ratio show title, copies, loans and the ratio rounded to 2 decimals. Break ties by title.", ["Join aggregated loans to books and divide."],
  "SELECT b.title, b.copies, x.loans, ROUND(1.0 * x.loans / b.copies, 2) AS per_copy FROM books b JOIN (SELECT book_id, COUNT(*) AS loans FROM loans GROUP BY book_id) x ON x.book_id = b.id ORDER BY per_copy DESC, b.title LIMIT 5;", ordered=True)
p("Genre pivot by tier", "H", "pivot", "For each genre show the number of loans by `basic`, `plus` and `premium` members as three columns.", ["Conditional aggregation over member tier."],
  "SELECT b.genre, SUM(CASE WHEN m.tier = 'basic' THEN 1 ELSE 0 END) AS basic, SUM(CASE WHEN m.tier = 'plus' THEN 1 ELSE 0 END) AS plus, SUM(CASE WHEN m.tier = 'premium' THEN 1 ELSE 0 END) AS premium FROM loans l JOIN books b ON b.id = l.book_id JOIN members m ON m.id = l.member_id GROUP BY b.genre;")
p("Consecutive loan streaks", "H", "gaps-islands", "For member 1, group their loan dates into streaks where consecutive loans are at most 30 days apart, and show each streak's start, end and size. Order by start.", ["`LAG` to flag gaps over 30 days, running sum of the flags to number the streaks."],
  "WITH d AS (SELECT loan_date, CASE WHEN julianday(loan_date) - julianday(LAG(loan_date) OVER (ORDER BY loan_date, id)) > 30 THEN 1 ELSE 0 END AS new_streak FROM loans WHERE member_id = 1), g AS (SELECT loan_date, SUM(new_streak) OVER (ORDER BY loan_date ROWS UNBOUNDED PRECEDING) AS grp FROM d) SELECT MIN(loan_date) AS streak_start, MAX(loan_date) AS streak_end, COUNT(*) AS loans FROM g GROUP BY grp ORDER BY streak_start;", ordered=True)
p("Extend overdue loans", "M", "dml", "Extend the due date of every unreturned loan by 14 days (use `date(due_date, '+14 days')`), then count how many of them are still overdue as of 2024-07-01.", ["`UPDATE` then `SELECT COUNT(*)`."],
  "UPDATE loans SET due_date = date(due_date, '+14 days') WHERE return_date IS NULL; SELECT COUNT(*) AS still_overdue FROM loans WHERE return_date IS NULL AND due_date < '2024-07-01';")
p("Retire unloved books", "M", "dml", "Delete books that have never been loaned, then report how many books remain.", ["`DELETE ... WHERE id NOT IN (SELECT book_id FROM loans)`."],
  "DELETE FROM books WHERE id NOT IN (SELECT book_id FROM loans); SELECT COUNT(*) AS remaining FROM books;")
p("Lowercase author search", "E", "strings", "Find authors whose name, ignoring case, contains `an`. Show the name in upper case.", ["`LOWER(name) LIKE '%an%'`, `UPPER(name)`."],
  "SELECT UPPER(name) AS name FROM authors WHERE LOWER(name) LIKE '%an%';")
p("Initials of members", "E", "strings", "Show each member's initials (first letter of the first name plus first letter of the last name, for example `AT` for Alan Turing).", ["`substr(name, 1, 1)` and the character after the space: `substr(name, instr(name, ' ') + 1, 1)`."],
  "SELECT name, substr(name, 1, 1) || substr(name, instr(name, ' ') + 1, 1) AS initials FROM members;")
p("Title length", "E", "strings", "Show the five books with the longest titles (by characters). Break ties by title.", ["`LENGTH(title)`."],
  "SELECT title, LENGTH(title) AS chars FROM books ORDER BY chars DESC, title LIMIT 5;", ordered=True)
p("Membership age bands", "M", "case", "Label each member by years since joining as of 2024-07-01: `new` (under 1 year), `regular` (1 to under 3), `veteran` (3 or more). Count members per label.", ["Years = days / 365.25."],
  "SELECT CASE WHEN (julianday('2024-07-01') - julianday(joined)) / 365.25 < 1 THEN 'new' WHEN (julianday('2024-07-01') - julianday(joined)) / 365.25 < 3 THEN 'regular' ELSE 'veteran' END AS label, COUNT(*) AS members FROM members GROUP BY label;")
p("Union of titles and authors", "M", "set-ops", "Produce one alphabetical list of all book titles and all author names (single column `entry`), without duplicates.", ["`UNION` then `ORDER BY`."],
  "SELECT title AS entry FROM books UNION SELECT name FROM authors ORDER BY entry;", ordered=True)
p("Genres borrowed by both Leeds and Osaka members", "M", "set-ops", "List genres that have been borrowed by members living in Leeds and also by members living in Osaka.", ["`INTERSECT`."],
  "SELECT b.genre FROM loans l JOIN members m ON m.id = l.member_id JOIN books b ON b.id = l.book_id WHERE m.city = 'Leeds' INTERSECT SELECT b.genre FROM loans l JOIN members m ON m.id = l.member_id JOIN books b ON b.id = l.book_id WHERE m.city = 'Osaka';")
