from flask import Blueprint, request, jsonify, Response
from services.player_service import PlayerService
from services.player_mission_service import PlayerMissionService

# Création du blueprint pour le contrôleur des joueurs
player_controller = Blueprint('player', __name__, url_prefix='/players')

# 🔹 1️⃣ Récupérer un joueur par ID (GET /players/{player_id})
@player_controller.route('/<int:player_id>', methods=['GET'])
def get_player(player_id: int) -> tuple[Response, int]:
    """
    Retourne les informations d'un joueur par son ID.
    Exemple : GET /players/1
    """
    player = PlayerService.get_player(player_id)
    if player:
        return jsonify(player), 200
    return jsonify({'error': 'Player not found'}), 404

# 🔹 2️⃣ Créer un joueur (POST /players/)
@player_controller.route('/', methods=['POST'])
def create_player() -> tuple[Response, int]:
    """
    Crée un nouveau joueur.
    Exemple : POST /players
    Body JSON attendu : { "username": "NeoHacker" }
    """
    data = request.get_json()
    if not data or "username" not in data:
        return jsonify({"error": "Missing username"}), 400
    new_player = PlayerService.create_player(data["username"])
    return jsonify(new_player), 201

# 🔹 3️⃣ Incrémenter la puissance de hacking (Clicker) (POST /players/{player_id}/click)
@player_controller.route('/<int:player_id>/click', methods=['POST'])
def increment_hacking_power(player_id: int) -> tuple[Response, int]:
    """
    Incrémente la puissance de hacking du joueur à chaque clic.
    Exemple : POST /players/1/click
    """
    updated_player = PlayerService.increment_hacking_power(player_id)
    if updated_player:
        return jsonify(updated_player), 200
    return jsonify({'error': 'Player not found'}), 404

# 🔹 4️⃣ Supprimer un joueur (DELETE /players/{player_id})
@player_controller.route('/<int:player_id>', methods=['DELETE'])
def delete_player(player_id: int) -> tuple[Response, int]:
    """
    Supprime un joueur par son ID.
    Exemple : DELETE /players/1
    """
    success = PlayerService.delete_player(player_id)
    if success:
        return jsonify({"message": "Player deleted"}), 200
    return jsonify({'error': 'Player not found'}), 404

# 🔹 5️⃣ Vérifier et compléter une mission (POST /players/{player_id}/complete_mission)
@player_controller.route('/<int:player_id>/complete_mission', methods=['POST'])
def complete_mission(player_id: int) -> tuple[Response, int]:
    """
    Vérifie et complète une mission d'un joueur.
    Exemple : POST /players/1/complete_mission
    Body JSON attendu : { "mission_id": 2 }
    """
    data = request.get_json()
    if not data or "mission_id" not in data:
        return jsonify({"error": "Missing mission_id"}), 400

    success = PlayerMissionService.complete_mission(player_id, data["mission_id"])
    if success:
        return jsonify({"message": "Mission completed successfully"}), 200
    return jsonify({'error': 'Mission completion failed'}), 400