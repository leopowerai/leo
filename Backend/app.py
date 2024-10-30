from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from profile_generator import Student
from project_assigner import Project, ProjectAssigner

app = Flask(__name__)
CORS(app)

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
