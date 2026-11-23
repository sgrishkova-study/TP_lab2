from flask import Flask, render_template
from database import get_db, init_db

app = Flask(__name__)

init_db()

@app.route("/")
def home_page():
    db = get_db()

    petitions = db.execute("""
    """).fetchall()

    db.close()

    return render_template("index.html", petitions=petitions)

if __name__ == "__main__":
    app.run(debug=True)