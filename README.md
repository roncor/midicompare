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

* normalized_manhattan_distance: A value between 0 and 1 representing the normalized Manhattan distance between the two MIDI files. A lower value indicates greater similarity.
* manhattan_message: A qualitative description based on the normalized_manhattan_distance value. It can be "Excellent", "Acceptable", or "Need to improve".
  * segment: Segment number.
  * file1: Note strings for file1 in this segment.
  * file2: Note strings for file2 in this segment.
  * difference_percent: Difference percentage between the note strings in this segment.
  * message: A message describing the level of difference: "Segments are completely different", "Segments are somewhat different", or "Segments are slightly different".

# Additional Information
## MIDI Comparison
* The compare_midi endpoint first extracts note, velocity, and time information from the uploaded MIDI files.
* It calculates the cosine similarity and Manhattan distance between the two sets of notes.
* It concatenates notes that occur within 10 seconds of each other and compares the resulting note strings.
* The response contains the normalized Manhattan distance, a message regarding the Manhattan distance, and a list of differences for each concatenated note segment.

# MIDI Conversion

* The convert_midi endpoint first converts the uploaded video to MP3.
* It performs pitch inference on the audio and saves the result as a MIDI file.
* The response contains a message indicating the completion of the MIDI conversion.

Note: Update the output_directory in the convert_midi function to specify the directory to save the output MIDI file.

# Using gunicorn
If you haven’t installed Gunicorn, you can do so using pip:

`pip install gunicorn`

# Create a Gunicorn Configuration File:
Create a file named gunicorn_config.py and add the following contents to configure the bind address and the number of worker processes:

```python
# inside gunicorn_config.py
bind = "0.0.0.0:8080"
workers = 2
```

This configuration will run the Gunicorn server on all available network interfaces on port 8080 with 2 worker processes.


