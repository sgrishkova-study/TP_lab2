from flask import Flask, render_template
from database import get_db, init_db

app = Flask(__name__)

init_db()

@app.route("/")
def home_page():
    db = get_db()

    petitions = db.execute("""
        SELECT p.*, COUNT(s.id) AS signatures
        FROM petitions p
        LEFT JOIN signatures s ON s.petition_id = p.id
        GROUP BY p.id
    """).fetchall()

    db.close()

    return render_template("index.html", petitions=petitions)

if __name__ == "__main__":
    app.run(debug=True)