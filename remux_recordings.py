import os
import subprocess

def remux_to_mkv(ts_file):
    """Remuxes a .ts file to .mkv using ffmpeg and deletes the original."""
    mkv_file = ts_file.replace(".ts", ".mkv")
    
    ffmpeg_path = "ffmpeg"
    ffmpeg_command = [ffmpeg_path, "-i", ts_file, "-c", "copy", mkv_file]
    
    try:
        print(f"Converting {ts_file} to {mkv_file}")
        result = subprocess.run(ffmpeg_command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error converting {ts_file} to {mkv_file}:")
        print(e.stderr)
    else:
        print(f"Success! Done converting {ts_file} to {mkv_file}")
        os.remove(ts_file)
        print(f"Deleted original file: {ts_file}")

def remux_recordings():
    """Remuxes all .ts files in the directory, then empties the "recordings" file."""
    for filename in os.listdir():
        if filename.endswith(".ts"):
            remux_to_mkv(filename)

    # Empty the recordings file
    recordings_file = "recordings"
    try:
        with open(recordings_file, 'w') as f:
            f.write("[]")  # Write an empty JSON array
        print(f"Emptied {recordings_file} DVR metadata file")
    except FileNotFoundError:
        print(f"Warning: {recordings_file} not found.")

if __name__ == "__main__":
    remux_recordings()
