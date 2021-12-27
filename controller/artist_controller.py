from init import app, db
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import sys
from models.artist import Artist

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

