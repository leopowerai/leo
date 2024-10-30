from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from profile_generator import Student
from project_assigner import Project, ProjectAssigner

app = Flask(__name__)
CORS(app)

# TODO: Endpoint para desasignar un PBI
# TODO: Actualizar el estado de la PBI a completado
# TODO: Actualizar el estado de la PBI a en progreso
# TODO: Retornar un bool si un PBI está asignado a un usuario y debe estar en progreso

# Configure logging
logging.basicConfig(level=logging.INFO)


def get_projects():
    """Retrieve the list of projects."""
    # Placeholder for actual project retrieval logic
    project1 = Project(
        name="Test Project 1",
        stack=["Python", "Django", "JavaScript", "React"]
    )
    return [project1]


# TODO: EL endpoint de submit debe retornar la url del iframe
@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    platzi_url = data.get("username")
    github_url = data.get("githubUrl")

    if not platzi_url or not github_url:
        return jsonify({"error": "Ambos campos son requeridos"}), 400

    try:
        # Retrieve projects
        projects = get_projects()

        # Create a Student instance
        student = Student(platzi_url, github_url)

        if not student.profiles_exist():
            no_profile_text = "No se encontraron los perfiles de Platzi o GitHub"
            logging.info(no_profile_text)
            return jsonify({"message": no_profile_text}), 404

        # Assign a project to the student
        project_assigner = ProjectAssigner(student, projects)
        project_match = project_assigner.find_project_for_student()

        if project_match:
            project, matched_tech = project_match
            match_text = (
                f"Match de proyecto {project.name} con {matched_tech} tech, "
                f"para el estudiante {student.platzi_username}"
            )
            logging.info(match_text)
            return jsonify({"message": match_text}), 200
        else:
            not_match_text = "No hubo match de proyecto"
            logging.info(not_match_text)
            return jsonify({"message": not_match_text}), 200

    except Exception as e:
        logging.error(f"Error processing submit request: {e}")
        return jsonify({"message": "Error procesando la solicitud"}), 500


@app.route("/unassign", methods=["POST"])
def unassign():
    data = request.get_json()
    student_username = data.get("username")

    if not student_username:
        return jsonify({"error": "El campo 'username' es requerido"}), 400

    # Check from the database if the student has an assignment
    if True:#db.assignment_exists(student_username):
        # Remove the assignment from the database
        #db.delete_assignment(student_username)
        logging.info(f"Student {student_username} has been unassigned from their project")
        return jsonify({"message": f"El estudiante {student_username} ha sido desasignado del proyecto"}), 200
    else:
        logging.info(f"Student {student_username} has no assigned project to unassign")
        return jsonify({"error": f"El estudiante {student_username} no tiene un proyecto asignado"}), 400


@app.route("/update_status", methods=["POST"])
def update_status():
    data = request.get_json()
    student_username = data.get("username")
    new_status = data.get("status")

    if not student_username or not new_status:
        return jsonify({"error": "Los campos 'username' y 'status' son requeridos"}), 400

    # Retrieve from the database the assignment
    #assignment = db.get_assignment(student_username)
    if True:
        # Set new status
        #assignment.pbi.status = new_status
        logging.info(f"Student {student_username} assignment status updated to {new_status}")
        return jsonify({
            "message": f"El estado del proyecto asignado al estudiante {student_username} ha sido actualizado a {new_status}"
        }), 200
    else:
        logging.info(f"Student {student_username} has no assigned project to update")
        return jsonify({"error": f"El estudiante {student_username} no tiene un proyecto asignado"}), 400


@app.route("/has_in_progress/<username>", methods=["GET"])
def has_in_progress(username):
    # Retrieve from the database the assignment
    #assignment = db.get_assignment(username)
    if True:
        if True: #assignment.pbi.status == "In Progress":
            return jsonify({"has_in_progress": True}), 200
        else:
            return jsonify({"has_in_progress": False}), 200
    else:
        return jsonify({"error": f"El estudiante {username} no tiene un proyecto asignado"}), 400



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
