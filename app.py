from flask import Flask, render_template,request
import sqlite3;

app = Flask(__name__)

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
conn.close()

@app.route("/")
def landing_page():
    return render_template("loginpage.html")

@app.route("/",methods=['POST','GET'])
def login_func():
    if request.method == 'POST':
        username = request.form["loginuser"]
        password = request.form["loginpass"]

        if username == "" or password == "":
            return "Enter all the fields please!!" + render_template("loginpage.html")
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user is None:
            return "User does not exist. Please sign up."
        stored_password = user[1]
        if password != stored_password:
            return "Incorrect password. Please try again."

        conn.close()
        return f"Welcome {user[0]}, the page is under development. Hold onto your seat will be done soon"
    return render_template("loginpage.html")

@app.route("/signup",methods=['POST','GET'])
def signup_page():
    if request.method == 'POST':
        username = request.form["signupname"]
        password = request.form["signuppass"]
        repass = request.form["signuprepass"]

        if username == "" or password == "" or repass == "":
            return "you cannot let the fields be empty, Fill them up please!!" + render_template("signuppage.html")
        if password != repass:
            return "Passwords do not match"
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()

        conn.close()
        return "User Created and now login using those credentials" + render_template("loginpage.html")
    return render_template("signuppage.html")

if __name__ == "__main__":
    app.run(debug=True)