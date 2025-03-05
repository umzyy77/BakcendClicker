from flask import Flask
from flask_cors import CORS


# Import des controllers
from controllers.mission_controller import mission_controller
from controllers.upgrade_controller import upgrade_controller
from controllers.player_controller import player_controller
from controllers.player_mission_controller import player_mission_controller
from utils.logger import log_error

app = Flask(__name__)
CORS(app)  # Active CORS

# Enregistrement des blueprints
app.register_blueprint(player_controller)
app.register_blueprint(mission_controller)
app.register_blueprint(player_mission_controller)
app.register_blueprint(upgrade_controller)

@app.route('/', methods=['GET'])
def health_check():
    """
    Vérifie que l'API est en ligne.
    """
    return {"message": "API Hacking Clicker en ligne"}, 200


if __name__ == '__main__':
    print("✅ Serveur en cours d'exécution sur http://127.0.0.1:5000/")
    app.run(debug=True)