import os

from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "reads file content line by line in a specified file relative to the working directory and returns it",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file to read path, relative to the working directory",
                },
            },
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        target_dir = os.path.normpath(
            os.path.join(os.path.abspath(working_directory), file_path)
        )

        valid_target_dir = os.path.commonpath(
            [os.path.abspath(working_directory), target_dir]
        ) == os.path.abspath(working_directory)
        if not valid_target_dir:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" is not a file'
        # else:
        #     return f'Success: "{directory}" is within the working directory'

        contents = ""
        with open(target_dir) as f:
            contents = f.read(MAX_CHARS)
            if f.read(1):
                contents += (
                    f'[...File "{target_dir}" truncated at {MAX_CHARS} characters]'
                )
        print(f"Results for: {target_dir}")
        return contents
    except RuntimeError as e:
        return f"Error: {e}"
