import os
import subprocess
def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        target_dir=os.path.normpath(os.path.join(os.path.abspath(working_directory),file_path))
        
        valid_target_dir = os.path.commonpath([os.path.abspath(working_directory), target_dir]) == os.path.abspath(working_directory)
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]
        if(args!=None):
            command.extend(args)

        completed = subprocess.run(command,text = True, timeout=30, capture_output=True)

        ret_value =""
        if completed.returncode !=0:
            ret_value+= f"Process exited with code {completed.returncode} "
        if len(completed.stderr)==0 and len(completed.stdout)==0:
            ret_value+= "No output produced "
        elif len(completed.stderr)==0:
            ret_value+=f"STDOUT: {completed.stdout}"
        elif len(completed.stdout)==0:
            ret_value+=f"STDERR: {completed.stderr}"
        else:
            ret_value+=f"STDOUT: {completed.stdout}"
            ret_value+=f"STDERR: {completed.stderr}"
        return ret_value
    except Exception as e:
        return f"Error: executing Python file: {e}"