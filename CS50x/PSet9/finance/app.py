import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    """Show portfolio of stocks"""

    user_id = session['user_id']
    ''' select data from database '''
    portfolio = db.execute('SELECT symbol, name, sum(shares) as tot_shares, price FROM transactions WHERE user_id = ? GROUP BY symbol', user_id)
    cash = db.execute('SELECT cash FROM users WHERE id = ?', user_id)[0]['cash']

    """ total cash ins each stock """
    total = cash
    for stock in portfolio:
        total += stock['tot_shares'] * stock['price']

    return render_template('index.html', portfolio=portfolio, cash=cash, usd=usd, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == 'POST':
        """ searches in templates the name symbol """
        ticker_symbol = request.form.get('symbol').upper()
        stock = lookup(ticker_symbol)

        """ if there is no symbol """
        if not ticker_symbol:
            return apology('Please enter a correct symbol!')
        elif not stock:
            return apology('Invalid symbol!')

        """try to get an positive int od shares"""
        try:
            shares = int(request.form.get('shares'))
        except:
            return apology('Shares must be an integer!')
        if shares <= 0:
            return apology('Shares must be an positive integer!')

        user_id = session['user_id']
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]['cash']

        company = stock['name']
        stock_price = stock['price']
        total = stock_price * shares

        if cash < total:
            return apology('No enough cash :(')
        else:
            '''atualizar a base de dados, atualizadno "cash" subtraindo o total'''
            db.execute('UPDATE users SET cash = ? WHERE id = ?', cash-total, user_id)
            db.execute('INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)',
                        user_id, company, shares, stock_price, 'Buy', ticker_symbol)
        return redirect('/')

    else:
        return render_template('buy.html')


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session['user_id']
    transactions = db.execute('SELECT type, symbol, shares, price, time FROM transactions WHERE user_id = ?', user_id)

    return render_template('history.html', transactions=transactions, usd=usd)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """ Change password """
    user_id = session['user_id']

    if request.method == 'POST':

        password_hashed = db.execute('SELECT hash FROM users WHERE id = ?', user_id)[0]['hash']

        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirmation = request.form.get('confirmation')


        # Ensure old, new and confirmation password was submitted
        if not old_password:
            return apology("must provide you're old password", 403)
        elif not new_password:
            return apology("must provide you're new password", 403)
        elif not confirmation:
            return apology("must confirm you're new password", 403)

        if not check_password_hash(password_hashed, old_password):
            return apology('old password is wrong')

        if new_password != confirmation:
            return apology("confirm correctly you're new password")

        hash = generate_password_hash(new_password)
        db.execute('UPDATE users SET hash = ?, hash = ? WHERE id = ?', password_hashed, hash, user_id)
        return redirect("/")

    else:
        return render_template('change_password.html')

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        """ searches in templates, tha name symbol """
        symbol = request.form.get('symbol')

        """ if there is no symbol """
        if not symbol:
            return apology('Symbol requiered!')

        """ search for this symbol """
        stock_symbol = lookup(symbol)

        """ if the symbol exists """
        if not stock_symbol:
            return apology('Invalid symbol!')

        """ if the item is valid"""
        return render_template('quoted.html', item=stock_symbol, usd=usd)

    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    """ - when requested via get, display registration form
        - when form is submited via post, check for errors and insert the new user into users table
        - log user in
    """
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        if not username:
            return apology("Username is required!")
        elif not password:
            return apology("Password is required!")
        elif not confirmation:
            return apology("Password confirmation is required!")

        if password != confirmation:
            return apology("Password and confirmation do not match!")

        hash = generate_password_hash(password)
        try:
            db.execute('INSERT INTO users (username, hash) VALUES (?, ?)', username, hash)
            return redirect('/')
        except:
            return apology("This username already been registered!")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    user_id = session['user_id']

    if request.method == 'POST':
        symbol = request.form.get('symbol')
        shares = int(request.form.get('shares'))

        if shares <= 0:
            return apology('Must be a positive number!')
        if not symbol:
            return apology('Must include an ticker symbol')

        stock = lookup(symbol)

        company = stock['name']
        stock_price = stock['price']
        price = stock_price * shares

        shares_owned = db.execute('SELECT shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol', user_id, symbol)[0]['shares']

        if shares_owned < shares:
            return apology("You don't have enough shares!")

        cash = db.execute('SELECT cash FROM users WHERE id = ?', user_id)[0]['cash']
        db.execute('UPDATE users SET cash = ? WHERE id = ?', cash + price, user_id)
        db.execute('INSERT INTO transactions (user_id, name, shares, price, type, symbol) VALUES (?, ?, ?, ?, ?, ?)',
                        user_id, company, -shares, stock_price, 'Sell', symbol)
        return redirect('/')

    else:
        symbols = db.execute('SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol', user_id)
        return render_template('sell.html', symbols=symbols)
