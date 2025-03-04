from flask import Blueprint, request, jsonify, Response
from services.upgrade_service import UpgradeService

# Création du blueprint pour le contrôleur des améliorations
upgrade_controller = Blueprint('upgrade', __name__, url_prefix='/upgrades')

# 🔹 1️⃣ Récupérer une amélioration par ID (GET /upgrades/{upgrade_id})
@upgrade_controller.route('/<int:upgrade_id>', methods=['GET'])
def get_upgrade(upgrade_id: int) -> tuple[Response, int]:
    """
    Retourne les informations d'une amélioration par son ID.
    Exemple : GET /upgrades/1
    """
    upgrade = UpgradeService.get_upgrade(upgrade_id)
    if upgrade:
        return jsonify(upgrade), 200
    return jsonify({'error': 'Upgrade not found'}), 404

# 🔹 2️⃣ Récupérer toutes les améliorations (GET /upgrades/)
@upgrade_controller.route('/', methods=['GET'])
def get_all_upgrades() -> tuple[Response, int]:
    """
    Retourne la liste de toutes les améliorations disponibles.
    Exemple : GET /upgrades/
    """
    upgrades = UpgradeService.get_all_upgrades()
    return jsonify(upgrades), 200

# 🔹 3️⃣ Acheter une amélioration (POST /upgrades/purchase)
@upgrade_controller.route('/purchase', methods=['POST'])
def purchase_upgrade() -> tuple[Response, int]:
    """
    Permet à un joueur d'acheter une amélioration.
    Exemple : POST /upgrades/purchase
    Body JSON attendu : { "player_id": 1, "upgrade_id": 2 }
    """
    data = request.get_json()
    if not data or "player_id" not in data or "upgrade_id" not in data:
        return jsonify({"error": "Missing player_id or upgrade_id"}), 400

    result = UpgradeService.purchase_upgrade(data["player_id"], data["upgrade_id"])
    if result is None:
        return jsonify({'error': 'Player or upgrade not found'}), 404
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result), 200