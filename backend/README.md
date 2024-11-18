# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

### API Documentation

****
GET "\categories" 
curl -X GET 'http://127.0.0.1:5000/categories'

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Parameters: None
- Response Body:

categories: A dictionary containing Category ID and Category Type as a key value pair

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

****
GET "\questions?page=<page_number>" 
curl -X GET 'http://127.0.0.1:5000/questions' 
curl -X GET 'http://127.0.0.1:5000/questions?page=2'

- Fetches a paginated dictionary of questions of all available categories. A page contains 10 questions.
- Request parameters (optional): page number in integer
- Response Body:

categories: A dictionary containing Category ID and Category Type as a key value pair
current_category: Null 
questions: List of questions
total_questions: Total Number of questions

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_questions": 46
}
```

****
DELETE "/questions/<question_id>" 
curl -X DELETE 'http://127.0.0.1:5000/questions/2'

- Delete an existing questions from the available questions based on the question ID
- Request Parameters: question_id in integer that needs to be deleted
- Response Body:

deleted: Question ID that is deleted

```json
{
  "deleted": "49",
  "success": true
}
```

****
POST "/questions"   
curl -X POST -H "Content-Type: application/json" -d '{"question":"What is the capital city of India?", "answer":"New Delhi", "difficulty":2, "category":3}' 'http://127.0.0.1:5000/questions'


- Add a new question to the list of available questions
- Request Paremeter: Need to provide the new question and its answer, difficulty level and category ID in the following format
{question:string, answer:string, difficulty:int, category:int}
- Response Body: 

created: Question ID that is created

```json
{
  "created": 91, 
  "success": true
}
```

****
POST "/questions/search"    
curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"Taj"}' 'http://127.0.0.1:5000/questions/search'

- Fetches all questions based on the search string provided (not case-sensitive)
- Request body: Need to provide the search string in the following format 
{searchTerm:string}
- Response Body:

current_category: Null 
questions: List of questions having the search string (not case sensitive)
total_questions: Total Number of questions having the search string

```json
{
  "current_category": null,
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

****
GET "/categories/<int:category_id>/questions"  
curl -X GET 'http://127.0.0.1:5000/categories/2/questions'

- Fetches a dictionary of questions for the given category ID
- Request Parameter: Category ID for questions should be in integer
- Response Body:

current_category: Current category ID 
questions: List of questions under the given category
total_questions: Total Number of questions under the given category

```json
{
  "current_category": 2,
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

****
POST "/quizzes" 
For a particular category :  
curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": "Sports", "id": "6"}}' 'http://127.0.0.1:5000/quizzes'    
For All categories: 
curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": "click", "id": 0}}' 'http://127.0.0.1:5000/quizzes'

- Fetches one random question within a specified category or all categories based on the option chosen. It does not repeat the previous question. 
- Request Parameter: The request parameter consists of previous questions and quiz category containing category ID and category type
{previous_questions: arr, quiz_category: {id:int, type:string}}
- Response Body:

question: Random questions under the given or any category based on the option chosen

```json
{
  "question": {
    "answer": "The Liver", 
    "category": 1, 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }, 
  "success": true
}
```

## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
