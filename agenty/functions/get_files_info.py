import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        target_dir=os.path.normpath(os.path.join(os.path.abspath(working_directory),directory))

        valid_target_dir = os.path.commonpath([os.path.abspath(working_directory), target_dir]) == os.path.abspath(working_directory)
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        # else:
        #     return f'Success: "{directory}" is within the working directory'

        contents = ""
        for file in os.listdir(target_dir):
            file_path = os.path.join(target_dir, file)
            contents+=str(f"- {file_path}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}\n")
        print(f"Results for: {target_dir}")
        return contents
    except Exception as e:
        return f'Error: {e}'