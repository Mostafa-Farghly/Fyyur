import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('student', 'student', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_questions_defaut_page(self):
        """
        GET request for '/questions' endpoint should return a list of
        questions (default page), number of total questions, current category, categories.  
        """
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(len(data['categories']))
        self.assertTrue(len(data['questions']))

    def test_get_paginated_questions_page_2(self):
        """
        GET request for '/questions?page=2' endpoint should return a list of
        questions (page 2), number of total questions, current category,
        categories.  
        """
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(len(data['categories']))
        self.assertTrue(len(data['questions']))

    def test_404_requesting_paginated_questions_beyond_valid_page(self):
        """
        GET request for '/questions?page=1000' endpoint should result in
        a 404 error, as it is requesting beyond the valid pages.
        """
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()