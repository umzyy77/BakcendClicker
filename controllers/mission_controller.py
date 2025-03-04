from flask import Blueprint, request, jsonify
from services.mission_service import MissionService

mission_controller = Blueprint('mission', __name__, url_prefix='/missions')

# 🔹 1️⃣ Récupérer une mission par ID (GET /missions/{mission_id})
@mission_controller.route('/<int:mission_id>', methods=['GET'])
def get_mission(mission_id: int):
    """
    Retourne les informations d'une mission par son ID, avec sa difficulté associée.
    """
    try:
        mission = MissionService.get_mission(mission_id)
        if mission:
            return jsonify({"status": "success", "data": mission}), 200
        return jsonify({"status": "error", "message": "Mission not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred while retrieving the mission: {str(e)}"}), 500


# 🔹 2️⃣ Récupérer toutes les missions (GET /missions/)
@mission_controller.route('/', methods=['GET'])
def get_all_missions():
    """
    Retourne la liste de toutes les missions disponibles, avec leur difficulté.
    """
    try:
        missions = MissionService.get_all_missions()
        return jsonify({"status": "success", "data": missions}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred while retrieving missions: {str(e)}"}), 500


# 🔹 3️⃣ Démarrer une mission pour un joueur (POST /missions/start)
@mission_controller.route('/start', methods=['POST'])
def start_mission():
    """
    Démarre une mission pour un joueur.
    """
    data = request.get_json()
    if not data or "player_id" not in data or "mission_id" not in data:
        return jsonify({"status": "error", "message": "Missing player_id or mission_id"}), 400

    try:
        result = MissionService.start_mission(data["player_id"], data["mission_id"])
        if result:
            return jsonify({"status": "success", "message": "Mission started"}), 200
        return jsonify({"status": "error", "message": "Failed to start mission"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred while starting the mission: {str(e)}"}), 500


# 🔹 4️⃣ Récupérer les missions d'un joueur (GET /missions/player/{player_id})
@mission_controller.route('/player/<int:player_id>', methods=['GET'])
def get_player_missions(player_id: int):
    """
    Retourne les missions d'un joueur.
    """
    try:
        missions = MissionService.get_player_missions(player_id)
        return jsonify({"status": "success", "data": missions}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred while retrieving player missions: {str(e)}"}), 500


# 🔹 5️⃣ Marquer une mission comme complétée (POST /missions/complete)
@mission_controller.route('/complete', methods=['POST'])
def complete_mission():
    """
    Marque une mission comme complétée pour un joueur.
    """
    data = request.get_json()
    if not data or "player_id" not in data or "mission_id" not in data:
        return jsonify({"status": "error", "message": "Missing player_id or mission_id"}), 400

    try:
        success = MissionService.complete_mission(data["player_id"], data["mission_id"])
        if success:
            return jsonify({"status": "success", "message": "Mission completed successfully"}), 200
        return jsonify({"status": "error", "message": "Mission completion failed"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred while completing the mission: {str(e)}"}), 500


# 🔹 6️⃣ Récupérer les missions en cours d'un joueur (GET /missions/player/{player_id}/in_progress)
@mission_controller.route('/player/<int:player_id>/in_progress', methods=['GET'])
def get_player_in_progress_missions(player_id: int):
    """
    Retourne les missions actuellement en cours pour un joueur.
    """
    try:
        missions = MissionService.get_player_in_progress_missions(player_id)
        return jsonify({"status": "success", "data": missions}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred while retrieving in-progress missions: {str(e)}"}), 500
