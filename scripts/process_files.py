import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
from src.data.processing import Video
from src.utils import list_files

def parse_args():
    """
    Parse the command-line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.

    Examples:
        >>> parse_args()
        Namespace(debug=False, extensions=['mov', 'mp4', 'avi', 'mkv'], input=None, output='./data/processed', recursive=False, threshold=27.0)
    """
    parser = argparse.ArgumentParser(description="Process video files.")
    parser.add_argument(
        "--input",
        help="Folder containing unprocessed videos."
    )
    parser.add_argument(
        "--output",
        default="./data/processed",
        help="Folder to store processed videos (default: ./data/processed)."
    )
    parser.add_argument(
        "--extensions",
        nargs="+",
        default=["mov", "mp4", "avi", "mkv"],
        help="Video file extensions to look for (default: mov mp4 avi mkv)."
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=27.0,
        help="Threshold used by the split function (default: 27.0)."
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="If set, it will search subdirectories recursively."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enables debug mode to print additional information."
    )
    return parser.parse_args()

def process_files(input_path, output_path, extensions, threshold, recursive, debug):
    """
    Process video files in a directory.

    Args:
        input_path (str): The path to the directory containing the video files.
        output_path (str): The path to the directory to store the processed videos.
        extensions (List[str]): A list of extensions to filter the video files.
        threshold (float): The threshold used by the split function.
        recursive (bool): Whether to search subdirectories recursively.
        debug (bool): Whether to enable debug mode.

    Returns:
        None

    Examples:
        >>> process_files(
        ...     input_path="./data/raw",
        ...     output_path="./data/processed",
        ...     extensions=["mov", "mp4"],
        ...     threshold=27.0,
        ...     recursive=True,
        ...     debug=True
        ... )
    """
    video_files = list_files(
        path=input_path,
        extensions=extensions,
        recursive=recursive
    )

    for video_file in video_files:
        video = Video(path=video_file, debug=debug)
        video.split_and_save_shots(
            output_path=output_path,
            threshold=threshold
        )

def main():
    """
    Main function to process video files based on the command-line arguments.
    
    Returns:
        None

    Examples:
        >>> main()
    """
    args = parse_args()

    process_files(
        input_path=args.input,
        output_path=args.output,
        extensions=args.extensions,
        threshold=args.threshold,
        recursive=args.recursive,
        debug=args.debug
    )

if __name__ == "__main__":
    main()