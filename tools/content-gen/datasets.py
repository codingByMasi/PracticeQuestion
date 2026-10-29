"""Generates the seeded SQL datasets in content/datasets. Run: python3 tools/content-gen/datasets.py"""
import json, random, datetime, os

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "content", "datasets")
FIRST = "Ada Alan Grace Linus Margaret Ken Barbara Steve Mary Jack Indra Sheryl David Warren Abigail Ray Tim Olivia Liam Sofia Noah Emma Lucas Mia Ethan Ava Leo Zoe Omar Priya Chen Yuki Fatima Diego Nia Hugo Ines Kofi Lena Mateo Nora Raj Sana Tariq Uma Vera Wen Xavier Yara".split()
LAST = "Hopper Turing Lovelace Torvalds Hamilton Thompson Liskov Jobs Barra Ma Nooyi Sandberg Ogilvy Buffett Johnson Dalio Berners Chen Novak Rossi Smith Dubois Silva Tanaka Brown Muller Garcia Okafor Patel Kim Sato Haddad Lopez Mensah Costa Ivanov Singh Nguyen Moreau Larsen Khan Mehta Rivera Baker Ortiz Young Zhang Weber Adams".split()

def esc(v):
    if v is None: return "NULL"
    if isinstance(v, (int, float)): return repr(round(v, 2)) if isinstance(v, float) else str(v)
    return "'" + str(v).replace("'", "''") + "'"

def insert(table, cols, rows):
    out = []
    for i in range(0, len(rows), 50):
        chunk = rows[i:i+50]
        out.append(f"INSERT INTO {table} ({', '.join(cols)}) VALUES\n  " + ",\n  ".join("(" + ", ".join(esc(v) for v in r) + ")" for r in chunk) + ";")
    return "\n".join(out)

def date(rng, start, end):
    s = datetime.date.fromisoformat(start); e = datetime.date.fromisoformat(end)
    return (s + datetime.timedelta(days=rng.randint(0, (e - s).days))).isoformat()

def person(rng, used):
    while True:
        n = f"{rng.choice(FIRST)} {rng.choice(LAST)}"
        if n not in used:
            used.add(n); return n

def write(id_, title, desc, sql):
    open(f"{OUT}/{id_}.json", "w").write(json.dumps({"id": id_, "title": title, "description": desc}) + "\n")
    open(f"{OUT}/{id_}.sql", "w").write(sql.strip() + "\n")

def library():
    r = random.Random(11); used = set()
    schema = """CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT NOT NULL, country TEXT NOT NULL, birth_year INTEGER NOT NULL);
CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER NOT NULL REFERENCES authors(id), genre TEXT NOT NULL, published_year INTEGER NOT NULL, pages INTEGER NOT NULL, copies INTEGER NOT NULL);
CREATE TABLE members (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL, tier TEXT NOT NULL, joined TEXT NOT NULL);
CREATE TABLE loans (id INTEGER PRIMARY KEY, book_id INTEGER NOT NULL REFERENCES books(id), member_id INTEGER NOT NULL REFERENCES members(id), loan_date TEXT NOT NULL, due_date TEXT NOT NULL, return_date TEXT);
"""
    countries = ["UK", "USA", "France", "Japan", "Nigeria", "Argentina", "Russia", "India"]
    authors = [(i, person(r, used), r.choice(countries), r.randint(1890, 1990)) for i in range(1, 21)]
    genres = ["Fantasy", "Mystery", "Sci-Fi", "History", "Romance", "Biography", "Poetry"]
    adj = "Silent Hidden Last Golden Broken Distant Crimson Forgotten Electric Quiet Burning Endless".split()
    noun = "River Garden Empire Signal Harbor Winter Mirror Orchard Archive Compass Lantern Voyage".split()
    books = []; seen = set()
    for i in range(1, 61):
        while True:
            t = f"The {r.choice(adj)} {r.choice(noun)}"
            if t not in seen: seen.add(t); break
        a = r.choice(authors)
        books.append((i, t, a[0], r.choice(genres), r.randint(a[3] + 25, min(2024, a[3] + 80)), r.randint(90, 820), r.randint(1, 6)))
    cities = ["Leeds", "Austin", "Lyon", "Osaka", "Lagos", "Salta"]
    members = [(i, person(r, used), r.choice(cities), r.choices(["basic", "plus", "premium"], [5, 3, 2])[0], date(r, "2019-01-01", "2024-01-31")) for i in range(1, 41)]
    loans = []
    for i in range(1, 301):
        b = r.choice(books); m = r.choice(members)
        ld = date(r, max(m[4], "2023-01-01"), "2024-06-30")
        due = (datetime.date.fromisoformat(ld) + datetime.timedelta(days=21)).isoformat()
        ret = None if r.random() < 0.12 else (datetime.date.fromisoformat(ld) + datetime.timedelta(days=r.randint(3, 40))).isoformat()
        loans.append((i, b[0], m[0], ld, due, ret))
    sql = schema + "\n".join([insert("authors", "id name country birth_year".split(), authors), insert("books", "id title author_id genre published_year pages copies".split(), books), insert("members", "id name city tier joined".split(), members), insert("loans", "id book_id member_id loan_date due_date return_date".split(), loans)])
    write("library", "Library", "A public library: authors, books, members and loans (with due and return dates).", sql)

def school():
    r = random.Random(23); used = set()
    schema = """CREATE TABLE teachers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, department TEXT NOT NULL, hired_year INTEGER NOT NULL);
CREATE TABLE courses (id INTEGER PRIMARY KEY, title TEXT NOT NULL, department TEXT NOT NULL, credits INTEGER NOT NULL, teacher_id INTEGER REFERENCES teachers(id));
CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT NOT NULL, grade_level INTEGER NOT NULL, city TEXT NOT NULL, birth_date TEXT NOT NULL);
CREATE TABLE enrollments (student_id INTEGER NOT NULL REFERENCES students(id), course_id INTEGER NOT NULL REFERENCES courses(id), semester TEXT NOT NULL, score INTEGER, PRIMARY KEY (student_id, course_id, semester));
"""
    depts = ["Math", "Science", "Languages", "Arts", "History"]
    teachers = [(i, person(r, used), depts[(i - 1) % 5], r.randint(2004, 2023)) for i in range(1, 13)]
    topics = {"Math": ["Algebra", "Geometry", "Calculus", "Statistics", "Number Theory"], "Science": ["Physics", "Chemistry", "Biology", "Astronomy", "Geology"], "Languages": ["English Literature", "Spanish", "French", "Creative Writing", "Linguistics"], "Arts": ["Painting", "Music Theory", "Drama", "Photography", "Sculpture"], "History": ["World History", "Local History", "Ancient Rome", "Industrial Age", "Civics"]}
    courses = []; cid = 1
    for d in depts:
        pool = [t for t in teachers if t[2] == d]
        for k, title in enumerate(topics[d]):
            courses.append((cid, title, d, r.choice([2, 3, 4]), None if (cid == 24) else pool[k % len(pool)][0])); cid += 1
    cities = ["Springfield", "Rivertown", "Lakeside", "Hillview"]
    students = [(i, person(r, used), r.randint(9, 12), r.choice(cities), date(r, "2006-09-01", "2010-08-31")) for i in range(1, 61)]
    enr = []; seen = set()
    for s in students:
        for c in r.sample(courses, r.randint(3, 7)):
            sem = r.choice(["2023-fall", "2024-spring"])
            if (s[0], c[0], sem) in seen: continue
            seen.add((s[0], c[0], sem))
            score = None if r.random() < 0.07 else max(35, min(100, int(r.gauss(76, 14))))
            enr.append((s[0], c[0], sem, score))
    sql = schema + "\n".join([insert("teachers", "id name department hired_year".split(), teachers), insert("courses", "id title department credits teacher_id".split(), courses), insert("students", "id name grade_level city birth_date".split(), students), insert("enrollments", "student_id course_id semester score".split(), enr)])
    write("school", "School", "A high school: teachers, courses, students and enrollments with scores (some not yet graded).", sql)

def flights():
    r = random.Random(37); used = set()
    schema = """CREATE TABLE airlines (code TEXT PRIMARY KEY, name TEXT NOT NULL, country TEXT NOT NULL);
CREATE TABLE airports (code TEXT PRIMARY KEY, city TEXT NOT NULL, country TEXT NOT NULL, elevation_ft INTEGER NOT NULL);
CREATE TABLE flights (id INTEGER PRIMARY KEY, airline_code TEXT NOT NULL REFERENCES airlines(code), origin TEXT NOT NULL REFERENCES airports(code), destination TEXT NOT NULL REFERENCES airports(code), depart_date TEXT NOT NULL, duration_min INTEGER NOT NULL, base_price REAL NOT NULL, status TEXT NOT NULL);
CREATE TABLE bookings (id INTEGER PRIMARY KEY, flight_id INTEGER NOT NULL REFERENCES flights(id), passenger TEXT NOT NULL, seat_class TEXT NOT NULL, fare REAL NOT NULL, booked_on TEXT NOT NULL);
"""
    airlines = [("AZ", "Azure Air", "Italy"), ("BN", "Boreal Nordic", "Norway"), ("CX", "Condor Express", "Chile"), ("DJ", "Dune Jet", "UAE"), ("EK", "Eastern Kite", "Japan"), ("FL", "Fleetwing", "USA")]
    airports = [("LHR", "London", "UK", 83), ("JFK", "New York", "USA", 13), ("CDG", "Paris", "France", 392), ("HND", "Tokyo", "Japan", 21), ("DXB", "Dubai", "UAE", 62), ("SCL", "Santiago", "Chile", 1555), ("OSL", "Oslo", "Norway", 681), ("FCO", "Rome", "Italy", 13), ("SFO", "San Francisco", "USA", 13), ("LOS", "Lagos", "Nigeria", 135), ("SYD", "Sydney", "Australia", 21), ("DEL", "Delhi", "India", 777), ("MEX", "Mexico City", "Mexico", 7316), ("YYZ", "Toronto", "Canada", 569)]
    fl = []
    for i in range(1, 141):
        o, d = r.sample(airports, 2)
        fl.append((i, r.choice(airlines)[0], o[0], d[0], date(r, "2024-01-01", "2024-06-30"), r.randint(55, 900), round(r.uniform(60, 1100), 2), r.choices(["on_time", "delayed", "cancelled"], [10, 3, 1])[0]))
    bk = []
    for i in range(1, 451):
        f = r.choice(fl); cls = r.choices(["economy", "business", "first"], [8, 3, 1])[0]
        mult = {"economy": 1.0, "business": 2.4, "first": 4.0}[cls]
        bk.append((i, f[0], person(r, set()), cls, round(f[6] * mult * r.uniform(0.9, 1.15), 2), date(r, "2023-10-01", f[4])))
    sql = schema + "\n".join([insert("airlines", "code name country".split(), airlines), insert("airports", "code city country elevation_ft".split(), airports), insert("flights", "id airline_code origin destination depart_date duration_min base_price status".split(), fl), insert("bookings", "id flight_id passenger seat_class fare booked_on".split(), bk)])
    write("flights", "Flights", "Airlines, airports, scheduled flights and passenger bookings.", sql)

def music():
    r = random.Random(41); used = set()
    schema = """CREATE TABLE artists (id INTEGER PRIMARY KEY, name TEXT NOT NULL, country TEXT NOT NULL, formed_year INTEGER NOT NULL);
CREATE TABLE albums (id INTEGER PRIMARY KEY, artist_id INTEGER NOT NULL REFERENCES artists(id), title TEXT NOT NULL, release_year INTEGER NOT NULL, genre TEXT NOT NULL);
CREATE TABLE tracks (id INTEGER PRIMARY KEY, album_id INTEGER NOT NULL REFERENCES albums(id), title TEXT NOT NULL, track_no INTEGER NOT NULL, seconds INTEGER NOT NULL, explicit INTEGER NOT NULL);
CREATE TABLE listeners (id INTEGER PRIMARY KEY, name TEXT NOT NULL, country TEXT NOT NULL, plan TEXT NOT NULL, signup_date TEXT NOT NULL);
CREATE TABLE plays (id INTEGER PRIMARY KEY, track_id INTEGER NOT NULL REFERENCES tracks(id), listener_id INTEGER NOT NULL REFERENCES listeners(id), played_at TEXT NOT NULL, device TEXT NOT NULL);
"""
    aw = "Neon Velvet Paper Static Solar Midnight Glass Wild Cobalt Hollow Ivory Rust".split(); an = "Echoes Tigers Parade Hearts Rivers Engines Ghosts Letters Gardens Wolves Skies Orbit".split()
    countries = ["UK", "USA", "Sweden", "Brazil", "Nigeria", "Korea", "Canada"]
    artists = []; seen = set()
    while len(artists) < 15:
        n = f"{r.choice(aw)} {r.choice(an)}"
        if n in seen: continue
        seen.add(n); artists.append((len(artists) + 1, n, r.choice(countries), r.randint(1975, 2018)))
    genres = ["Rock", "Pop", "Jazz", "Electronic", "Hip-Hop", "Folk"]
    albums = []; ts = set()
    for i in range(1, 41):
        a = r.choice(artists)
        while True:
            t = f"{r.choice(an)} of {r.choice(aw)}"
            if t not in ts: ts.add(t); break
        albums.append((i, a[0], t, r.randint(a[3], 2024), r.choice(genres)))
    tracks = []; tid = 1; tn = set()
    tw = "Run Fade Burn Dream Stay Fall Shine Break Float Chase Hold Drift".split(); tx = "Tonight Away Again Forever Alone Home Slowly Higher Together Tomorrow".split()
    for al in albums:
        tn = set()
        for k in range(1, r.randint(5, 9)):
            while True:
                t = f"{r.choice(tw)} {r.choice(tx)}"
                if t not in tn: tn.add(t); break
            tracks.append((tid, al[0], t, k, r.randint(110, 430), 1 if r.random() < 0.18 else 0)); tid += 1
    ls = [(i, person(r, used), r.choice(countries), r.choices(["free", "premium", "family"], [5, 4, 2])[0], date(r, "2020-01-01", "2024-03-31")) for i in range(1, 31)]
    plays = []
    for i in range(1, 801):
        t = r.choice(tracks); l = r.choice(ls)
        plays.append((i, t[0], l[0], date(r, max(l[4], "2024-01-01"), "2024-06-30") + f" {r.randint(0, 23):02d}:{r.randint(0, 59):02d}", r.choice(["phone", "web", "speaker", "car"])))
    sql = schema + "\n".join([insert("artists", "id name country formed_year".split(), artists), insert("albums", "id artist_id title release_year genre".split(), albums), insert("tracks", "id album_id title track_no seconds explicit".split(), tracks), insert("listeners", "id name country plan signup_date".split(), ls), insert("plays", "id track_id listener_id played_at device".split(), plays)])
    write("music", "Music streaming", "A streaming service: artists, albums, tracks, listeners and individual plays.", sql)

def bank():
    r = random.Random(53); used = set()
    schema = """CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL, joined TEXT NOT NULL, segment TEXT NOT NULL);
CREATE TABLE accounts (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(id), type TEXT NOT NULL, opened TEXT NOT NULL, closed INTEGER NOT NULL DEFAULT 0);
CREATE TABLE transactions (id INTEGER PRIMARY KEY, account_id INTEGER NOT NULL REFERENCES accounts(id), tx_date TEXT NOT NULL, amount REAL NOT NULL, kind TEXT NOT NULL, merchant TEXT);
"""
    cities = ["Boston", "Denver", "Miami", "Seattle", "Chicago"]
    cust = [(i, person(r, used), r.choice(cities), date(r, "2015-01-01", "2023-12-31"), r.choices(["retail", "premier", "business"], [6, 2, 2])[0]) for i in range(1, 31)]
    acc = []
    for c in cust:
        for t in r.sample(["checking", "savings", "credit"], r.randint(1, 3)):
            acc.append((len(acc) + 1, c[0], t, date(r, c[3], "2024-01-31"), 1 if r.random() < 0.08 else 0))
    merchants = ["Grocer", "Fuel Stop", "Cafe Nero", "Streamly", "Rent Co", "Gym Plus", "Bookshop", "Pharmacy", "Airline", "Utilities"]
    tx = []
    for i in range(1, 901):
        a = r.choice(acc); k = r.choices(["deposit", "purchase", "withdrawal", "fee", "transfer"], [3, 8, 3, 1, 2])[0]
        amt = round(r.uniform(20, 2500), 2) if k == "deposit" else round(-r.uniform(2, 400), 2) if k in ("purchase", "withdrawal", "transfer") else -round(r.uniform(1, 25), 2)
        tx.append((i, a[0], date(r, max(a[3], "2024-01-01"), "2024-06-30"), amt, k, r.choice(merchants) if k == "purchase" else None))
    sql = schema + "\n".join([insert("customers", "id name city joined segment".split(), cust), insert("accounts", "id customer_id type opened closed".split(), acc), insert("transactions", "id account_id tx_date amount kind merchant".split(), tx)])
    write("bank", "Bank", "Retail banking: customers, their accounts and a ledger of signed transactions (deposits positive, spending negative).", sql)

def stocks():
    r = random.Random(67)
    schema = """CREATE TABLE tickers (symbol TEXT PRIMARY KEY, company TEXT NOT NULL, sector TEXT NOT NULL);
CREATE TABLE prices (symbol TEXT NOT NULL REFERENCES tickers(symbol), trade_date TEXT NOT NULL, open REAL NOT NULL, high REAL NOT NULL, low REAL NOT NULL, close REAL NOT NULL, volume INTEGER NOT NULL, PRIMARY KEY (symbol, trade_date));
"""
    tick = [("ACME", "Acme Industrial", "Industrials"), ("BYTE", "ByteWorks", "Technology"), ("CLOUD", "Cloudline", "Technology"), ("DRUG", "Drugwell", "Healthcare"), ("ENRG", "Enerigo", "Energy"), ("FOOD", "FreshFoods", "Consumer"), ("GRID", "GridPower", "Energy"), ("HOME", "HomeNest", "Consumer")]
    rows = []
    d0 = datetime.date(2024, 3, 1)
    days = []
    d = d0
    while len(days) < 45:
        if d.weekday() < 5: days.append(d)
        d += datetime.timedelta(days=1)
    for s, _, _ in tick:
        p = r.uniform(20, 180)
        for day in days:
            o = p * r.uniform(0.985, 1.015); c = o * r.uniform(0.96, 1.04)
            h = max(o, c) * r.uniform(1.0, 1.02); l = min(o, c) * r.uniform(0.98, 1.0)
            rows.append((s, day.isoformat(), round(o, 2), round(h, 2), round(l, 2), round(c, 2), r.randint(80, 900) * 1000)); p = c
    sql = schema + "\n".join([insert("tickers", "symbol company sector".split(), tick), insert("prices", "symbol trade_date open high low close volume".split(), rows)])
    write("stocks", "Stock prices", "Eight tickers with 45 trading days of daily open/high/low/close prices and volume.", sql)

if __name__ == "__main__":
    for f in (library, school, flights, music, bank, stocks): f()
    print("ok")
