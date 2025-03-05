from flask import Blueprint, request, jsonify

from services.player_mission_service import PlayerMissionService

# -----------------------------
# 🔹 Player Mission Controller
# -----------------------------
player_mission_controller = Blueprint('player_mission', __name__, url_prefix='/player_missions')

@player_mission_controller.route('/<int:player_id>/start', methods=['POST'])
def start_mission(player_id):
    """Assigne une mission à un joueur."""
    data = request.get_json()
    if "mission_id" not in data:
        return jsonify({"status": "error", "message": "Missing mission_id"}), 400
    return jsonify(PlayerMissionService.start_mission(player_id, data["mission_id"]))

@player_mission_controller.route('/<int:player_id>/complete', methods=['POST'])
def complete_mission(player_id):
    """Marque une mission comme complétée."""
    data = request.get_json()
    if "mission_id" not in data:
        return jsonify({"status": "error", "message": "Missing mission_id"}), 400
    return jsonify(PlayerMissionService.complete_mission(player_id, data["mission_id"]))

@player_mission_controller.route('/<int:player_id>/mission', methods=['GET'])
def get_player_missions(player_id):
    """Récupère les missions d'un joueur."""
    return jsonify({"status": "success", "data": PlayerMissionService.get_player_missions(player_id)})

@player_mission_controller.route('/<int:player_id>/mission/<int:mission_id>', methods=['GET'])
def get_player_mission(player_id, mission_id):
    """Récupère une mission spécifique d'un joueur."""
    mission = PlayerMissionService.get_player_mission(player_id, mission_id)
    return jsonify({"status": "success", "data": mission}) if mission else jsonify({"status": "error", "message": "Mission not found"}), 404

@player_mission_controller.route('/<int:player_id>/assign', methods=['POST'])
def assign_mission(player_id):
    """Assigne une mission spécifique à un joueur avec un statut donné."""
    data = request.get_json()
    if "mission_id" not in data or "status_id" not in data:
        return jsonify({"status": "error", "message": "Missing mission_id or status_id"}), 400
    return jsonify(PlayerMissionService.assign_mission_to_player(player_id, data["mission_id"], data["status_id"]))

@player_mission_controller.route('/<int:player_id>/in_progress', methods=['GET'])
def get_player_in_progress_missions(player_id):
    """Récupère toutes les missions en cours d'un joueur."""
    return jsonify({"status": "success", "data": PlayerMissionService.get_player_in_progress_missions(player_id)})
