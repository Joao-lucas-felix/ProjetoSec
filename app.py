from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")


@app.route("/")
def index():
    return render_template("index.html")


# ENDPOINT 1 (SEGURO)
@app.route("/users")
def list_users():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()

    conn.close()

    return render_template("index.html", users=users)


# ENDPOINT 2 (SEGURO)
@app.route("/user")
def get_user():

    user_id = request.args.get("id")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    conn.close()

    return render_template("user.html", user=user)


# ENDPOINT 3 (VULNERÁVEL)
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        query = f"""
        SELECT * FROM users
        WHERE username = '{username}'
        AND password = '{password}'
        """

        print("QUERY:", query)

        cursor.execute(query)
        user = cursor.fetchone()

        conn.close()

        if user:
            return f"Bem-vindo {user[1]}"
        else:
            return "Login inválido"

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)