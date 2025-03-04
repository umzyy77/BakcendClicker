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


# 🔹 3️⃣ Acheter une amélioration (POST /players/{player_id}/upgrades/purchase)
@upgrade_controller.route('/purchase', methods=['POST'])
def purchase_upgrade():
    """
    Permet à un joueur d'acheter une amélioration.
    """
    data = request.get_json()

    if not data or "player_id" not in data or "upgrade_id" not in data:
        return jsonify({"status": "error", "message": "Missing player_id or upgrade_id"}), 400  # Bad request si données manquantes

    try:
        result = UpgradeService.purchase_upgrade(data["player_id"], data["upgrade_id"])
        if result:
            return jsonify({"status": "success", "data": result}), 200
        return jsonify({"status": "error", "message": "Purchase failed"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred while purchasing the upgrade: {str(e)}"}), 500


# 🔹 4️⃣ Récupérer les améliorations achetées par un joueur (GET /players/{player_id}/upgrades)
@upgrade_controller.route('/<int:player_id>/upgrades', methods=['GET'])
def get_player_upgrades(player_id: int):
    """
    Récupère toutes les améliorations achetées par un joueur.
    """
    try:
        upgrades = UpgradeService.get_player_upgrades(player_id)
        if not upgrades:
            return jsonify({"status": "error", "message": "No upgrades found for this player"}), 404
        return jsonify({"status": "success", "data": upgrades}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred while retrieving player upgrades: {str(e)}"}), 500
