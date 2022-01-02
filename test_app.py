import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import app
from models.models import Artist, Movie, setup_db

'''
ROLE CHART TO UNDERSTAND THE TEST OUTCOME
PERMISSION          ASSISTANT           DIRECTOR            PRODUCER
----------------------------------------------------------------------
get:artist              *                   *                   *
get:movies              *                   *                   *
post:artist                                 *                   *
post:movies                                                     *
delete:artist                               *                   *
delete:movies                                                   *
patch:artist                                *                   *
'''

TEST_DATABASE_URI = os.getenv('DATABASE_URL_TEST')
ASSISTANT_TOKEN = os.getenv('ASSISTANT_TOKEN')
DIRECTOR_TOKEN = os.getenv('DIRECTOR_TOKEN')
PRODUCER_TOKEN = os.getenv('PRODUCER_TOKEN')


class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        setup_db(self.app, TEST_DATABASE_URI)
        self.casting_assistant = ASSISTANT_TOKEN
        self.casting_director = DIRECTOR_TOKEN
        self.executive_producer = PRODUCER_TOKEN
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_artist(self):
        res = self.client().get('/artists',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.casting_assistant)
                                })
        data = json.loads(res.data)
        print(data)
        if res.status_code == 200:
            self.assertTrue(data['success'])
            self.assertNotEqual(len(data['artists']), 0)

    def test_get_all_movies(self):
        res = self.client().get('/movies',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.casting_assistant)
                                })
        data = json.loads(res.data)
        print(data)
        if res.status_code == 200:
            self.assertTrue(data['success'])
            self.assertNotEqual(len(data['movies']), 0)

    def test_delete_a_movie_by_assistant(self):
        res = self.client().delete('/movies/1',
                                   headers={
                                        "Authorization": "Bearer {}"
                                        .format(self.casting_assistant)
                                   })
        self.assertEqual(401, res.status_code)

    def test_delete_a_movie_by_director(self):
        res = self.client().delete('/movies/1',
                                   headers={
                                        "Authorization": "Bearer {}"
                                        .format(self.casting_director)
                                   })
        self.assertEqual(401, res.status_code)

    def test_post_a_movie_by_director(self):
        movie = {
            "title": "Captain America",
            "release_date": "2020-03-02",
            "genre": "SuperHero"
        }
        res = self.client().post('/movies',
                                 headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.casting_director)
                                 }, json=movie)
        data = json.loads(res.data)
        print(res.status_code)
        self.assertEqual(401, res.status_code)

    def test_post_a_artist_by_director(self):
        artist = {
            "name": "Brendan Fraser",
            "age": "45",
            "gender": "male",
            "phone": "871869522"
        }
        res = self.client().post('/artists',
                                 headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.casting_director)
                                 }, json=artist)
        data = json.loads(res.data)
        print(data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_patch_a_movie_by_producer(self):
        new_artist = {
            "name": "Jaden Smith",
            "age": "20",
            "gender": "male",
            "phone": "871869523"
        }
        update_artist = {
            "name": "Will Smith",
            "age": "45",
            "gender": "male",
            "phone": "871869524"
        }
        self.client().post('/artists',
                           headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.casting_director)
                           }, json=new_artist)
        artist = Artist.query.filter_by(name='Jaden Smith').first()
        res = self.client().patch('/artists/'+str(artist.id),
                                  headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.executive_producer)
                                  }, json=update_artist)

        data = json.loads(res.data)
        print(data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_delete_a_artist_by_director(self):
        artist = Artist.query.filter_by(name='Will Smith').first()
        res = self.client().delete('/artists/'+str(artist.id),
                                   headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.casting_director)
                                  })
        print(res.status_code)
        self.assertEqual(res.status_code, 200)

    def test_post_a_movie_by_producer(self):
        movie = {
            "title": "Captain America",
            "release_date": "2020-03-02",
            "genre": "SuperHero"
        }
        res = self.client().post('/movies',
                                 headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.executive_producer)
                                 }, json=movie)

        data = json.loads(res.data)
        print(data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_delete_a_movie_by_producer(self):
        movie = Movie.query.filter_by(title='Captain America').first()
        res = self.client().delete('/movies/'+str(movie.id),
                                   headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.executive_producer)
                                   })
        print(res.status_code)
        self.assertEqual(res.status_code, 200)

if __name__ == "__main__":
    unittest.main()
