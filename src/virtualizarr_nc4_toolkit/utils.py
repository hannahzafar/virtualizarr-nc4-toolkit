""" """

from pathlib import Path


# Query a list of paths to be virtualized from a directory
def find_directory_files(path):
    """
    Validate that a path exists and is a directory.

    Args:
        path: string path to validate

    Returns:
        list: List of .nc4 file paths if valid directory with multiple files,
                None if invalid or insufficient files
    """
    # Convert to Path object if it's a string
    path = Path(path) if not isinstance(path, Path) else path

    if not path.exists():
        print(f"Error: '{path}' does not exist.")
        return None

    if not path.is_dir():
        print(f"Error: '{path}' is not a directory.")
        return None

    # Search directory for .nc4 files
    nc4_files = list(path.glob("*.nc4"))

    if len(nc4_files) < 2:
        print(
            f"Error: Found {len(nc4_files)} .nc4 files found in '{path}'. Multiple files required."
        )
        return None

    print(f"Found {len(nc4_files)} .nc4 files in '{path}'.")
    return nc4_files
