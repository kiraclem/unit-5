# crud operations
from model import db, User, Movie, Rating, connect_to_db


def create_user(email, password):
    """Create and return a new user."""
    user = User(
        email=email,
        password=password
        )
    return user


def get_users():
    """returns all users"""
    return User.query.all()


def get_user_by_id(user_id):
    """returns user's details through id"""
    return User.query.get(user_id)


def get_user_by_email(email):
    """returns a user based on email"""
    return User.query.filter(User.email == email).first()


def create_movie(title, overview, release_date, poster_path):
    """creates and returns a movie"""
    movie1 = Movie(
        title=title,
        overview=overview,
        release_date=release_date,
        poster_path=poster_path
        )
    return movie1


def get_movies():
    """returns all movies"""
    return Movie.query.all()


def get_movie_by_id(movie_id):
    """returns a movie's details through id"""
    return Movie.query.get(movie_id)


def create_rating(user, movie, score):
    """creates and returns a rating"""
    rating1 = Rating(
        user=user, 
        movie=movie, 
        score=score
        )
    return rating1


def get_ratings_by_user(user):
    user = User.query.get(user)
    return user.ratings


if __name__ == '__main__':
    from server import app
    connect_to_db(app)

