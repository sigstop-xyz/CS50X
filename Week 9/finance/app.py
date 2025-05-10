import os
import hashlib

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    purchases = db.execute(
        "SELECT symbol, SUM(shares) AS total_shares, SUM(CAST(REPLACE(REPLACE(total, '$', ''),',','')AS FLOAT)) AS total_sum, CAST(REPLACE(price, '$', '') AS FLOAT) AS price  FROM purchases WHERE customer_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
        session["user_id"],
    )
    users = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    cash = float(users[0]["cash"])
    total_sum_query = db.execute(
        "SELECT SUM(CAST(REPLACE(REPLACE(total, '$', ''),',','')AS FLOAT)) AS total_sum FROM purchases WHERE customer_id = ?",
        session["user_id"],
    )
    total_sum = (
        float(total_sum_query[0]["total_sum"])
        if total_sum_query[0]["total_sum"] is not None
        else 0.0
    )
    total_money = usd(total_sum + cash)

    print("Cash:", cash)
    print("Total Sum:", total_sum)
    print("Total Money:", total_money)

    return render_template(
        "index.html", purchases=purchases, cash=usd(cash), total_money=total_money
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        if not request.form.get("shares"):
            return apology("must provide shares", 400)

        # Query lookup for stock symbol
        stock = lookup(request.form.get("symbol"))
        if stock == None:
            return apology("must provide valid name", 400)
        price = stock["price"]
        if not request.form.get("shares").isdigit():
            return apology("must be valid number of shares", 400)
        if int(request.form.get("shares")) <= 0:
            return apology("must buy more than 0 Shares", 400)

        old_money = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )

        if int(price) * int(request.form.get("shares")) < old_money[0]["cash"]:
            new_money = float(old_money[0]["cash"]) - (
                float(price) * float(request.form.get("shares"))
            )
            db.execute(
                "UPDATE users SET cash = ? WHERE id = ?", new_money, session["user_id"]
            )
            shares = int(request.form.get("shares"))
            db.execute(
                "INSERT INTO purchases (symbol, total, shares, price, customer_id) VALUES (?, ?, ?, ?, ?)",
                request.form.get("symbol"),
                usd(price * shares),
                shares,
                usd(price),
                session["user_id"],
            )
            db.execute(
                "INSERT INTO transactions (symbol, shares, price, customer_id) VALUES (?, ?,?, ?)",
                request.form.get("symbol"),
                shares,
                usd(price),
                session["user_id"],
            )
            return redirect("/")
        else:
            return apology("You dont have enough Money", 403)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT * FROM transactions WHERE customer_id = ?", session["user_id"]
    )
    return render_template("history.html", transactions=transactions)


@app.route("/topup", methods=["GET", "POST"])
@login_required
def topup():
    """topup"""
    if request.method == "POST":
        if not request.form.get("cash"):
            return apology("Invalid Cash Number", 403)
        old_money = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )
        new_money = float(old_money[0]["cash"]) + float(request.form.get("cash"))
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", new_money, session["user_id"]
        )
        return redirect("/")
    else:
        return render_template("index.html")


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """password change"""
    user_password = db.execute(
        "SELECT hash FROM users WHERE id = ?", session["user_id"]
    )
    if request.method == "POST":
        if not check_password_hash(
            user_password[0]["hash"], request.form.get("old_password")
        ):
            return apology("Invalid Password", 403)
        if not request.form.get("new_password"):
            return apology("Invalid new Password", 403)

        new_hash = generate_password_hash(request.form.get("new_password"))
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?", new_hash, session["user_id"]
        )
        return redirect("/")
    else:
        return render_template("password.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page after successful login
        return redirect("/")

    # If it's a GET request (i.e., user navigates to /login)
    else:
        # Render the login page template without passing 'user' variable
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Query lookup for stock symbol
        stock = lookup(request.form.get("symbol"))
        if stock is None or stock["price"] is None:
            return apology("Invalid Ticker Symbol", 400)

        stock["price"] = usd(stock["price"])

        # Redirect user to home page
        return render_template("quoted.html", stock=stock)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        usernames = db.execute("SELECT username FROM users")
        for user in usernames:
            if request.form.get("username") == user["username"]:
                return apology("Username already exists", 400)
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Password dont match", 400)

        # Hash password
        hash_p = generate_password_hash(request.form.get("password"))

        # Save database for username and password
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            request.form.get("username"),
            hash_p,
        )

        return redirect("/login")

        # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Redirect user to home page
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    stocks = db.execute(
        "SELECT DISTINCT(symbol) AS stock_symbol FROM purchases WHERE customer_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
        session["user_id"],
    )
    share_count = db.execute(
        "SELECT symbol, SUM(shares) FROM purchases GROUP BY symbol"
    )
    old_money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

    if request.method == "POST":
        stock = lookup(request.form.get("symbol"))
        price = float(stock["price"])

        if not request.form.get("symbol"):
            return apology("must provide valid symbol", 400)
        elif int(request.form.get("shares")) <= 0:
            return apology("must provide valid shares number", 400)
        for item in share_count:
            if item["symbol"] == request.form.get("symbol"):
                total_shares = int(item["SUM(shares)"])
                input_shares = int(request.form.get("shares"))
                if total_shares < input_shares:
                    return apology("must have more shares", 400)
        shares = -float(request.form.get("shares"))
        new_money = float(old_money[0]["cash"]) - float(shares * price)
        db.execute(
            "INSERT INTO purchases (symbol, total, shares, price, customer_id) VALUES (?,?,?,0,?)",
            request.form.get("symbol"),
            usd(price * shares),
            shares,
            session["user_id"],
        )
        db.execute(
            "INSERT INTO transactions (symbol, shares, price, customer_id) VALUES (?, ?, ?, ?)",
            request.form.get("symbol"),
            shares,
            usd(price),
            session["user_id"],
        )
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", new_money, session["user_id"]
        )
        return redirect("/")

    else:
        return render_template("sell.html", stocks=stocks)
