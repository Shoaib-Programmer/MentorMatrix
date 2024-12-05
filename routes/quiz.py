from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from notes import generate_answer, generate_choices_from_context, generate_fill_in_the_blank, generate_question, semantic_compare

quiz_blueprint = Blueprint('quiz', __name__)

# Sample storage (replace with database integration)
all_questions = []  # List of all questions
completed_questions = []  # List of completed questions
active_session_questions = []  # Questions for the active session

# Utility function to generate a unique ID for questions
def generate_question_id():
    return len(all_questions) + 1

# Route to display the quiz page
@quiz_blueprint.route('/quiz')
def quiz():
    session_active = 'active_session' in session and session['active_session']
    return render_template('quiz.html',
                           session_active=session_active,
                           questions=active_session_questions,
                           completed_questions=completed_questions)

# Route to start a new quiz session
@quiz_blueprint.route('/start_session', methods=['POST'])
def start_session():
    session['active_session'] = True
    active_session_questions.clear()
    
    # Example of generating questions (could be replaced with database queries)
    for i in range(5):
        question = {
            'id': generate_question_id(),
            'title': f"Sample Question {i + 1}",
            'content': f"This is the content for question {i + 1}.",
            'hint': f"Hint for question {i + 1}.",
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        active_session_questions.append(question)
        all_questions.append(question)
    
    flash('New quiz session started!', 'success')
    return redirect(url_for('quiz.quiz'))

# Route to end the current quiz session
@quiz_blueprint.route('/end_session', methods=['POST'])
def end_session():
    if 'active_session' in session:
        session.pop('active_session')
    flash('Quiz session ended.', 'info')
    return redirect(url_for('quiz.quiz'))

# Route to submit an answer
@quiz_blueprint.route('/submit_answer', methods=['POST'])
def submit_answer():
    question_id = int(request.form.get('question_id'))
    user_answer = request.form.get('answer')

    # Find the question
    question = next((q for q in active_session_questions if q['id'] == question_id), None)
    if question:
        # Move to completed questions
        question['user_answer'] = user_answer
        question['completed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        completed_questions.append(question)
        active_session_questions.remove(question)
        flash('Answer submitted successfully!', 'success')
    else:
        flash('Question not found.', 'danger')

    return redirect(url_for('quiz.quiz'))

# Route to add a new question
@quiz_blueprint.route('/add_question', methods=['POST'])
def add_question():
    title = request.form.get('title')
    content = request.form.get('content')
    hint = request.form.get('hint')

    if not title or not content:
        flash('Title and content are required!', 'danger')
        return redirect(url_for('quiz.quiz'))

    question = {
        'id': generate_question_id(),
        'title': title,
        'content': content,
        'hint': hint,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    all_questions.append(question)
    flash('New question added successfully!', 'success')
    return redirect(url_for('quiz.quiz'))
