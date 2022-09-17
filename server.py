from flask import Flask, render_template, session, request, redirect
import random

app = Flask(__name__)
app.secret_key = "shhhhhhh"

leaderboard = []

@app.route("/")
def game():
    if not "number" in session:
        session["number"] = random.randint(1, 100)
        session["attempts_left"] = 5
        session["guess_history"] = []
    return render_template("index.html")

@app.route("/evaluate", methods=["POST"])
def evaluate_guess():
    int_guess = int(request.form["guess"])
    if int_guess > session["number"]:
        session["indicator"] = "high"
    elif int_guess < session["number"]:
        session["indicator"] = "low"
    else:
        session["indicator"] = "win"

    session["attempts_left"] -= 1
    if session["attempts_left"] <= 0 and session["indicator"] != "win":
        session["indicator"] = "lose"
    session["guess_history"].append(int_guess)
    print(session["number"])
    return redirect("/")

@app.route("/play_again")
def play_again():
    session.clear()
    return redirect("/")

@app.route("/add_name", methods=["POST"])
def add_name():
    # print("Received name:", request.form["name"])
    leaderboard.append({"name": request.form["name"], "attempts": 5 - session["attempts_left"]})
    return redirect("/leaderboard")

@app.route("/leaderboard")
def display_leaderboard():
    session["leaderboard"] = leaderboard; # so that when the leaderboard page is refreshed, the leaderboard is not lost
    return render_template("leaderboard.html")

if __name__ == "__main__":
    app.run(debug = True)