from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from notes import generate_quiz_basic  # Function to generate a Quiz object
from models import db

# Blueprint for quiz-related routes
quiz_blueprint = Blueprint('quiz', __name__)

# Sample storage (replace with database integration)
all_questions = []  # List of all questions
completed_questions = []  # List of completed questions
active_session_questions = []  # Questions for the active session

# Utility function to generate a unique ID for questions
def generate_question_id():
    """
    Generate a unique ID for each question based on the length of all_questions list.
    """
    return len(all_questions) + 1

# Route to display the quiz page
@quiz_blueprint.route('/quiz')
def quiz():
    """
    Display the quiz page with the active session questions and completed questions.
    """
    session_active = 'active_session' in session and session['active_session']
    return render_template(
        'quiz.html',
        current_route='quiz',
        session_active=session_active,
        questions=active_session_questions,
        completed_questions=completed_questions
    )

# Route to start a new quiz session
@quiz_blueprint.route('/start_session', methods=['POST'])
def start_session():
    """
    Start a new quiz session by generating questions using the `generate_quiz_basic` function.
    """
    session['active_session'] = True
    active_session_questions.clear()

    # Replace this with dynamic context retrieval logic
    context = request.form.get('context')  # Get context from the user form input
    if not context:
        flash('Please provide a valid context to start a quiz!', 'danger')
        return redirect(url_for('quiz.quiz'))

    # Generate quiz questions using `generate_quiz_basic`
    try:
        quiz = generate_quiz_basic(context)  # Generates a Quiz instance
    except Exception as e:
        flash(f"Error generating quiz: {str(e)}", 'danger')
        return redirect(url_for('quiz.quiz'))

    # Populate active session questions
    for question in quiz.open_ended + quiz.multiple_choice:
        question['id'] = generate_question_id()  # Assign unique ID to each question
        question['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        active_session_questions.append(question)
        all_questions.append(question)

    flash('New quiz session started!', 'success')
    return redirect(url_for('quiz.quiz'))

# Route to end the current quiz session
@quiz_blueprint.route('/end_session', methods=['POST'])
def end_session():
    """
    End the current quiz session by clearing the active session data in Flask session.
    """
    if 'active_session' in session:
        session.pop('active_session')
    flash('Quiz session ended.', 'info')
    return redirect(url_for('quiz.quiz'))

# Route to submit an answer
@quiz_blueprint.route('/submit_answer', methods=['POST'])
def submit_answer():
    """
    Submit an answer for a question in the active session. 
    Moves the question to completed questions after submission.
    """
    question_id = int(request.form.get('question_id'))
    user_answer = request.form.get('answer')

    # Find the question in active session
    question = next((q for q in active_session_questions if q['id'] == question_id), None)
    if question:
        # Mark as completed and store the user answer
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
    """
    Add a new question to the quiz. Requires a title and content as minimum inputs.
    """
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
