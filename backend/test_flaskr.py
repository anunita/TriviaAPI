import os
import unittest
import json

from flaskr import create_app
from models import db, Question, Category, setup_db
from dotenv import load_dotenv
import os 

load_dotenv()

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
    
        self.database_host = os.getenv("database_host")
        self.database_name = os.getenv("database_name_test")
        self.database_user = os.getenv("database_user")
        self.database_password = os.getenv("database_password")
        if self.database_password:
            self.database_path = f'postgresql://{self.database_user}:{self.database_password}@{self.database_host}/{self.database_name}'
        else:
            self.database_path = f'postgresql://{self.database_user}@{self.database_host}/{self.database_name}'

        # Create app with the test configuration
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        # Bind the app to the current context and create all tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # test cases for getting valid and invalid categories

    def test_get_categories(self):
        res = self.client.get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))

    def test_404_sent_requesting_invalid_categories(self):
        res = self.client.get("/categories/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # test cases for getting questions for valid and invalid number of pages 

    def test_get_paginated_questions(self):
        res = self.client.get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["categories"]))

    def test_404_sent_requesting_questions_beyond_valid_page(self):
        res = self.client.get("/questions?page=100000000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # test cases for deleting valid and invalid question id
    def test_delete_question(self):
        with self.app.app_context():
            sample_question = Question(question="what is the sample question?", answer="this",
                                   difficulty = 1, category = 3)
            sample_question.insert()
            sample_question_id = sample_question.id

            res = self.client.delete(f'/questions/{sample_question_id}')
            data = json.loads(res.data)

            question = Question.query.filter(Question.id == sample_question_id).one_or_none()

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["success"], True)
            self.assertEqual(data["deleted"], str(sample_question_id))
            self.assertEqual(question, None)
    
    def test_422_if_question_does_not_exist(self):
        res = self.client.delete("/questions/-1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    # test cases for creating valid and invalid questions
    def test_create_new_question(self):
        sample_question = {"question": "what is the sample question?", 
                           "answer": "this",
                           "difficulty": 1, 
                           "category":  3}
        res = self.client.post("/questions", json=sample_question)
        data = json.loads(res.data)    

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)    
        self.assertTrue(data["created"])
    
    def test_422_if_question_creation_not_allowed(self):
        sample_question = {"question": "what is the sample question?", 
                           "answer": "this",
                           "difficulty": 1}
        res = self.client.post("/questions", json=sample_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    # test cases for searching valid and invalid keywords in questions
    def test_get_question_search_with_results(self):
        res = self.client.post("/questions/search", json={"searchTerm": "is"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])
    
    def test_get_book_search_without_results(self):
        res = self.client.post("/questions/search", json={"searchTerm": {}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "internal server error")
    
    # test cases for getting valid and invalid questions by categories
    def test_get_questions_by_category(self):
        res = self.client.get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
    
    def test_404_get_questions_by_category(self):
        res = self.client.get('/categories/-1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    
    # test cases for playing quiz with valid and invalid inputs sent
    def test_play_quiz(self):
        quiz = {'previous_questions': [],
                          'quiz_category': {'type': 'click', 'id': 0}}

        res = self.client.post('/quizzes', json=quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_422_play_quiz_fields_missing(self):
        quiz = {'quiz_category': {'type': 'click', 'id': 0}}
        res = self.client.post('/quizzes', json=quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
