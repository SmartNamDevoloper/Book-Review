import os;
import requests
from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.exc import IntegrityError

app=Flask(__name__)

# engine = create_engine(os.getenv(DATABASE_URL))
engine = create_engine("postgres://khwgtrmjmjgyqr:c7be07a0488d99e4cfa1d3524c2c9070b98a687632351c8739ee5186a31cb969@ec2-52-44-55-63.compute-1.amazonaws.com:5432/deudp50obrak6t")
db = scoped_session(sessionmaker(bind=engine))
session={}

@app.route("/")
def login():
    name = session.get("name")
    if name:
        # print(f"Session user name: {name}")
        return render_template("welcome.html", name=name, message="You are logged in ")

    return render_template("login.html")

@app.route("/register_form")
def register_form():
    return render_template("register_form.html")

@app.route("/register",methods=["POST"])
def register():
    try:
        name = request.form.get ("name")
        password=request.form.get("password")
        if(not name or not password):
            return render_template("error_login.html", message="User name and password fields are required!")
        db.execute("INSERT INTO book_user (name, password) VALUES (:name, :password)",
                {"name": name, "password": password})
        db.commit()
        return render_template("login.html")

    except IntegrityError:
        return render_template("error_login.html", message="User name already exists. Try again")

@app.route("/check_login", methods=["POST"])
def check_login():
    name = request.form.get("name")
    password = request.form.get("password")
    if(not name or not password):
        return render_template("error_login.html", message="User name and password fields are required!")
    user_exists =db.execute("SELECT * FROM book_user WHERE name = :name and password = :password", {"name": name,"password": password}).fetchone()
    # print(f"User Exists{user_exists}")
    if not user_exists:
        return render_template("error_login.html", message="Error in username or password. If you haven't registered please register")

    session["name"]=name
    return render_template("welcome.html", name=session.get("name"))

@app.route("/logout")
def logout():
    name=session.pop("name")
    return render_template("logged_out.html",message=f"Good Bye {name}")

@app.route("/search_book", methods=["POST"])
def search_book():
    search_book_criteria = request.form.get("search_book_criteria")
    search_text =  request.form.get("search_text")
    books_list = db.execute(f"SELECT * FROM books WHERE {search_book_criteria} ILIKE '%{search_text}%' ").fetchall()
    if not books_list :
        return render_template("error_book.html", message ="Did not match any books")
    return render_template("book_list.html", books_list=books_list)

@app.route("/book_info/<int:book_id>")
def book_info(book_id):
    book_info = db.execute("SELECT * FROM books WHERE id=:id", {"id":book_id}).fetchone()

    if(book_info is None):
        return render_template("error_book.html", message = "Book does not exist")

    book_review = db.execute("SELECT * FROM reviews WHERE book_id=:book_id", {"book_id":book_id}).fetchall()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "s1Rc8XiHtGBq55HT4ojZw", "isbns": book_info.isbn})
    # print(res.json())
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    goodreads_review_count = data["books"][0]
    goodreads_review_count = data["books"][0]["reviews_count"]
    goodreads_average_rating = data['books'][0]['average_rating']
    # print(f"goodreads_review_count:{goodreads_review_count}")

    return render_template("book_details.html", book_info=book_info, book_review=book_review, goodreads_review_count=goodreads_review_count, goodreads_average_rating =goodreads_average_rating)

@app.route("/review", methods=['POST'])
def review():
    try:
        book_id=request.form.get ("book_id")
        review_text = request.form.get ("review_text")
        rating=request.form.get("rating")
        name=session.get("name")

        user_id = db.execute("SELECT id FROM book_user WHERE name=:name",{"name":name}).fetchone()
        user_id = user_id[0]
        exists =  db.execute("SELECT * FROM reviews WHERE book_id=:book_id and user_id =:user_id",{"book_id":book_id,"user_id":user_id}).fetchall()
        # print(f"Does a record already exist:{exists}")
        if len(exists):
            return render_template("error_book.html", message="Your review for this book already exists")

        db.execute("INSERT INTO reviews (book_id,user_id,user_review, user_review_score) VALUES (:book_id, :user_id, :review_text, :rating)",
                {"book_id":book_id, "user_id":user_id, "review_text":review_text, "rating":rating})
        db.commit()
        return render_template("success.html")

    except IntegrityError:
        return render_template("error_book.html", message="Error while uploading your review")

@app.route("/api/<string:isbn>")
def book_review_api(isbn):
    review_count =0
    average_score=0
    # Make sure book exists.
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
    # print(f"Book in API{book}")
    if book is None:
        # return jsonify({"error": "Invalid isbn"}), 422
        return render_template('api_error.html', title = 'Invalid Isbn'), 404
    reviews = db.execute("SELECT * FROM reviews WHERE book_id=:book_id",{"book_id":book[0]}).fetchall()
    # print(f"review in API{review}")


     #Calculate the average score
    if reviews:
        review_count=len(reviews),
        total_reviews=[]
        for a_review in reviews:
             total_reviews.append(a_review[3])

        print(f"Total Reviews{total_reviews}")

        average_score = sum(total_reviews)/len(total_reviews)
    return jsonify({
                    "title": book[2],
                    "author": book[3],
                    "year": book[4],
                    "isbn": book[1],
                    "review_count": len(reviews),
                    "average_score": average_score
                    })
