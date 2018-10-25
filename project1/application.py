import os
import requests

from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register/form_completed", methods=["POST"])
#get form information
def form_completed():
    try:
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
    except ValueError:
        return render_template("error.html", message="Check all the forms!")

#Check if the username is already taken
    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone():
        return render_template("error.html", message="Username already taken")
    db.execute("INSERT INTO users (username, password, mail) VALUES (:username, :password, :email)", {"username": username, "password": password, "email": email})
    db.commit()
    return render_template("success.html")

#Login
@app.route("/home", methods=["POST"])
def home():

    try:
        username = request.form.get("username")
        password = request.form.get("password")
    except ValueError:
        return render_template("error.html")

    if (username == "" or password == ""):
        return render_template("error.html", message="Fill username and password")

    user = db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username": username, "password": password}).fetchone()
    if user == None:
        return render_template("error.html", message="Username does not exist or password incorrect.")

    session['key'] = '1'
    session['user_id'] = user.id
    return render_template("home.html", user=username)

@app.route("/search", methods=["POST","GET"])
def search():
    if ( request.method == "GET" and session['key'] == '1'):
        return render_template("home.html")
    if session['key'] == '0':
        return render_template("error.html", message="Not logged in.")

    try:
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        author = request.form.get("author")
    except ValueError:
        return render_template("errorb.html", message="Insert author.")

    if (isbn == "" and title == "" and author == ""):
        return render_template("errorb.html", message="You must fill at least one form in order to search a book.")

    try:
        books = db.execute("SELECT DISTINCT * FROM (SELECT DISTINCT * FROM (SELECT DISTINCT * FROM books WHERE author iLIKE :author) AS valid_name WHERE title iLIKE :title) AS valid_name WHERE isbn iLIKE :isbn ORDER BY title DESC", {"isbn": '%'+isbn+'%', "title": '%'+title+'%', "author": '%'+author+'%'}).fetchall()
        return render_template("search.html", books=books)
    except ValueError:
        return render_template("errorb.html", message = "No matches.")

@app.route("/logout", methods=["POST"])
def logout():
    session['key']='0'
    session['user_id'] = None
    session['control']= 0
    return render_template("logout.html")

@app.route("/review", methods=["POST","GET"])
def review():
    if request.method == "GET":
        if session['key'] == '1':
            session['book_id'] = request.args.get('book_id')
            try:
                book = db.execute("SELECT * FROM books WHERE book_id = :book_id", {"book_id": session['book_id']}).fetchone()
                reviews = db.execute("SELECT * FROM reviews WHERE r_book_id = :r_book_id", {"r_book_id": session['book_id']}).fetchall()
                #res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "HMi6BEjUA6UtwzymbnKw", "isbns": "book.isbn"})
                #print(res.json())
                for review in reviews:
                    if review.r_user_id == session['user_id']:
                        session['control']=1
                        break
            except ValueError:
                return render_template("error.html");

            return render_template("review.html", book=book.title, reviews=reviews)

        return render_template("error.html", message="Not logged in.")

    try:
        review=request.form.get('review')
    except ValueError:
        return render_template("error.html")

    if session['control']==1:
        return render_template("errorb.html", message= "One review per user.")


    if review == None:
        return render_template("errorb.html", message="Review cannot be empty.")


    db.execute("INSERT INTO reviews (review, r_user_id, r_book_id) VALUES (:review, :r_user_id, :r_book_id)", {"review": review, "r_user_id": session['user_id'], "r_book_id": session['book_id']})
    db.commit()
    return render_template("successb.html")

@app.route("/api/<isbn>", methods=["GET"])
def api(isbn):
    #res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "HMi6BEjUA6UtwzymbnKw", "isbns": isbn})
    #if res.status_code != 200:
    #    raise Exception("ERROR: API request unsuccessful.")

    #book = res.json()
    #return render_template("api.html", isbn=book["books"][0]["reviews_count"])
    # Make sure flight exists.
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()

    if book is None:
        return jsonify({"error": "Invalid ISBN"}), 422

    return jsonify({
            "book_id": book.book_id,
            "isbn": book.isbn,
            "title": book.title,
            "author": book.author
        })




#@app.route("/casos", methods=["GET","POST"])
def casos():

    if request.method == "GET":
        return render_template("gsa.html")

    try:
        ot = request.form.get("ot")
        base = request.form.get("base")
        caso = request.form.get("caso")
    except ValueError:
        return render_template("error.html")

    db.execute("INSERT INTO casos (ot, base, caso) VALUES (:ot, :base, :caso)",
            {"ot": ot, "base": base, "caso": caso})
    db.commit()
    return render_template("gsa.html")

@app.route("/casos/listar", methods=["GET","POST"])
def listar():
    casos = db.execute("SELECT * FROM casos ORDER BY base DESC").fetchall()
    return render_template("listar.html", casos=casos)

#for isbns!!!
#@app.route("/api/<isbn>", methods=["GET"])
#def api():
#    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "HMi6BEjUA6UtwzymbnKw", "isbns": "<isbn>"})
#    print(res.json())
