from flask import Blueprint, request, jsonify
from services.upgrade_service import UpgradeService

upgrade_controller = Blueprint('upgrade', __name__, url_prefix='/upgrades')


@upgrade_controller.route('/<int:player_id>/total_click_bonus', methods=['GET'])
def get_total_click_bonus(player_id):
    """
    Récupère le bonus total de clics d'un joueur en fonction de ses améliorations.
    Utilisé dans la gameloop du player_mission_service.py.
    """
    total_bonus = UpgradeService.get_total_click_bonus(player_id)
    return jsonify({"total_click_bonus": total_bonus}), 200


@upgrade_controller.route('/<int:player_id>', methods=['GET'])
def get_all_upgrades(player_id):
    """
    Récupère toutes les améliorations disponibles et le niveau actuel du joueur.
    Permet au frontend d'afficher les upgrades achetables ou déjà possédées.
    """
    upgrades = UpgradeService.get_all_upgrades(player_id)
    if upgrades:
        return jsonify(upgrades), 200
    return jsonify({"error": "Aucune amélioration trouvée"}), 404


@upgrade_controller.route('/<int:player_id>/buy', methods=['POST'])
def buy_upgrade(player_id):
    """
    Permet d'acheter une amélioration pour le joueur.
    Vérifie que le joueur a assez d'argent et que l'amélioration peut être achetée.
    """
    data = request.json
    upgrade_id = data.get('upgrade_id')

    if not upgrade_id:
        return jsonify({"error": "L'ID de l'amélioration est requis"}), 400

    success = UpgradeService.buy_upgrade(player_id, upgrade_id)
    if success:
        return jsonify({"message": "Amélioration achetée avec succès"}), 200
    return jsonify({"error": "Impossible d'acheter cette amélioration"}), 400
