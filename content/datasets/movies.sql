CREATE TABLE directors (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  country TEXT NOT NULL,
  birth_year INTEGER NOT NULL
);

CREATE TABLE movies (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  release_year INTEGER NOT NULL,
  genre TEXT NOT NULL,
  director_id INTEGER REFERENCES directors(id),
  runtime_minutes INTEGER NOT NULL,
  budget_millions REAL,
  gross_millions REAL
);

CREATE TABLE reviews (
  id INTEGER PRIMARY KEY,
  movie_id INTEGER NOT NULL REFERENCES movies(id),
  reviewer TEXT NOT NULL,
  rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 10),
  review_date TEXT NOT NULL
);

INSERT INTO directors (id, name, country, birth_year) VALUES
  (1, 'Christopher Nolan', 'UK', 1970),
  (2, 'Greta Gerwig', 'USA', 1983),
  (3, 'Bong Joon-ho', 'South Korea', 1969),
  (4, 'Hayao Miyazaki', 'Japan', 1941),
  (5, 'Denis Villeneuve', 'Canada', 1967),
  (6, 'Kathryn Bigelow', 'USA', 1951),
  (7, 'Agnès Varda', 'France', 1928);

INSERT INTO movies (id, title, release_year, genre, director_id, runtime_minutes, budget_millions, gross_millions) VALUES
  (1, 'Inception', 2010, 'Sci-Fi', 1, 148, 160, 837),
  (2, 'Interstellar', 2014, 'Sci-Fi', 1, 169, 165, 773),
  (3, 'Oppenheimer', 2023, 'Drama', 1, 180, 100, 975),
  (4, 'Lady Bird', 2017, 'Comedy', 2, 94, 10, 79),
  (5, 'Little Women', 2019, 'Drama', 2, 135, 40, 218),
  (6, 'Barbie', 2023, 'Comedy', 2, 114, 145, 1446),
  (7, 'Parasite', 2019, 'Thriller', 3, 132, 11.4, 262),
  (8, 'Memories of Murder', 2003, 'Thriller', 3, 131, 2.8, 1.1),
  (9, 'Spirited Away', 2001, 'Animation', 4, 125, 19, 395),
  (10, 'Princess Mononoke', 1997, 'Animation', 4, 134, 23.5, 194),
  (11, 'Arrival', 2016, 'Sci-Fi', 5, 116, 47, 203),
  (12, 'Dune', 2021, 'Sci-Fi', 5, 155, 165, 407),
  (13, 'The Hurt Locker', 2008, 'Thriller', 6, 131, 15, 49),
  (14, 'Zero Dark Thirty', 2012, 'Thriller', 6, 157, 40, 132),
  (15, 'Cléo from 5 to 7', 1962, 'Drama', 7, 90, NULL, NULL),
  (16, 'The Room Next Door', 2024, 'Drama', NULL, 107, NULL, 12);

INSERT INTO reviews (id, movie_id, reviewer, rating, review_date) VALUES
  (1, 1, 'sam', 9, '2024-01-03'),
  (2, 1, 'riley', 8, '2024-01-10'),
  (3, 1, 'jordan', 10, '2024-02-01'),
  (4, 2, 'sam', 10, '2024-01-04'),
  (5, 2, 'casey', 7, '2024-03-12'),
  (6, 3, 'riley', 9, '2024-02-20'),
  (7, 3, 'jordan', 8, '2024-02-22'),
  (8, 3, 'alex', 9, '2024-03-02'),
  (9, 4, 'casey', 8, '2024-01-15'),
  (10, 5, 'casey', 9, '2024-01-16'),
  (11, 5, 'alex', 7, '2024-04-01'),
  (12, 6, 'sam', 6, '2024-02-11'),
  (13, 6, 'riley', 7, '2024-02-12'),
  (14, 6, 'jordan', 5, '2024-02-13'),
  (15, 7, 'sam', 10, '2024-01-20'),
  (16, 7, 'alex', 10, '2024-01-25'),
  (17, 7, 'casey', 9, '2024-03-30'),
  (18, 8, 'jordan', 9, '2024-04-04'),
  (19, 9, 'riley', 10, '2024-01-08'),
  (20, 9, 'alex', 9, '2024-02-09'),
  (21, 10, 'sam', 8, '2024-03-03'),
  (22, 11, 'casey', 9, '2024-02-27'),
  (23, 11, 'jordan', 8, '2024-03-08'),
  (24, 12, 'riley', 8, '2024-04-10'),
  (25, 12, 'sam', 7, '2024-04-11'),
  (26, 13, 'alex', 7, '2024-01-29'),
  (27, 14, 'jordan', 6, '2024-02-05');
