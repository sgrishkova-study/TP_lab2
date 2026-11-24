import sqlite3
from pathlib import Path

from crypto_utils import encrypt_data

DB_PATH = Path(__file__).resolve().parent / "secure_database.db"


def main():

    if not DB_PATH.exists():
        raise FileNotFoundError("Secure database not found.")

    db = sqlite3.connect(DB_PATH)

    try:
        db.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                name TEXT PRIMARY KEY
            )
        """)

        completed = db.execute(
            "SELECT name FROM migrations WHERE name = ?",
            ("encrypt_signatures_v1",)
        ).fetchone()

        if completed:
            print("Signatures are already encrypted.")
            return

        signatures = db.execute(
            "SELECT id, name, email FROM signatures"
        ).fetchall()

        for signature_id, name, email in signatures:

            db.execute("""
                UPDATE signatures
                SET name = ?, email = ?
                WHERE id = ?
            """, (
                encrypt_data(name),
                encrypt_data(email),
                signature_id
            ))

        db.execute(
            "INSERT INTO migrations (name) VALUES (?)",
            ("encrypt_signatures_v1",)
        )

        db.commit()

        print(f"Successfully encrypted {len(signatures)} signatures!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
