"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "TheLegendOfZelda"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """view homepage"""
    logged_in = session.get("user_id")

    if logged_in:
        return redirect("/home")
    else:
        return render_template("homepage.html")

@app.route("/home")
def home():
    """view home logged in"""
    return render_template("home_logged_in.html")

@app.route("/movies")
def view_movies():
    """view all movies"""

    movies = crud.get_movies()
    return render_template("view_movies.html", movies=movies)

@app.route("/movies/<movie_id>")
def movie_details(movie_id):
    """shows a movies details"""

    movie = crud.get_movie_by_id(movie_id)
    return render_template("show_movie.html", movie=movie)

@app.route("/users")
def view_users():
    """view all users"""

    allusers = crud.get_users()
    return render_template("view_users.html", allusers=allusers)

@app.route("/users/<user_id>")
def user_details(user_id):
    """view user details"""

    user = crud.get_user_by_id(user_id)
    return render_template("show_user.html", user=user)

@app.route("/users", methods=["POST"])
def register_user():
    """creates a new user"""
    email = request.form.get("email")
    password = request.form.get("password")

    email_check = crud.get_user_by_email(email)
    
    if email_check:
        flash("Try again, that user already exists")
    else:
        user1 = crud.create_user(email, password)
        db.session.add(user1)
        db.session.commit()
        flash("user successfully added")  
    return redirect("/")

@app.route("/login", methods=["POST"])
def login_user():
    """logs in a user"""
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)
    
    if user:
        if user.password == password:
            session["user_id"] = user.user_id
            flash("successfully logged in") 
        else:
            flash("login information doesn't match, please try again.")
            return redirect("/")
    else:
        flash("login information doesn't match, please try again.")
    return redirect("/")

@app.route("/logout")
def logout():
    """logs the user out"""

    del session["user_id"]
    flash("you successfully logged out!")
    return redirect("/")

@app.route("/movies/<movie_id>/rate")
def rate(movie_id):

    logged_in = session.get("user_id")

    if logged_in:
        movie = crud.get_movie_by_id(movie_id)
        return render_template("rate_movie.html", movie=movie)
    else:
        flash("please log in to access this feature")
        return redirect("/")

@app.route("/movies/<movie_id>/rate", methods=["POST"])
def rated(movie_id):
    """adds a rating to database"""
    logged_in = session.get("user_id")

    if logged_in:
        score = request.form.get("radio_rating")
        user = crud.get_user_by_id(logged_in)
        movie = crud.get_movie_by_id(movie_id)

        movie_rating = crud.create_rating(user, movie, score)

        db.session.add(movie_rating)
        db.session.commit()
        return redirect("/")
    else:
        flash("please log in to access this page")
        return redirect("/")

@app.route("/ratings")
def view_ratings():
    """view ratings"""

    logged_in = session.get("user_id")

    if logged_in:
        user_id = session["user_id"]
        ratings = crud.get_ratings_by_user(user_id)
        return render_template("view_ratings.html", ratings=ratings)
    else:
        flash("please log in to access this feature")
        return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

