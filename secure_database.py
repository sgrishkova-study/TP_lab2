import sqlite3

DB_NAME = "petitions.db"


def get_db(db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_name=DB_NAME):
    conn = get_db(db_name)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS petitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            goal INTEGER NOT NULL DEFAULT 0
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
        demo_petitions = [
            (
                "Защитим бобров!",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "ENVIRONMENT",
                1100
            ),
            (
                "BAC_DELETE_TEST",
                "Disposable security testing record",
                "ENVIRONMENT",
                10
            )
        ]

        conn.executemany("""
            INSERT INTO petitions (title, description, category, goal)
            VALUES (?, ?, ?, ?)
        """, demo_petitions)

    signature_count = conn.execute(
        "SELECT COUNT(*) FROM signatures"
    ).fetchone()[0]

    if signature_count == 0:
        petition_id = conn.execute(
            "SELECT id FROM petitions LIMIT 1"
        ).fetchone()[0]

        demo_signatures = [
            ("Alex Morgan", "alex.morgan@example.test"),
            ("Sophie Miller", "sophie.miller@example.test"),
            ("Daniel Weber", "daniel.weber@example.test"),
            ("Emma Taylor", "emma.taylor@example.test"),
            ("Noah Fischer", "noah.fischer@example.test")
        ]

        conn.executemany("""
            INSERT INTO signatures (petition_id, name, email)
            VALUES (?, ?, ?)
        """, [
            (petition_id, name, email)
            for name, email in demo_signatures
        ])

    conn.commit()
    conn.close()