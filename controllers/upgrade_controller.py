from flask import Blueprint, request, jsonify
from services.upgrade_service import UpgradeService

upgrade_controller = Blueprint('upgrade', __name__, url_prefix='/upgrades')

# 🔹 1️⃣ Récupérer une amélioration par ID (GET /upgrades/{upgrade_id})
@upgrade_controller.route('/<int:upgrade_id>', methods=['GET'])
def get_upgrade(upgrade_id: int):
    """
    Retourne les informations d'une amélioration par son ID.
    """
    try:
        upgrade = UpgradeService.get_upgrade(upgrade_id)
        if upgrade:
            return jsonify({"status": "success", "data": upgrade}), 200
        return jsonify({"status": "error", "message": "Upgrade not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred while retrieving the upgrade: {str(e)}"}), 500


# 🔹 2️⃣ Récupérer toutes les améliorations disponibles (GET /upgrades/)
@upgrade_controller.route('/', methods=['GET'])
def get_all_upgrades():
    """
    Retourne la liste de toutes les améliorations disponibles.
    """
    try:
        upgrades = UpgradeService.get_all_upgrades()
        return jsonify({"status": "success", "data": upgrades}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred while retrieving upgrades: {str(e)}"}), 500


@upgrade_controller.route('/<int:player_id>', methods=['GET'])
def get_player_upgrades(player_id):
    """Récupère les améliorations achetées par un joueur."""
    return jsonify({"status": "success", "data": UpgradeService.get_player_upgrades(player_id)})

@upgrade_controller.route('/<int:player_id>/purchase', methods=['POST'])
def purchase_upgrade(player_id):
    """Permet à un joueur d'acheter une amélioration."""
    data = request.get_json()
    if "upgrade_level_id" not in data:
        return jsonify({"status": "error", "message": "Missing upgrade_level_id"}), 400
    return jsonify(UpgradeService.purchase_upgrade(player_id, data["upgrade_level_id"]))

