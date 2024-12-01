from flask import Flask, render_template
from config import Config, DevelopmentConfig  # Import the config dictionary
from routes import dashboard_blueprint, notes_blueprint, transcribe_blueprint, chatbot_blueprint, quiz_blueprint, flashcards_blueprint
from models import init_db

# Initialize the Flask app
app = Flask(__name__)

# Load the appropriate configuration based on the environment
app.config.from_object(DevelopmentConfig)

# Initialize the app's folders (i.e., create the directories if they don't exist)
Config.init_app(app)


# Initialize SQLite database (this will create the tables)
init_db()  # Pass the app instance to initialize db

# Register blueprints for different routes
app.register_blueprint(dashboard_blueprint)
app.register_blueprint(notes_blueprint)
app.register_blueprint(transcribe_blueprint)
app.register_blueprint(chatbot_blueprint)
app.register_blueprint(quiz_blueprint)
app.register_blueprint(flashcards_blueprint)

# Miscellaneous routes for now

@app.route('/settings')
def settings():
    return render_template('settings.html', current_route='settings')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

if __name__ == '__main__':
    app.run(debug=True)
