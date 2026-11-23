from flask import Flask, render_template
from database import get_db, init_db

app = Flask(__name__)

init_db()

petitions = [
    {
        "id": 1,
        "category": "ECOLOGY",
        "title": "Защитите бобров!",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        "signatures": 1105,
        "goal": 1500,
        "color": "green"
    }
]

@app.route("/")
def home_page():
    return render_template("index.html", petitions=petitions)

if __name__ == "__main__":
    app.run(debug=True)