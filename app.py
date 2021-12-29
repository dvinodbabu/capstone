from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import sys
from models.models import Artist, Movie, setup_db
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    """ 
    create app method, sets the db and CORS related configuration
    Args:
    Returns:
    """
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


    @app.route('/testdata')
    def setuptestdata():
        setup_data()

    @app.route('/artists', methods=['GET'])
    @requires_auth('get:artist')
    def artists(jwt):
        artists = Artist.query.all()
        if not artists:
            abort(404)
        return jsonify({
            'success': True,
            'actors': [artist.get_formatted_json() for artist in artists]
        }), 200


    @app.route('/movies', methods=["GET"])
    @requires_auth('get:movies')
    def movies(jwt):
        movies = Movie.query.all()
        if not movies:
            abort(404)
        return jsonify({
            'success': True,
            'actors': [movie.get_formatted_json() for movie in movies]
        }), 200


    @app.route('/artists', methods=["POST"])
    @requires_auth('post:artist')
    def new_artist(jwt):
        try:
            body = request.get_json()
            print(body)
            print(body.get("name", None))
            artist = Artist(name=body.get("name", None),
                            age=body.get("age", None),
                            gender=body.get("gender", None),
                            phone=body.get("phone", None))
            Artist.insert(artist)
            return jsonify({
                "success": True
            })
        except Exception as e:
            print(repr(e))
            abort(422)


    @app.route('/movies', methods=["POST"])
    @requires_auth('post:movies')
    def new_movie(jwt):
        try:
            body = request.get_json()
            movie = Movie(title=body.get("title", None),
                        genre=body.get("age", None),
                        release_date=body.get("release_date", None))
            Movie.insert(movie)
            return jsonify({
                "success": True
            })
        except Exception as e:
            print(repr(e))
            abort(422)

    @app.route("/artists/<int:artist_id>", methods=["DELETE"])
    @requires_auth('delete:artist')
    def delete_artist(jwt, artist_id):
        try:
            artist = Artist.query.filter(
                Artist.id == artist_id).one_or_none()
            if question is None:
                abort(404)
            artist.delete()
            return jsonify({
                'success' : True,
                'deleted' : Artist.id
            })
        except Exception as e:
            abort(422)


    @app.route("/movies/<int:movie_id>", methods=["DELETE"])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        try:
            movie = Movie.query.filter(
                Movie.id == movie_id).one_or_none()
            if question is None:
                abort(404)
            artist.delete()
            return jsonify({
                'success' : True,
                'deleted' : Movie.id
            })
        except Exception as e:
            abort(422)
            
    @app.route("/artists/<int:artist_id>", methods=["PATCH"])
    @requires_auth('patch:artist')
    def patch_artist(jwt, artist_id):
        try:
            artist = Artist.query.filter(Artist.id == artist_id).one_or_none()
            if artist is None:
                abort(404)
            artist.name = request.get_json().get("name", None)
            artist.age = request.get_json().get("age", None)
            artist.gender = request.get_json().get("gender", None)
            artist.phone = request.get_json().get("phone", None)
            Artist.update(artist)
            return jsonify({
                "success": True
            })
        except Exception as e:
            print(repr(e))
            abort(422)
     
    @app.after_request
    def after_request(response):
        """
        Method will be called after the request and adds the below paramteres
        in the response headers.
        Access-Control-Allow-Headers=Content-Type, Authorization
        Access-Control-Allow-Methods=GET, POST, PATCH, DELETE, OPTION
        Args:
        Returns:
        """
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTION')
        return response
    
    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server Error"
        }), 500
        
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app