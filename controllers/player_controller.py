from flask import Blueprint, jsonify, request, Response
from services.player_service import PlayerService

player_controller = Blueprint('player', __name__, url_prefix='/players')

@player_controller.route('/', methods=['POST'])
def create_player() -> tuple[Response, int]:
    """
    Ajoute un nouveau joueur.
    Exemple : POST /players/
    Body JSON attendu : { "pseudo": "NomDuJoueur", "id_enemy": 1 }
    """
    data = request.get_json()
    if not data or "pseudo" not in data or "id_enemy" not in data:
        return jsonify({"error": "Missing pseudo or id_enemy"}), 400

    new_player = PlayerService.create_player(data["pseudo"], data["id_enemy"])
    return jsonify(new_player), 201


@player_controller.route('/<int:player_id>', methods=['GET'])
def get_player(player_id: int) -> tuple[Response, int]:
    """
    Retourne les informations d'un joueur.
    Exemple : GET /players/1
    """
    player = PlayerService.get_player(player_id)

    if player:
        return jsonify(player), 200
    else:
        return jsonify({'error': 'Player not found'}), 404  # ✅ Gère proprement les joueurs inexistants


@player_controller.route('/<int:player_id>/click', methods=['POST'])
def click(player_id: int) -> tuple[Response, int]:
    """
    Incrémente l'expérience du joueur en simulant un clic.
    Exemple : POST /players/1/click
    """
    new_data = PlayerService.increment_clicks(player_id)

    if new_data:  # ✅ Vérifie si l'XP a été mis à jour correctement
        return jsonify(new_data), 200
    else:
        return jsonify({'error': 'Player not found'}), 404  # ✅ Gère proprement les joueurs inexistants


@player_controller.route('/<int:player_id>/buy', methods=['POST'])
def buy_enhancement(player_id: int) -> tuple[Response, int]:
    """
    Permet à un joueur d'acheter une amélioration.
    Exemple : POST /players/1/buy
    Body JSON attendu : { "enhancement_id": 2 }
    """
    data = request.get_json()
    enhancement_id = data.get('enhancement_id')

    if enhancement_id is None:
        return jsonify({'error': 'Missing enhancement_id'}), 400  # ✅ Mauvaise requête

    result = PlayerService.buy_enhancement(player_id, enhancement_id)

    if result is None:  # ✅ Vérifie si le joueur ou l'amélioration n'existe pas
        return jsonify({'error': 'Player or enhancement not found'}), 404  # ✅ Retourne 404 Not Found

    if "error" in result:
        status_code = 400 if result["error"] == "Not enough experience to buy this enhancement" else 404
        return jsonify(result), status_code  # ✅ Retourne le bon code HTTP (400 ou 404)

    return jsonify(result), 200  # ✅ Si tout est bon, retour en 200

@player_controller.route('/<int:player_id>', methods=['DELETE'])
def delete_player(player_id: int) -> tuple[Response, int]:
    """
    Supprime un joueur par son ID.
    Exemple : DELETE /players/1
    """
    success = PlayerService.delete_player(player_id)

    if success:
        return jsonify({"message": "Player deleted"}), 200
    else:
        return jsonify({"error": "Player not found"}), 404  # ✅ Retourne 404 si le joueur n'existe pas




