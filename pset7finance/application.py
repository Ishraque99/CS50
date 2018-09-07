from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    ##Variables
    idt = session["user_id"]
    monies = db.execute("SELECT cash FROM users where id = :idt", idt=idt)
    cash = monies[0]["cash"]
    totalsum = cash
    
    portfolio = db.execute("SELECT * FROM portfolios WHERE id = :idt", idt=idt)
    for item in portfolio:
        symbol = item["symbol"]
        units = item["units"]
        quote = lookup(symbol)
        cprice = quote["price"]
        
        totalvalue = units*cprice
        
        totalsum += totalvalue
        db.execute("UPDATE portfolios SET price = :price, totalvalue = :totalvalue WHERE id = :idt AND symbol = :symbol", price=cprice, totalvalue=totalvalue, idt=idt, symbol=symbol)
        
    pfl = db.execute("SELECT * FROM portfolios WHERE id = :idt", idt=idt)
    
    return render_template("index.html", pfl=pfl, cash=cash, totalsum=totalsum)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    quote = {}
    n = None
    cash = 0
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("Invalid Stock")
        
        quoteprice = float(quote["price"])
        n = int(request.form.get("sharen"))
        if not n or n <= 0:
            return apology("Must buy at least 1 share")
            
        ##transaction stuff
            
        cashlist = db.execute("SELECT * FROM users WHERE id = :idt", idt=session["user_id"])
        cash = float(cashlist[0]["cash"])
        totalprice = n*quoteprice
        username = cashlist[0]["username"]
        if not cashlist or cash < totalprice:
            return apology("Database error or insufficient funds")
        
        db.execute("INSERT INTO transactions (id, username, symbol, unitprice, units, totalprice, status) \
                    VALUES (:idn, :username, :symbol, :unitprice, :units, :totalprice, :status)", \
                    idn=session["user_id"], username=username, symbol=quote["symbol"], unitprice=quoteprice, units=n, totalprice=totalprice, status="Bought")
                    
        ##portfolio stuff
        portfolio = db.execute("SELECT * FROM portfolios WHERE username = :username AND id = :idn AND symbol = :symbol", username=username, idn=session["user_id"], symbol=quote["symbol"])
        if not portfolio:
            db.execute("INSERT INTO portfolios (id, username, symbol, units, price) VALUES (:idn, :username, :symbol, :units, :price)", idn=session["user_id"], username=username, symbol=quote["symbol"], units=n, price=quoteprice)
        else:
            
            shares = portfolio[0]["units"] + n
            db.execute("UPDATE portfolios SET units = :shares WHERE id = :idn AND username = :username AND symbol = :symbol", shares=shares, idn=session["user_id"], username=username, symbol=quote["symbol"])
        
        ##cash stuff
        cash = cash - totalprice
        db.execute("UPDATE users SET cash = :cash WHERE id = :idn AND username = :username", cash=cash, idn=session["user_id"], username=username)
        return render_template("buy.html", quote=quote, n=n, cash=cash, username=username, totalprice = totalprice)
    else:
        return render_template("buy.html", quote=quote)

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    ##Variables
    idt = session["user_id"]
    trs = db.execute("SELECT * FROM transactions WHERE id =:idt", idt=idt)
    return render_template("history.html", trs=trs)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    quote = {}
    
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        
        if not quote:
            return apology("Stock info unavailable")
        else:
            return render_template("quote.html", quote=quote)
    else:
        return render_template("quote.html", quote=quote)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    if request.method == "POST":
        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
            
        elif not request.form.get("password2"):
            return apology("must retype password")
        
        elif request.form.get("password") != request.form.get("password2"):
            return apology("Retyped Password must match")
        
        else: 
            hashword = pwd_context.hash(request.form.get("password"))
            result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=hashword)
        
            if not result:
                return apology("Username Already Exists or Database Error")
            
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
            session["user_id"] = rows[0]["id"]
            return redirect(url_for("index"))
        
        return apology("Unknown Error")
            
    else:        
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    
    idt = session["user_id"]
    quote = {}
    n = None
    uc = 0
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("Invalid Stock")
        
        ##Variables
        qs = quote["symbol"]
        qp = float(quote["price"])
        
        n = int(request.form.get("sharen"))
        if not n or n <= 0:
            return apology("Must sell at least 1 share")
        
        ##Portfolio check
        pfl = db.execute("SELECT * FROM portfolios WHERE id = :idt AND symbol = :symbol", idt=idt, symbol=qs)
        if not pfl:
            return apology("Database Error")
        
        m = pfl[0]["units"]
        if n > m:
            return apology("You don't have that many shares to sell")
            
        ##Transaction Stuff
        u = -1*(n)
        tp = u*qp
        
        userinfo = db.execute("SELECT * FROM users WHERE id = :idt", idt=idt)
        
        un = userinfo[0]["username"] 
        db.execute("INSERT INTO transactions (id, username, symbol, unitprice, units, totalprice, status) \
                    VALUES (:idt, :username, :symbol, :unitprice, :units, :totalprice, :status)", \
                    idt=idt, username=un, symbol=qs, unitprice=qp, units=u, totalprice=tp, status="Sold")
        
        ##Portfolio Stuff
        m = m + u
        db.execute("UPDATE portfolios SET units = :m WHERE symbol = :symbol AND id = :idt", m=m, symbol=qs, idt=idt)
        
        ##Cash Stuff
        uc = userinfo[0]["cash"]
        uc = uc - tp
        db.execute("UPDATE users SET cash = :uc WHERE id = :idt AND username = :un", uc=uc, idt=idt, un=un)
        
        return render_template("sell.html", quote=quote, n=n, cash=uc, username=un, totalprice = tp)
    
    else:
        return render_template("sell.html", quote=quote, cash=uc)
        
@app.route("/cngpss", methods=["GET", "POST"])
@login_required
def cngpss():
    """Change password."""
    ##Variables
    idt = session["user_id"]
    currenthash = db.execute("SELECT hash FROM users WHERE id = :idt", idt=idt)
    msg = ""
    #POST Stuff
    if request.method == "POST":
        #Current Password stuff
        if not request.form.get("currentpass"):
            return apology("Enter Current Password")
        
        if len(currenthash) != 1 or not pwd_context.verify(request.form.get("currentpass"), currenthash[0]["hash"]):
            return apology("invalid current password")
            
        
        # ensure password was submitted
        elif not request.form.get("newpass"):
            return apology("must provide New password")
            
        elif not request.form.get("newpass2"):
            return apology("must retype New password")
        
        elif request.form.get("newpass") != request.form.get("newpass2"):
            return apology("Retyped New Password must match")
            
        ##Changing Password
        hesh = pwd_context.hash(request.form.get("newpass"))
        db.execute("UPDATE users SET hash = :hesh WHERE id = :idt", hesh=hesh, idt=idt)
        return render_template("cp.html", msg="Password Changed Succesfully!")
        
    
    else:
        return render_template("cp.html", msg=msg)