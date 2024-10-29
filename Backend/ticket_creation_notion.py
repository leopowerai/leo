from notion_client import Client
import datetime
# Initialize the Notion client
notion = Client(auth="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")

# Replace with your database ID (you can get this from the Notion board URL)
database_id = "12e3386028bd817abbb5d696d604fa17"


# Define the properties for the new item
task_data = {
    "task": {  # This is the title of the task; make sure it matches the actual title property name in your database
        "title": [
            {
                "text": {
                    "content": "Implementar endpoint para listar tareas de usuario"
                }
            }
        ]
    },
    "technologies": {
        "multi_select": [
            { "name": "Python" },
            { "name": "FastAPI" },
            { "name": "SQLite" }
        ]
    },
    "description": {
        "rich_text": [
            {
                "text": {
                    "content": "Esta tarea implica crear un endpoint para listar todas las tareas de un usuario específico."
                }
            }
        ]
    },
    "initial_date": {
        "date": {
            "start": "2023-10-08"
        }
    },
    "final_date": {
        "date": {
            "start": "2023-10-09"
        }
    },
    "story_points": {
        "number": 3
    },
    "feedback": {
        "rich_text": [
            {
                "text": {
                    "content": ""
                }
            }
        ]
    },
    "id": {
        "number": 7
    },
    "id_initial_tasks": {  # Example of initial task IDs as a multi-select list
        "multi_select": [
            { "name": "6" },
            { "name": "7" },
            { "name": "8" }
        ]
    },
    "category": {
        "select": {
            "name": "backend"
        }
    }
}


# Create a new item in the database
try:
    response = notion.pages.create(
        parent={"database_id": database_id},
        properties=task_data
    )
    print("Item added successfully:", response)
except Exception as e:
    print("Failed to add item:", e)
