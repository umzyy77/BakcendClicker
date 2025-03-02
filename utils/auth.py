from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import jsonify

def generate_token(user_id):
    """
    Génère un token JWT pour un utilisateur.
    """
    return create_access_token(identity=user_id)

def protected_route():
    """
    Exemple de route protégée nécessitant un token.
    """
    @jwt_required()
    def secured():
        current_user = get_jwt_identity()
        return jsonify(message=f"Bienvenue, utilisateur {current_user}"), 200
    return secured
