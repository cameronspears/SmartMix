from tkinter import filedialog, Tk
from pydub import AudioSegment

def create_hidden_tk_instance():
    root = Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)
    return root

def load():
    root = create_hidden_tk_instance()
    file_paths = filedialog.askopenfilenames(
        parent=root,
        title="Load .WAV files",
        filetypes=[("WAV files", "*.wav")]
    )
    audio_segments = [AudioSegment.from_wav(file_path) for file_path in file_paths]
    root.destroy()
    return file_paths, audio_segments

def save(mixed_audio, filename=None):
    root = create_hidden_tk_instance()
    if filename:
        output_file_path = f"{filename}.wav"
    else:
        output_file_path = filedialog.asksaveasfilename(
            parent=root,
            title="Save the mixed WAV file as",
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav")]
        )
    if output_file_path:
        mixed_audio.export(output_file_path, format="wav")
    root.destroy()
