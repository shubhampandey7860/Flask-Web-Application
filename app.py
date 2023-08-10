from flask import Flask, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost / 127.0.0.1 / quiz api'
db = SQLAlchemy(app)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    options = db.Column(db.JSON, nullable=False)
    right_answer = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

def validate_datetime(datetime_str):
    try:
        datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False

@app.route('/create_quiz', methods=['POST'])
def create_quiz():
    data = request.json
    question = data['question']
    options = data['options']
    right_answer = data['rightAnswer']
    start_date = data['startDate']
    end_date = data['endDate']

    if not isinstance(options, list) or not isinstance(right_answer, int):
        return jsonify({'message': 'Options must be an array and rightAnswer must be an integer.'}), 400

    if not (0 <= right_answer < len(options)):
        return jsonify({'message': 'Invalid rightAnswer index.'}), 400

    if not validate_datetime(start_date) or not validate_datetime(end_date):
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD HH:MM:SS.'}), 400

    quiz = Quiz(
        question=question,
        options=options,
        right_answer=right_answer,
        start_date=datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S'),
        end_date=datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    )
    db.session.add(quiz)
    db.session.commit()
    return jsonify({'message': 'Quiz created successfully.'}), 201

@app.route('/get_active_quiz', methods=['GET'])
def get_active_quiz():
    now = datetime.now()
    active_quiz = Quiz.query.filter(Quiz.start_date <= now, Quiz.end_date >= now).first()

    if active_quiz is None:
        return jsonify({'message': 'No active quiz.'}), 404

    return jsonify({
        'question': active_quiz.question,
        'options': active_quiz.options
    }), 200

@app.route('/get_quiz_result', methods=['GET'])
def get_quiz_result():
    now = datetime.now()
    ended_quizzes = Quiz.query.filter(Quiz.end_date < now).all()

    if not ended_quizzes:
        return jsonify({'message': 'No quiz results available yet.'}), 404

    results = []
    for quiz in ended_quizzes:
        results.append({
            'question': quiz.question,
            'right_answer': quiz.options[quiz.right_answer]
        })

    return jsonify(results), 200

if __name__ == '_main_':
    db.create_all()
    app.run(debug=True)