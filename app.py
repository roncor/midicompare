from flask import Flask, request, jsonify
import mido
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cityblock
from io import BytesIO

#For midi convert

from basic_pitch.inference import predict
from basic_pitch import ICASSP_2022_MODEL_PATH
from basic_pitch.inference import predict_and_save

app = Flask(__name__)


def extract_midi_info(uploaded_file):
    midi = mido.MidiFile(file=BytesIO(uploaded_file))
    notes = []
    velocities = []
    times = []
    time = 0
    for track in midi.tracks:
        for msg in track:
            time += msg.time
            if msg.type == 'note_on':
                notes.append(msg.note)
                velocities.append(msg.velocity)
                times.append(time)
    frequencies = [440.0 * pow(2.0, (note - 69) / 12.0) for note in notes]
    return notes, velocities, frequencies, times


def note_number_to_name(note_number):
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = note_number // 12 - 1
    note_name = note_names[note_number % 12]
    return f"{note_name}{octave}"


def concatenate_notes(notes, times):
    concatenated_notes = []
    start_time = 0
    segment = []
    for note, time in zip(notes, times):
        if time - start_time < 10 * mido.second2tick(1, 480, 500000): # 10 seconds * ticks per second
            segment.append(note)
        else:
            concatenated_segment = ' '.join([note_number_to_name(note) for note in segment])
            concatenated_notes.append(concatenated_segment)
            segment = [note]
            start_time = time
    # append the last segment
    if segment:
        concatenated_segment = ' '.join([note_number_to_name(note) for note in segment])
        concatenated_notes.append(concatenated_segment)
    return concatenated_notes


def compare_note_strings(note_strings1, note_strings2):
    differences = []
    for i, (note_string1, note_string2) in enumerate(zip(note_strings1, note_strings2)):
        set1 = set(note_string1.split())
        set2 = set(note_string2.split())
        common = len(set1 & set2)
        total = len(set1 | set2)
        difference_percent = (1 - common / total) * 100 if total > 0 else 0

        if difference_percent > 66.66:
            message = "Segments are completely different"
        elif difference_percent > 33.33:
            message = "Segments are somewhat different"
        else:
            message = "Segments are slightly different"

        differences.append((i, note_string1, note_string2, difference_percent, message))
    return differences


@app.route('/compare_midi', methods=['POST'])
def compare_midi():
    file1 = request.files['file1'].read()
    file2 = request.files['file2'].read()

    if file1 and file2:
        notes1, velocities1, frequencies1, times1 = extract_midi_info(file1)
        notes2, velocities2, frequencies2, times2 = extract_midi_info(file2)

        min_length = min(len(notes1), len(notes2))
        cos_sim = cosine_similarity(np.array(notes1[:min_length]).reshape(1, -1), np.array(notes2[:min_length]).reshape(1, -1))[0][0]

        manhattan_distance = cityblock(notes1[:min_length], notes2[:min_length])
        max_possible_distance = min_length * (max(notes1 + notes2) - min(notes1 + notes2))
        normalized_manhattan_distance = manhattan_distance / max_possible_distance if max_possible_distance > 0 else 0
        normalized_manhattan_distance = round(normalized_manhattan_distance, 2)

        if normalized_manhattan_distance > 0.8:
            message = "Excellent"
        elif normalized_manhattan_distance > 0.6:
            message = "Acceptable"
        else:
            message = "Need to improve"

        concatenated_notes1 = concatenate_notes(notes1, times1)
        concatenated_notes2 = concatenate_notes(notes2, times2)

        differences = compare_note_strings(concatenated_notes1, concatenated_notes2)
        difference_list = []

        if differences:
            for diff in differences:
                difference_list.append({
                    "segment": diff[0] + 1,
                    "file1": diff[1],
                    "file2": diff[2],
                    "difference_percent": round(diff[3], 2),
                    "message": diff[4]
                })

        result = {
            "normalized_manhattan_distance": normalized_manhattan_distance,
            "manhattan_message": message,
            "differences": difference_list
        }

        return jsonify(result)

    return jsonify({"error": "MIDI files are required"})

@app.route('/convert_midi', methods=['POST'])
def convert_midi():
    audio_file = request.files['audio'].read()

    if audio_file:
        input_audio_path_list = [audio_file]
        output_directory = ""  # Specify the directory where you want to save the output MIDI file,
        save_midi = True  # Set to True if you want to save the generated MIDI file
        sonify_midi = False  # Set to True if you want to play the generated MIDI file
        save_model_outputs = False  # Set to True if you want to save the intermediate model outputs
        save_notes = False  # Set to True if you want to save the extracted notes from the audio

        predict_and_save(
            input_audio_path_list,
            output_directory,
            save_midi,
            sonify_midi,
            save_model_outputs,
            save_notes
        )

        return jsonify({"message": "MIDI conversion completed."})

    return jsonify({"error": "Audio file is required."})

if __name__ == '__main__':
    app.run(debug=True)
