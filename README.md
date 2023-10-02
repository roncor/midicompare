# MIDI Comparison and Conversion

This application provides two main functionalities:

    Comparing two MIDI files.
    Converting a video file to MIDI.

## Installation

Before you run the server, ensure you have the required packages installed. You can install them using the following command:
  `pip install flask mido numpy scikit-learn scipy moviepy pydub basic_pitch`
## API Endpoints

POST /compare_midi

This endpoint compares two uploaded MIDI files.

Response:

The API responds with a JSON object that contains the following keys:

    normalized_manhattan_distance: A value between 0 and 1 representing the normalized Manhattan distance between the two MIDI files. A lower value indicates greater similarity.
    manhattan_message: A qualitative description based on the normalized_manhattan_distance value. It can be "Excellent", "Acceptable", or "Need to improve".
    differences: A list of dictionaries where each dictionary represents a segment comparison between the two MIDI files. Each dictionary contains:
        segment: Segment number.
        file1: Note strings for file1 in this segment.
        file2: Note strings for file2 in this segment.
        difference_percent: Difference percentage between the note strings in this segment.
        message: A message describing the level of difference: "Segments are completely different", "Segments are somewhat different", or "Segments are slightly different".
