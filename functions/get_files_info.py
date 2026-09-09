import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        # Convert the working directory to an absolute path.
        working_dir_abs = os.path.abspath(working_directory)

        # Build and normalize the target directory path.
        target_dir = os.path.normpath(
            os.path.join(working_dir_abs, directory)
        )

        # Make sure the target stays inside the allowed working directory.
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir])
            == working_dir_abs
        )

        if not valid_target_dir:
            return (
                f'Error: Cannot list "{directory}" '
                "as it is outside the permitted working directory"
            )

        # The target must be an existing directory, not a file.
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # List the directory contents and collect each item's name, size, and type.
        items = os.listdir(target_dir)

        result = []

        # Collect information about each item in the directory.
        for item in items:
            full_path = os.path.join(target_dir, item)
            file_size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)

            result.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(result)
    

    except Exception as e:
        return f"Error: {e}"