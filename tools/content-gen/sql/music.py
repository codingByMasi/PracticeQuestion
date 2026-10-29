import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import SqlSet

S = SqlSet("music", ["artists", "albums", "tracks", "listeners", "plays"])
p = S.p

p("Artist list", "E", "select", "List every artist's name and country.", ["Two columns."], "SELECT name, country FROM artists;")
p("Jazz albums", "E", "where", "List the titles and release years of Jazz albums.", ["`genre = 'Jazz'`."], "SELECT title, release_year FROM albums WHERE genre = 'Jazz';")
p("Albums since 2015", "E", "where", "List albums released in 2015 or later.", ["`release_year >= 2015`."], "SELECT title, release_year FROM albums WHERE release_year >= 2015;")
p("Explicit tracks", "E", "where", "How many tracks are marked explicit?", ["`explicit = 1`."], "SELECT COUNT(*) AS explicit_tracks FROM tracks WHERE explicit = 1;")
p("Long tracks", "E", "where", "List tracks longer than 6 minutes (360 seconds) with their length in seconds. Show only the first 10 by id.", ["Filter, sort by id, limit."],
  "SELECT id, title, seconds FROM tracks WHERE seconds > 360 ORDER BY id LIMIT 10;", ordered=True)
p("Free plan listeners", "E", "where", "List the names of listeners on the `free` plan.", ["`plan = 'free'`."], "SELECT name FROM listeners WHERE plan = 'free';")
p("Oldest bands", "E", "order-by", "The five artists formed earliest. Show name and year, ties by name.", ["Sort by year then name."],
  "SELECT name, formed_year FROM artists ORDER BY formed_year, name LIMIT 5;", ordered=True)
p("Album genres", "E", "distinct", "List each album genre once.", ["`DISTINCT`."], "SELECT DISTINCT genre FROM albums;")
p("Track length in minutes", "E", "expressions", "For tracks 1 to 5 show title and length as minutes rounded to 2 decimals.", ["`seconds / 60.0`."],
  "SELECT title, ROUND(seconds / 60.0, 2) AS minutes FROM tracks WHERE id <= 5;")
p("Total plays", "E", "aggregate", "How many plays are recorded in total?", ["`COUNT(*)`."], "SELECT COUNT(*) AS plays FROM plays;")
p("Average track length", "E", "aggregate", "Average track length in seconds, rounded to 1 decimal.", ["`ROUND(AVG(seconds), 1)`."], "SELECT ROUND(AVG(seconds), 1) AS avg_seconds FROM tracks;")
p("Plays by device", "E", "group-by", "Count plays per device.", ["`GROUP BY device`."], "SELECT device, COUNT(*) AS plays FROM plays GROUP BY device;")
p("Listeners per plan", "E", "group-by", "Count listeners per plan.", ["`GROUP BY plan`."], "SELECT plan, COUNT(*) AS listeners FROM listeners GROUP BY plan;")
p("Albums per genre", "E", "group-by", "Number of albums per genre.", ["`GROUP BY genre`."], "SELECT genre, COUNT(*) AS albums FROM albums GROUP BY genre;")
p("Albums with artist names", "E", "join", "For albums 1 to 5 show title and artist name.", ["Join albums to artists."],
  "SELECT al.title, ar.name AS artist FROM albums al JOIN artists ar ON ar.id = al.artist_id WHERE al.id <= 5;")
p("Tracks with album titles", "E", "join", "For tracks 1 to 6 show track title and album title.", ["Join tracks to albums."],
  "SELECT t.title AS track, al.title AS album FROM tracks t JOIN albums al ON al.id = t.album_id WHERE t.id <= 6;")
p("Genres with many albums", "E", "having", "Which genres have at least 7 albums?", ["`HAVING COUNT(*) >= 7`."],
  "SELECT genre, COUNT(*) AS albums FROM albums GROUP BY genre HAVING COUNT(*) >= 7;")
p("Tracks per album", "M", "group-by", "For each album with tracks show title and track count; list the five largest albums, ties by title.", ["Group by album."],
  "SELECT al.title, COUNT(*) AS tracks FROM tracks t JOIN albums al ON al.id = t.album_id GROUP BY al.id, al.title ORDER BY tracks DESC, al.title LIMIT 5;", ordered=True)
p("Album running time", "M", "aggregate", "For each album show total running time in minutes (rounded to 1 decimal). List the 5 longest, ties by title.", ["`SUM(seconds) / 60.0`."],
  "SELECT al.title, ROUND(SUM(t.seconds) / 60.0, 1) AS minutes FROM tracks t JOIN albums al ON al.id = t.album_id GROUP BY al.id, al.title ORDER BY minutes DESC, al.title LIMIT 5;", ordered=True)
p("Most played tracks", "M", "join", "The 5 most played tracks with their play counts. Ties by track title then id.", ["Group plays by track."],
  "SELECT t.title, COUNT(*) AS plays FROM plays p JOIN tracks t ON t.id = p.track_id GROUP BY t.id, t.title ORDER BY plays DESC, t.title, t.id LIMIT 5;", ordered=True)
p("Most played artists", "M", "multi-join", "Total plays per artist, top 5 (ties by name).", ["Join plays to tracks to albums to artists."],
  "SELECT ar.name, COUNT(*) AS plays FROM plays p JOIN tracks t ON t.id = p.track_id JOIN albums al ON al.id = t.album_id JOIN artists ar ON ar.id = al.artist_id GROUP BY ar.id, ar.name ORDER BY plays DESC, ar.name LIMIT 5;", ordered=True)
p("Genre popularity by plays", "M", "multi-join", "Number of plays per album genre, most first.", ["Join plays, tracks, albums."],
  "SELECT al.genre, COUNT(*) AS plays FROM plays p JOIN tracks t ON t.id = p.track_id JOIN albums al ON al.id = t.album_id GROUP BY al.genre ORDER BY plays DESC;", ordered=True)
p("Tracks never played", "M", "left-join", "How many tracks have never been played?", ["Anti-join and count."],
  "SELECT COUNT(*) AS never_played FROM tracks t LEFT JOIN plays p ON p.track_id = t.id WHERE p.id IS NULL;")
p("Quiet artists", "M", "left-join", "List artists whose tracks together have fewer than 30 plays (include zero). Show name and plays.", ["Left join through albums and tracks."],
  "SELECT ar.name, COUNT(p.id) AS plays FROM artists ar LEFT JOIN albums al ON al.artist_id = ar.id LEFT JOIN tracks t ON t.album_id = al.id LEFT JOIN plays p ON p.track_id = t.id GROUP BY ar.id, ar.name HAVING COUNT(p.id) < 30;")
p("Listening hours", "M", "aggregate", "Total listening time per listener in hours (sum of the played tracks' lengths), rounded to 2 decimals. Show the top five, ties by name.", ["Join plays to tracks and listeners."],
  "SELECT l.name, ROUND(SUM(t.seconds) / 3600.0, 2) AS hours FROM plays p JOIN tracks t ON t.id = p.track_id JOIN listeners l ON l.id = p.listener_id GROUP BY l.id, l.name ORDER BY hours DESC, l.name LIMIT 5;", ordered=True)
p("Plays by hour of day", "M", "dates", "How many plays started in each hour of the day? Show hour (00-23) and plays, ordered by hour.", ["`strftime('%H', played_at)`."],
  "SELECT strftime('%H', played_at) AS hour, COUNT(*) AS plays FROM plays GROUP BY hour ORDER BY hour;", ordered=True)
p("Plays per month", "M", "dates", "Number of plays per month (YYYY-MM).", ["`strftime('%Y-%m', played_at)`."],
  "SELECT strftime('%Y-%m', played_at) AS month, COUNT(*) AS plays FROM plays GROUP BY month ORDER BY month;", ordered=True)
p("Night owls", "M", "dates", "Count plays between midnight and 05:59 for each plan.", ["Hour below 06."],
  "SELECT l.plan, COUNT(*) AS night_plays FROM plays p JOIN listeners l ON l.id = p.listener_id WHERE strftime('%H', p.played_at) < '06' GROUP BY l.plan;")
p("Listeners by country", "M", "group-by", "Plays per listener country, most first.", ["Join plays to listeners."],
  "SELECT l.country, COUNT(*) AS plays FROM plays p JOIN listeners l ON l.id = p.listener_id GROUP BY l.country ORDER BY plays DESC, l.country;", ordered=True)
p("Explicit share of plays", "M", "aggregate", "What percentage of all plays were of explicit tracks (rounded to 1 decimal)?", ["Join and average a flag."],
  "SELECT ROUND(100.0 * SUM(t.explicit) / COUNT(*), 1) AS explicit_pct FROM plays p JOIN tracks t ON t.id = p.track_id;")
p("Listeners of the opening track", "M", "exists", "List listeners who played a track number 1 on any album. Show distinct names.", ["Join plays to tracks with `track_no = 1`."],
  "SELECT DISTINCT l.name FROM listeners l JOIN plays p ON p.listener_id = l.id JOIN tracks t ON t.id = p.track_id WHERE t.track_no = 1;")
p("Albums above average length", "M", "subquery", "List albums whose total running time is above the average album running time. Show title and minutes rounded to 1 decimal.", ["Per-album sums in a CTE."],
  "WITH a AS (SELECT album_id, SUM(seconds) AS total FROM tracks GROUP BY album_id) SELECT al.title, ROUND(a.total / 60.0, 1) AS minutes FROM a JOIN albums al ON al.id = a.album_id WHERE a.total > (SELECT AVG(total) FROM a);")
p("Artists with several genres", "M", "having", "List artists who released albums in at least two different genres.", ["`COUNT(DISTINCT genre) >= 2`."],
  "SELECT ar.name, COUNT(DISTINCT al.genre) AS genres FROM artists ar JOIN albums al ON al.artist_id = ar.id GROUP BY ar.id, ar.name HAVING COUNT(DISTINCT al.genre) >= 2;")
p("Signup before first play", "M", "dates", "Count listeners whose first play happened within 30 days of signing up.", ["Per-listener minimum played date."],
  "SELECT COUNT(*) AS quick_starters FROM (SELECT l.id FROM listeners l JOIN plays p ON p.listener_id = l.id GROUP BY l.id, l.signup_date HAVING julianday(MIN(substr(p.played_at, 1, 10))) - julianday(l.signup_date) <= 30);")
p("Top track per album", "H", "ranking", "For each album, show its most played track (album title, track title, plays). Break ties by track title. Only albums with at least one play.", ["Rank tracks within album."],
  "WITH c AS (SELECT t.album_id, t.title, COUNT(*) AS plays FROM plays p JOIN tracks t ON t.id = p.track_id GROUP BY t.id), r AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY album_id ORDER BY plays DESC, title) AS rn FROM c) SELECT al.title AS album, r.title AS track, r.plays FROM r JOIN albums al ON al.id = r.album_id WHERE r.rn = 1;")
p("Listener top artist", "H", "ranking", "For each of listeners 1 to 5, show their most played artist and the play count (ties: alphabetically first artist).", ["Count per listener and artist, then rank."],
  "WITH c AS (SELECT p.listener_id, ar.name, COUNT(*) AS plays FROM plays p JOIN tracks t ON t.id = p.track_id JOIN albums al ON al.id = t.album_id JOIN artists ar ON ar.id = al.artist_id WHERE p.listener_id <= 5 GROUP BY p.listener_id, ar.id), r AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY listener_id ORDER BY plays DESC, name) AS rn FROM c) SELECT listener_id, name, plays FROM r WHERE rn = 1 ORDER BY listener_id;", ordered=True)
p("Cumulative plays by day", "H", "running-total", "For each of the first 10 days with plays (by date), show date, plays that day and the cumulative total.", ["Daily counts in a CTE, then running sum, then limit."],
  "WITH d AS (SELECT substr(played_at, 1, 10) AS day, COUNT(*) AS plays FROM plays GROUP BY day) SELECT day, plays, SUM(plays) OVER (ORDER BY day) AS cumulative FROM d ORDER BY day LIMIT 10;", ordered=True)
p("Seven-day moving average", "H", "window-functions", "Daily plays for the first 12 days with plays, plus the 7-day trailing moving average (current day and the 6 previous days with plays) rounded to 1 decimal.", ["`ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`."],
  "WITH d AS (SELECT substr(played_at, 1, 10) AS day, COUNT(*) AS plays FROM plays GROUP BY day) SELECT day, plays, ROUND(AVG(plays) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 1) AS moving_avg FROM d ORDER BY day LIMIT 12;", ordered=True)
p("Listening sessions", "H", "gaps-islands", "For listener 1, order plays by time and start a new session whenever more than 60 minutes pass since the previous play. Show the session number (starting at 1), its first play time and its number of plays, ordered by session.", ["`LAG` to detect gaps, running sum for session ids."],
  "WITH x AS (SELECT played_at, (julianday(played_at) - julianday(LAG(played_at) OVER (ORDER BY played_at, id))) * 1440 AS gap FROM plays WHERE listener_id = 1), s AS (SELECT played_at, SUM(CASE WHEN gap IS NULL OR gap > 60 THEN 1 ELSE 0 END) OVER (ORDER BY played_at ROWS UNBOUNDED PRECEDING) AS session FROM x) SELECT session, MIN(played_at) AS started, COUNT(*) AS plays FROM s GROUP BY session ORDER BY session LIMIT 10;", ordered=True)
p("Genre rank per country", "H", "ranking", "For each listener country show the most played album genre and its plays (ties: alphabetically first genre).", ["Count by country and genre, rank."],
  "WITH c AS (SELECT l.country, al.genre, COUNT(*) AS plays FROM plays p JOIN listeners l ON l.id = p.listener_id JOIN tracks t ON t.id = p.track_id JOIN albums al ON al.id = t.album_id GROUP BY l.country, al.genre), r AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY country ORDER BY plays DESC, genre) AS rn FROM c) SELECT country, genre, plays FROM r WHERE rn = 1;")
p("Plan pivot by device", "H", "pivot", "For each plan show plays on `phone`, `web`, `speaker` and `car` as four columns.", ["Conditional sums."],
  "SELECT l.plan, SUM(p.device = 'phone') AS phone, SUM(p.device = 'web') AS web, SUM(p.device = 'speaker') AS speaker, SUM(p.device = 'car') AS car FROM plays p JOIN listeners l ON l.id = p.listener_id GROUP BY l.plan;")
p("Listeners sharing taste", "H", "self-join", "For listener 1, list the 3 other listeners who share the most distinct played tracks with them. Show listener id and the number of shared tracks, ties by listener id.", ["Self-join distinct (listener, track) pairs."],
  "WITH lt AS (SELECT DISTINCT listener_id, track_id FROM plays) SELECT b.listener_id, COUNT(*) AS shared FROM lt a JOIN lt b ON a.track_id = b.track_id AND b.listener_id <> a.listener_id WHERE a.listener_id = 1 GROUP BY b.listener_id ORDER BY shared DESC, b.listener_id LIMIT 3;", ordered=True)
p("Artist discography span", "M", "aggregate", "For each artist with albums show first and last album year and the span in years. Ties are fine; list all.", ["`MIN` and `MAX` of year."],
  "SELECT ar.name, MIN(al.release_year) AS first_album, MAX(al.release_year) AS last_album, MAX(al.release_year) - MIN(al.release_year) AS span FROM artists ar JOIN albums al ON al.artist_id = ar.id GROUP BY ar.id, ar.name;")
p("Longest and shortest track per album", "M", "aggregate", "For albums 1 to 5 show the album title, the shortest and the longest track length in seconds.", ["Two aggregates per album."],
  "SELECT al.title, MIN(t.seconds) AS shortest, MAX(t.seconds) AS longest FROM albums al JOIN tracks t ON t.album_id = al.id WHERE al.id <= 5 GROUP BY al.id, al.title;")
p("Remove explicit tracks", "M", "dml", "Delete all explicit tracks, then report how many tracks and how many plays of the remaining tracks exist (two columns).", ["`DELETE FROM tracks WHERE explicit = 1`."],
  "DELETE FROM tracks WHERE explicit = 1; SELECT (SELECT COUNT(*) FROM tracks) AS tracks, (SELECT COUNT(*) FROM plays WHERE track_id IN (SELECT id FROM tracks)) AS plays;")
p("Upgrade free listeners", "M", "dml", "Move every free listener who signed up before 2022 to the `premium` plan, then count listeners per plan.", ["`UPDATE listeners SET plan = 'premium' WHERE ...`."],
  "UPDATE listeners SET plan = 'premium' WHERE plan = 'free' AND signup_date < '2022-01-01'; SELECT plan, COUNT(*) AS listeners FROM listeners GROUP BY plan;")
p("Long artist names in capitals", "E", "strings", "Show each artist name in upper case along with its length in characters, for artists whose name is longer than 12 characters.", ["`UPPER`, `LENGTH`."],
  "SELECT UPPER(name) AS name, LENGTH(name) AS chars FROM artists WHERE LENGTH(name) > 12;")
p("Track titles with 'Again'", "E", "like", "List tracks whose title ends with the word `Again`. Show the first ten by id.", ["`LIKE '% Again'`."],
  "SELECT id, title FROM tracks WHERE title LIKE '% Again' ORDER BY id LIMIT 10;", ordered=True)
p("Countries in both lists", "M", "set-ops", "Which countries appear among both artists and listeners?", ["`INTERSECT`."],
  "SELECT country FROM artists INTERSECT SELECT country FROM listeners;")
