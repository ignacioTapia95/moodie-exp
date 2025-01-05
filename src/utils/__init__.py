import os


def list_files(path, extensions, recursive=False):
    """
    List all files in a directory that have an extension in the list of extensions.

    Args:
        path (str): The path to the directory.
        extensions (List[str]): A list of extensions to filter the files.
        recursive (bool): Whether to list files recursively.

    Returns:
        List[str]: A list with the paths of the files that have an extension in the list of extensions.

    Examples:
        >>> list_files(path='./data/raw', extensions=['mov', 'mp4'], recursive=True)
        ['./data/raw/video1.mov', './data/raw/video2.mp4', ...]
    """
    files = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.split('.')[-1] in extensions:
                files.append(os.path.join(root, filename))
        if not recursive:
            break
    return files
