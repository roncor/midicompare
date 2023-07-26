from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import tempfile
import os
from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH

# Step 1: Convert Video to MP3 and store it in a variable

def convert_to_mp3(filename):
    clip = VideoFileClip(filename)
    mp3_filename = filename[:-4] + ".mp3"
    clip.audio.write_audiofile(mp3_filename, codec='libmp3lame')
    clip.close()
    return mp3_filename

video_path = ""

mp3_file = convert_to_mp3(video_path)

# Step 2: Perform Pitch Inference and Save

input_audio_path_list = [mp3_file]  # Use the mp3 file

output_directory = ""
save_midi = True
sonify_midi = False
save_model_outputs = False
save_notes = False

predict_and_save(
    input_audio_path_list,
    output_directory,
    save_midi,
    sonify_midi,
    save_model_outputs,
    save_notes,
)


