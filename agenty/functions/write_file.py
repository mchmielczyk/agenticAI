import os
def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        target_dir=os.path.normpath(os.path.join(os.path.abspath(working_directory),file_path))
        
        valid_target_dir = os.path.commonpath([os.path.abspath(working_directory), target_dir]) == os.path.abspath(working_directory)
        if not valid_target_dir:
            return f'Error: Cannot list "{target_dir}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{target_dir}" as it is a directory'
        # else:
        #     return f'Success: "{directory}" is within the working directory'

        os.makedirs(os.path.dirname(target_dir),exist_ok=True)
        with open(target_dir,'w') as f:
            f.write(content)
        return f'Successfully wrote to "{target_dir}" ({len(content)} characters written)'
            

    except Exception as e:
        return f'Error: {e}'