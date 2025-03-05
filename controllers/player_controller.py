from flask import Blueprint, request, jsonify

from services.player_service import PlayerService

player_controller = Blueprint('player', __name__, url_prefix='/players')

@player_controller.route('/<int:player_id>', methods=['GET'])
def get_player(player_id):
    """Récupère les informations d'un joueur."""
    player = PlayerService.get_player(player_id)
    return jsonify({"status": "success", "data": player}) if player else jsonify({"status": "error", "message": "Player not found"}), 404

@player_controller.route('/', methods=['POST'])
def create_player():
    """Crée un nouveau joueur."""
    data = request.get_json()
    if not data or "username" not in data:
        return jsonify({"status": "error", "message": "Missing username"}), 400
    player = PlayerService.create_player(data["username"])
    return jsonify({"status": "success", "data": player}), 201 if player else jsonify({"status": "error", "message": "Failed to create player"}), 500

@player_controller.route('/<int:player_id>/click', methods=['POST'])
def increment_hacking_power(player_id):
    """Augmente la puissance de hacking d'un joueur."""
    updated_player = PlayerService.increment_hacking_power(player_id)
    return jsonify({"status": "success", "data": updated_player}) if updated_player else jsonify({"status": "error", "message": "Player not found"}), 404

@player_controller.route('/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    """Supprime un joueur."""
    return jsonify({"status": "success", "message": "Player deleted"}) if PlayerService.delete_player(player_id) else jsonify({"status": "error", "message": "Player not found"}), 404

@player_controller.route('/<int:player_id>/stats', methods=['GET'])
def get_player_stats(player_id):
    """Récupère les statistiques du joueur."""
    stats = PlayerService.get_player_stats(player_id)
    return jsonify({"status": "success", "data": stats}) if stats else jsonify({"status": "error", "message": "Stats not found"}), 404