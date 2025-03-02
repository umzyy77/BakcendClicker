from flask import Flask
from flask_cors import CORS

# Import des controllers
from controllers.enemy_controller import enemy_controller
from controllers.enhancement_controller import enhancement_controller
from controllers.player_controller import player_controller

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)  # Autorise les requêtes cross-origin (CORS)

# Enregistrement des blueprints (controllers)
app.register_blueprint(enemy_controller)
app.register_blueprint(enhancement_controller)
app.register_blueprint(player_controller)

if __name__ == '__main__':
    print("✅ Serveur en cours d'exécution sur http://127.0.0.1:5000/")
    app.run(debug=True)
