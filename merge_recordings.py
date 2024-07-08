import json
import os
import subprocess
import re
import glob
from datetime import datetime

def sanitize_filename(filename):
    return re.sub(r'[^\w\s.-]', '', filename).replace(" ", "_")

def merge_recordings(recordings_file):
    with open(recordings_file, 'r') as f:
        data = json.load(f)

    merged_files = {}
    processed_files = set()

    for recording in data[:]:  
        program_id = recording["ProgramId"]
        start_time = recording.get("Start", 0)
        date_str = datetime.fromtimestamp(start_time / 1000).strftime("%Y%m%d")

        matching_file = next((f for f in os.listdir() if date_str in f), None)
        if matching_file:
            show_name = matching_file.split('_')[0]

            file_name_pattern = re.compile(rf"{show_name}.*{date_str}\.ts", re.IGNORECASE)
            matching_files = [f for f in os.listdir() if file_name_pattern.match(f)]

            if not matching_files:
                print(f"Warning: No files found matching pattern: {file_name_pattern}")
                continue

            for file in matching_files:
                if file in processed_files:
                    continue

                processed_files.add(file)  
                merged_files.setdefault(program_id, []).append(file)

    for program_id, files in merged_files.items():
        if len(files) > 1:
            output_file = f"{show_name}_{date_str}.ts"
            print("Files to merge:", files)
            file_list = "|".join(files)

            ffmpeg_path = "ffmpeg"  # Specify full path
            ffmpeg_command = [ffmpeg_path, "-i", f"concat:{file_list}", "-c", "copy", output_file]

            try:
                result = subprocess.run(ffmpeg_command, check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                print(f"Error merging files for {program_id}:")
                print(e.stderr)
            else:
                print(f"Merged recordings for {program_id} into {output_file}")

                # Remove source files
                for file in files:
                    file_path = os.path.abspath(file)  
                    try:
                        os.remove(file_path)
                        print(f"Removed source file: {file}")
                    except FileNotFoundError:
                        print(f"Warning: Source file not found: {file}")

                # Remove corresponding recording entry
                data = [rec for rec in data if rec["ProgramId"] != program_id]

    # Update the recordings file, preserving the original format
    with open(recordings_file, 'w') as f:
        json.dump(data, f, separators=(',', ':'))  # Use separators to control formatting
        print("Recordings file updated.")

if __name__ == "__main__":
    recordings_file = "recordings"
    merge_recordings(recordings_file)
