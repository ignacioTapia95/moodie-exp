import os
import json
from typing import Iterable, Tuple

from scenedetect import open_video, SceneManager, split_video_ffmpeg, save_images
from scenedetect.detectors import ContentDetector
from scenedetect.frame_timecode import FrameTimecode


class Video:
    """
    Represents a video that can be split into shots using the SceneDetect library,
    and provides functionality to save both the shot files and their metadata.

    This class uses content detection based on a defined threshold to identify scene
    boundaries (shots). Once detected, it can split the original video into separate
    shot files, and optionally store information about each shot in a JSON file.

    Attributes:
        path (str): The file path to the source video.
        video_name (str): The name used to identify the video. 
            If None, the name is inferred from the video's filename.
        debug (bool): Flag indicating whether to display debug information 
            during shot detection and video splitting.

    Methods:
        _get_shot_list(threshold: float = 27.0) -> Iterable[Tuple[FrameTimecode, FrameTimecode]]:
            Detects shots in the video based on a content threshold and returns 
            a list of (start_timecode, end_timecode) tuples.

        _save_video_shots(
            shot_list: Iterable[Tuple[FrameTimecode, FrameTimecode]], 
            output_path: str, 
            output_file_template: str = '$VIDEO_NAME-Shot-$SCENE_NUMBER.mp4'
        ) -> None:
            Splits the video into multiple shot files based on the provided shot list 
            and saves them to the specified output directory.

        _save_shots_info(
            shot_list: Iterable[Tuple[FrameTimecode, FrameTimecode]], 
            output_path: str
        ) -> None:
            Saves shot metadata (start/end times, shot IDs) in a JSON file located 
            in the specified output directory.

        split_and_save_shots(
            threshold: float = 27.0, 
            output_path: str = './data/processed'
        ) -> None:
            High-level method that retrieves the shot list (using _get_shot_list),
            splits the video into separate shot files (_save_video_shots),
            and saves their metadata (_save_shots_info).

    Examples:
        >>> video = Video(path='data/raw/video1.mp4', debug=True)
        >>> video.split_and_save_shots(output_path='data/processed', threshold=30.0)
    """

    def __init__(
            self,
            path: str,
            video_name: str = None,
            debug: bool = False,
    ):
        """
        Initializes the Video instance.

        Args:
            path (str): The full path to the video file.
            video_name (str, optional): The name/identifier for the video. 
                If None, it is derived from the file's base name.
                Default is None.
            debug (bool, optional): If True, debug information is displayed during 
                shot detection and video splitting. 
                Default is False.

        Returns:
            None
        """
        self.path = path
        self.debug = debug
        self.video = open_video(self.path)

        if video_name is None:
            self.video_name = path.split('/')[-1].split('.')[0]
        else:
            self.video_name = video_name

    def _get_shot_list(
            self,
            threshold: float = 27.0,
    ) -> Iterable[Tuple[FrameTimecode, FrameTimecode]]:
        """
        Detects the shots in the video based on a specified threshold.

        Args:
            threshold (float, optional): The threshold used by the content detector. 
                A higher threshold generally produces fewer, longer shots.
                Default is 27.0.

        Returns:
            Iterable[Tuple[FrameTimecode, FrameTimecode]]: An iterable of tuples 
            (start_timecode, end_timecode) for each detected shot.

        Examples:
            >>> video = Video(path='data/raw/video1.mp4', debug=True)
            >>> shot_list = video._get_shot_list(threshold=30.0)
        """
        shot_manager = SceneManager()
        shot_manager.add_detector(ContentDetector(threshold=threshold))
        shot_manager.detect_scenes(self.video, show_progress=self.debug)
        shot_list = shot_manager.get_scene_list()

        return shot_list

    def _save_video_shots(
            self,
            shot_list: Iterable[Tuple[FrameTimecode, FrameTimecode]],
            output_path: str,
            output_file_template: str = '$VIDEO_NAME-Shot-$SCENE_NUMBER.mp4',
    ):
        """
        Splits the video into individual shot files and saves them in the specified directory.

        Args:
            shot_list (Iterable[Tuple[FrameTimecode, FrameTimecode]]): An iterable 
                of (start_timecode, end_timecode) tuples representing the detected shots.
            output_path (str): The directory path where the shot files will be stored.
            output_file_template (str, optional): A naming template for each shot file. 
                Default is '$VIDEO_NAME-Shot-$SCENE_NUMBER.mp4'.

        Returns:
            None

        Examples:
            >>> video = Video(path='data/raw/video1.mp4', debug=True)
            >>> video._save_video_shots(shot_list, output_path='data/processed/video1')
        """
        split_video_ffmpeg(
            input_video_path=self.path,
            scene_list=shot_list,
            output_dir=output_path,
            output_file_template=output_file_template,
            show_progress=self.debug
        )

    def _save_image_shots(
            self,
            shot_list: Iterable[Tuple[FrameTimecode, FrameTimecode]],
            output_path: str,
            output_file_template: str = "$VIDEO_NAME-Scene-$SCENE_NUMBER-$IMAGE_NUMBER",
    ):
        """
        Splits the video into individual shot files and saves them in the specified directory.

        Args:
            shot_list (Iterable[Tuple[FrameTimecode, FrameTimecode]]): An iterable
                of (start_timecode, end_timecode) tuples representing the detected shots.
            output_path (str): The directory path where the shot files will be stored.
            output_file_template (str, optional): A naming template for each shot file.
                Default is '$VIDEO_NAME-Shot-$SCENE_NUMBER.mp4'.

        Returns:
            None

        Examples:
            >>> video = Video(path='data/raw/video1.mp4', debug=True)
            >>> video._save_video_shots(shot_list, output_path='data/processed/video1')
        """
        save_images(
            shot_list,
            self.video,
            num_images=3,
            output_dir=output_path,
            image_name_template=output_file_template,
            show_progress=self.debug,
        )

    def _save_shots_metadata(
            self,
            shot_list: Iterable[Tuple[FrameTimecode, FrameTimecode]],
            output_path: str,
    ):
        """
        Saves metadata about each shot (ID, start time, end time) to a JSON file.

        Args:
            shot_list (Iterable[Tuple[FrameTimecode, FrameTimecode]]): An iterable 
                of (start_timecode, end_timecode) tuples representing the detected shots.
            output_path (str): The directory path where the JSON metadata file will be stored.

        Returns:
            None

        Examples:
            >>> video = Video(path='data/raw/video1.mp4', debug=True)
            >>> video._save_shots_info(shot_list, output_path='data/processed)
        """
        metadata = {
            "video_name": self.video_name,
            "shots": []
        }

        for idx, shot in enumerate(shot_list, start=1):
            shot_info = {
                "shot_id": f'{idx:03d}',
                "start_time": str(shot[0]),
                "end_time": str(shot[1]),
            }
            metadata["shots"].append(shot_info)

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        json_path = os.path.join(output_path, f"{self.video_name}.json")
        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(metadata, file, ensure_ascii=False, indent=4)

    def split_and_save_shots(
            self,
            save_video_shots: bool,
            save_image_shots: bool,
            save_metadata_shots: bool,
            threshold: float = 27.0,
            output_path: str = './data/processed',

    ):
        """
        High-level method that performs the entire process of detecting shots, 
        splitting the video into shot files, and saving shot metadata.

        It does the following:
            1. Detects shots in the video using the specified threshold.
            2. Splits the video into multiple shot files.
            3. Saves a JSON file containing shot metadata.

        Args:
            threshold (float, optional): The threshold for shot detection. 
                A higher value typically produces fewer, longer shots.
                Default is 27.0.
            output_path (str, optional): The base directory for storing the shot files 
                and metadata JSON file. 
                Default is './data/processed'.

        Returns:
            None

        Examples:
            >>> video = Video(path='data/raw/video1.mp4', debug=True)
            >>> video.split_and_save_shots(output_path='data/processed', threshold=30.0)
        """
        shot_list = self._get_shot_list(threshold=threshold)

        if save_video_shots:
            video_output_dir = os.path.join(
                output_path,
                "video",
                self.video_name
            )
            self._save_video_shots(
                shot_list=shot_list,
                output_path=video_output_dir,
            )

        if save_image_shots:
            image_output_dir = os.path.join(
                output_path,
                "image",
                self.video_name
            )
            self._save_image_shots(
                shot_list=shot_list,
                output_path=image_output_dir
            )

        if save_metadata_shots:
            metadata_output_dir = os.path.join(output_path, "metadata")
            self._save_shots_metadata(
                shot_list=shot_list,
                output_path=metadata_output_dir,
            )
