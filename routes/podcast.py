from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash

podcast_blueprint = Blueprint('podcast', __name__)

@podcast_blueprint.route('/podcast')
def podcast():
    return render_template("podcast.html", current_route="podcast")
