import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import SqlSet
S = SqlSet("library", ["authors", "books", "members", "loans"])
p = S.p

p("Longest book per genre", "M", "correlated-subquery", "For each genre show its longest book (genre, title, pages).", ["Compare to `MAX(pages)` of the same genre."],
  "SELECT b.genre, b.title, b.pages FROM books b WHERE b.pages = (SELECT MAX(b2.pages) FROM books b2 WHERE b2.genre = b.genre);")
p("Author rank within country", "H", "ranking", "Rank authors within their country by number of books (most first) with `RANK()`. Show country, rank, author, books for ranks 1 only (ties allowed), ordered by country then author.", ["Count books per author, rank by country."],
  "WITH c AS (SELECT a.country, a.name, COUNT(*) AS books FROM authors a JOIN books b ON b.author_id = a.id GROUP BY a.id), r AS (SELECT *, RANK() OVER (PARTITION BY country ORDER BY books DESC) AS rk FROM c) SELECT country, rk, name, books FROM r WHERE rk = 1 ORDER BY country, name;", ordered=True)
p("Average days kept per genre", "M", "dates", "Average number of days a book is kept per genre (returned loans only), rounded to 1 decimal.", ["`julianday` difference."],
  "SELECT b.genre, ROUND(AVG(julianday(l.return_date) - julianday(l.loan_date)), 1) AS avg_days FROM loans l JOIN books b ON b.id = l.book_id WHERE l.return_date IS NOT NULL GROUP BY b.genre;")
p("Time between first and second loan", "H", "window-functions", "For each member with at least two loans show days between their first and second loan, and list the 5 smallest gaps (ties by member id).", ["`ROW_NUMBER()` per member, then self-join rn 1 and 2."],
  "WITH r AS (SELECT member_id, loan_date, ROW_NUMBER() OVER (PARTITION BY member_id ORDER BY loan_date, id) AS rn FROM loans) SELECT a.member_id, CAST(julianday(b.loan_date) - julianday(a.loan_date) AS INTEGER) AS days FROM r a JOIN r b ON a.member_id = b.member_id AND a.rn = 1 AND b.rn = 2 ORDER BY days, a.member_id LIMIT 5;", ordered=True)
p("Books by authors from several countries", "E", "join", "How many books are by authors from each country? Most first, ties by country.", ["Join books to authors."],
  "SELECT a.country, COUNT(*) AS books FROM books b JOIN authors a ON a.id = b.author_id GROUP BY a.country ORDER BY books DESC, a.country;", ordered=True)
p("Premium member return behaviour", "H", "case", "Compare tiers: for each tier show total loans, loans returned late, loans still out and the late percentage among returned loans (rounded to 1 decimal).", ["Conditional sums per tier."],
  "SELECT m.tier, COUNT(*) AS loans, SUM(l.return_date > l.due_date) AS late, SUM(l.return_date IS NULL) AS still_out, ROUND(100.0 * SUM(l.return_date > l.due_date) / SUM(l.return_date IS NOT NULL), 1) AS late_pct FROM loans l JOIN members m ON m.id = l.member_id GROUP BY m.tier;")
p("Most prolific decade", "M", "expressions", "Which decade of publication has the most books? Show decade start year and count (no tie).", ["`published_year / 10 * 10`."],
  "SELECT published_year / 10 * 10 AS decade, COUNT(*) AS books FROM books GROUP BY decade ORDER BY books DESC, decade LIMIT 1;")
