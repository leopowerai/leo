# profile_generator.py

import json
import os
import re
import asyncio
from typing import List, Optional, Tuple
import aiohttp
from bs4 import BeautifulSoup
from profile_generation.profile_utils import convert_js_to_json, get_titles_from_courses
# from config import settings

# TODO: Student could be a dataclass and there may be a ProfileFetcher class
# that handles the fetching of the profiles and the parsing of the data

class Student:
    def __init__(self, platzi_profile_url, github_profile_url):
        self.platzi_profile_url = platzi_profile_url
        self.github_profile_url = github_profile_url
        self.platzi_username = platzi_profile_url.rstrip("/").split("/")[-1]
        self.platzi_profile_str = None
        self.courses = []
        self.cache_file = "student_cache.json"

        # Load cache if available
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as file:
                self.cache = json.load(file)
        else:
            self.cache = {}

    async def profile_exists(self):
        # Check cache first
        if self.platzi_username in self.cache:
            cached_data = self.cache[self.platzi_username]
            self.platzi_profile_str = cached_data.get("profile_str")
            self.courses = cached_data.get("courses", [])
            return True

        async with aiohttp.ClientSession() as session:
            tasks = [
                self._check_url(session, self.platzi_profile_url),
                self._check_url(session, self.github_profile_url),
            ]
            platzi_response, github_response = await asyncio.gather(*tasks)

        if platzi_response and github_response:
            self.platzi_profile_str = await self._fetch_platzi_profile_info(platzi_response)
            self._update_cache()  # Save the fetched profile to cache
            return True
        else:
            return False

    async def _fetch_platzi_profile_info(self, text):
        soup = BeautifulSoup(text, "html.parser")
        script = soup.find("script", string=re.compile(r"window\.data\s*="))
        if not script or not script.string:
            raise Exception("User data not found on the page.")
        data_match = re.search(r"window\.data\s*=\s*({.*?});", script.string, re.DOTALL)
        if not data_match:
            raise Exception("Unable to parse user data.")
        python_data_str = data_match.group(1)
        json_string = convert_js_to_json(python_data_str)
        return json_string

    async def fetch_student_courses(self) -> Tuple[Optional[List[str]], Optional[str]]:
        if self.courses:
            return self.courses, None  # Return cached courses if available

        course_titles, error = get_titles_from_courses(self.platzi_profile_str["courses"])
        if error:
            return False, f"Error fetching courses: {error}"

        self.courses = course_titles
        self._update_cache()  # Cache courses after fetching
        return True, None

    def _update_cache(self):
        # Update cache with current profile and courses
        self.cache[self.platzi_username] = {
            "profile_str": self.platzi_profile_str,
            "courses": self.courses
        }
        with open(self.cache_file, "w") as file:
            json.dump(self.cache, file)

    async def _check_url(self, session, url):
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Failed to retrieve the profile for {url}. Status code: {response.status}")
                return None
            return await response.text()


# # Tests
# platzi_profile_url = "https://platzi.com/p/LuisManuel/"  # Replace with a valid Platzi profile
# github_profile_url = "https://github.com/LuisMa9L/"         # Replace with a valid GitHub profile

# student = Student(platzi_profile_url, github_profile_url)

# async def test_profile():
#     profiles_exist = await student.profiles_exist()
#     if profiles_exist:
#         print("Profile data fetched successfully!")
#         print("Platzi Username:", student.platzi_username)
#         print("Platzi Profile JSON Data:", student.platzi_profile_str)
#     else:
#         print("One or both profiles do not exist.")

# asyncio.run(test_profile())
