from flask import Flask, jsonify, request
from flask_cors import CORS
from profile_generator import Student
from project_assigner import Project, ProjectAssigner

app = Flask(__name__)
CORS(app)


@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    platzi_url = data.get("username")
    github_url = data.get("githubUrl")

    if not platzi_url or not github_url:
        return jsonify({"error": "Ambos campos son requeridos"}), 400

    try:
        # Get the projects
        project1 = Project(
            name="Test Project 1", stack=["Python", "Django", "JavaScript", "React"]
        )
        projects = [project1]

        # Get the student
        student = Student(platzi_url, github_url)

        if not student.profiles_exist():
            no_profile_text = "No se encontraron los perfiles de Platzi o GitHub"
            print(no_profile_text)
            return jsonify({"message": no_profile_text}), 404
        else:
            project_assigner = ProjectAssigner(student, projects)
            project_match = project_assigner.find_project_for_student()

            if project_match:
                match_text = f"Match de proyecto {project_match[0].name} con {project_match[1]} tech, para el estudiante {student.platzi_username}"
                print(match_text)
                return jsonify({"message": match_text}), 200
            else:
                not_match_text = "No hubo match de proyecto"
                print(not_match_text)
                return jsonify({"message": not_match_text}), 200

    except Exception as e:
        print(f"Error: {e}")
        # Process the data (e.g., save to database, etc.)
        return jsonify({"message": e}), 500


if __name__ == "__main__":
    app.run(debug=True)
