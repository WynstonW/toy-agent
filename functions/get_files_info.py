import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:

        abspath = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abspath, directory))
        # Will be True or False
        valid_target_dir = os.path.commonpath([abspath, target_dir]) == abspath

        file_info = f"Result for '{directory}' directory:"

        if valid_target_dir == False:
            return file_info + f'\n    Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return file_info + f'\n    Error: "{directory}" is not a directory'

        file_list = os.listdir(target_dir)

        for file in file_list:
            file_bytes = os.path.getsize(target_dir + "/" + file)
            is_dir = os.path.isdir(target_dir + "/" + file)
            file_str = f"\n  - {file}: file_size={file_bytes}, is_dir={is_dir}"
            file_info += file_str
    

        return file_info


    except Exception as e:
        return f"Error: something is amiss! {e}"

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