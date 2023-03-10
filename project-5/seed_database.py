import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server 

os.system("dropdb ratings")
os.system("createdb ratings")

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

movies_in_db = []
for movie in movie_data:
    title = movie["title"]
    overview = movie["overview"]
    poster_path = movie["poster_path"]

    date_string = movie["release_date"]
    format = "%Y-%m-%d"
    release_date = datetime.strptime(date_string, format)

    db_movie = crud.create_movie(title, overview, release_date, poster_path) 
    movies_in_db.append(db_movie)

model.db.session.add_all(movies_in_db)
model.db.session.commit()

for n in range(10):
    email = f"user{n}@mail.com" 
    password= f"123{n}test"

    db_user = crud.create_user(email, password)
    model.db.session.add(db_user)

    for r in range(3):
        random_movie = choice(movies_in_db)
        random_score = randint(1,5)

        db_rating = crud.create_rating(db_user, random_movie, random_score)
        model.db.session.add(db_rating)

model.db.session.commit()