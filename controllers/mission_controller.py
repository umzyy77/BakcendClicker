from flask import Blueprint, request, jsonify
from services.mission_service import MissionService

mission_controller = Blueprint('mission', __name__, url_prefix='/missions')



@mission_controller.route('/<int:mission_id>', methods=['GET'])
def get_mission(mission_id):
    """
    Récupère une mission spécifique par son ID.
    """
    mission = MissionService.get_mission(mission_id)
    if mission:
        return jsonify(mission), 200
    return jsonify({"error": "Mission non trouvée"}), 404

@mission_controller.route('/difficulties', methods=['GET'])
def get_all_difficulties():
    """
    Récupère toutes les difficultés de missions.
    """
    difficulties = MissionService.get_all_difficulties()
    return jsonify(difficulties), 200


@mission_controller.route('', methods=['GET'])
def get_all_missions():
    """
    Récupère toutes les missions disponibles.
    """
    missions = MissionService.get_all_missions()
    return jsonify(missions), 200


@mission_controller.route('/<int:mission_id>/objective', methods=['GET'])
def get_mission_objective(mission_id):
    """
    Récupère l'objectif d'une mission spécifique (nombre de clics requis).
    """
    objective = MissionService.get_mission_objective(mission_id)
    if objective is not None:
        return jsonify({"clicks_required": objective}), 200
    return jsonify({"error": "Objectif non trouvé"}), 404
