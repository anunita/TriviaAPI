from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random
from flask_sqlalchemy import pagination

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    
    paginated = selection.paginate(page=page, per_page=QUESTIONS_PER_PAGE, error_out=False)

    current_questions = [question.format() for question in paginated.items]

    return current_questions



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r'/*': {'origins': '*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    with app.app_context():
        db.create_all()


    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories", methods=["GET"])
    def retrieve_categories():
        try: 
            category = Category.query.order_by(Category.type).all()

            if len(category) == 0:
                abort(404)

            categories = {}
            for cat in category:
                categories[cat.id] = cat.type

            return jsonify ({
                    "success": True,
                    "categories": categories

            })
        except Exception as e:
            print(f"Error retrieving categories: {e}")
            abort(500)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions", methods=["GET"])
    def retrieve_questions():
        try:
            selection = Question.query.order_by(Question.id)
            current_questions = paginate_questions(request, selection)
            if len(current_questions) == 0:
                abort(404)

            category = Category.query.order_by(Category.type).all()
            categories = {}
            for cat in category:
                categories[cat.id] = cat.type

            return jsonify (
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": selection.count(),
                    "categories": categories,
                    "current_category": None
            }) 
        except Exception as e:
            print(f"Error retrieving questions: {e}")
            abort(404)
       
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id)
            current_questions = paginate_questions(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                }
            )

        except Exception as e:
            print(f"Error deleting questions: {e}")
            abort(422)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()

        # to check if the body has all the fields 
        if not ('question' in body and 'answer' in body and
                'difficulty' in body and 'category' in body):
            abort(422)


        new_question = body.get('question')
        new_answer = body.get('answer')
        new_difficulty = body.get('difficulty')
        new_category = body.get('category')
        
        # to check if all fields are provided by user
        if ((new_question is None or new_question == "") or (new_answer is None or new_answer == "") or
                (new_difficulty is None or new_difficulty == "") or (new_category is None or new_category == "")):
            abort(422)

        try:
            create_quest = Question(question=new_question, answer=new_answer, 
                                       difficulty=new_difficulty,category=new_category)
            create_quest.insert()

            return jsonify(
                {
                    "success": True,
                    "created": create_quest.id,
                }
            ), 201
        except Exception as e:
            print(f"Error creating questions: {e}")
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        body = request.get_json()

        search = body.get("searchTerm", None)

        try:
            if search:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search)))
                current_questions = paginate_questions(request, selection)

                return jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "total_questions": selection.count(),
                        "current_category": None
                    }
                )
            abort(404)
        except Exception as e:
            print(f"Error searching questions: {e}")
            abort(500)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_questions_by_category(category_id):
        selection = Question.query.order_by(Question.id).filter(Question.category==category_id)
        current_questions = paginate_questions(request, selection)
        
        try:
            if len(current_questions) == 0:
                abort(404)

            return jsonify (
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": selection.count(),
                    "current_category": category_id
            }) 
        except Exception as e:
            print(f"Error retrieving questions by category: {e}")
            abort(500)    
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_random_question_for_quiz():

        body = request.get_json()
        if not ('quiz_category' in body and 'previous_questions' in body):
            abort(422)

        quiz_category = body.get('quiz_category')
        previous_questions = body.get('previous_questions')

        if ((quiz_category is None) or (previous_questions is None)):
            abort(400)

        try:
            category_id = quiz_category['id']

            if category_id == 0:
                quiz_questions = Question.query.filter(Question.id.notin_((previous_questions))).all()
            else:   
                quiz_questions = Question.query.filter(Question.category==category_id).filter(
                    Question.id.notin_((previous_questions))).all()        
            
            if len(quiz_questions) > 0:
                new_question = random.choice(quiz_questions).format()
            else:
                new_question = None

            return jsonify({
                'success': True,
                'question': new_question
            })
        except Exception as e:
            print(f"Error playing quiz: {e}")
            abort(500)              

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}), 
            400,
        )
    
    @app.errorhandler(500)
    def internal_server(error):
        return (
            jsonify({"success": False, "error": 500, "message": "internal server error"}), 
            500,
        )    
    return app

