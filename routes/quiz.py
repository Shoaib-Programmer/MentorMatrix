from flask import Blueprint, render_template, request, redirect, url_for, flash
from notes import generate_answer, generate_choices_from_context, generate_fill_in_the_blank, generate_question, semantic_compare


quiz_blueprint = Blueprint('quiz', __name__)

@quiz_blueprint.route('/quiz')
def quiz():
    return render_template('quiz.html')

