import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import SqlSet

S = SqlSet("movies", ["movies", "directors", "reviews"])
p = S.p

p("Movie titles and years", "E", "select", "List every movie title with its release year.", ["Two columns from `movies`."], "SELECT title, release_year FROM movies;")
p("Long movies", "E", "where", "Find movies longer than 150 minutes. Show title and runtime.", ["Compare `runtime_minutes`."], "SELECT title, runtime_minutes FROM movies WHERE runtime_minutes > 150;")
p("Twenty-first century films", "E", "where", "List titles released in the year 2000 or later.", ["`release_year >= 2000`."], "SELECT title, release_year FROM movies WHERE release_year >= 2000;")
p("Sci-Fi or Animation", "E", "where", "List titles whose genre is either Sci-Fi or Animation.", ["`IN ('Sci-Fi', 'Animation')`."], "SELECT title, genre FROM movies WHERE genre IN ('Sci-Fi', 'Animation');")
p("Titles starting with The", "E", "like", "List movies whose title starts with `The`.", ["`LIKE 'The %'`."], "SELECT title FROM movies WHERE title LIKE 'The %';")
p("Missing box office", "E", "null", "List movies with no recorded `gross_millions`.", ["`IS NULL`."], "SELECT title FROM movies WHERE gross_millions IS NULL;")
p("Movies without a director", "E", "null", "List movies whose director is unknown.", ["`director_id IS NULL`."], "SELECT title FROM movies WHERE director_id IS NULL;")
p("Shortest first", "E", "order-by", "List titles and runtimes, shortest movie first.", ["`ORDER BY runtime_minutes`."], "SELECT title, runtime_minutes FROM movies ORDER BY runtime_minutes;", ordered=True)
p("Top three grossing films", "E", "order-by", "The three highest-grossing movies, biggest first. Show title and gross.", ["NULL gross sorts low in SQLite when descending."],
  "SELECT title, gross_millions FROM movies ORDER BY gross_millions DESC LIMIT 3;", ordered=True)
p("Genres list", "E", "distinct", "List each genre once.", ["`DISTINCT`."], "SELECT DISTINCT genre FROM movies;")
p("Profit in millions", "E", "expressions", "For movies with both budget and gross known, show title and profit (gross minus budget) rounded to 1 decimal.", ["Filter out NULLs first."],
  "SELECT title, ROUND(gross_millions - budget_millions, 1) AS profit FROM movies WHERE budget_millions IS NOT NULL AND gross_millions IS NOT NULL;")
p("Runtime in hours and minutes", "E", "strings", "Show each title with its runtime formatted like `2h 28m`.", ["Integer division and `%`."],
  "SELECT title, (runtime_minutes / 60) || 'h ' || (runtime_minutes % 60) || 'm' AS runtime FROM movies;")
p("Average review rating", "E", "aggregate", "What is the average review rating across all reviews, rounded to 2 decimals?", ["`ROUND(AVG(rating), 2)`."], "SELECT ROUND(AVG(rating), 2) AS avg_rating FROM reviews;")
p("Movies per genre", "E", "group-by", "Count movies in each genre.", ["`GROUP BY genre`."], "SELECT genre, COUNT(*) AS movies FROM movies GROUP BY genre;")
p("Reviews per reviewer", "E", "group-by", "How many reviews did each reviewer write?", ["`GROUP BY reviewer`."], "SELECT reviewer, COUNT(*) AS reviews FROM reviews GROUP BY reviewer;")
p("Movies with their director", "E", "join", "List each movie title with its director's name (movies without a director are not shown).", ["Inner join."],
  "SELECT m.title, d.name AS director FROM movies m JOIN directors d ON d.id = m.director_id;")
p("All movies even without director", "M", "left-join", "List every movie with its director's name, showing `Unknown` when there is none.", ["`LEFT JOIN` plus `COALESCE`."],
  "SELECT m.title, COALESCE(d.name, 'Unknown') AS director FROM movies m LEFT JOIN directors d ON d.id = m.director_id;")
p("Films per director", "M", "group-by", "For each director show their name and how many movies they made.", ["Join and group."],
  "SELECT d.name, COUNT(*) AS movies FROM directors d JOIN movies m ON m.director_id = d.id GROUP BY d.id, d.name;")
p("Average runtime by director country", "M", "multi-join", "Average movie runtime per director country, rounded to 1 decimal.", ["Join movies to directors, group by country."],
  "SELECT d.country, ROUND(AVG(m.runtime_minutes), 1) AS avg_runtime FROM movies m JOIN directors d ON d.id = m.director_id GROUP BY d.country;")
p("Average rating per movie", "M", "join", "For every reviewed movie show the title, number of reviews and average rating rounded to 2 decimals.", ["Join reviews to movies."],
  "SELECT m.title, COUNT(*) AS reviews, ROUND(AVG(r.rating), 2) AS avg_rating FROM movies m JOIN reviews r ON r.movie_id = m.id GROUP BY m.id, m.title;")
p("Unreviewed movies", "M", "left-join", "List movies that have no reviews.", ["`LEFT JOIN reviews ... WHERE r.id IS NULL`."],
  "SELECT m.title FROM movies m LEFT JOIN reviews r ON r.movie_id = m.id WHERE r.id IS NULL;")
p("Directors with a perfect ten", "M", "exists", "List directors who have at least one movie that received a rating of 10.", ["`EXISTS` over movies and reviews."],
  "SELECT d.name FROM directors d WHERE EXISTS (SELECT 1 FROM movies m JOIN reviews r ON r.movie_id = m.id WHERE m.director_id = d.id AND r.rating = 10);")
p("Consistent reviewers", "M", "having", "List reviewers whose lowest rating is at least 7 and who wrote at least three reviews.", ["`HAVING MIN(rating) >= 7 AND COUNT(*) >= 3`."],
  "SELECT reviewer, COUNT(*) AS reviews, MIN(rating) AS lowest FROM reviews GROUP BY reviewer HAVING MIN(rating) >= 7 AND COUNT(*) >= 3;")
p("Genre revenue", "M", "aggregate", "Total gross per genre (ignoring unknown grosses), biggest first.", ["`SUM` skips NULLs."],
  "SELECT genre, SUM(gross_millions) AS total_gross FROM movies GROUP BY genre ORDER BY total_gross DESC;", ordered=True)
p("Return on investment", "M", "expressions", "For movies with known budget and gross, show the title and the gross-to-budget ratio rounded to 1 decimal. Highest ratio first.", ["Divide gross by budget."],
  "SELECT title, ROUND(gross_millions / budget_millions, 1) AS roi FROM movies WHERE budget_millions IS NOT NULL AND gross_millions IS NOT NULL ORDER BY roi DESC;", ordered=True)
p("Movies above their genre's average runtime", "M", "correlated-subquery", "List movies longer than the average runtime of their own genre.", ["Correlated subquery on genre."],
  "SELECT m.title, m.genre, m.runtime_minutes FROM movies m WHERE m.runtime_minutes > (SELECT AVG(m2.runtime_minutes) FROM movies m2 WHERE m2.genre = m.genre);")
p("Rated above the overall average", "M", "subquery", "List movies whose average rating is above the average of all ratings. Show title and average rounded to 2 decimals.", ["Subquery on `AVG(rating)`."],
  "SELECT m.title, ROUND(AVG(r.rating), 2) AS avg_rating FROM movies m JOIN reviews r ON r.movie_id = m.id GROUP BY m.id, m.title HAVING AVG(r.rating) > (SELECT AVG(rating) FROM reviews);")
p("Decade summary", "M", "expressions", "Group movies by decade (for example 2010 for 2010-2019) and show decade and count. Oldest first.", ["`release_year / 10 * 10` uses integer division."],
  "SELECT release_year / 10 * 10 AS decade, COUNT(*) AS movies FROM movies GROUP BY decade ORDER BY decade;", ordered=True)
p("Reviews by month", "M", "dates", "How many reviews were written in each month (YYYY-MM)? Earliest first.", ["`strftime('%Y-%m', review_date)`."],
  "SELECT strftime('%Y-%m', review_date) AS month, COUNT(*) AS reviews FROM reviews GROUP BY month ORDER BY month;", ordered=True)
p("Directors older than 75", "M", "dates", "List directors who were born in 1950 or earlier, with their age in 2024.", ["Subtract birth year from 2024."],
  "SELECT name, 2024 - birth_year AS age FROM directors WHERE birth_year <= 1950;")
p("Rating histogram", "M", "group-by", "How many reviews gave each rating? Highest rating first.", ["Group by rating."],
  "SELECT rating, COUNT(*) AS n FROM reviews GROUP BY rating ORDER BY rating DESC;", ordered=True)
p("Disagreeing reviewers", "H", "self-join", "Find pairs of reviewers who rated the same movie with a difference of at least 3 points. Show movie title, the two reviewers (alphabetical order within the pair) and the difference.", ["Self-join reviews on `movie_id` with `a.reviewer < b.reviewer`."],
  "SELECT m.title, a.reviewer AS reviewer_a, b.reviewer AS reviewer_b, ABS(a.rating - b.rating) AS diff FROM reviews a JOIN reviews b ON a.movie_id = b.movie_id AND a.reviewer < b.reviewer JOIN movies m ON m.id = a.movie_id WHERE ABS(a.rating - b.rating) >= 3;")
p("Best movie per genre", "H", "ranking", "For each genre show its best-reviewed movie by average rating (title and average). If two tie, pick the alphabetically first title.", ["Rank within genre using average rating desc, title asc."],
  "WITH s AS (SELECT m.genre, m.title, AVG(r.rating) AS avg_rating FROM movies m JOIN reviews r ON r.movie_id = m.id GROUP BY m.id), k AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY genre ORDER BY avg_rating DESC, title) AS rn FROM s) SELECT genre, title, ROUND(avg_rating, 2) AS avg_rating FROM k WHERE rn = 1;")
p("Rating versus reviewer average", "H", "window-functions", "For every review show the reviewer, the movie id, the rating and how far it is from that reviewer's own average rating (rounded to 2 decimals). Order by reviewer then review id.", ["`AVG(rating) OVER (PARTITION BY reviewer)`."],
  "SELECT reviewer, movie_id, rating, ROUND(rating - AVG(rating) OVER (PARTITION BY reviewer), 2) AS vs_own_avg FROM reviews ORDER BY reviewer, id;", ordered=True)
p("Running box office by year", "H", "running-total", "For each release year show total gross that year and the cumulative gross up to that year (ignoring unknown grosses; years with only unknown gross are excluded). Oldest first.", ["Aggregate per year, then running `SUM() OVER`."],
  "WITH y AS (SELECT release_year, SUM(gross_millions) AS gross FROM movies WHERE gross_millions IS NOT NULL GROUP BY release_year) SELECT release_year, gross, SUM(gross) OVER (ORDER BY release_year) AS cumulative FROM y ORDER BY release_year;", ordered=True)
p("Directors who stayed in one genre", "H", "having", "List directors whose movies all belong to a single genre and who made at least two movies.", ["`COUNT(DISTINCT genre) = 1`."],
  "SELECT d.name, MIN(m.genre) AS genre, COUNT(*) AS movies FROM directors d JOIN movies m ON m.director_id = d.id GROUP BY d.id, d.name HAVING COUNT(DISTINCT m.genre) = 1 AND COUNT(*) >= 2;")
p("Rating rank within each movie", "H", "ranking", "Rank each review within its movie from highest rating to lowest with `RANK()`. Show movie id, reviewer, rating, rank. Only for movies with at least three reviews. Order by movie id, rank, reviewer.", ["Window `RANK()` partitioned by movie; filter on a count window."],
  "SELECT movie_id, reviewer, rating, rk FROM (SELECT movie_id, reviewer, rating, RANK() OVER (PARTITION BY movie_id ORDER BY rating DESC) AS rk, COUNT(*) OVER (PARTITION BY movie_id) AS n FROM reviews) WHERE n >= 3 ORDER BY movie_id, rk, reviewer;", ordered=True)
p("Longest film per director country", "H", "correlated-subquery", "For each director country, show the longest movie (title and runtime) made by a director from that country.", ["Compare runtime to the max per country."],
  "SELECT d.country, m.title, m.runtime_minutes FROM movies m JOIN directors d ON d.id = m.director_id WHERE m.runtime_minutes = (SELECT MAX(m2.runtime_minutes) FROM movies m2 JOIN directors d2 ON d2.id = m2.director_id WHERE d2.country = d.country);")
p("Genres by profit and share", "H", "window-functions", "For each genre with known financials, show total profit (gross minus budget) and its share of all profit as a percentage rounded to 1 decimal.", ["Window total beside grouped rows."],
  "WITH g AS (SELECT genre, SUM(gross_millions - budget_millions) AS profit FROM movies WHERE gross_millions IS NOT NULL AND budget_millions IS NOT NULL GROUP BY genre) SELECT genre, ROUND(profit, 1) AS profit, ROUND(100.0 * profit / SUM(profit) OVER (), 1) AS share_pct FROM g;")
p("Remove low-rated reviews", "M", "dml", "Delete all reviews rated below 6, then show the new average rating rounded to 2 decimals.", ["`DELETE FROM reviews WHERE rating < 6`."],
  "DELETE FROM reviews WHERE rating < 6; SELECT ROUND(AVG(rating), 2) AS avg_rating FROM reviews;")
p("Add a missing budget", "M", "dml", "Set the budget of the movie titled `The Room Next Door` to 15 and then list movies with a budget above 100.", ["`UPDATE movies SET budget_millions = 15 WHERE ...`."],
  "UPDATE movies SET budget_millions = 15 WHERE title = 'The Room Next Door'; SELECT title, budget_millions FROM movies WHERE budget_millions > 100;")
