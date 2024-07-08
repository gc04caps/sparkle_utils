# sparkle_utils
Utilities for sparkle player. Place these in your DVR recordings folder and use python to run them.

## merge_recordings
This is used when your recording has an error that sparkle recovers from by creating multple recordings for a single program, but does not stitch them into a single file after.

- Finds all pieces/partial recordings associated with a ProgramId
- uses ffmpeg to merge them into a single file
- removes the "source" pieces/partial recording files
- removes the associated entry from the recordings metadata file

## remux_recordings
This is used to remux recordings from .ts to .mkv so that they "play nice" with things like plex. It also cleans out (sets to an empty array) the sparkle DVR recordings metadata file. I have a plex library pointed at this folder that picks up the mkv files, so there is no need for me to retain them in the sparkle DVR metadata after remuxing as I will play them back outside of sparkle. 

- Finds all .ts files in the directory
- uses ffmpeg to remux them to .mkv
- removes the "source" recording files
- clears out the recordings metadata file

## purge_recordings
This does exactly what it says on the tin:

- deletes all of your recordings (everything in the folder with .ts file extension)
- clears out the DVR metadata file
- **Make sure you move or otherwise retain the recordings you want to keep before running this**

## how to use
Example of using `remux_recordings.py`: 

- Place remux_recordings.py in the same folder as my DVR recordings
- Execute command:
```
python .\remux_recordings.py
```
Console output:
```
Converting Sesame_Street_1100_20240708.ts to Sesame_Street_1100_20240708.mkv
Success! Done converting Sesame_Street_1100_20240708.ts to Sesame_Street_1100_20240708.mkv
Deleted original file: Sesame_Street_1100_20240708.ts
Emptied recordings DVR metadata file
```

Before running, I have the following files in my folder:
- remux_recordings.py
- Sesame_Street_1100_20240708.ts
- recordings (sparkle DVR metadata file) with contents:
```
[
  {
    "ChannelId": "PBSKAET.us",
    "Description": "S53E20 Count On\nGrover is a cat sitter; The Count helps him count all the cats.",
    "Name": "Sesame Street",
    "ProgramId": "PBSKAET.us_1720458000000",
    "RecordingId": "d9c73bf2-a060-4d9f-bff8-b9a2a51b91fc",
    "Start": 1720458000899,
    "Stop": 1720458785727,
    "Url": "smb://192.168.0.242/DVR/Sesame_Street_1100_20240708.ts"
  }
]
```

After running I have the following files in my folder:
- remux_recordings.py
- Sesame_Street_1100_20240708.mkv
- recordings (sparkle DVR metadata file) with contents:
```
[]
```
