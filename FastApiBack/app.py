# app.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os
from workflows import assign_workflow
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

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
    logging.info(f"Received request {os.getenv("NOTION_API_KEY")}")
    data = await request.json()
    platzi_url = data.get("username")
    github_url = data.get("githubUrl")

    try:
        response_dict, response_code = await assign_workflow(platzi_url, github_url)
        return JSONResponse(content=response_dict, status_code=response_code)

    except Exception as e:
        logging.error(f"Error processing submit request: {e}")
        raise HTTPException(status_code=500, detail="Error procesando la solicitud")
