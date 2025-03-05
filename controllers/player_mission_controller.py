from flask import Blueprint, request, jsonify
from services.player_mission_service import PlayerMissionService

player_mission_controller = Blueprint('player_mission', __name__, url_prefix='/player_missions')

@player_mission_controller.route('/<int:player_id>', methods=['GET'])
def get_missions_for_player(player_id):
    """
    Récupère toutes les missions d'un joueur avec leur statut.
    """
    missions = PlayerMissionService.get_missions_for_player(player_id)
    if missions:
        return jsonify(missions), 200
    return jsonify({"error": "Aucune mission trouvée pour ce joueur"}), 404


@player_mission_controller.route('/<int:player_id>/first_unlocked', methods=['GET'])
def get_first_unlocked_mission(player_id):
    """
    Récupère la première mission déverrouillée d'un joueur.
    """
    mission_id = PlayerMissionService.get_first_unlocked_mission(player_id)
    if mission_id:
        return jsonify({"first_unlocked_mission": mission_id}), 200
    return jsonify({"error": "Aucune mission déverrouillée trouvée"}), 404


@player_mission_controller.route('/<int:player_id>/start', methods=['POST'])
def start_mission(player_id):
    """
    Démarre une mission pour le joueur.
    """
    data = request.json
    mission_id = data.get('mission_id')

    if not mission_id:
        return jsonify({"error": "L'ID de la mission est requis"}), 400

    success = PlayerMissionService.start_mission(player_id, mission_id)
    if success:
        return jsonify({"message": "Mission démarrée avec succès"}), 200
    return jsonify({"error": "Impossible de démarrer la mission"}), 400

@player_mission_controller.route('/<int:player_id>/newly_unlocked', methods=['GET'])
def check_newly_unlocked_mission(player_id):
    """
    Vérifie si une nouvelle mission a été débloquée pour un joueur.
    """
    mission_status = PlayerMissionService.check_newly_unlocked_mission(player_id)
    if mission_status is not None:
        return jsonify(mission_status), 200
    return jsonify({"error": "Impossible de vérifier les nouvelles missions"}), 500



@player_mission_controller.route('/<int:player_id>/increment', methods=['PATCH'])
def increment_clicks(player_id):
    """
    Incrémente les clics d'une mission en cours et vérifie la complétion.
    """
    data = request.json
    mission_id = data.get('mission_id')

    if not mission_id:
        return jsonify({"error": "L'ID de la mission est requis"}), 400

    success = PlayerMissionService.increment_clicks(player_id, mission_id)
    if success:
        return jsonify({"message": "Clic enregistré avec succès"}), 200
    return jsonify({"error": "Impossible d'incrémenter les clics"}), 400


