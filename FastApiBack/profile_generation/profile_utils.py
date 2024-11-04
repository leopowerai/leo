import json
from typing import Tuple, Optional, List, Dict, Any
import re
from openai import OpenAI
from config import settings
import logging


import re
from typing import Tuple, Optional

client = OpenAI(
    api_key = settings.OPENAI_KEY
)

def convert_js_to_json(data_string):
    """
    There is some processing in here to transform the input string into a dict
    We currently have problems to do the conversion, so for now it's just the string
    """
    
    prompt = f"""
    Given the following JSON object:

    {data_string}

    Extract a new JSON object with only the "username" and a list of course titles. The format should be:

    {{
    "username": "the username here",
    "courses": [
        {{ "title": "course title here" }},
        {{ "title": "next course title here" }},
        ...
    ]
    }}
    """
    
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that can process and extract data from Javascript objects."},
        {"role": "user", "content": prompt}
    ],
    temperature=0
    )
    
    gpt_result = response.choices[0].message.content
    json_result = extract_json(gpt_result)
    
    logging.info(f"Scrapped data: {json_result}")
    return json_result

# Function to extract JSON from response text
def extract_json(response_text):
    # Regular expression to find JSON-like structure in the text
    json_match = re.search(r'({[\s\S]*})', response_text)
    if json_match:
        json_data = json_match.group(0)
        try:
            # Parse JSON data
            parsed_data = json.loads(json_data)
            return parsed_data
        except json.JSONDecodeError:
            print("Error decoding JSON")
            return None
    else:
        print("No JSON found in the response text")
        return None

def fix_inner_quotes(json_string: str) -> Tuple[str, Optional[str]]:
    """
    Fixes inner double quotes in text values within a JSON-like string.

    Args:
        json_string (str): JSON-like string containing user data.

    Returns:
        Tuple[str, Optional[str]]: A tuple with the corrected JSON string and an error message, if any.
    """

    # Regular expression pattern to find key-value pairs where values contain unescaped inner double quotes
    pattern = r'(".*?"):\s"(.*?)(?<!\\)"(,|\s*\})'

    def replace_inner_quotes(match):
        key = match.group(1)
        # Escape only inner double quotes in the value, ignoring already escaped quotes
        value = match.group(2).replace('"', '\\"')
        end = match.group(3)
        return f'{key}: "{value}"{end}'

    try:
        # Apply the function to replace inner quotes only in text values
        corrected_json = re.sub(pattern, replace_inner_quotes, json_string)
        return corrected_json, None

    except re.error as e:
        # Capture regex errors if they occur
        return json_string, f"Regex error: {str(e)}"


def get_courses_from_dict(data: Dict[str, Any]) -> Tuple[Optional[List[str]], Optional[str]]:
    """
    Extracts course titles from a dictionary and returns a list of titles or an error message.

    Args:
        data (Dict[str, Any]): Dictionary containing user data with courses.

    Returns:
        Tuple[Optional[List[str]], Optional[str]]: A tuple with a list of course titles if available,
                                                   or an error message if courses are not found.
    """
    try:
        # Attempt to get the list of courses from the dictionary
        courses = data.get('courses')

        # Check if 'courses' exists and is a list
        if not isinstance(courses, list):
            return None, "'courses' key is missing or is not a list."

        # Extract course titles
        course_titles = [course['title']
                         for course in courses if 'title' in course]

        return course_titles, None

    except Exception as e:
        # Handle any unexpected error
        return None, f"An unexpected error occurred: {str(e)}"


def get_courses(json_string: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    """
    Extracts courses from a JSON string and returns a list of courses or an error message.

    Args:
        json_string (str): JSON string containing user data.

    Returns:
        Tuple[Optional[List[Dict[str, Any]]], Optional[str]]: A tuple with either a list of course dictionaries or an error message.
    """
    # try:
    # Preprocess the JSON-like string to make it valid JSON
    # Replace single quotes with double quotes for keys and values
    # Add double quotes around keys
    json_string = re.sub(r'(\w+):', r'"\1":', json_string)
    json_string = json_string.replace("True", "true").replace(
        "False", "false").replace("None", "null").replace("'", '"')
    json_string = re.sub(r'""https"://', r'"https://', json_string)
    json_string = re.sub(r'\bTrue\b', 'true', json_string)
    json_string = re.sub(r'\bFalse\b', 'false', json_string)
    json_string = re.sub(r'\bNone\b', 'null', json_string)
    json_string, err = fix_inner_quotes(json_string)
    if err is not None:
        return None, err
    print(json_string)
    # Parse the JSON string to a dictionary
    data = json.loads(json_string)

    # Extract courses
    courses = data.get("courses")

    if not isinstance(courses, list):
        return None, "'courses' key is missing or is not a list."

    return courses, None

    # except json.JSONDecodeError as e:
    #    return None, f"Invalid JSON format: {e.msg}"

    # except Exception as e:
    #    return None, f"An unexpected error occurred: {str(e)}"


def get_titles_from_courses(courses_list: List[Dict[str, Any]]) -> Tuple[Optional[List[str]], Optional[str]]:
    """
    Extracts the titles from a list of course dictionaries.

    Args:
        courses_list (List[Dict[str, Any]]): A list of dictionaries, where each dictionary represents a course 
                                             and contains a 'title' key.

    Returns:
        Tuple[Optional[List[str]], Optional[str]]: A tuple with either a list of course titles or an error message.
    """
    try:
        # Initialize a list to store course titles
        courses_titles = []

        # Extract the title from each course and add it to the list
        for course in courses_list:
            if 'title' in course:

                courses_titles.append(course['title'])

            else:
                return None, f"Missing 'title' key in course {course} dictionary."

        return courses_titles, None

    except Exception as e:
        # Catch any unexpected error and return an error message
        return None, f"An unexpected error occurred: {str(e)}"


def find_project_by_name(projects, name):
    """
    Search for a project by name in a list of projects.

    Args:
        projects (list): List of projects.
        name (str): The name of the project to search for.

    Returns:
        dict or None: The project with the specified name, or None if not found.
    """
    for project in projects:
        if project["nombre"] == name:
            return project
    return None  # Return None if no project with the given name is found


# async def fetch_student_courses(student: Student) -> Tuple[Optional[List[str]], Optional[str]]:
#     """
#     Fetches the Platzi courses data for a given student if both profiles exist.

#     Args:
#         student (Student): The student object containing Platzi and GitHub profile URLs.

#     Returns:
#         Tuple[Optional[List[str]], Optional[str]]: A tuple containing a list of course titles if available, or an error message.
#     """

#     # Check if both profiles exist
#     if not await student.valid_profile():
#         return None, "One or both profiles do not exist or could not be retrieved."

#     # Fetch and parse courses data
#     course_titles, error = get_titles_from_courses(
#         student.platzi_profile_str["courses"])
#     if error:
#         return None, f"Error fetching courses: {error}"

#     return course_titles, None