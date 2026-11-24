import hmac
import os
import secrets
from functools import wraps
from flask import Flask, redirect, render_template, request, session, url_for
from database import get_db, init_db

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax"
)

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):

        if not session.get("is_admin"):
            return "Forbidden: administrator access required", 403

        return view(*args, **kwargs)

    return wrapped

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if not ADMIN_PASSWORD:
        return "Administrator password is not configured", 503

    if request.method == "POST":

        password = request.form.get("password", "")

        if hmac.compare_digest(
            password.encode("utf-8"),
            ADMIN_PASSWORD.encode("utf-8")
        ):
            session.clear()
            session["is_admin"] = True

            return redirect(url_for("home_page"))

        return "Invalid password", 401

    return render_template("admin_login.html")


@app.route("/admin/logout", methods=["POST"])
@admin_required
def admin_logout():

    session.clear()

    return redirect(url_for("home_page"))


init_db()

@app.route("/")
def home_page():
    db = get_db()

    petitions = db.execute("""
        SELECT p.*, COUNT(s.id) AS signatures
        FROM petitions p
        LEFT JOIN signatures s ON s.petition_id = p.id
        GROUP BY p.id
        ORDER BY p.id DESC
    """).fetchall()

    db.close()

    return render_template("index.html", petitions=petitions)

@app.route("/create", methods=["GET", "POST"])
def create_petition():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()
        goal_text = request.form.get("goal", "")

        allowed_categories = {
            "ENVIRONMENT"
        }

        ### нет ручек нет конфетки
        if not title or not description:
            return "Title and description are requered", 400

        if category not in allowed_categories:
            return "Invalid category.", 400

        try:
            goal = int(goal_text)
        except ValueError:
            return "Goal must be a number.", 400

        db = get_db()

        db.execute("""
            INSERT INTO petitions (title, description, category, goal)
            VALUES (?, ?, ?, ?)
        """, (title, description, category, goal))

        db.commit()
        db.close()

        return redirect(url_for("home_page"))
    
    return render_template("create_petition.html")


@app.route("/delete/<int:petition_id>", methods=["POST"])
@admin_required
def delete_petition(petition_id):
    db = get_db()

    db.execute(
        "DELETE FROM signatures WHERE petition_id = ?",
        (petition_id,)
    )

    db.execute(
        "DELETE FROM petitions WHERE id = ?",
        (petition_id,)
    )

    db.commit()
    db.close()

    return redirect(url_for("home_page"))


@app.route("/assignment/search")
def vulnerable_search():
    query = request.args.get("q", "")

    db = get_db()

    sql = """
        SELECT id, title, description, category
        FROM petitions
        WHERE title LIKE ?
        ORDER BY id DESC
    """

    petitions = db.execute(sql,(f"%{query}%",)).fetchall()

    db.close()

    return render_template(
        "vulnerable_search.html",
        petitions=petitions,
        query=query
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)