import os
import textwrap
import requests

from llama_index.tools import FunctionTool


def download_image(url: str):
    file_name = url.split("/")[-1]

    response = requests.get(
        url,
        headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
        },
    )
    response.raise_for_status()

    file_path = os.path.join("data", file_name)
    with open(file_path, "wb") as file:
        file.write(response.content)

    return file_path


def save_note_to_file(note: str):
    note_file_path = os.path.join("data", "notes.txt")
    if not os.path.isfile(note_file_path):
        with open(note_file_path, "w"):
            pass
    with open(note_file_path, "a") as file:
        wrapped_note = textwrap.wrap(note, width=80)
        file.write("\n".join(wrapped_note) + "\n")
    return note


downlod_engine = FunctionTool.from_defaults(
    fn=download_image,
    name="download_image",
    description="This tool allows the user to download images at a specified url",
)

note_engine = FunctionTool.from_defaults(
    fn=save_note_to_file,
    name="make_note",
    description="This tool allows the user to save a text note to a file.",
)
