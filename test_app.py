import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import app
from models.models import Artist, Movie, setup_db


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
            # create all tables
            #create_and_drop_all()
            # self.db.create_all()

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
            


if __name__ == "__main__":
    unittest.main()