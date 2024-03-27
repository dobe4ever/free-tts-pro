from datetime import datetime
import os
import time
from elevenlabs import generate, save

def text_to_parags(text):
    """Split text into paragraphs."""
    parags = []
    start = 0
    while start < len(text):
        # Find the next period within the max length
        end_period = text.rfind(".", start, start + 499 + 1)
        # Find the next comma within the max length (if no period)
        end_comma = text.rfind(",", start, start + 499 + 1) if end_period == -1 else -1

        # Use the closest valid delimiter
        if end_period != -1:
            end = end_period
        elif end_comma != -1:
            end = end_comma
        else:
            end = start + 499

        # Extract parag without the delimiter
        parag = text[start:end + 1]

        # Remove leading whitespace only for subsequent parags
        if start > 0:
            parag = parag.lstrip()

        parags.append(parag)

        # Update start for the next iteration
        start = end + 1

    return parags

def parags_to_speech(parags):
    """Convert paragraphs to speech and save as MP3 files."""
    files_dir = 'files'
    os.makedirs(files_dir, exist_ok=True)

    mp3s = []
    for parag in parags:
        time.sleep(2)
        audio = generate(
            text=parag,
            voice="Bella",
            model="eleven_monolingual_v1"
        )

        # Get & format datetime
        current_time = datetime.now().strftime("%d-%m_%H-%M-%S")

        # Save audio
        audio_file = os.path.join(files_dir, f"{current_time}.mp3")
        save(audio, audio_file)

        with open(audio_file, 'rb') as f:
            mp3s.append(f.read())

    # Combine all audios into one
    output_audio = b"".join(mp3s)

    # Save the combined audio as 'speech.mp3' in the root directory
    output_file = 'speech.mp3'
    with open(output_file, "wb") as f:
        f.write(output_audio)

    # Delete the small audio files in the 'files' folder
    for file_name in os.listdir(files_dir):
        file_path = os.path.join(files_dir, file_name)
        os.remove(file_path)

    os.rmdir(files_dir)

    return output_audio

# User Input:
text = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
"""

parags = text_to_parags(text)
output_audio = parags_to_speech(parags)

### python tests.py