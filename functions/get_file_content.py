import os

def get_file_content(working_directory: str, file_path: str) -> str:
    try:

        abspath = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abspath, file_path))
        print(target_dir)
        # Will be True or False
        valid_target_dir = os.path.commonpath([abspath, target_dir]) == abspath

        if valid_target_dir == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        MAX_CHARS = 10_000
        
        with open(target_dir, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string


    except Exception as e:
        return "Error: something is amiss! {e}"


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the content of a file. Capped to 10000 bytes.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to read file from or name of the file relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}