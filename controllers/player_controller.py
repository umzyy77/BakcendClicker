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
    return jsonify(player), 200 if player else (jsonify({'error': 'Player not found'}), 404)

@player_controller.route('/<int:player_id>/click', methods=['POST'])
def click(player_id: int) -> tuple[Response, int]:
    """
    Incrémente l'expérience du joueur en simulant un clic.
    Exemple : POST /players/1/click
    """
    new_data = PlayerService.increment_clicks(player_id)
    return jsonify(new_data), 200 if new_data else (jsonify({'error': 'Player not found'}), 404)

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
        return jsonify({'error': 'Missing enhancement_id'}), 400

    result = PlayerService.buy_enhancement(player_id, enhancement_id)
    return jsonify(result), 200 if result else (jsonify({'error': 'Player not found or not enough experience'}), 400)
