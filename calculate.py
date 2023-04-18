from pydub import AudioSegment
import pyloudnorm as pyln
import numpy as np

def calculate_lufs(audio_segment):
    audio_data = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)
    sample_rate = audio_segment.frame_rate

    # Normalize the audio data to be in the range of -1 to 1
    audio_data /= np.iinfo(np.int32).max

    if audio_segment.channels > 1:
        audio_data = audio_data.reshape(-1, audio_segment.channels)

    meter = pyln.Meter(sample_rate)
    loudness = meter.integrated_loudness(audio_data)
    return loudness

def analyze_wav_files(file_paths):
    audio_segments = [AudioSegment.from_wav(file_path) for file_path in file_paths]
    individual_loudness = [calculate_lufs(audio_segment) for audio_segment in audio_segments]
    return audio_segments, individual_loudness

def calculate_gain_adjustment(individual_loudness, target_loudness):
    gain_adjustments = [target_loudness - loudness for loudness in individual_loudness]

    scaling_factor = min(1, target_loudness / max(gain_adjustments))
    adjusted_gains = [gain * scaling_factor for gain in gain_adjustments]

    return adjusted_gains

def calculate_peak_level(audio_segment):
    return audio_segment.max_dBFS
