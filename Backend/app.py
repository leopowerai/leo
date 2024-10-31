import logging

from flask import Flask, jsonify, request
from flask_cors import CORS
from workflows import assign_workflow

app = Flask(__name__)
CORS(app)

# TODO: Endpoint para desasignar un PBI
# TODO: Actualizar el estado de la PBI a completado
# TODO: Actualizar el estado de la PBI a en progreso
# TODO: Retornar un bool si un PBI está asignado a un usuario y debe estar en progreso

# Configure logging
logging.basicConfig(level=logging.INFO)


# TODO: EL endpoint de submit debe retornar la url del iframe
@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    platzi_url = data.get("username")
    github_url = data.get("githubUrl")

    try:
        # This could be improved by assigning the http code depending on the message tag
        response_dict, response_code = assign_workflow(platzi_url, github_url)
        return jsonify(response_dict), response_code

    except Exception as e:
        logging.error(f"Error processing submit request: {e}")
        return jsonify({"message": "Error procesando la solicitud"}), 500


@app.route("/unassign", methods=["POST"])
def unassign():
    data = request.get_json()
    student_username = data.get("username")
    pbi_id = data.get("pbi_id")

    if not student_username:
        return jsonify({"error": "El campo 'username' es requerido"}), 400

    # Check from the database if the student has an assignment
    if True:  # db.assignment_exists(student_username):
        # Remove the assignment from the database
        # db.delete_assignment(student_username)
        logging.info(
            f"Student {student_username} has been unassigned from their project"
        )
        return (
            jsonify(
                {
                    "message": f"El estudiante {student_username} ha sido desasignado del proyecto"
                }
            ),
            200,
        )
    else:
        logging.info(f"Student {student_username} has no assigned project to unassign")
        return (
            jsonify(
                {
                    "error": f"El estudiante {student_username} no tiene un proyecto asignado"
                }
            ),
            400,
        )


@app.route("/update_status", methods=["POST"])
def update_status():
    data = request.get_json()
    student_username = data.get("username")
    new_status = data.get("status")

    if not student_username or not new_status:
        return (
            jsonify({"error": "Los campos 'username' y 'status' son requeridos"}),
            400,
        )

    # Retrieve from the database the assignment
    # assignment = db.get_assignment(student_username)
    if True:
        # Set new status
        # assignment.pbi.status = new_status
        logging.info(
            f"Student {student_username} assignment status updated to {new_status}"
        )
        return (
            jsonify(
                {
                    "message": f"El estado del proyecto asignado al estudiante {student_username} ha sido actualizado a {new_status}"
                }
            ),
            200,
        )
    else:
        logging.info(f"Student {student_username} has no assigned project to update")
        return (
            jsonify(
                {
                    "error": f"El estudiante {student_username} no tiene un proyecto asignado"
                }
            ),
            400,
        )


@app.route("/has_in_progress/<username>", methods=["GET"])
def has_in_progress(username):
    # Retrieve from the database the assignment
    # assignment = db.get_assignment(username)
    if True:
        if True:  # assignment.pbi.status == "In Progress":
            return jsonify({"has_in_progress": True}), 200
        else:
            return jsonify({"has_in_progress": False}), 200
    else:
        return (
            jsonify(
                {"error": f"El estudiante {username} no tiene un proyecto asignado"}
            ),
            400,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
