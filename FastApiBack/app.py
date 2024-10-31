# app.py
import logging
import os

# from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from notion_connector.notion_handler import NotionHandler
from notion_connector.update_pbi import update_notion_pbi
from workflows import assign_workflow
from pydantic_settings import BaseSettings, SettingsConfigDict

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:8080",
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
async def submit(request: Request):
    logging.info("Received request on /submit")
    data = await request.json()
    platzi_url = data.get("username")
    github_url = data.get("githubUrl")

    try:
        response_dict, response_code = await assign_workflow(platzi_url, github_url)
        return JSONResponse(content=response_dict, status_code=response_code)

    except Exception as e:
        logging.error(f"Error processing submit request: {e}")
        raise HTTPException(
            status_code=500, detail="Error procesando la solicitud /submit"
        )


@app.post("/unassign")
async def unassign(request: Request):
    logging.info("Received request on /unassign")
    data = await request.json()
    student_username = data.get("username")
    pbi_id = data.get("pbiId")

    if not student_username or not pbi_id:
        response_dict = {"error": "El campo 'username' y 'pbiId' son requeridos"}
        return JSONResponse(content=response_dict, status_code=400)

    try:
        notion_handler = NotionHandler()

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
        is_assigned = await notion_handler.is_student_assigned_to_open_pbi(
            student_username
        )
        await notion_handler.close()

        response_dict = {"isAssigned": is_assigned}
        return JSONResponse(content=response_dict, status_code=200)
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
    url_pr = data.get("urlPR") or None

    try:
        # Call the function to update the PBI in Notion
        notion_handler = NotionHandler()
        success, result = await notion_handler.update_pbi(
            pbi_id, status=pbi_status, url_pr=url_pr
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
