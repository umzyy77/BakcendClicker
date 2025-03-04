from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

# Import des controllers
from controllers.mission_controller import mission_controller
from controllers.upgrade_controller import upgrade_controller
from controllers.player_controller import player_controller
from utils.logger import log_error

app = Flask(__name__)
CORS(app)  # Active CORS

# Enregistrement des blueprints
app.register_blueprint(mission_controller)
app.register_blueprint(upgrade_controller)
app.register_blueprint(player_controller)

# Middleware Global pour gérer les erreurs
@app.errorhandler(Exception)
def handle_exception(e):
    """
    Capture toutes les erreurs non gérées et retourne un JSON propre.
    """
    if isinstance(e, HTTPException):
        return jsonify({"error": e.description}), e.code
    log_error(f"❌ Erreur non gérée : {e}")
    return jsonify({"error": "Internal Server Error"}), 500

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    print("✅ Serveur en cours d'exécution sur http://127.0.0.1:5000/")
    app.run(debug=True)