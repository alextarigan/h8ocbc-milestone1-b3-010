"""
This is the movies module and supports all the REST actions for the
movies data
"""

from flask import make_response, abort
from config import db
from models import Director, Movies, MoviesSchema


def read_all():
    """
    This function responds to a request for /api/movies
    with the complete list of movies, sorted by id movies

    :return:                json list of all movies for all director
    """
    # Query the database for all the movies
    movies = Movies.query.order_by(Movies.id).all()
    

    # Serialize the list of movies from our data
    movies_schema = MoviesSchema(many=True)
    data = movies_schema.dump(movies)
    return data

def read_one(id):
    """
    This function responds to a request for
    /api/movies/{id}
    with one matching movies for the associated director

    :param id:         Id of the movie
    :return:                json string of movies contents
    """
    # Query the database for the movies
    movies = Movies.query.filter(Movies.id == id).one_or_none()

    # Was a movie found?
    if movies is not None:
        movies_schema = MoviesSchema()
        data = movies_schema.dump(movies)
        return data, 200

    # Otherwise, nope, didn't find that movie
    else:
        abort(404, f"Movies not found for Id: {id}")

def get_director_movies(director_id):
    movies = Movies.query.join(Director, Movies.director_id == Director.id).filter(Director.id == director_id).all()
    print(dir(movies))
    if movies:
        schema = MoviesSchema(many = True)
        data = schema.dump(movies)
        return data
    else:
        return f"Data not found for director_id : {director_id}"
    
def create(director_id,movies):
    """
    This function creates a new movies in the movies structure
    based on the passed in director data

    :param director_id:  director_id to create in movies structure
    :return:        201 on success
    """
    director = Director.query.filter(Director.id == director_id).one_or_none()
    if director is None:
        return f"Director not found for id : {director_id}"

    else:
        schema = MoviesSchema()
        new_movies = schema.load(movies, session=db.session)

        director.movies.append(new_movies)
        db.session.add(new_movies)
        db.session.commit()

        # Serialize and return the newly created director in the response
        data = schema.dump(new_movies)

        return data, 201

def update(id, movies):
    """
    This function updates an existing moves related to the passed in
    movies id.

    :param id:               Id of the movies to update
    :param content:            The JSON containing the note data
    :return:                200 on success
    """
    update_movies = (
        Movies.query.filter(Movies.id == id)
        .one_or_none()
    )

    # Did we find an existing movies?
    if update_movies is not None:

        # turn the passed in movies into a db object
        schema = MoviesSchema()
        update = schema.load(movies, session=db.session)

        # Set the id's to the movies we want to update
        update.id = update_movies.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated note in the response
        data = schema.dump(update_movies)

        return data, 200

    # Otherwise, nope, didn't find that note
    else:
        abort(404, f"Movies not found for Id: {id}")


def delete(id):
    """
    This function deletes a movie from the movies structure
    
    :param id:     Id of the movies to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the note requested
    movies = Movies.query.filter(Movies.id == id).one_or_none()

    # did we find a movies?
    if movies is not None:
        db.session.delete(movies)
        db.session.commit()
        return f"Movies {id} deleted"

    # Otherwise, nope, didn't find that movies
    else:
        abort(404, f"Movies not found for Id: {id}")
