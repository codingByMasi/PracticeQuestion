import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import SqlSet

S = SqlSet("stocks", ["tickers", "prices"])
p = S.p

p("Ticker list", "E", "select", "List every ticker symbol with its company and sector.", ["Select three columns."], "SELECT symbol, company, sector FROM tickers;")
p("Technology stocks", "E", "where", "List the symbols of stocks in the Technology sector.", ["`sector = 'Technology'`."], "SELECT symbol, company FROM tickers WHERE sector = 'Technology';")
p("Price rows for one day", "E", "where", "Show the closing price of every ticker on 2024-03-15.", ["Filter on `trade_date`."],
  "SELECT symbol, close FROM prices WHERE trade_date = '2024-03-15';")
p("High volume days", "E", "where", "Count price rows where volume exceeded 800,000.", ["Numeric filter."], "SELECT COUNT(*) AS busy_days FROM prices WHERE volume > 800000;")
p("ACME history head", "E", "order-by", "List the first five trading days of `ACME` with the closing price.", ["Order by date, limit 5."],
  "SELECT trade_date, close FROM prices WHERE symbol = 'ACME' ORDER BY trade_date LIMIT 5;", ordered=True)
p("Highest closing price", "E", "aggregate", "What is the highest closing price ever recorded across all tickers? Show symbol, date and price.", ["Order by close desc and take one."],
  "SELECT symbol, trade_date, close FROM prices ORDER BY close DESC LIMIT 1;")
p("Price rows per ticker", "E", "group-by", "Count the number of price rows per symbol.", ["`GROUP BY symbol`."], "SELECT symbol, COUNT(*) AS days FROM prices GROUP BY symbol;")
p("Average close per ticker", "E", "group-by", "Average closing price per symbol rounded to 2 decimals.", ["`ROUND(AVG(close), 2)`."],
  "SELECT symbol, ROUND(AVG(close), 2) AS avg_close FROM prices GROUP BY symbol;")
p("Daily range", "E", "expressions", "For BYTE on its first five trading days show the date and the daily range (high minus low) rounded to 2 decimals.", ["`ROUND(high - low, 2)`."],
  "SELECT trade_date, ROUND(high - low, 2) AS day_range FROM prices WHERE symbol = 'BYTE' ORDER BY trade_date LIMIT 5;", ordered=True)
p("Up days and down days", "E", "case", "For symbol `CLOUD`, count days that closed above their open (`up`), below (`down`) or equal (`flat`).", ["`CASE` and group."],
  "SELECT CASE WHEN close > open THEN 'up' WHEN close < open THEN 'down' ELSE 'flat' END AS direction, COUNT(*) AS days FROM prices WHERE symbol = 'CLOUD' GROUP BY direction;")
p("Prices with company names", "E", "join", "Show company name and closing price for all rows on 2024-03-04.", ["Join prices to tickers."],
  "SELECT t.company, p.close FROM prices p JOIN tickers t ON t.symbol = p.symbol WHERE p.trade_date = '2024-03-04';")
p("Sector average volume", "M", "join", "Average daily volume per sector (rounded to the nearest whole number).", ["Join, group by sector."],
  "SELECT t.sector, ROUND(AVG(p.volume)) AS avg_volume FROM prices p JOIN tickers t ON t.symbol = p.symbol GROUP BY t.sector;")
p("Best and worst close per ticker", "M", "aggregate", "For each symbol show its lowest and highest closing price.", ["`MIN`/`MAX` per group."],
  "SELECT symbol, MIN(close) AS low_close, MAX(close) AS high_close FROM prices GROUP BY symbol;")
p("First and last close", "M", "correlated-subquery", "For each symbol show the closing price on its first trading day and on its last trading day.", ["Join to the min/max dates, or use window functions."],
  "SELECT f.symbol, f.close AS first_close, l.close AS last_close FROM prices f JOIN prices l ON l.symbol = f.symbol WHERE f.trade_date = (SELECT MIN(trade_date) FROM prices WHERE symbol = f.symbol) AND l.trade_date = (SELECT MAX(trade_date) FROM prices WHERE symbol = f.symbol);")
p("Total return", "M", "expressions", "For each symbol compute total return as percentage change from first close to last close, rounded to 1 decimal. Highest first.", ["Compare last and first close."],
  "WITH r AS (SELECT symbol, FIRST_VALUE(close) OVER (PARTITION BY symbol ORDER BY trade_date) AS first_close, FIRST_VALUE(close) OVER (PARTITION BY symbol ORDER BY trade_date DESC) AS last_close FROM prices) SELECT DISTINCT symbol, ROUND(100.0 * (last_close - first_close) / first_close, 1) AS return_pct FROM r ORDER BY return_pct DESC;", ordered=True)
p("Volatile days", "M", "expressions", "List the 5 days with the largest intraday range as a percentage of the open price (high minus low divided by open), with symbol, date and percentage rounded to 2 decimals. Ties by symbol then date.", ["Compute the ratio in the `ORDER BY`."],
  "SELECT symbol, trade_date, ROUND(100.0 * (high - low) / open, 2) AS range_pct FROM prices ORDER BY range_pct DESC, symbol, trade_date LIMIT 5;", ordered=True)
p("Biggest daily gains", "M", "window-functions", "The five biggest day-over-day closing price increases (in percent, rounded to 2 decimals) with symbol and date. Ties by symbol.", ["`LAG(close)` partitioned by symbol."],
  "WITH g AS (SELECT symbol, trade_date, 100.0 * (close - LAG(close) OVER (PARTITION BY symbol ORDER BY trade_date)) / LAG(close) OVER (PARTITION BY symbol ORDER BY trade_date) AS chg FROM prices) SELECT symbol, trade_date, ROUND(chg, 2) AS change_pct FROM g WHERE chg IS NOT NULL ORDER BY chg DESC, symbol LIMIT 5;", ordered=True)
p("Weekly volume", "M", "dates", "Total volume per ISO week of the year (`strftime('%W')`) for symbol `FOOD`. Show week and volume, ordered by week.", ["`strftime('%W', trade_date)`."],
  "SELECT strftime('%W', trade_date) AS week, SUM(volume) AS volume FROM prices WHERE symbol = 'FOOD' GROUP BY week ORDER BY week;", ordered=True)
p("Mondays versus Fridays", "M", "dates", "Average closing change (close minus open) on Mondays and on Fridays, rounded to 3 decimals. Two rows labelled `Monday` and `Friday`.", ["`strftime('%w')` is 1 for Monday and 5 for Friday."],
  "SELECT CASE strftime('%w', trade_date) WHEN '1' THEN 'Monday' ELSE 'Friday' END AS weekday, ROUND(AVG(close - open), 3) AS avg_change FROM prices WHERE strftime('%w', trade_date) IN ('1', '5') GROUP BY weekday;")
p("Three-day moving average", "H", "window-functions", "For `ACME`, show each trading day's close and the average of the close and the two previous closes (rounded to 2 decimals). Only from the third trading day on. Order by date.", ["Window frame of 3 rows; filter on a row number."],
  "WITH m AS (SELECT trade_date, close, ROUND(AVG(close) OVER (ORDER BY trade_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS ma3, ROW_NUMBER() OVER (ORDER BY trade_date) AS rn FROM prices WHERE symbol = 'ACME') SELECT trade_date, close, ma3 FROM m WHERE rn >= 3 ORDER BY trade_date;", ordered=True)
p("Cumulative volume", "H", "running-total", "For `DRUG` show the first 10 trading days with daily volume and cumulative volume.", ["Running `SUM(volume) OVER (ORDER BY trade_date)`."],
  "SELECT trade_date, volume, SUM(volume) OVER (ORDER BY trade_date) AS cumulative_volume FROM prices WHERE symbol = 'DRUG' ORDER BY trade_date LIMIT 10;", ordered=True)
p("Rolling high", "H", "window-functions", "For `ENRG`, show each day's close and the highest close seen so far (running maximum). First 10 days.", ["`MAX(close) OVER (ORDER BY trade_date)`."],
  "SELECT trade_date, close, MAX(close) OVER (ORDER BY trade_date) AS running_high FROM prices WHERE symbol = 'ENRG' ORDER BY trade_date LIMIT 10;", ordered=True)
p("Drawdown from the peak", "H", "window-functions", "For `GRID`, show date, close and drawdown percent from the running high (zero at new highs), rounded to 2 decimals. Return the 5 days with the deepest drawdown (most negative first, ties by date).", ["Running max in a CTE."],
  "WITH r AS (SELECT trade_date, close, MAX(close) OVER (ORDER BY trade_date) AS peak FROM prices WHERE symbol = 'GRID') SELECT trade_date, close, ROUND(100.0 * (close - peak) / peak, 2) AS drawdown_pct FROM r ORDER BY drawdown_pct, trade_date LIMIT 5;", ordered=True)
p("Rank of the day by volume", "H", "ranking", "For `HOME` rank all trading days by volume (1 = highest) with `RANK()` and show the top 5 (rank, date, volume). Ties by date.", ["`RANK() OVER (ORDER BY volume DESC)`."],
  "SELECT rk, trade_date, volume FROM (SELECT trade_date, volume, RANK() OVER (ORDER BY volume DESC) AS rk FROM prices WHERE symbol = 'HOME') WHERE rk <= 5 ORDER BY rk, trade_date;", ordered=True)
p("Best performer each week", "H", "ranking", "For each week (`strftime('%W')`) find the symbol with the highest weekly return (last close of the week divided by first close of the week minus one, as a percentage rounded to 2 decimals). Show week, symbol, return. Ties by symbol.", ["Per symbol-week first and last close with `FIRST_VALUE`, then rank weeks."],
  "WITH w AS (SELECT DISTINCT symbol, strftime('%W', trade_date) AS week, FIRST_VALUE(close) OVER (PARTITION BY symbol, strftime('%W', trade_date) ORDER BY trade_date) AS first_close, FIRST_VALUE(close) OVER (PARTITION BY symbol, strftime('%W', trade_date) ORDER BY trade_date DESC) AS last_close FROM prices), r AS (SELECT week, symbol, 100.0 * (last_close - first_close) / first_close AS ret FROM w), k AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY week ORDER BY ret DESC, symbol) AS rn FROM r) SELECT week, symbol, ROUND(ret, 2) AS return_pct FROM k WHERE rn = 1 ORDER BY week;", ordered=True)
p("Correlated sector pairs", "H", "self-join", "For each trading day compare the technology tickers: list days where BYTE and CLOUD both closed up (close above open). Show the count of such days as `both_up_days`.", ["Self-join prices on date."],
  "SELECT COUNT(*) AS both_up_days FROM prices a JOIN prices b ON a.trade_date = b.trade_date AND a.symbol = 'BYTE' AND b.symbol = 'CLOUD' WHERE a.close > a.open AND b.close > b.open;")
p("Longest winning streak", "H", "gaps-islands", "For `FOOD`, find the longest run of consecutive trading days that closed above the previous day's close. Show the length as `longest_streak`.", ["Flag up days, then islands by row-number differences."],
  "WITH d AS (SELECT trade_date, close > LAG(close) OVER (ORDER BY trade_date) AS up FROM prices WHERE symbol = 'FOOD'), n AS (SELECT trade_date, ROW_NUMBER() OVER (ORDER BY trade_date) AS rn FROM d WHERE up = 1), g AS (SELECT rn - ROW_NUMBER() OVER (ORDER BY rn) AS grp FROM n) SELECT COALESCE(MAX(c), 0) AS longest_streak FROM (SELECT COUNT(*) AS c FROM g GROUP BY grp);")
p("Volume weighted average price", "M", "expressions", "Volume-weighted average close per symbol (sum of close times volume divided by total volume), rounded to 2 decimals.", ["Weighted average formula."],
  "SELECT symbol, ROUND(SUM(close * volume) * 1.0 / SUM(volume), 2) AS vwap FROM prices GROUP BY symbol;")
p("Price percent of sector leader", "H", "window-functions", "On 2024-04-15 show each ticker's close as a percentage of the highest close within its sector that day (rounded to 1 decimal). Show symbol, sector and percentage.", ["`MAX(close) OVER (PARTITION BY sector)`."],
  "SELECT p.symbol, t.sector, ROUND(100.0 * p.close / MAX(p.close) OVER (PARTITION BY t.sector), 1) AS pct_of_leader FROM prices p JOIN tickers t ON t.symbol = p.symbol WHERE p.trade_date = '2024-04-15';")
p("Quartile of closing price", "H", "window-functions", "For 2024-04-15 assign each ticker to a price quartile with `NTILE(4)` by close (1 = lowest). Show symbol, close and quartile, ordered by close.", ["`NTILE(4) OVER (ORDER BY close)`."],
  "SELECT symbol, close, NTILE(4) OVER (ORDER BY close) AS quartile FROM prices WHERE trade_date = '2024-04-15' ORDER BY close;", ordered=True)
p("Sector normalised index", "H", "window-functions", "For each sector and trading date compute the average close across its tickers, then index it to 100 on the first date. Show sector, date, index rounded to 2 decimals for dates in the first week (2024-03-01 to 2024-03-07). Order by sector, date.", ["Average per sector-date, divide by `FIRST_VALUE` over the sector."],
  "WITH s AS (SELECT t.sector, p.trade_date, AVG(p.close) AS avg_close FROM prices p JOIN tickers t ON t.symbol = p.symbol GROUP BY t.sector, p.trade_date) SELECT sector, trade_date, ROUND(100.0 * avg_close / FIRST_VALUE(avg_close) OVER (PARTITION BY sector ORDER BY trade_date), 2) AS idx FROM s WHERE trade_date <= '2024-03-07' ORDER BY sector, trade_date;", ordered=True)
p("Dollar volume ranking", "M", "ranking", "Rank tickers by total dollar volume (sum of close times volume), showing symbol, total rounded to the nearest whole number, and rank with `RANK()`. Order by rank.", ["`RANK() OVER (ORDER BY total DESC)`."],
  "SELECT symbol, ROUND(SUM(close * volume)) AS dollar_volume, RANK() OVER (ORDER BY SUM(close * volume) DESC) AS rk FROM prices GROUP BY symbol ORDER BY rk;", ordered=True)
p("Sector counts of up days", "M", "group-by", "For each sector count ticker-days that closed higher than they opened.", ["Join and filter."],
  "SELECT t.sector, COUNT(*) AS up_days FROM prices p JOIN tickers t ON t.symbol = p.symbol WHERE p.close > p.open GROUP BY t.sector;")
p("Split-adjusted prices", "M", "dml", "Pretend `ACME` did a 2-for-1 split on 2024-03-15: halve the open/high/low/close prices of ACME rows before that date with an `UPDATE`, double the volume, then show ACME's average close rounded to 2 decimals.", ["`UPDATE prices SET open = open / 2, ... WHERE symbol = 'ACME' AND trade_date < '2024-03-15'`."],
  "UPDATE prices SET open = open / 2, high = high / 2, low = low / 2, close = close / 2, volume = volume * 2 WHERE symbol = 'ACME' AND trade_date < '2024-03-15'; SELECT ROUND(AVG(close), 2) AS avg_close FROM prices WHERE symbol = 'ACME';")
p("Delist a ticker", "M", "dml", "Delete all price rows of the `HOME` ticker and the ticker itself, then count the remaining tickers.", ["Two `DELETE` statements."],
  "DELETE FROM prices WHERE symbol = 'HOME'; DELETE FROM tickers WHERE symbol = 'HOME'; SELECT COUNT(*) AS tickers FROM tickers;")
p("Calendar of missing days", "H", "recursive", "Generate every calendar date from 2024-03-01 to 2024-03-10 with a recursive CTE and list those that have no price rows for any ticker. These are the weekends.", ["Recursive CTE with `date(d, '+1 day')`."],
  "WITH RECURSIVE cal(d) AS (SELECT '2024-03-01' UNION ALL SELECT date(d, '+1 day') FROM cal WHERE d < '2024-03-10') SELECT d AS missing_date FROM cal WHERE d NOT IN (SELECT trade_date FROM prices);")
p("Weekly candles", "H", "group-by", "Build weekly candles for `ENRG`: for each week (`strftime('%W')`) show the first open, highest high, lowest low and last close. Order by week.", ["`FIRST_VALUE`/`LAST_VALUE` or correlated subqueries for the first open and last close."],
  "WITH w AS (SELECT strftime('%W', trade_date) AS week, trade_date, open, high, low, close FROM prices WHERE symbol = 'ENRG') SELECT week, (SELECT open FROM w x WHERE x.week = w.week ORDER BY trade_date LIMIT 1) AS open, MAX(high) AS high, MIN(low) AS low, (SELECT close FROM w x WHERE x.week = w.week ORDER BY trade_date DESC LIMIT 1) AS close FROM w GROUP BY week ORDER BY week;", ordered=True)
p("Average true range", "H", "window-functions", "For `GRID`, true range of a day is the largest of: high minus low, absolute high minus previous close, absolute low minus previous close. Show the average true range over days that have a previous close, rounded to 3 decimals.", ["Use `LAG(close)` and `MAX(a, b, c)` (scalar max)."],
  "WITH t AS (SELECT high, low, LAG(close) OVER (ORDER BY trade_date) AS pc FROM prices WHERE symbol = 'GRID') SELECT ROUND(AVG(MAX(high - low, ABS(high - pc), ABS(low - pc))), 3) AS atr FROM t WHERE pc IS NOT NULL;")
p("Top sector by average close", "M", "subquery", "Which sector has the highest average closing price across all its price rows? Show sector and average rounded to 2 decimals.", ["Group, order, limit 1."],
  "SELECT t.sector, ROUND(AVG(p.close), 2) AS avg_close FROM prices p JOIN tickers t ON t.symbol = p.symbol GROUP BY t.sector ORDER BY AVG(p.close) DESC LIMIT 1;")
