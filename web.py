from flask import Flask, render_template

app = Flask(__name__)

petitions = [
    {
        "id": 1,
        "title": "Защитите бобров!",
    }
]

@app.route("/")
def home_page():
    return render_template("index.html", petitions=petitions)

if __name__ == "__main__":
    app.run(debug=True)