from ast import NotIn, Try
from operator import not_, truediv
import os
from pickle import TRUE
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import cross_origin, CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    #cors = CORS(app,resources={r"*":{"origins" : "*"}})
    cors = CORS(app)
     
   
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization,true")
        response.headers.add("Access-Control-Allow-methods", "GET, POST, PATCH, DELETE, OPTIONS")
        return response

    @app.route("/categories",methods=["GET"])
    def get_categories():
        try:
            categories = Category.query.all()
        except:
            abort(422)
        categories_dict={}
        for category in categories:
            categories_dict[category.id]= category.type

        #formatted_categories = [category.format() for category in categories]

        return jsonify({
            "success": True,
            "categories": categories_dict,
            "total_categories": len(categories_dict)
            })

    @app.route("/questions",methods=["GET"])
    def get_questions():

        page=request.args.get("page",1,type=int)

        start =(page-1)*QUESTIONS_PER_PAGE

        end = start + QUESTIONS_PER_PAGE

        questions = Question.query.all()
        categories = Category.query.all()

        if len(questions[start:end]) == 0:
           abort(404)

        categories_dict={}
        for category in categories:
            categories_dict[category.id]= category.type
        formatted_questions = [question.format() for question in questions]
 
        return jsonify({
            "questions": formatted_questions[start:end],
            "totalQuestions": len(formatted_questions),
            "categories": categories_dict,
            "currentCategory": "History"
            })
  
    @app.route("/questions/<int:id>",methods=["DELETE"])
    def delete_question(id):
        try:
            question=Question.query.filter(Question.id == id).one_or_none()
            if question is None:
                abort(404)
                    
            question.delete()
            return jsonify({
                "success": True,
                "id": id
                })
        except:
            abort(422)

    
    @app.route("/questions", methods=["POST"])
    def add_new_question():

        body=request.get_json()
       
        srchterm=body.get("searchTerm")

        if srchterm is not None:
            try:
                ques_list = Question.query.filter(Question.question.ilike(f"%{srchterm}%"))
            except:
                abort(422)

            formatted_questions = [question.format() for question in ques_list]     

            if len(formatted_questions) == 0:
                abort(404)

            return jsonify({
                "success": True,
                "questions": formatted_questions,
                "totalQuestions":len(formatted_questions),
                "current_category": None
                        })
        else:
            new_question = body.get("question")
            new_answer = body.get("answer")
            new_category = body.get("category")
            new_difficulty = body.get("difficult")

            try:
                question = Question(question = new_question,
                                    answer = new_answer,
                                    category = new_category,
                                    difficulty = new_difficulty)
                question.insert()
            except:
                abort(422)

            return jsonify({
                "success": True 
                })
   
    @app.route("/categories/<int:id>/questions",methods=["GET"])
    def getquesforcategory(id):
        try:

            questions = Question.query.filter(Question.category == id).all()
            category = Category.query.get(id)
        except:
            abort(422)

        if questions and category is None:
            abort(404)

        formatted_questions = [question.format() for question in questions]
        return jsonify({"success": True,
            "success": True,
            "questions": formatted_questions,
            "totalQuestions":  len(formatted_questions),
            "currentCategory": category.type
            })
    
    @app.route("/quizzes",methods=["POST"]) 
    def get_quiz():

        body=request.get_json()
        
        prev_ques = body.get('previous_questions')
        quiz_cat = body.get('quiz_category')


        if quiz_cat['id'] !=  0:
            try:
                questions = Question.query.filter(Question.category == quiz_cat['id']).all()
            except:
                abort(422)
        else:
            try:
                questions = Question.query.all()
            except:
                abort(422)

        if len(questions) == 0:
            abort(404)

        for question in questions:
            if question.id not in prev_ques:
                return jsonify({
                    "success": True,
                    'question': {
                    'id': question.id,
                    'question': question.question,
                    'answer': question.answer,
                    'difficulty':question.difficulty,
                    'category': question.category
                    }
                })
        return jsonify({
            'error': True
            })

    
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
"""
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Unprocessable"
            }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Not Found"
            }), 404
    return app

    return app