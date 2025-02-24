from flask import blueprint, render_template  # type: ignore

auth_blueprint = blueprint('auth', __name__, url_prefix='/auth')

@auth_blueprint.route('/login')
def login():
    return render_template('login.html')

@auth_blueprint.route('/register')
def register():
    return render_template('register.html')
