from flask import Blueprint, render_template, request, redirect, url_for, flash
from notes import generate_flashcards

flashcards_blueprint = Blueprint('flashcards', __name__)

@flashcards_blueprint.route('/flashcards')
def flashcards():
    return render_template('flashcards.html')