API Reference
Getting Started
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.


Error Handling
Errors are returned as JSON objects in the following format:

{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
The API will return 2 error types when requests fail:

404: Resource Not Found
422: Not Processable

Endpoints
---------
GET/categories
---------------
General:
Returns a list of categories, success value, and total categories

Sample: curl http://127.0.0.1:5000/categories

Response Body:
--------------
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
GET/questions
-------------
Returns a list of questions, success value, Total questions, dictionary of categories and current category

Sample: curl http:/127.0.0.1:5000/questions


Response Body:
--------------

{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History",
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    {
      "answer": "Thiruvalluvar",
      "category": 4,
      "difficulty": 2,
      "id": 53,
      "question": "Who is the greatest poet in the world'?"
    }
  ],
  "success": true,
  "totalQuestions": 31
}

GET /questions?page=4
---------------------
Returns a list of questions for the page number passed as query parm, success value, Total questions, dictionary of categories and current category

Sample: curl http:/127.0.0.1:5000/questions?page=4


Response Body:
--------------

E:\Udacity\cd0037-API-Development-and-Documentation-project\backend>curl http:/127.0.0.1:5000/questions?page=4
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History",
  "questions": [
    {
      "answer": "test answer 1",
      "category": 4,
      "difficulty": null,
      "id": 86,
      "question": "test question 1"
    }
  ],
  "success": true,
  "totalQuestions": 31
}

DELTE /questions/<int:id>
--------------------------
Delete the question of the ID that is passed. Returns the id of the deleted question and success value.

curl -X DELETE http://127.0.0.1:5000/questions/10

E:\Udacity\cd0037-API-Development-and-Documentation-project\backend>curl -X DELETE http://127.0.0.1:5000/questions/20
{
  "id": 20,
  "success": true
}


POST /questions
---------------
General:
Returns a list of questions that matches the search term passed, along with the success value, Total no of matched questions and Current Category.

curl "http://127.0.0.1:5000/questions" -X POST -H "Content-Type: application/json" --data "{\"searchTerm\": \"poet\"}"

Request Body:
-------------
{"searchTerm": "poet"}

Response Body:
--------------
{
    "current_category": null,
    "questions": [
        {
            "answer": "Thiruvalluvar",
            "category": 4,
            "difficulty": 2,
            "id": 53,
            "question": "Who is the greatest poet in the world'?"
        }
    ],
    "success": true,
    "totalQuestions": 1
}

POST /questions
---------------
General:
Creates a new question using the answer, category, difficulty, and question that is passed in the request body and returns the sucess value

curl "127.0.0.1:5000/questions" -X POST -H "Content-Type: application/json" --data "{\"answer\": "\layaraja\", \"category\": 4,\"difficulty\": 2,\"question\": \"Who is the best music composer in India\"}"  

Request Body:
-------------

{
"answer": "Thiruvalluvar", 
"category": 4, 
"difficulty": 2, 
"question": "Who is the greatest poet in the world'?"

}
Response Body:
--------------
{"success":true}



GET /categories/<int:id>/questions
----------------------------------

General:
Returns a list of questions that matches the category that is passed, along with the success value, Total number of question and Current Category

curl -X GET http://127.0.0.1:5000/categories/1/questions


Response Body:
--------------
{
  "currentCategory": "Science",
  "questions": [
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "science answer 2",
      "category": 1,
      "difficulty": null,
      "id": 66,
      "question": "science question 2"
    }
  ],
  "success": true,
  "totalQuestions": 3
}



GET http://127.0.0.1:5000/quizzes
----------------------------------
General:
Returns the next question that is not in the list of previous questions thaat is passed. If the quiz cateogry is passed as zero then list of all questions irrespective of categories is returned.

Request Body:
--------------
{
    "previous_questions": [
        5,
        9,
        23
    ],

    "quiz_category": {"id": 4
    }
}


Response Body:
--------------
{
    "question": {
        "answer": "George Washington Carver",
        "category": 4,
        "difficulty": 2,
        "id": 12,
        "question": "Who invented Peanut Butter?"
    },
    "success": true
}
