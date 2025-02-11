from flask import Blueprint, render_template, redirect # type: ignore

dashboard_blueprint = Blueprint('dashboard', __name__)

@dashboard_blueprint.route("/")
def index():
    return redirect("/dashboard")

@dashboard_blueprint.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', current_route='dashboard')
