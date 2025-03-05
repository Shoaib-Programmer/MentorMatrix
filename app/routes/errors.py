from flask import Blueprint, render_template  # type: ignore

error_blueprint = Blueprint("errors", __name__)


@error_blueprint.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@error_blueprint.app_errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

@error_blueprint.app_errorhandler(401)
def unauthorized(e):
    return render_template("401.html"), 401
