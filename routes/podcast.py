from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash # type: ignore
from notes.AI import generate_podcast, text_to_podcast
from models import db

podcast_blueprint = Blueprint('podcast', __name__)

@podcast_blueprint.route('/podcast')
def podcast():
    podcasts = ...
    return render_template("podcast.html", current_route="podcast", podcasts=podcasts) # Not implemented yet
