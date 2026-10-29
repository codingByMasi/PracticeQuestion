import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import SqlSet

S = SqlSet("flights", ["airlines", "airports", "flights", "bookings"])
p = S.p

p("Airport directory", "E", "select", "List every airport's code, city and country.", ["Select three columns."], "SELECT code, city, country FROM airports;")
p("Flights on a date", "E", "where", "List the ids of flights departing on 2024-03-15 or later but before 2024-03-20.", ["Date range on `depart_date`."],
  "SELECT id, depart_date FROM flights WHERE depart_date >= '2024-03-01' AND depart_date < '2024-03-20';")
p("Cancelled flights", "E", "where", "How many flights were cancelled? Show the count.", ["Filter on status."], "SELECT COUNT(*) AS cancelled FROM flights WHERE status = 'cancelled';")
p("Long-haul flights", "E", "where", "List flights longer than 10 hours (600 minutes) with their duration.", ["`duration_min > 600`."], "SELECT id, origin, destination, duration_min FROM flights WHERE duration_min > 600;")
p("High-altitude airports", "E", "where", "List airports with elevation above 1,000 feet, highest first.", ["Sort descending."], "SELECT code, city, elevation_ft FROM airports WHERE elevation_ft > 1000 ORDER BY elevation_ft DESC;", ordered=True)
p("Flights from London", "E", "where", "List flights departing from `LHR`: id, destination and date.", ["`origin = 'LHR'`."], "SELECT id, destination, depart_date FROM flights WHERE origin = 'LHR';")
p("Five cheapest base fares", "E", "order-by", "The five lowest base prices among flights, cheapest first. Break ties by flight id.", ["Order by price then id."],
  "SELECT id, base_price FROM flights ORDER BY base_price, id LIMIT 5;", ordered=True)
p("Airlines by country", "E", "order-by", "List airlines sorted by country and then name.", ["Two sort keys."], "SELECT name, country FROM airlines ORDER BY country, name;", ordered=True)
p("Distinct statuses", "E", "distinct", "List each flight status that occurs.", ["`DISTINCT status`."], "SELECT DISTINCT status FROM flights;")
p("Business and first class bookings", "E", "where", "Count bookings in the business or first seat classes.", ["`IN ('business', 'first')`."],
  "SELECT COUNT(*) AS premium_bookings FROM bookings WHERE seat_class IN ('business', 'first');")
p("Hours and minutes", "E", "expressions", "Show each flight id (first 5 ids only) with its duration as hours, rounded to 1 decimal.", ["`ROUND(duration_min / 60.0, 1)` and `LIMIT`."],
  "SELECT id, ROUND(duration_min / 60.0, 1) AS hours FROM flights WHERE id <= 5;")
p("Fare statistics", "E", "aggregate", "Show the number of bookings, total fare and average fare (rounded to 2 decimals).", ["Three aggregates."],
  "SELECT COUNT(*) AS bookings, ROUND(SUM(fare), 2) AS total_fare, ROUND(AVG(fare), 2) AS avg_fare FROM bookings;")
p("Flights per airline", "E", "group-by", "Number of flights per airline code.", ["Group by `airline_code`."], "SELECT airline_code, COUNT(*) AS flights FROM flights GROUP BY airline_code;")
p("Bookings per class", "E", "group-by", "Average fare per seat class, rounded to 2 decimals.", ["Group by seat class."],
  "SELECT seat_class, ROUND(AVG(fare), 2) AS avg_fare FROM bookings GROUP BY seat_class;")
p("Flights with airline names", "E", "join", "For flights 1 to 5, show the flight id and airline name.", ["Join to `airlines` on the code."],
  "SELECT f.id, a.name AS airline FROM flights f JOIN airlines a ON a.code = f.airline_code WHERE f.id <= 5;")
p("Routes with city names", "M", "multi-join", "For flights 1 to 5 show origin city and destination city. Join `airports` twice.", ["Alias the airports table as `o` and `d`."],
  "SELECT f.id, o.city AS from_city, d.city AS to_city FROM flights f JOIN airports o ON o.code = f.origin JOIN airports d ON d.code = f.destination WHERE f.id <= 5;")
p("Airlines with more than 20 flights", "E", "having", "Which airlines operate more than 20 flights? Show the code and count.", ["`HAVING COUNT(*) > 20`."],
  "SELECT airline_code, COUNT(*) AS flights FROM flights GROUP BY airline_code HAVING COUNT(*) > 20;")
p("Busiest origin airports", "M", "group-by", "The five airports with the most departures. Show city and departures, ties by city.", ["Join airports to flights by origin."],
  "SELECT a.city, COUNT(*) AS departures FROM flights f JOIN airports a ON a.code = f.origin GROUP BY a.code, a.city ORDER BY departures DESC, a.city LIMIT 5;", ordered=True)
p("Airports with no departures", "M", "left-join", "List airports with fewer than 8 departures (zero counts). Show city and departures.", ["Left join and `HAVING COUNT(f.id) < 8`."],
  "SELECT a.city, COUNT(f.id) AS departures FROM airports a LEFT JOIN flights f ON f.origin = a.code GROUP BY a.code, a.city HAVING COUNT(f.id) < 8;")
p("Passengers per flight", "M", "join", "Show the five flights with the most bookings: flight id, bookings. Ties by flight id.", ["Group bookings by flight."],
  "SELECT flight_id, COUNT(*) AS bookings FROM bookings GROUP BY flight_id ORDER BY bookings DESC, flight_id LIMIT 5;", ordered=True)
p("Flights nobody booked", "M", "left-join", "Count flights that have no bookings.", ["Anti-join then count."],
  "SELECT COUNT(*) AS empty_flights FROM flights f LEFT JOIN bookings b ON b.flight_id = f.id WHERE b.id IS NULL;")
p("Revenue by airline", "M", "multi-join", "Total booking fares per airline name, rounded to 2 decimals, biggest first.", ["Join bookings, flights, airlines."],
  "SELECT a.name, ROUND(SUM(b.fare), 2) AS revenue FROM bookings b JOIN flights f ON f.id = b.flight_id JOIN airlines a ON a.code = f.airline_code GROUP BY a.code, a.name ORDER BY revenue DESC;", ordered=True)
p("Delay rate per airline", "M", "group-by", "For each airline show the percentage of its flights that were delayed or cancelled, rounded to 1 decimal. Highest first (ties by name).", ["Average a 0/1 flag."],
  "SELECT a.name, ROUND(100.0 * SUM(CASE WHEN f.status <> 'on_time' THEN 1 ELSE 0 END) / COUNT(*), 1) AS disrupted_pct FROM flights f JOIN airlines a ON a.code = f.airline_code GROUP BY a.code, a.name ORDER BY disrupted_pct DESC, a.name;", ordered=True)
p("Premium share of bookings", "M", "aggregate", "What percentage of bookings are business or first class (rounded to 1 decimal)?", ["Divide premium count by all."],
  "SELECT ROUND(100.0 * SUM(CASE WHEN seat_class <> 'economy' THEN 1 ELSE 0 END) / COUNT(*), 1) AS premium_pct FROM bookings;")
p("Fare versus base price", "M", "join", "For each booking made in economy class on flight 1 to 20, show the booking id and the ratio of fare to the flight's base price rounded to 2 decimals.", ["Join bookings to flights."],
  "SELECT b.id, ROUND(b.fare / f.base_price, 2) AS ratio FROM bookings b JOIN flights f ON f.id = b.flight_id WHERE b.seat_class = 'economy' AND f.id <= 20;")
p("Early birds", "M", "dates", "For each booking show the number of days between booking and departure. List the 5 earliest-booked (largest gap), ties by booking id.", ["`julianday(depart_date) - julianday(booked_on)`."],
  "SELECT b.id, CAST(julianday(f.depart_date) - julianday(b.booked_on) AS INTEGER) AS days_ahead FROM bookings b JOIN flights f ON f.id = b.flight_id ORDER BY days_ahead DESC, b.id LIMIT 5;", ordered=True)
p("Flights per month", "M", "dates", "Number of flights departing each month (YYYY-MM), earliest first.", ["`strftime('%Y-%m', depart_date)`."],
  "SELECT strftime('%Y-%m', depart_date) AS month, COUNT(*) AS flights FROM flights GROUP BY month ORDER BY month;", ordered=True)
p("Weekend departures", "M", "dates", "How many flights depart on a Saturday or Sunday? (`strftime('%w')` gives 0 for Sunday and 6 for Saturday.)", ["`IN ('0', '6')`."],
  "SELECT COUNT(*) AS weekend_flights FROM flights WHERE strftime('%w', depart_date) IN ('0', '6');")
p("Return pairs", "H", "self-join", "Find city pairs that have flights in both directions. List each pair once as (origin, destination) with origin alphabetically smaller.", ["Self-join flights where origin/destination are swapped; use `DISTINCT`."],
  "SELECT DISTINCT a.origin AS city_a, a.destination AS city_b FROM flights a JOIN flights b ON a.origin = b.destination AND a.destination = b.origin WHERE a.origin < a.destination;")
p("Most popular routes", "M", "group-by", "The five most frequent origin-destination routes with their flight counts. Ties by origin then destination.", ["Group by both columns."],
  "SELECT origin, destination, COUNT(*) AS flights FROM flights GROUP BY origin, destination ORDER BY flights DESC, origin, destination LIMIT 5;", ordered=True)
p("Average price per hour", "M", "expressions", "For each airline show the average base price per flight hour (base price divided by duration in hours), rounded to 2 decimals.", ["Average the ratio per flight."],
  "SELECT a.name, ROUND(AVG(f.base_price / (f.duration_min / 60.0)), 2) AS price_per_hour FROM flights f JOIN airlines a ON a.code = f.airline_code GROUP BY a.code, a.name;")
p("Passengers with multiple bookings", "M", "having", "List passengers (by name) who made more than one booking. Show name and count, by count then name.", ["`HAVING COUNT(*) > 1`."],
  "SELECT passenger, COUNT(*) AS bookings FROM bookings GROUP BY passenger HAVING COUNT(*) > 1 ORDER BY bookings DESC, passenger;", ordered=True)
p("Cheapest flight per origin", "M", "correlated-subquery", "For each origin airport show the cheapest flight (id and base price).", ["Compare with the minimum price of the same origin."],
  "SELECT f.origin, f.id, f.base_price FROM flights f WHERE f.base_price = (SELECT MIN(f2.base_price) FROM flights f2 WHERE f2.origin = f.origin);")
p("Longest flight per airline", "M", "correlated-subquery", "For each airline code show its longest flight (id and duration).", ["Compare with the airline's maximum duration."],
  "SELECT f.airline_code, f.id, f.duration_min FROM flights f WHERE f.duration_min = (SELECT MAX(f2.duration_min) FROM flights f2 WHERE f2.airline_code = f.airline_code);")
p("Spend per passenger tier", "H", "case", "Classify passengers by total fare spent: `bronze` under 1000, `silver` 1000 to under 3000, `gold` 3000 or more. Count passengers per tier.", ["Aggregate per passenger in a subquery, then CASE."],
  "SELECT CASE WHEN total < 1000 THEN 'bronze' WHEN total < 3000 THEN 'silver' ELSE 'gold' END AS tier, COUNT(*) AS passengers FROM (SELECT passenger, SUM(fare) AS total FROM bookings GROUP BY passenger) GROUP BY tier;")
p("Most expensive booking per class", "H", "ranking", "For each seat class show the booking with the highest fare (booking id, passenger, fare).", ["`ROW_NUMBER() OVER (PARTITION BY seat_class ORDER BY fare DESC)`."],
  "WITH r AS (SELECT id, passenger, seat_class, fare, ROW_NUMBER() OVER (PARTITION BY seat_class ORDER BY fare DESC, id) AS rn FROM bookings) SELECT seat_class, id, passenger, fare FROM r WHERE rn = 1;")
p("Top three routes per airline", "H", "ranking", "For each airline, rank routes (origin, destination) by number of flights and show the top route with its count (ties: alphabetical origin then destination).", ["Rank in a CTE."],
  "WITH r AS (SELECT airline_code, origin, destination, COUNT(*) AS flights FROM flights GROUP BY airline_code, origin, destination), k AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY airline_code ORDER BY flights DESC, origin, destination) AS rn FROM r) SELECT airline_code, origin, destination, flights FROM k WHERE rn = 1;")
p("Running revenue by month", "H", "running-total", "Monthly booking revenue (by departure month) with a cumulative total, both rounded to 2 decimals. Earliest first.", ["Monthly sum in a CTE, then running sum."],
  "WITH m AS (SELECT strftime('%Y-%m', f.depart_date) AS month, SUM(b.fare) AS revenue FROM bookings b JOIN flights f ON f.id = b.flight_id GROUP BY month) SELECT month, ROUND(revenue, 2) AS revenue, ROUND(SUM(revenue) OVER (ORDER BY month), 2) AS cumulative FROM m ORDER BY month;", ordered=True)
p("Airline market share", "H", "window-functions", "Each airline's share of total booking revenue as a percentage rounded to 1 decimal. Highest first.", ["Window total over grouped rows."],
  "WITH r AS (SELECT a.name, SUM(b.fare) AS revenue FROM bookings b JOIN flights f ON f.id = b.flight_id JOIN airlines a ON a.code = f.airline_code GROUP BY a.code, a.name) SELECT name, ROUND(100.0 * revenue / SUM(revenue) OVER (), 1) AS share_pct FROM r ORDER BY share_pct DESC;", ordered=True)
p("Previous flight on the same route", "H", "window-functions", "For flights departing from `LHR`, ordered by date then id, show the id of the previous LHR departure and the days between them (NULL for the first).", ["`LAG` over all flights from LHR."],
  "SELECT id, depart_date, LAG(id) OVER (ORDER BY depart_date, id) AS previous_id, CAST(julianday(depart_date) - julianday(LAG(depart_date) OVER (ORDER BY depart_date, id)) AS INTEGER) AS gap_days FROM flights WHERE origin = 'LHR' ORDER BY depart_date, id;", ordered=True)
p("Connecting itineraries", "H", "self-join", "Find two-leg itineraries starting at LHR: a first flight from LHR to some airport X, and a second flight leaving X on the same day or up to 30 days later (to anywhere except back to LHR). For each connecting airport X show the number of such (first, second) flight pairs. Show the top 5, ordered by pairs descending then airport.", ["Self-join flights on `a.destination = b.origin` with a date window."],
  "SELECT a.destination AS via, COUNT(*) AS pairs FROM flights a JOIN flights b ON b.origin = a.destination AND b.destination <> 'LHR' AND b.depart_date >= a.depart_date AND julianday(b.depart_date) - julianday(a.depart_date) <= 30 WHERE a.origin = 'LHR' GROUP BY a.destination ORDER BY pairs DESC, via LIMIT 5;", ordered=True)
p("Reachable cities in two hops", "H", "recursive", "Starting from LHR, list the destinations reachable with at most 2 flights (ignoring dates) together with the minimum number of hops. Order by hops then airport code.", ["Recursive CTE over distinct routes; take `MIN(hops)`."],
  "WITH RECURSIVE routes AS (SELECT DISTINCT origin, destination FROM flights), reach(code, hops) AS (SELECT destination, 1 FROM routes WHERE origin = 'LHR' UNION ALL SELECT r.destination, reach.hops + 1 FROM reach JOIN routes r ON r.origin = reach.code WHERE reach.hops < 2) SELECT code, MIN(hops) AS hops FROM reach WHERE code <> 'LHR' GROUP BY code ORDER BY hops, code;", ordered=True)
p("Passenger class pivot per airline", "H", "pivot", "For each airline show the number of bookings by `economy`, `business` and `first` as three columns.", ["Conditional counts."],
  "SELECT a.name, SUM(b.seat_class = 'economy') AS economy, SUM(b.seat_class = 'business') AS business, SUM(b.seat_class = 'first') AS first FROM bookings b JOIN flights f ON f.id = b.flight_id JOIN airlines a ON a.code = f.airline_code GROUP BY a.code, a.name;")
p("Months where cancellations spiked", "H", "having", "List months (YYYY-MM) in which more than 5% of departing flights were cancelled. Show month and the percentage rounded to 1 decimal.", ["Average a 0/1 flag per month and filter in `HAVING`."],
  "SELECT strftime('%Y-%m', depart_date) AS month, ROUND(100.0 * SUM(status = 'cancelled') / COUNT(*), 1) AS cancelled_pct FROM flights GROUP BY month HAVING 100.0 * SUM(status = 'cancelled') / COUNT(*) > 5;")
p("Refund cancelled bookings", "M", "dml", "Delete bookings for cancelled flights, then report the total fare of the remaining bookings rounded to 2 decimals.", ["`DELETE FROM bookings WHERE flight_id IN (SELECT id FROM flights WHERE status = 'cancelled')`."],
  "DELETE FROM bookings WHERE flight_id IN (SELECT id FROM flights WHERE status = 'cancelled'); SELECT ROUND(SUM(fare), 2) AS remaining_fare FROM bookings;")
p("Upgrade to business", "M", "dml", "Upgrade all economy bookings on flight 1 to `business` and then list the seat class counts for flight 1.", ["`UPDATE bookings SET seat_class = 'business' ...`."],
  "UPDATE bookings SET seat_class = 'business' WHERE flight_id = 1 AND seat_class = 'economy'; SELECT seat_class, COUNT(*) AS n FROM bookings WHERE flight_id = 1 GROUP BY seat_class;")
p("Airport name patterns", "E", "like", "List airports whose city name has exactly 5 letters (`_____`).", ["`LIKE '_____'` matches any five characters."],
  "SELECT code, city FROM airports WHERE city LIKE '_____';")
p("Country names merged", "M", "set-ops", "List all countries that appear either as an airline country or an airport country, once each.", ["`UNION`."],
  "SELECT country FROM airlines UNION SELECT country FROM airports;")
p("Countries with airports but no airlines", "M", "set-ops", "List countries that have an airport but no airline based there.", ["`EXCEPT`."],
  "SELECT country FROM airports EXCEPT SELECT country FROM airlines;")
p("Countries with both", "M", "set-ops", "List countries that have both an airline and an airport.", ["`INTERSECT`."],
  "SELECT country FROM airlines INTERSECT SELECT country FROM airports;")
p("Passengers by first letter", "E", "strings", "Count bookings by the first letter of the passenger's name. Show letter and count, letters in alphabetical order.", ["`substr(passenger, 1, 1)`."],
  "SELECT substr(passenger, 1, 1) AS letter, COUNT(*) AS bookings FROM bookings GROUP BY letter ORDER BY letter;", ordered=True)
