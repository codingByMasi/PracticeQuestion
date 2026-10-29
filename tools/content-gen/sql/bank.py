import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import SqlSet

S = SqlSet("bank", ["customers", "accounts", "transactions"])
p = S.p

p("Customer directory", "E", "select", "List each customer's name, city and segment.", ["Three columns."], "SELECT name, city, segment FROM customers;")
p("Business customers", "E", "where", "List the names of customers in the `business` segment.", ["`segment = 'business'`."], "SELECT name FROM customers WHERE segment = 'business';")
p("Closed accounts", "E", "where", "How many accounts are closed (`closed = 1`)?", ["Count rows with `closed = 1`."], "SELECT COUNT(*) AS closed_accounts FROM accounts WHERE closed = 1;")
p("Big deposits", "E", "where", "List deposits of more than 2000. Show id, date and amount, and keep the first 10 by id.", ["Filter on kind and amount."],
  "SELECT id, tx_date, amount FROM transactions WHERE kind = 'deposit' AND amount > 2000 ORDER BY id LIMIT 10;", ordered=True)
p("Fees charged", "E", "aggregate", "What is the total amount of fees charged (the sum is negative)?", ["Sum amounts where `kind = 'fee'`."], "SELECT SUM(amount) AS total_fees FROM transactions WHERE kind = 'fee';")
p("Merchants seen", "E", "distinct", "List the distinct merchants that appear in the ledger (ignore NULL).", ["`WHERE merchant IS NOT NULL`."],
  "SELECT DISTINCT merchant FROM transactions WHERE merchant IS NOT NULL;")
p("Latest transactions", "E", "order-by", "The 5 latest transactions by date (ties by id descending). Show id, date, amount.", ["Sort by date desc then id desc."],
  "SELECT id, tx_date, amount FROM transactions ORDER BY tx_date DESC, id DESC LIMIT 5;", ordered=True)
p("Accounts per type", "E", "group-by", "Count accounts of each type.", ["`GROUP BY type`."], "SELECT type, COUNT(*) AS accounts FROM accounts GROUP BY type;")
p("Transactions per kind", "E", "group-by", "For each transaction kind show the count and the total amount rounded to 2 decimals.", ["Two aggregates."],
  "SELECT kind, COUNT(*) AS n, ROUND(SUM(amount), 2) AS total FROM transactions GROUP BY kind;")
p("Customers per city", "E", "group-by", "Count customers in each city.", ["Group by city."], "SELECT city, COUNT(*) AS customers FROM customers GROUP BY city;")
p("Accounts with owners", "E", "join", "For accounts 1 to 6 show the account id, type and the owner's name.", ["Join to customers."],
  "SELECT a.id, a.type, c.name FROM accounts a JOIN customers c ON c.id = a.customer_id WHERE a.id <= 6;")
p("Accounts per customer", "M", "left-join", "For every customer show the number of accounts they hold. Show only customers with 3 accounts.", ["Group and `HAVING`."],
  "SELECT c.name, COUNT(*) AS accounts FROM customers c JOIN accounts a ON a.customer_id = c.id GROUP BY c.id, c.name HAVING COUNT(*) = 3;")
p("Balance per account", "M", "aggregate", "Compute each account's balance as the sum of its transactions (rounded to 2 decimals). Show the five lowest balances, ties by account id.", ["Group by account."],
  "SELECT account_id, ROUND(SUM(amount), 2) AS balance FROM transactions GROUP BY account_id ORDER BY balance, account_id LIMIT 5;", ordered=True)
p("Overdrawn accounts", "M", "having", "List accounts whose transaction total is negative. Show account id and balance rounded to 2 decimals.", ["`HAVING SUM(amount) < 0`."],
  "SELECT account_id, ROUND(SUM(amount), 2) AS balance FROM transactions GROUP BY account_id HAVING SUM(amount) < 0;")
p("Customer net worth", "M", "multi-join", "Total balance per customer across all their accounts (rounded to 2 decimals). Top five, ties by name.", ["Join customers, accounts and transactions."],
  "SELECT c.name, ROUND(SUM(t.amount), 2) AS balance FROM customers c JOIN accounts a ON a.customer_id = c.id JOIN transactions t ON t.account_id = a.id GROUP BY c.id, c.name ORDER BY balance DESC, c.name LIMIT 5;", ordered=True)
p("Spending by merchant", "M", "group-by", "Total spent per merchant (positive numbers), biggest first. Round to 2 decimals.", ["Negate the sum of purchases."],
  "SELECT merchant, ROUND(-SUM(amount), 2) AS spent FROM transactions WHERE kind = 'purchase' GROUP BY merchant ORDER BY spent DESC;", ordered=True)
p("Average purchase", "M", "aggregate", "Average purchase size (positive) per merchant, rounded to 2 decimals, for merchants with at least 10 purchases.", ["`HAVING COUNT(*) >= 10`."],
  "SELECT merchant, ROUND(-AVG(amount), 2) AS avg_purchase FROM transactions WHERE kind = 'purchase' GROUP BY merchant HAVING COUNT(*) >= 10;")
p("Activity by month", "M", "dates", "For each month show the number of transactions and total deposits. Earliest first.", ["`strftime('%Y-%m', tx_date)` and conditional sum."],
  "SELECT strftime('%Y-%m', tx_date) AS month, COUNT(*) AS transactions, ROUND(SUM(CASE WHEN kind = 'deposit' THEN amount ELSE 0 END), 2) AS deposits FROM transactions GROUP BY month ORDER BY month;", ordered=True)
p("Weekend spending", "M", "dates", "Total purchase spending (positive) on weekends versus weekdays: two rows `weekend` / `weekday`.", ["Weekday from `strftime('%w')`."],
  "SELECT CASE WHEN strftime('%w', tx_date) IN ('0', '6') THEN 'weekend' ELSE 'weekday' END AS day_type, ROUND(-SUM(amount), 2) AS spent FROM transactions WHERE kind = 'purchase' GROUP BY day_type;")
p("Customers with closed accounts", "M", "exists", "List customers who have at least one closed account.", ["`EXISTS`."],
  "SELECT c.name FROM customers c WHERE EXISTS (SELECT 1 FROM accounts a WHERE a.customer_id = c.id AND a.closed = 1);")
p("Fee-heavy accounts", "M", "having", "List accounts that were charged at least 3 fees. Show account id and the fee total rounded to 2 decimals.", ["Filter on fees then `HAVING COUNT(*) >= 3`."],
  "SELECT account_id, ROUND(SUM(amount), 2) AS fees FROM transactions WHERE kind = 'fee' GROUP BY account_id HAVING COUNT(*) >= 3;", allow_empty=True) if False else None
p("Accounts with fees", "M", "having", "List accounts that were charged at least 2 fees, with the fee total (rounded to 2 decimals).", ["Filter on fees then `HAVING COUNT(*) >= 2`."],
  "SELECT account_id, ROUND(SUM(amount), 2) AS fees FROM transactions WHERE kind = 'fee' GROUP BY account_id HAVING COUNT(*) >= 2;")
p("Segment comparison", "M", "multi-join", "For each customer segment show the average account balance (average of per-account totals, rounded to 2 decimals).", ["Per-account totals in a subquery."],
  "SELECT c.segment, ROUND(AVG(b.balance), 2) AS avg_balance FROM (SELECT account_id, SUM(amount) AS balance FROM transactions GROUP BY account_id) b JOIN accounts a ON a.id = b.account_id JOIN customers c ON c.id = a.customer_id GROUP BY c.segment;")
p("Largest withdrawal per account", "M", "correlated-subquery", "For accounts 1 to 5, show the largest withdrawal in absolute value (positive number). Skip accounts without withdrawals.", ["`MAX(-amount)` on withdrawals."],
  "SELECT account_id, MAX(-amount) AS largest_withdrawal FROM transactions WHERE kind = 'withdrawal' AND account_id <= 5 GROUP BY account_id;")
p("Salary-like deposits", "M", "having", "Find accounts that received at least 3 deposits of 1000 or more. Show account id and number of such deposits.", ["Filter, group, having."],
  "SELECT account_id, COUNT(*) AS big_deposits FROM transactions WHERE kind = 'deposit' AND amount >= 1000 GROUP BY account_id HAVING COUNT(*) >= 3;")
p("Months since joining", "M", "dates", "For the five customers who joined most recently show name and months between joining and 2024-06-30 (days / 30.44, rounded down). Ties by name.", ["`julianday` difference."],
  "SELECT name, CAST((julianday('2024-06-30') - julianday(joined)) / 30.44 AS INTEGER) AS months FROM customers ORDER BY joined DESC, name LIMIT 5;", ordered=True)
p("Running balance of account 1", "H", "running-total", "For account 1 list its transactions in date order (ties by id) with a running balance rounded to 2 decimals.", ["`SUM(amount) OVER (ORDER BY tx_date, id)`."],
  "SELECT id, tx_date, amount, ROUND(SUM(amount) OVER (ORDER BY tx_date, id), 2) AS balance FROM transactions WHERE account_id = 1 ORDER BY tx_date, id;", ordered=True)
p("Lowest point of a balance", "H", "running-total", "For account 2 find the minimum running balance reached (rounded to 2 decimals).", ["Compute the running sum in a CTE then `MIN`."],
  "WITH r AS (SELECT SUM(amount) OVER (ORDER BY tx_date, id) AS balance FROM transactions WHERE account_id = 2) SELECT ROUND(MIN(balance), 2) AS lowest_balance FROM r;")
p("First overdraft date", "H", "running-total", "For each account whose running balance ever goes below zero, show the account id and the date of the first transaction that makes it negative.", ["Running sum per account, then the earliest negative row."],
  "WITH r AS (SELECT account_id, tx_date, id, SUM(amount) OVER (PARTITION BY account_id ORDER BY tx_date, id) AS balance FROM transactions) SELECT account_id, MIN(tx_date) AS first_negative FROM r WHERE balance < 0 GROUP BY account_id;")
p("Largest transaction per customer", "H", "ranking", "For each customer, find the transaction with the largest absolute amount (customer name, transaction id, amount). Ties go to the lowest id.", ["`ROW_NUMBER()` by `ABS(amount) DESC, id`."],
  "WITH r AS (SELECT a.customer_id, t.id, t.amount, ROW_NUMBER() OVER (PARTITION BY a.customer_id ORDER BY ABS(t.amount) DESC, t.id) AS rn FROM transactions t JOIN accounts a ON a.id = t.account_id) SELECT c.name, r.id AS transaction_id, r.amount FROM r JOIN customers c ON c.id = r.customer_id WHERE r.rn = 1;")
p("Spend rank within city", "H", "ranking", "Rank customers within their city by total purchase spending (1 = highest spender) using `RANK()`. Show city, rank, name and spend rounded to 2 decimals. Keep ranks 1 and 2, ordered by city, rank, name.", ["Totals per customer, then rank by city."],
  "WITH s AS (SELECT c.city, c.name, -SUM(t.amount) AS spent FROM transactions t JOIN accounts a ON a.id = t.account_id JOIN customers c ON c.id = a.customer_id WHERE t.kind = 'purchase' GROUP BY c.id), r AS (SELECT *, RANK() OVER (PARTITION BY city ORDER BY spent DESC) AS rk FROM s) SELECT city, rk, name, ROUND(spent, 2) AS spent FROM r WHERE rk <= 2 ORDER BY city, rk, name;", ordered=True)
p("Month over month spending", "H", "window-functions", "Monthly purchase spending (positive, rounded to 2 decimals) and the change from the previous month. NULL for the first month. Earliest first.", ["`LAG` over months."],
  "WITH m AS (SELECT strftime('%Y-%m', tx_date) AS month, -SUM(amount) AS spent FROM transactions WHERE kind = 'purchase' GROUP BY month) SELECT month, ROUND(spent, 2) AS spent, ROUND(spent - LAG(spent) OVER (ORDER BY month), 2) AS change FROM m ORDER BY month;", ordered=True)
p("Spend share per merchant", "H", "window-functions", "For each merchant show its share (percentage, 1 decimal) of all purchase spending. Largest share first.", ["Window total over merchants."],
  "WITH m AS (SELECT merchant, -SUM(amount) AS spent FROM transactions WHERE kind = 'purchase' GROUP BY merchant) SELECT merchant, ROUND(100.0 * spent / SUM(spent) OVER (), 1) AS share_pct FROM m ORDER BY share_pct DESC;", ordered=True)
p("Cumulative share of spending", "H", "window-functions", "Order merchants by spending (largest first, ties by name) and show the cumulative percentage of total spend after each merchant, rounded to 1 decimal.", ["Running sum divided by the grand total."],
  "WITH m AS (SELECT merchant, -SUM(amount) AS spent FROM transactions WHERE kind = 'purchase' GROUP BY merchant) SELECT merchant, ROUND(100.0 * SUM(spent) OVER (ORDER BY spent DESC, merchant) / SUM(spent) OVER (), 1) AS cumulative_pct FROM m ORDER BY spent DESC, merchant;", ordered=True)
p("Active days per account", "M", "group-by", "Number of distinct days with at least one transaction for the five busiest accounts (ties by account id).", ["`COUNT(DISTINCT tx_date)`."],
  "SELECT account_id, COUNT(DISTINCT tx_date) AS active_days FROM transactions GROUP BY account_id ORDER BY active_days DESC, account_id LIMIT 5;", ordered=True)
p("Longest quiet period", "H", "window-functions", "For account 3 find the longest gap in days between two consecutive transaction dates.", ["`LAG(tx_date)` then `MAX` of the difference."],
  "WITH d AS (SELECT tx_date, julianday(tx_date) - julianday(LAG(tx_date) OVER (ORDER BY tx_date, id)) AS gap FROM transactions WHERE account_id = 3) SELECT CAST(MAX(gap) AS INTEGER) AS longest_gap_days FROM d;")
p("Streak of daily activity", "H", "gaps-islands", "For account 3, group distinct transaction days into runs of consecutive calendar days and show the longest run length in days as `longest_streak`.", ["Subtract a row number from the day number to identify islands."],
  "WITH d AS (SELECT DISTINCT tx_date FROM transactions WHERE account_id = 3), g AS (SELECT CAST(julianday(tx_date) AS INTEGER) - ROW_NUMBER() OVER (ORDER BY tx_date) AS grp FROM d) SELECT MAX(c) AS longest_streak FROM (SELECT COUNT(*) AS c FROM g GROUP BY grp);")
p("Transfers by size band", "M", "case", "Classify transfers (negative amounts, kind `transfer`) as `small` (under 50), `medium` (50 to under 200) or `large`, and count each band.", ["Use the absolute value."],
  "SELECT CASE WHEN -amount < 50 THEN 'small' WHEN -amount < 200 THEN 'medium' ELSE 'large' END AS band, COUNT(*) AS transfers FROM transactions WHERE kind = 'transfer' GROUP BY band;")
p("Customers who never paid a fee", "M", "exists", "List customers none of whose accounts were ever charged a fee.", ["`NOT EXISTS` through accounts and transactions."],
  "SELECT c.name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM accounts a JOIN transactions t ON t.account_id = a.id WHERE a.customer_id = c.id AND t.kind = 'fee');")
p("Cities ranked by deposits", "M", "multi-join", "Total deposits per customer city, biggest first, rounded to 2 decimals.", ["Join up to customers."],
  "SELECT c.city, ROUND(SUM(t.amount), 2) AS deposits FROM transactions t JOIN accounts a ON a.id = t.account_id JOIN customers c ON c.id = a.customer_id WHERE t.kind = 'deposit' GROUP BY c.city ORDER BY deposits DESC;", ordered=True)
p("Account type pivot", "H", "pivot", "For each customer segment show total balance in `checking`, `savings` and `credit` accounts as three columns (rounded to 2 decimals, NULL treated as 0).", ["Conditional sums over account type."],
  "SELECT c.segment, ROUND(COALESCE(SUM(CASE WHEN a.type = 'checking' THEN t.amount END), 0), 2) AS checking, ROUND(COALESCE(SUM(CASE WHEN a.type = 'savings' THEN t.amount END), 0), 2) AS savings, ROUND(COALESCE(SUM(CASE WHEN a.type = 'credit' THEN t.amount END), 0), 2) AS credit FROM transactions t JOIN accounts a ON a.id = t.account_id JOIN customers c ON c.id = a.customer_id GROUP BY c.segment;")
p("Monthly cashflow", "H", "pivot", "For each month show `income` (sum of deposits) and `outgoing` (sum of everything else, as a positive number) with the net difference, all rounded to 2 decimals. Earliest first.", ["Conditional aggregation per month."],
  "SELECT strftime('%Y-%m', tx_date) AS month, ROUND(SUM(CASE WHEN kind = 'deposit' THEN amount ELSE 0 END), 2) AS income, ROUND(-SUM(CASE WHEN kind <> 'deposit' THEN amount ELSE 0 END), 2) AS outgoing, ROUND(SUM(amount), 2) AS net FROM transactions GROUP BY month ORDER BY month;", ordered=True)
p("Apply an overdraft fee", "M", "dml", "Insert a fee transaction of -35 (kind `fee`, date `2024-07-01`, id 901) for every account whose balance is negative, then report how many fee rows were inserted in total with that date.", ["`INSERT INTO ... SELECT` over a grouped query."],
  "INSERT INTO transactions (id, account_id, tx_date, amount, kind, merchant) SELECT 900 + ROW_NUMBER() OVER (ORDER BY account_id), account_id, '2024-07-01', -35, 'fee', NULL FROM transactions GROUP BY account_id HAVING SUM(amount) < 0; SELECT COUNT(*) AS inserted FROM transactions WHERE tx_date = '2024-07-01';")
p("Close dormant accounts", "M", "dml", "Mark as closed (`closed = 1`) all accounts that have no transactions after 2024-05-31, then count open accounts.", ["`UPDATE accounts SET closed = 1 WHERE id NOT IN (...)`."],
  "UPDATE accounts SET closed = 1 WHERE id NOT IN (SELECT account_id FROM transactions WHERE tx_date > '2024-05-31'); SELECT COUNT(*) AS open_accounts FROM accounts WHERE closed = 0;")
p("Customer names uppercase", "E", "strings", "Show customers in the city of Boston with their name in upper case.", ["`UPPER(name)`."],
  "SELECT UPPER(name) AS name FROM customers WHERE city = 'Boston';")
p("Top merchants per customer segment", "H", "ranking", "For each customer segment show its top merchant by purchase spending (segment, merchant, spent rounded to 2 decimals; ties by merchant).", ["Group by segment and merchant, rank."],
  "WITH s AS (SELECT c.segment, t.merchant, -SUM(t.amount) AS spent FROM transactions t JOIN accounts a ON a.id = t.account_id JOIN customers c ON c.id = a.customer_id WHERE t.kind = 'purchase' GROUP BY c.segment, t.merchant), r AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY segment ORDER BY spent DESC, merchant) AS rn FROM s) SELECT segment, merchant, ROUND(spent, 2) AS spent FROM r WHERE rn = 1;")
p("Customers above segment median", "H", "window-functions", "For each customer compute total purchase spending; list those who spend more than the average of their segment. Show name, segment and spend rounded to 2 decimals.", ["Window average per segment."],
  "WITH s AS (SELECT c.id, c.name, c.segment, -SUM(t.amount) AS spent FROM transactions t JOIN accounts a ON a.id = t.account_id JOIN customers c ON c.id = a.customer_id WHERE t.kind = 'purchase' GROUP BY c.id) SELECT name, segment, ROUND(spent, 2) AS spent FROM (SELECT *, AVG(spent) OVER (PARTITION BY segment) AS seg_avg FROM s) WHERE spent > seg_avg;")
p("First transaction of each account", "M", "window-functions", "For accounts 1 to 5 show the earliest transaction (date, id, amount); tie on date goes to the lowest id.", ["`ROW_NUMBER()` per account."],
  "WITH r AS (SELECT account_id, tx_date, id, amount, ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY tx_date, id) AS rn FROM transactions WHERE account_id <= 5) SELECT account_id, tx_date, id, amount FROM r WHERE rn = 1;")
p("Transactions before account opening", "M", "join", "Count transactions dated before the account's opening date.", ["Join transactions to accounts."],
  "SELECT COUNT(*) AS suspicious FROM transactions t JOIN accounts a ON a.id = t.account_id WHERE t.tx_date < a.opened;", allow_empty=True) if False else None
