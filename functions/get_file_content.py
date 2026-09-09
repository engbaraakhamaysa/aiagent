import os

# Safely read the contents of a file within the permitted working directory.
def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        # Convert the working directory to an absolute path.
        working_dir_abs = os.path.abspath(working_directory)

        # Build and normalize the target file path.
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        # Make sure the target file stays inside the allowed working directory.
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file])
            == working_dir_abs
        )

        if not valid_target_file:
            return (
                f'Error: Cannot read "{file_path}" '
                "as it is outside the permitted working directory"
            )

        # Make sure the target exists and is a regular file.
        if not os.path.isfile(target_file):
            return (
                f'Error: File not found or is not a regular file: '
                f'"{file_path}"'
            )

        MAX_CHARS = 10000

        # Read at most MAX_CHARS to avoid loading very large files.
        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)

            # Check whether there is more content after the limit.
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at '
                    f'{MAX_CHARS} characters]'
                )

        return content

    except Exception as e:
        return f"Error: {e}"