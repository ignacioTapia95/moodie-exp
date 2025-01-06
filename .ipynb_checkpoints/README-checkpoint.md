# Moodie Exp

## Project Structure

```bash
.
├── README.md
├── data
│   ├── processed
│   └── raw
├── notebooks
│   ├── audio
│   │   ├── 01-eda-anime.ipynb
│   │   └── 01-eda-intersetellar.ipynb
│   ├── cross
│   │   ├── 01-split-videos.ipynb
│   │   └── 02-split-scene.ipynb
│   └── video
│       ├── CLIP.ipynb
│       ├── VEDM.ipynb
│       └── XCLIP.ipynb
├── requirements.txt
├── scripts
│   └── process_files.py
└── src
    ├── data
    │   └── processing.py
    └── utils
```

## Setup

To set up the project, follow these steps:

1. Create a virtual environment:

   ```sh
   python -m venv venv
   ```

2. Activate the virtual environment:

   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```

3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Processing Files

To process video files using the available script, follow these steps:

1. Run the [process_files.py](scripts/process_files.py) script with the necessary arguments:

   ```sh
   python scripts/process_files.py --input <input_path> --output <output_path> --extensions <extensions> --threshold <threshold> [--recursive] [--debug]
   ```

   - `--input`: Path to the input directory containing video files.
   - `--output`: Path to the output directory where processed files will be saved.
   - `--extensions`: File extensions to process (e.g., `mp4, avi`).
   - `--threshold`: (Optional) Threshold value for processing (defaul=27.0).
   - `--recursive`: (Optional) If set, it will search subdirectories recursively.
   - `--debug`: (Optional) Enables debug mode to print additional information.

Example:

```sh
python scripts/process_files.py --input data/raw --output data/processed
```

This will process the video files in the [raw](data/raw) directory and save the processed files in the [processed](data/processed/)
