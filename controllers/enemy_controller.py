from flask import Blueprint, jsonify, Response
from services.enemy_service import EnemyService

enemy_controller = Blueprint('enemy', __name__, url_prefix='/enemies')

@enemy_controller.route('/', methods=['GET'])
def get_all_enemies() -> tuple[Response, int]:
    """
    Retourne la liste de tous les ennemis.
    Exemple : GET /enemies
    """
    enemies = EnemyService.get_all_enemies()
    return jsonify(enemies), 200


@enemy_controller.route('/<int:level>', methods=['GET'])
def get_enemy(level: int) -> tuple[Response, int]:
    """
    Retourne un ennemi spécifique par son niveau.
    Exemple : GET /enemies/2
    """
    enemy = EnemyService.get_enemy(level)
    return jsonify(enemy), 200 if enemy else (jsonify({'error': 'Enemy not found'}), 404)
