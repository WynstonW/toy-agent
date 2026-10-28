import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try: 
        abspath = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abspath, file_path))
        # print(target_dir)
        # Will be True or False
        valid_target_dir = os.path.commonpath([abspath, target_dir]) == abspath

        if valid_target_dir == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(target_dir):
            return f'Error: "{file_path}" does not exist'

        if file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]

        if args:
            command.extend(args)

        result = subprocess.run(command, timeout=30, text=True, capture_output=True , cwd=abspath)

        output: list[str] = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        return "\n".join(output)


    except Exception as e:
        return f"Error: something is amiss! {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a python file, with or without arguments, the python file is ran directly from the provided name, as it is relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to run file from, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "array with items of type string OR none",
                    "description": "Optional arguments for executing the python script."
                }
            },
        },
    },
}