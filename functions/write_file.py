import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abspath = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abspath, file_path))
        # print(target_dir)
        # Will be True or False
        valid_target_dir = os.path.commonpath([abspath, target_dir]) == abspath

        if valid_target_dir == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(working_directory, exist_ok=True)

        with open(target_dir, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return "Error: something is amiss!"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes a file or overwrites file contents to a specified file path",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to write file from, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "Contents to be written to file"
                }
            },
        },
    },
}