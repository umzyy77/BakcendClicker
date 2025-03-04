from flask import Blueprint, request, jsonify
from services.mission_task_service import MissionTaskService

mission_task_controller = Blueprint('mission_task', __name__, url_prefix='/mission_tasks')

# 🔹 1️⃣ Récupérer toutes les tâches associées à une mission (GET /mission_tasks/{mission_id})
@mission_task_controller.route('/<int:mission_id>', methods=['GET'])
def get_mission_tasks(mission_id: int):
    """
    Récupère toutes les tâches associées à une mission.
    """
    try:
        tasks = MissionTaskService.get_tasks_by_mission(mission_id)
        if not tasks:
            return jsonify({"status": "error", "message": "No tasks found for this mission"}), 404
        return jsonify({"status": "success", "data": tasks}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred while retrieving tasks: {str(e)}"}), 500


# 🔹 2️⃣ Vérifier si une tâche est complétée (POST /mission_tasks/validate)
@mission_task_controller.route('/validate', methods=['POST'])
def validate_mission_task():
    """
    Vérifie si un joueur a complété une tâche.
    """
    data = request.get_json()
    if not data or "player_id" not in data or "mission_id" not in data or "task_type" not in data or "progress" not in data:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    try:
        is_completed = MissionTaskService.check_task_completion(data["player_id"], data["mission_id"], data["task_type"], data["progress"])
        if is_completed:
            return jsonify({"status": "success", "message": "Task completed successfully"}), 200
        return jsonify({"status": "error", "message": "Task not yet completed"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"An error occurred while validating the task: {str(e)}"}), 500
