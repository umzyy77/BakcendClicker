from flask import Blueprint, request, jsonify

from services.player_mission_service import PlayerMissionService
from services.player_service import PlayerService

player_controller = Blueprint('player', __name__, url_prefix='/players')

# 🔹 1️⃣ Récupérer un joueur par ID (GET /players/{player_id})
@player_controller.route('/<int:player_id>', methods=['GET'])
def get_player(player_id: int):
    """
    Retourne les informations d'un joueur par son ID.
    """
    try:
        player = PlayerService.get_player(player_id)
        if player:
            return jsonify({"status": "success", "data": player}), 200
        return jsonify({"status": "error", "message": "Player not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred while retrieving the player: {str(e)}"}), 500


# 🔹 2️⃣ Créer un joueur (POST /players/)
@player_controller.route('/', methods=['POST'])
def create_player():
    """
    Crée un nouveau joueur.
    """
    data = request.get_json()
    if not data or "username" not in data:
        return jsonify({"status": "error", "message": "Missing username"}), 400

    try:
        new_player = PlayerService.create_player(data["username"])
        return jsonify({"status": "success", "data": new_player}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred while creating the player: {str(e)}"}), 500


# 🔹 3️⃣ Incrémenter la puissance de hacking (Clicker) (POST /players/{player_id}/click)
@player_controller.route('/<int:player_id>/click', methods=['POST'])
def increment_hacking_power(player_id: int):
    """
    Incrémente la puissance de hacking du joueur à chaque clic.
    """
    try:
        updated_player = PlayerService.increment_hacking_power(player_id)
        if updated_player:
            return jsonify({"status": "success", "data": updated_player}), 200
        return jsonify({"status": "error", "message": "Player not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred while incrementing hacking power: {str(e)}"}), 500


# 🔹 4️⃣ Supprimer un joueur (DELETE /players/{player_id})
@player_controller.route('/<int:player_id>', methods=['DELETE'])
def delete_player(player_id: int):
    """
    Supprime un joueur par son ID.
    """
    try:
        success = PlayerService.delete_player(player_id)
        if success:
            return jsonify({"status": "success", "message": "Player deleted"}), 200
        return jsonify({"status": "error", "message": "Player not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred while deleting the player: {str(e)}"}), 500


# 🔹 5️⃣ Vérifier et compléter une mission d'un joueur (POST /players/{player_id}/complete_mission)
@player_controller.route('/<int:player_id>/complete_mission', methods=['POST'])
def complete_mission(player_id: int):
    """
    Vérifie et complète une mission d'un joueur.
    """
    data = request.get_json()
    if not data or "mission_id" not in data:
        return jsonify({"status": "error", "message": "Missing mission_id"}), 400

    try:
        success = PlayerMissionService.complete_mission(player_id, data["mission_id"])
        if success:
            return jsonify({"status": "success", "message": "Mission completed successfully"}), 200
        return jsonify({"status": "error", "message": "Mission completion failed"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred while completing the mission: {str(e)}"}), 500


# 🔹 6️⃣ Récupérer les statistiques globales d'un joueur (GET /players/{player_id}/stats)
@player_controller.route('/<int:player_id>/stats', methods=['GET'])
def get_player_stats(player_id: int):
    """
    Récupère les statistiques globales d'un joueur :
    - Missions complétées
    - Améliorations achetées
    """
    try:
        stats = PlayerService.get_player_stats(player_id)
        if stats:
            return jsonify({"status": "success", "data": stats}), 200
        return jsonify({"status": "error", "message": "Player stats not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred while retrieving the player stats: {str(e)}"}), 500
