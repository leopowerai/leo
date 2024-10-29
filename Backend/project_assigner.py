from typing import List, Optional


def check_profile_project_match(profile: str, tech_stack: List[str]) -> Optional[str]:
    """
    Searches for the first occurrence of any keyword in the provided text.

    Parameters:
    text (str): The text to search within.
    keywords (List[str]): A list of keywords to search for.

    Returns:
    Optional[str]: The first keyword found in the text, or None if no keywords are found.
    """
    for tech in tech_stack:
        if tech in profile:
            return tech
    return None
