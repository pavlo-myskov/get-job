import re


def generate_filename_from_email(email: str):
    """
    Generate a filename from the user's email.
    Replace all non-alphanumeric characters to underscores.
    """
    pattern = r"[^a-zA-Z0-9]"
    return re.sub(pattern, "_", email)
