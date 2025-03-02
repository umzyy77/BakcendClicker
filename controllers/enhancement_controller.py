from flask import Blueprint, jsonify, Response
from services.enhancement_service import EnhancementService

enhancement_controller = Blueprint('enhancement', __name__, url_prefix='/enhancements')


@enhancement_controller.route('/', methods=['GET'])
def get_all_enhancements() -> tuple[Response, int]:
    """
    Retourne toutes les améliorations disponibles.
    Exemple : GET /enhancements
    """
    enhancements = EnhancementService.get_all_enhancements()
    return jsonify(enhancements), 200


@enhancement_controller.route('/<int:enhancement_id>', methods=['GET'])
def get_enhancement(enhancement_id: int) -> tuple[Response, int]:
    """
    Retourne une amélioration spécifique par son ID.
    Exemple : GET /enhancements/1
    """
    enhancement = EnhancementService.get_enhancement(enhancement_id)
    return jsonify(enhancement), 200 if enhancement else (jsonify({'error': 'Enhancement not found'}), 404)
