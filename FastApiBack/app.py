# app.py
import logging
import os

# from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from notion_connector.update_pbi import update_notion_pbi
from workflows import assign_workflow

app = FastAPI()

# load_dotenv()

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
    logging.info("Received request")
    data = await request.json()
    platzi_url = data.get("username")
    github_url = data.get("githubUrl")

    try:
        response_dict, response_code = await assign_workflow(platzi_url, github_url)
        return JSONResponse(content=response_dict, status_code=response_code)

    except Exception as e:
        logging.error(f"Error processing submit request: {e}")
        raise HTTPException(status_code=500, detail="Error procesando la solicitud")


@app.post("/unassign")
async def unassign(request: Request):
    data = await request.json()
    student_username = data.get("username")
    pbi_id = data.get("pbi_id")

    if not student_username or pbi_id:
        response_dict = {"error": "El campo 'username' y 'pbi_id' son requeridos"}
        return JSONResponse(content=response_dict, status_code=400)

    update_notion_pbi(pbi_id=pbi_id)
