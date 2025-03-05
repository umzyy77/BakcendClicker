from flask import Blueprint, request, jsonify
from services.mission_service import MissionService

mission_controller = Blueprint('mission', __name__, url_prefix='/missions')



@mission_controller.route('/', methods=['GET'])
def get_all_missions():
    """Récupère toutes les missions."""
    return jsonify({"status": "success", "data": MissionService.get_all_missions()})

@mission_controller.route('/<int:mission_id>', methods=['GET'])
def get_mission(mission_id):
    """Récupère une mission par ID."""
    mission = MissionService.get_mission(mission_id)
    return jsonify({"status": "success", "data": mission}) if mission else jsonify({"status": "error", "message": "Mission not found"}), 404