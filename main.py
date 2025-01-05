from lib.preprocessing import Video
from lib.utils import list_files


if __name__ == '__main__':
    video_files = list_files(
        path='./data/raw',
        extensions=['mov', 'mp4'],
        recursive=True
    )

    for video_file in video_files:
        video = Video(path=video_file, debug=True)
        video.split_and_save_shots(
            output_path='./data/processed',
            threshold=27.0
        )
