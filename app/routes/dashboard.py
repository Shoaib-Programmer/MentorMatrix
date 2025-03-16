from flask import Blueprint, render_template, redirect  # type: ignore
from app.middleware import requires_auth  # noqa: F401

dashboard_blueprint = Blueprint("dashboard", __name__)


@dashboard_blueprint.route("/")
def index():
    return redirect("/dashboard")


@dashboard_blueprint.route("/dashboard")
@requires_auth
def dashboard():
    return render_template("dashboard.html", current_route="dashboard")
