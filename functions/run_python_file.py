import os
import subprocess


# Safely execute a Python file within the permitted working directory.
def run_python_file(
    working_directory: str,
    file_path: str,
    args: list[str] | None = None,
) -> str:
    try:
        # Convert the working directory to an absolute path.
        working_dir_abs = os.path.abspath(working_directory)

        # Build and normalize the target file path.
        absolute_file_path = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Make sure the target file stays inside the allowed working directory.
        valid_target_file = (
            os.path.commonpath([working_dir_abs, absolute_file_path])
            == working_dir_abs
        )

        if not valid_target_file:
            return (
                f'Error: Cannot execute "{file_path}" '
                "as it is outside the permitted working directory"
            )

        # Make sure the target exists and is a regular file.
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Make sure the file is a Python file.
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build the Python command.
        command = ["python", absolute_file_path]

        # Add any arguments provided by the caller.
        if args:
            command.extend(args)

        # Run the Python file with the required safety settings.
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = ""

        # Report a non-zero exit code.
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"

        # Report when the process produced no output.
        if not result.stdout and not result.stderr:
            output += "No output produced"
        else:
            if result.stdout:
                output += f"STDOUT:\n{result.stdout}"

            if result.stderr:
                output += f"STDERR:\n{result.stderr}"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"

# Define tool schemas that describe the available functions and their parameters to the LLM.
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file within the working directory, with optional arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}