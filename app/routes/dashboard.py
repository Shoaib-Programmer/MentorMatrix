from flask import Blueprint, render_template, redirect, g
import json
from app.middleware import requires_auth  # ensure this is imported

dashboard_blueprint = Blueprint("dashboard", __name__)


@dashboard_blueprint.route("/")
def index():
    return redirect("/dashboard")


@dashboard_blueprint.route("/dashboard")
@requires_auth
def dashboard():
    return render_template(
        "dashboard.html",
        current_route="dashboard",
        user=g.user,  # Pass the verified user payload here.
        pretty=json.dumps(g.user, indent=4),
    )
