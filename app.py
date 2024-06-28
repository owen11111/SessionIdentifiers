from flask import Flask, render_template, redirect, session, request, url_for
from datetime import timedelta
import sqlite3

app = Flask(__name__)
app.secret_key = "20"
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route("/")
@app.route("/Home")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = sqlite3.connect("testdb.db")
        cur = conn.cursor()
        userData = cur.execute("SELECT username, password FROM users;").fetchall()
        username = request.form["username"]
        password = request.form["password"]
        print(f"{username}: {password}")
        for i in userData:
            if i[0] == username and i[1] == password:
                session.permanent = True
                session["user"] = username
                conn.close()
                return redirect(url_for("private"))
        conn.close()
        return "Invalid Credentials"
    return render_template("login.html")

@app.route("/private")
def private():
    if "user" in session:
        return render_template("private.html")
    else:
        return redirect(url_for("login"))

@app.route("/privateDetails")
def privateDetails():
    if "user" in session:
        conn = sqlite3.connect("testdb.db")
        cur = conn.cursor()
        userData = cur.execute(f"SELECT email, name FROM users WHERE username = '{session["user"]}';").fetchone()
        return render_template("privateDetails.html", email = userData[0], name = userData[1])
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    # Remove user from session
    session.pop("user", None)
    # Clear session cookie
    session.clear()
    response = redirect(url_for("login"))
    response.set_cookie('session', '', expires=0)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()