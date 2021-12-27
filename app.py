from init import app, db
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import sys
from models.models import Artist, Movie, 


app = Flask(__name__)
setup_db(app)
CORS(app)


@app.route('/artists', methods=["GET"])
def artists():
    artists = Artist.query.all()
    if not artists:
        abort(404)
    return jsonify({
        'success': True,
        'actors': [artist.format() for artist in artists]
    }), 200


@app.route('/movies', methods=["GET"])
def movies():
    movies = Movie.query.all()
    if not movies:
        abort(404)
    return jsonify({
        'success': True,
        'actors': [movie.format() for movie in movies]
    }), 200


@app.route('/artists', methods=["POST"])
def new_artist():
    try:
        body = request.get_json()
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
def new_movie():
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
def delete_artist(artist_id):
    try:
        artist = Artist.query.filter(
            Artist.id == artist_id).one_or_none()
        if question is None:
            abort(404)
        artist.delete()
        return jsonify({
            'success' : True,
            'deleted' : Artist.id}
        )
        except Exception:
            abort(422)


@app.route("/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    try:
        movie = Movie.query.filter(
            Movie.id == movie_id).one_or_none()
        if question is None:
            abort(404)
        artist.delete()
        return jsonify({
            'success' : True,
            'deleted' : Movie.id}
        )
        except Exception:
            abort(422)
            
@app.route("/artists/<int:artist_id>", methods=["PATCH"])
def patch_artist(artist_id):
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