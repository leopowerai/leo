import ast
import json
import re
from typing import List

import requests
from bs4 import BeautifulSoup


# Function to convert the JS string to a valid JSON string
def convert_js_to_json(data_string):
    """
    There is some processing in here to transform the input string into a dict
    We currently have problems to do the conversion, so for now it's just the string
    """

    return data_string


def fetch_profile_info(url):
    # Extract the username from the URL
    username = url.rstrip("/").split("/")[-1]

    # Fetch the profile HTML from the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the profile. Status code: {response.status_code}")
        return

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Locate the script tag containing 'window.data' directly
    script = soup.find("script", string=re.compile(r"window\.data\s*="))
    if not script or not script.string:
        print("User data not found on the page.")
        return

    # Extract the data block from JavaScript
    data_match = re.search(r"window\.data\s*=\s*({.*?});", script.string, re.DOTALL)
    if not data_match:
        print("Unable to parse user data.")
        return

    # Convert the data to a Python dictionary format
    python_data_str = data_match.group(1)

    # Convert the string
    json_string = convert_js_to_json(python_data_str)
    return json_string

    # Print the JSON string for debugging
    # print("Converted JSON string:")
    # print(json_string)

    # # Load the string into a Python dictionary
    # try:
    #     python_dict = json.loads(json_string)
    #     print("Resulting Python dictionary:")
    #     print(python_dict)
    # except json.JSONDecodeError as e:
    #     print("JSON decoding error:", e)

    # # Extract the relevant fields
    # country_code = (
    #     data.get("flag", "").split("/")[-1].split(".")[0].upper()
    #     if data.get("flag")
    #     else "Unknown"
    # )
    # courses = [
    #     {"title": course["title"], "completion": course["completed"]}
    #     for course in data.get("courses", [])
    # ]

    # # Display information
    # print(f"Username: {username}")
    # print(f"Country: {country_code}")
    # print("Courses:")
    # for course in courses:
    #     print(f" - {course['title']}: {course['completion']}% completed")
