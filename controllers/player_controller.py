from flask import Blueprint, request, jsonify

from services.player_service import PlayerService

player_controller = Blueprint('player', __name__, url_prefix='/players')

@player_controller.route('', methods=['POST'])
def create_player():
    """
    Crée un nouveau joueur avec un nom d'utilisateur.
    """
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({"error": "Le nom d'utilisateur est requis"}), 400

    player_id = PlayerService.create_player(username)
    if player_id:
        return jsonify({"message": "Joueur créé avec succès", "player_id": player_id}), 201
    return jsonify({"error": "Échec de la création du joueur"}), 500


@player_controller.route('/<int:player_id>', methods=['GET'])
def get_player(player_id):
    """
    Récupère les informations d'un joueur.
    """
    player = PlayerService.get_player(player_id)
    if player:
        return jsonify(player), 200
    return jsonify({"error": "Joueur non trouvé"}), 404


@player_controller.route('/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    """
    Supprime un joueur.
    """
    success = PlayerService.delete_player(player_id)
    if success:
        return jsonify({"message": "Joueur supprimé avec succès"}), 200
    return jsonify({"error": "Impossible de supprimer le joueur"}), 400


@player_controller.route('/<int:player_id>/money', methods=['PATCH'])
def update_player_money(player_id):
    """
    Met à jour l'argent du joueur.
    """
    data = request.json
    amount = data.get('amount')

    if amount is None:
        return jsonify({"error": "Montant requis"}), 400

    success = PlayerService.update_player_money(player_id, amount)
    if success:
        return jsonify({"message": "Argent mis à jour avec succès"}), 200
    return jsonify({"error": "Impossible de mettre à jour l'argent"}), 400


@player_controller.route('/<int:player_id>/hacking_power', methods=['PATCH'])
def update_hacking_power(player_id):
    """
    Met à jour la puissance de hacking du joueur.
    """
    data = request.json
    power = data.get('power')

    if power is None:
        return jsonify({"error": "Valeur de hacking power requise"}), 400

    success = PlayerService.update_hacking_power(player_id, power)
    if success:
        return jsonify({"message": "Puissance de hacking mise à jour avec succès"}), 200
    return jsonify({"error": "Impossible de mettre à jour la puissance de hacking"}), 400
