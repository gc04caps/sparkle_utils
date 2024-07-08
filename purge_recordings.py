import os

def delete_ts_files(ts_file):
    """Deletes all .ts files in directory"""
    os.remove(ts_file)
    print(f"Deleted recording file: {ts_file}")
   

def purge_recordings():
    """Remuxes all .ts files in the directory, then empties the "recordings" file."""
    for filename in os.listdir():
        if filename.endswith(".ts"):
            delete_ts_files(filename)

    # Empty the recordings file
    recordings_file = "recordings"
    try:
        with open(recordings_file, 'w') as f:
            f.write("[]")  # Write an empty JSON array
        print(f"Emptied {recordings_file} DVR metadata file")
    except FileNotFoundError:
        print(f"Warning: {recordings_file} not found.")

if __name__ == "__main__":
    purge_recordings()
