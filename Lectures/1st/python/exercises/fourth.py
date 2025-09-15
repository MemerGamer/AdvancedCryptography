from pathlib import Path


def safe_file_access(file_path: str) -> Path:
    """
    Safely access a file, ensuring it's within the /safedir directory.
    
    Args:
        file_path: The file path to access
    
    Returns:
        Path object for the file
    
    Raises:
        ValueError: If the file is outside /safedir
        FileNotFoundError: If the file doesn't exist
    
    Method: AI assistance + pathlib documentation + security best practices
    """
    # Convert to absolute path and resolve any symbolic links
    abs_path = Path(file_path).resolve()
    
    # Define the safe directory
    safe_dir = Path("/safedir").resolve()
    
    # Check if the file is within the safe directory
    try:
        abs_path.relative_to(safe_dir)
    except ValueError:
        raise ValueError(f"Access denied: File '{file_path}' is outside the safe directory '/safedir'")
    
    # Check if file exists
    if not abs_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return abs_path