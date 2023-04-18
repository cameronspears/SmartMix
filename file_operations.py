from tkinter import filedialog
from pydub import AudioSegment

def load():
    file_paths = filedialog.askopenfilenames(title="Load .WAV files", filetypes=[("WAV files", "*.wav")])
    audio_segments = [AudioSegment.from_wav(file_path) for file_path in file_paths]
    return file_paths, audio_segments

def save(mixed_audio):
    output_file_path = filedialog.asksaveasfilename(
        title="Save the mixed WAV file as",
        defaultextension=".wav",
        filetypes=[("WAV files", "*.wav")])
    if output_file_path:
        mixed_audio.export(output_file_path, format="wav")