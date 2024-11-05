# app.py
import logging
from contextlib import asynccontextmanager

from config import settings  # Load env vars
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from notion_connector.notion_handler import NotionHandler
from notion_connector.update_pbi import update_notion_pbi
from utils import remove_char
from workflows.assign import assign_project_and_pbi
from workflows.startup import preload_projects


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    print("Running startup task...")
    app.notion_handler = NotionHandler()  # This works in spite of MyPy error
    app.project_assigner = await preload_projects(
        app.notion_handler
    )  # This works in spite of MyPy error
    await app.notion_handler.close()

    yield
    # Shutdown code
    print("Running shutdown task...")


app = FastAPI(lifespan=lifespan)


# Dependency to access notion_handler and project_assigner in endpoints
def get_notion_handler(request: Request):
    return request.app.notion_handler


def get_project_assigner(request: Request):
    return request.app.project_assigner


origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:8080",
    "44.226.145.213",
    "54.187.200.255",
    "34.213.214.55",
    "35.164.95.156",
    "44.230.95.183",
    "44.229.200.200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)


@app.post("/submit")
async def submit(
    request: Request,
    project_assigner=Depends(get_project_assigner),
):
    logging.info("Received request on /submit")
    data = await request.json()
    platzi_url = data.get("username")
    github_url = "https://github.com/someprofile"  # Placeholder for GitHub URL

    try:
        notion_handler = NotionHandler()
        # This can be more efficient, we need to evaluate this flow for checking if the student is already assigned to a PBI
        student_username = platzi_url.rstrip("/").split("/")[-1]
        # Check if the student is already assigned to a PBI
        assigned_project_id, assigned_pbi_id = (
            await notion_handler.is_student_assigned_to_open_pbi(student_username)
        )
        if assigned_project_id and assigned_pbi_id:
            f_proj_id = remove_char(assigned_project_id, "-")
            f_pbi_id = remove_char(assigned_pbi_id, "-")
            response_dict = {
                "isAssigned": "true",
                "pbiId": assigned_pbi_id,
                "iframeUrl": f"https://v2-embednotion.com/theffs/{f_proj_id}?p={f_pbi_id}&pm=s",
            }

            await notion_handler.close()
            return JSONResponse(content=response_dict, status_code=200)

        response_dict, response_code = await assign_project_and_pbi(
            notion_handler,
            project_assigner,
            platzi_url,
            github_url,
            recommended_pbis_count=3,
        )

        return JSONResponse(content=response_dict, status_code=response_code)

    except Exception as e:
        logging.error(f"Error processing submit request: {e}")
        raise HTTPException(
            status_code=500, detail="Error processing the /submit request"
        )


@app.post("/unassign")
async def unassign(request: Request):
    logging.info("Received request on /unassign")
    data = await request.json()
    platzi_url = data.get("username")
    pbi_id = data.get("pbiId")

    if not platzi_url or not pbi_id:
        response_dict = {"error": "El campo 'username' y 'pbiId' son requeridos"}
        return JSONResponse(content=response_dict, status_code=400)

    try:
        notion_handler = NotionHandler()
        student_username = platzi_url.rstrip("/").split("/")[-1]

        # Set owners to an empty list to unassign the student
        success, result = await notion_handler.update_pbi(
            pbi_id, owners=[], status="open"
        )

        await notion_handler.close()

        if success:
            response_dict = {
                "message": f"Estudiante {student_username} desasignado exitosamente"
            }
            return JSONResponse(content=response_dict, status_code=200)
        else:
            response_dict = {
                "error": f"Error desasignando estudiante {student_username}"
            }
            return JSONResponse(content=response_dict, status_code=400)

    except Exception as e:
        logging.error(f"Error processing unassign request: {e}")
        raise HTTPException(
            status_code=500, detail="Error procesando la solicitud /unassign"
        )


@app.post("/assign")
async def assign(request: Request):
    logging.info("Received request on /assign")
    data = await request.json()
    platzi_url = data.get("username")
    pbi_id = data.get("pbiId")

    if not platzi_url or not pbi_id:
        response_dict = {"error": "El campo 'username' y 'pbiId' son requeridos"}
        return JSONResponse(content=response_dict, status_code=400)

    try:
        notion_handler = NotionHandler()
        student_username = platzi_url.rstrip("/").split("/")[-1]

        # Assign the student to the PBI
        success, result = await notion_handler.update_pbi(
            pbi_id,
            owners=[student_username],
            status="in progress",
            update_due_date=True
        )

        await notion_handler.close()

        f_pbi_id = remove_char(pbi_id, "-")

        project_id = result['properties']['projects_test']['relation'][0]['id']
        f_proj_id = remove_char(project_id, "-")

        if success:
            response_dict = {
                "message": f"Estudiante {student_username} asignado exitosamente",
                "iframeUrl": f"https://v2-embednotion.com/theffs/{f_proj_id}?p={f_pbi_id}&pm=s"
            }
            return JSONResponse(content=response_dict, status_code=200)
        else:
            response_dict = {"error": f"Error asignando estudiante {student_username}"}
            return JSONResponse(content=response_dict, status_code=400)

    except Exception as e:
        logging.error(f"Error processing assign request: {e}")
        raise HTTPException(
            status_code=500, detail="Error procesando la solicitud /assign"
        )


@app.post("/is_assigned")
async def is_assigned_to_open_pbi(request: Request):
    logging.info("Received request on /is_assigned")
    data = await request.json()
    student_username = data.get("username")

    if not student_username:
        response_dict = {"error": "El campo 'username' es requerido"}
        return JSONResponse(content=response_dict, status_code=400)

    try:
        notion_handler = NotionHandler()
        assigned_project_id, assigned_pbi_id = (
            await notion_handler.is_student_assigned_to_open_pbi(student_username)
        )
        await notion_handler.close()

        # logging.info(f"Assigned project ID: {assigned_project_id}")
        # logging.info(f"Assigned PBI ID: {assigned_pbi_id}")
        # Retornar el iframe para renderizar de una la tarea en curso
        if assigned_project_id and assigned_pbi_id:
            f_proj_id = remove_char(assigned_project_id, "-")
            f_pbi_id = remove_char(assigned_pbi_id, "-")
            response_dict = {
                "isAssigned": "true",
                "iframeUrl": f"https://v2-embednotion.com/theffs/{f_proj_id}?p={f_pbi_id}&pm=s",
            }

            return JSONResponse(content=response_dict, status_code=200)
        else:
            response_dict = {"isAssigned": "false"}
            return JSONResponse(content=response_dict, status_code=400)

    except Exception as e:
        logging.error(f"Error processing isAssigned request: {e}")
        raise HTTPException(
            status_code=500, detail="Error procesando la solicitud /is_assigned"
        )


@app.post("/update_pbi_status")
async def update_pbi_status(request: Request):
    logging.info("Received request on /update_pbi_status")
    data = await request.json()
    pbi_id = data.get("pbiId")
    pbi_status = data.get(
        "status"
    )  # Status can be "open", "in progress", "in review", or "done"
    results_url = data.get("resultsURL") or None

    try:
        # Call the function to update the PBI in Notion
        notion_handler = NotionHandler()
        success, result = await notion_handler.update_pbi(
            pbi_id, status=pbi_status, results_url=results_url
        )
        await notion_handler.close()

        if success:
            response_dict = {"message": "PBI updated successfully"}
            return JSONResponse(content=response_dict, status_code=200)
        else:
            response_dict = {"error": "Error updating PBI"}
            return JSONResponse(content=response_dict, status_code=400)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
