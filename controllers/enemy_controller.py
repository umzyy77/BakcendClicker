from flask import Blueprint, jsonify, Response
from services.enemy_service import EnemyService
from utils.logger import log_info, log_error

enemy_controller = Blueprint('enemy', __name__, url_prefix='/enemies')

@enemy_controller.route('/', methods=['GET'])
def get_all_enemies() -> tuple[Response, int]:
    """
    Retourne la liste de tous les ennemis.
    Exemple : GET /enemies
    """
    enemies = EnemyService.get_all_enemies()
    if not enemies:  # ✅ Vérifie si la liste est vide
        return jsonify({"error": "Aucun ennemi trouvé"}), 404

    return jsonify(enemies), 200


@enemy_controller.route('/<int:level>', methods=['GET'])
def get_enemy(level: int) -> tuple[Response, int]:
    """
    Retourne un ennemi spécifique par son niveau.
    Exemple : GET /enemies/2
    """
    enemy = EnemyService.get_enemy(level)
    if enemy:
        return jsonify(enemy), 200
    else:
        return jsonify({'error': 'Enemy not found'}), 404  # ✅ Gère proprement les ennemis inexistants



@enemy_controller.route('/<int:level>', methods=['DELETE'])
def delete_enemy(level: int) -> tuple[Response, int]:
    """
    Supprime un ennemi par son niveau.
    Exemple : DELETE /enemies/2
    """
    success = EnemyService.delete_enemy(level)
    if success:
        log_info(f"Ennemi niveau {level} supprimé avec succès.")
        return jsonify({"message": "Enemy deleted"}), 200
    else:
        log_error(f"Échec de suppression : ennemi {level} introuvable.")
        return jsonify({"error": "Enemy not found"}), 404
