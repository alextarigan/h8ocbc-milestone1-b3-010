from dataclasses import field
from datetime import datetime
from email.policy import default
from inspect import BoundArguments
from logging.handlers import TimedRotatingFileHandler
from config import db, ma
from marshmallow import fields

class Director(db.Model):
    __tablename__ = 'directors'
    name = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Integer)
    department = db.Column(db.String)
    uid = db.Column(db.Integer)
    movies = db.relationship(
        'Movies',
        backref='directors',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Movies.popularity)'
    )
class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    original_title = db.Column(db.String)
    budget = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    release_date = db.Column(db.String)
    revenue = db.Column(db.Integer)
    title = db.Column(db.String)
    vote_average = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)
    overview = db.Column(db.String)
    tagline = db.Column(db.String)
    uid = db.Column(db.Integer)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))

class DirectorSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    class Meta:
        model = Director
        # sqla_session = db.session
        load_instance = True
class MoviesSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Movies
        # sqla_session = db.session
        load_instance = True
    
    
    directors = fields.Nested("MovieDirectorSchema", default=None)

class DirectorsWithMoviesSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    class Meta:
        model = Director
        load_instance = True
        include_relationship = True
    movies = fields.Nested(MoviesSchema,default=[],many=True)

class MovieDirectorSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    name = fields.Str()
    gender = fields.Int()
    uid = fields.Int()
    department = fields.Str()