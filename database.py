import sqlite3

DB_NAME = "petitions.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS petitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            goal INTEGER NOT NULL default 0
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS signatures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            petition_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            FOREIGN KEY (petition_id) REFERENCES petitions(id)
        )
    """)

    count = conn.execute(
        "SELECT COUNT(*) FROM petitions"
    ).fetchone()[0]

    if count == 0:
        demo_partitions = [
            (
                "Защитим бобров!",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
                "ECOLOGY",
                1100
            )
        ]

        conn.executemany("""
            INSERT INTO petitions (title, description, category, goal)
            VALUES (?, ?, ?, ?)
        """, demo_partitions)

    conn.commit()
    conn.close()