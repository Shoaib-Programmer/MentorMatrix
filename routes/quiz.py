from flask import Blueprint, render_template, request, redirect, url_for, flash

quiz_blueprint = Blueprint('quiz', __name__)

@quiz_blueprint.route('/quiz')
def quiz():
    return render_template('quiz.html')