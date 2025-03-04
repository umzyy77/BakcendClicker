from flask import Blueprint, request, jsonify, Response
from services.mission_service import MissionService

# Création du blueprint pour le contrôleur des missions
mission_controller = Blueprint('mission', __name__, url_prefix='/missions')

# 🔹 1️⃣ Récupérer une mission par ID (GET /missions/{mission_id})
@mission_controller.route('/<int:mission_id>', methods=['GET'])
def get_mission(mission_id: int) -> tuple[Response, int]:
    """
    Retourne les informations d'une mission par son ID.
    Exemple : GET /missions/1
    """
    mission = MissionService.get_mission(mission_id)
    if mission:
        return jsonify(mission), 200
    return jsonify({'error': 'Mission not found'}), 404

# 🔹 2️⃣ Récupérer toutes les missions (GET /missions/)
@mission_controller.route('/', methods=['GET'])
def get_all_missions() -> tuple[Response, int]:
    """
    Retourne la liste de toutes les missions disponibles.
    Exemple : GET /missions/
    """
    missions = MissionService.get_all_missions()
    return jsonify(missions), 200

# 🔹 3️⃣ Démarrer une mission pour un joueur (POST /missions/start)
@mission_controller.route('/start', methods=['POST'])
def start_mission() -> tuple[Response, int]:
    """
    Démarre une mission pour un joueur.
    Exemple : POST /missions/start
    Body JSON attendu : { "player_id": 1, "mission_id": 2 }
    """
    data = request.get_json()
    if not data or "player_id" not in data or "mission_id" not in data:
        return jsonify({"error": "Missing player_id or mission_id"}), 400

    result = MissionService.start_mission(data["player_id"], data["mission_id"])
    if result:
        return jsonify(result), 200
    return jsonify({'error': 'Failed to start mission'}), 500

# 🔹 4️⃣ Récupérer les missions d'un joueur (GET /missions/player/{player_id})
@mission_controller.route('/player/<int:player_id>', methods=['GET'])
def get_player_missions(player_id: int) -> tuple[Response, int]:
    """
    Retourne la liste des missions d'un joueur.
    Exemple : GET /missions/player/1
    """
    missions = MissionService.get_player_missions(player_id)
    return jsonify(missions), 200

# 🔹 5️⃣ Marquer une mission comme complétée (POST /missions/complete)
@mission_controller.route('/complete', methods=['POST'])
def complete_mission() -> tuple[Response, int]:
    """
    Marque une mission comme complétée pour un joueur.
    Exemple : POST /missions/complete
    Body JSON attendu : { "player_id": 1, "mission_id": 2 }
    """
    data = request.get_json()
    if not data or "player_id" not in data or "mission_id" not in data:
        return jsonify({"error": "Missing player_id or mission_id"}), 400

    success = MissionService.complete_mission(data["player_id"], data["mission_id"])
    if success:
        return jsonify({"message": "Mission completed successfully"}), 200
    return jsonify({'error': 'Mission completion failed'}), 400