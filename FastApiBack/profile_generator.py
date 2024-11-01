# profile_generator.py

import json
import re
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from openai import OpenAI
from config import settings
import logging

client = OpenAI(
    api_key = settings.OPENAI_KEY
)


def _convert_js_to_json(data_string):
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
    
class Student:
    def __init__(self, platzi_profile_url, github_profile_url):
        self.platzi_profile_url = platzi_profile_url
        self.github_profile_url = github_profile_url
        self.platzi_username = None
        self.platzi_profile_str = None

    async def _fetch_platzi_profile_info(self, text):
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(text, "html.parser")

        # Locate the script tag containing 'window.data' directly
        script = soup.find("script", string=re.compile(r"window\.data\s*="))
        if not script or not script.string:
            raise Exception("User data not found on the page.")

        # Extract the data block from JavaScript
        data_match = re.search(r"window\.data\s*=\s*({.*?});", script.string, re.DOTALL)
        if not data_match:
            raise Exception("Unable to parse user data.")

        # Convert the data to a Python dictionary format
        python_data_str = data_match.group(1)

        # Convert the string
        json_string = _convert_js_to_json(python_data_str)

        return json_string

    async def profiles_exist(self):
        async with aiohttp.ClientSession() as session:
            tasks = [
                self._check_url(session, self.platzi_profile_url),
                self._check_url(session, self.github_profile_url),
            ]
            platzi_response, github_response = await asyncio.gather(*tasks)

        if platzi_response and github_response:
            # Extract the username from the URL
            self.platzi_username = self.platzi_profile_url.rstrip("/").split("/")[-1]
            self.platzi_profile_str = await self._fetch_platzi_profile_info(platzi_response)
            return True
        else:
            return False

    async def _check_url(self, session, url):
        async with session.get(url) as response:
            if response.status != 200:
                print(
                    f"Failed to retrieve the profile for {url}. Status code: {response.status}"
                )
                return None
            return await response.text()
