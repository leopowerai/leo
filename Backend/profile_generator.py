import re

import requests
from bs4 import BeautifulSoup


# Function to convert the JS string to a valid JSON string
def _convert_js_to_json(data_string):
    """
    There is some processing in here to transform the input string into a dict
    We currently have problems to do the conversion, so for now it's just the string
    """

    return data_string


def _check_url(url):
    # Fetch the profile HTML from the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(
            f"Failed to retrieve the profile for {url}. Status code: {response.status_code}"
        )
        return None
    return response


class Student:
    def __init__(self, platzi_profile_url, github_profile_url):
        self.platzi_profile_url = platzi_profile_url
        self.github_profile_url = github_profile_url
        self.platzi_username = None
        self.platzi_profile_str = None

    def _fetch_platzi_profile_info(self, response):
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

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

    def profiles_exist(self):
        platzi_response = _check_url(self.platzi_profile_url)
        github_response = _check_url(self.github_profile_url)

        if platzi_response and github_response:
            # Extract the username from the URL
            self.platzi_username = self.platzi_profile_url.rstrip("/").split("/")[-1]
            self.platzi_profile_str = self._fetch_platzi_profile_info(platzi_response)
            return True
        else:
            return False
