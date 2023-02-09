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

    return render_template("homepage.html")

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
    return render_template("show_user.html", allusers=allusers)

@app.route("/users/<user_id>")
def user_details(user_id):
    """view user details"""

    users = crud.get_user_by_id(user_id)
    return render_template("view_users.html", users=users)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

