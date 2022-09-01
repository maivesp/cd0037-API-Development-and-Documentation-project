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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {"question": "test question 1", "answer": "test answer 1", "category": 4,"difficulty":1}
        self.searchTerm = {"searchTerm": "Test"}
        self.searchTerm1 = {"searchTerm": "Prabhu"}
        self.quiz_req = {"previous_questions": [12,23,53,55,78,79,80],'quiz_category': 1}
        self.quiz_req1 = {"previous_questions": [12,23,53,55,78,79,80,81,82],'quiz_category': 1}


    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res=self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])

    def test_get_questions(self):
        res=self.client().get("/questions")
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])


    def test_get_questions_page_found(self):
        res=self.client().get("/questions?page=1")
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])

    def test_get_questions_page_not_found(self):
        res=self.client().get("/questions?page=100")
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource Not Found")

    def test_questions_delete(self):
        res=self.client().delete("/questions/9")
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['id'])

    def test_questions_cant_delete(self):
        res=self.client().delete("/questions/1")
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource Not Found")

    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_search_question_found(self):
        res = self.client().post("/questions", json=self.searchTerm)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(len(data["questions"]))
#        self.assertTrue(data["current_category"])

    def test_search_question_notfound(self):
        res = self.client().post("/questions", json=self.searchTerm1)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource Not Found")

    def test_get_questions_by_category(self):
        res=self.client().get("/category/1/questions")
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['totalQuestions'],len(data['questions']))
        self.assertTrue(data['currentCategory'])

    def test_get_questions_by_category_notfound(self):
        res=self.client().get("/category/100/questions")
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource Not Found")    
        
    def test_get_quizzes_found(self):
        res=self.client().get("/quizes",json=self.quiz_req)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])

    def test_get_quizzes_found(self):
        res=self.client().get("/quizes",json=self.quiz_req1)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'],404)
        self.assertEqual(data['message'],"Resource Not Found")
       
# Make the tests conveniently"currentCategory" executable
if __name__ == "__main__":
    unittest.main()