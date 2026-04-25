import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

#Creat pitchers table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS pitchers (
        pitcher_id INTEGER PRIMARY KEY,
        name TEXT,
        mlb_team TEXT,
        era REAL,
        k9 REAL,
        wins INTEGER,
        status TEXT
    )
""")

# Insert pitchers
pitchers_data = [
    (1, 'Paul Skenes', 'Pittsburgh Pirates', 1.96, 11.2, 3, 'starter'),
    (2, 'Zack Wheeler', 'Philadelphia Phillies', 2.85, 9.8, 4, 'starter'),
    (3, 'Chris Sale', 'Atlanta Braves', 3.50, 10.1, 3, 'starter'),
    (4, 'Nathan Eovaldi', 'Texas Rangers', 4.20, 8.1, 2, 'starter'),
    (5, 'Spencer Strider', 'Atlanta Braves', 0.00, 10.5, 0, 'starter'),
]

cursor.executemany("INSERT OR IGNORE INTO pitchers VALUES (?,?,?,?,?,?,?)", pitchers_data)
conn.commit()
print("Database ready!")

# SELECT - basic query
print("\n--- SELECT ALL ---")
result = pd.read_sql("SELECT * FROM pitchers", conn)
print(result)

# WHERE - filtering rows
print("\n--- WHERE ---")
result = pd.read_sql("""
    SELECT name, era, wins
    FROM pitchers
    WHERE era < 3.00
""", conn)
print(result)

# AND - multiple conditions
print("\n--- AND ---")
result = pd.read_sql("""
    SELECT name, era, wins
    FROM pitchers
    WHERE era < 3.00
    AND wins > 0
""", conn)
print(result)

# ORDER BY
print("\n--- ORDER BY ---")
result = pd.read_sql("""
    SELECT name, era, k9
    FROM pitchers
    ORDER BY era ASC
""", conn)
print(result)

# GROUP BY
print("\n--- GROUP BY ---")
result = pd.read_sql("""
    SELECT mlb_team, COUNT(*) AS pitchers, ROUND(AVG(era), 2) AS avg_era
    FROM pitchers
    GROUP BY mlb_team
""", conn)
print(result)

# HAVING
print("\n--- HAVING ---")
result = pd.read_sql("""
    SELECT mlb_team, COUNT(*) AS pitchers, ROUND(AVG(era), 2) AS avg_era
    FROM pitchers
    GROUP BY mlb_team
    HAVING COUNT(*) > 1
""", conn)
print(result)

# INNER JOIN + LEFT JOIN
cursor.execute("""
    CREATE TABLE IF NOT EXISTS fantasy_roster (
        roster_id INTEGER PRIMARY KEY,
        pitcher_id INTEGER,
        fantasy_team TEXT
    )
""")

roster_data = [
    (1, 1, 'Team SueShar'),
    (2, 2, 'Team SueShar'),
    (3, 4, 'Opponent'),
]

cursor.executemany("INSERT OR IGNORE INTO fantasy_roster VALUES (?,?,?)", roster_data)
conn.commit()

# INNER JOIN - only matches
print("\n-- INNER JOIN ---")
result = pd.read_sql("""
    SELECT p.name, p.era, r.fantasy_team
    FROM pitchers p
    INNER JOIN fantasy_roster r ON p.pitcher_id = r.pitcher_id
""", conn)
print(result)

# LEFT JOIN - all pitchers, even without a roster spot
print("\n--- LEFT JOIN ---")
result = pd.read_sql("""
    SELECT p.name, p.era, r.fantasy_team
    FROM pitchers p
    LEFT JOIN fantasy_roster r ON p.pitcher_id = r.pitcher_id
""", conn)
print(result)

# SUBQUERY
print("\n--- SUBQUERY ---")
result = pd.read_sql("""
    SELECT name, era
    FROM pitchers
    WHERE era < (SELECT AVG(era) FROM pitchers)
""", conn)
print(result)

# CTE
print("\n--- CTE ---")
result = pd.read_sql("""
    WITH elite_pitchers AS (
        SELECT name, era, k9
        FROM pitchers
        WHERE era < 3.00
    )
    SELECT name, era, k9
    FROM elite_pitchers
    ORDER BY era ASC
""", conn)
print(result)

# WINDOW FUNCTIONS
print("\n--- WINDOW FUNCTION ---")
result = pd.read_sql("""
    SELECT name, era, k9,
            RANK() OVER (ORDER BY era ASC) AS era_rank,
            ROUND(AVG(era) OVER (), 2) AS avg_era
    FROM pitchers
""", conn)
print(result)

# CASE WHEN
print("\n--- CASE WHEN ---")
pooperstars = pd.read_sql("""
    SELECT name, era,
            CASE WHEN era < 3.00 THEN 'Elite'
                WHEN era < 4.00 THEN 'Solid'
                ELSE 'Struggling'
            END AS pitcher_grade
    FROM pitchers
""", conn)
print(pooperstars)

# DISTINCT
print("\n--- DISTINCT ---")
result = pd.read_sql("""
    SELECT DISTINCT mlb_team
    FROM pitchers
    ORDER BY mlb_team ASC
""", conn)
print(result)

# NULL HANDLING
print("\n--- NULL HANDLING ---")

# IS NULL - find pitchers with no fantasy roster
result = pd.read_sql("""
    SELECT p.name, p.era, r.fantasy_team
    FROM pitchers p
    LEFT JOIN fantasy_roster r ON p.pitcher_id = r.pitcher_id
    WHERE r.fantasy_team IS NULL
""", conn)
print("No fantasy team:")
print(result)

# COALESCE - replace NULL with a fallback value
result = pd.read_sql("""
    SELECT p.name, p.era,
            COALESCE(r.fantasy_team, 'Free Agent') AS fantasy_team
    FROM pitchers p
    LEFT JOIN fantasy_roster r on p.pitcher_id = r.pitcher_id
""", conn)
print("\nWith COALESCE:")
print(result)

# STRING FUNCTIONS
print("\n--- STRING FUNCTIONS ---")
result = pd.read_sql("""
    SELECT name,
            UPPER(name) AS name_upper,
            LENGTH(name) AS name_length,
            mlb_team
    FROM pitchers
    WHERE name LIKE 'P%'
""", conn)
print(result)