from pydub import AudioSegment
from pydub.effects import compress_dynamic_range
import pyloudnorm as pyln
import numpy as np

def first_gain_adjustment(audio_segments, gain_adjustments):
    mixed_audio = AudioSegment.silent(duration=int(audio_segments[0].duration_seconds * 1000))

    for audio, gain_adjustment in zip(audio_segments, gain_adjustments):
        adjusted_audio = audio.apply_gain(gain_adjustment)
        mixed_audio = mixed_audio.overlay(adjusted_audio, position=0)

    return mixed_audio

def apply_compression(audio_segment, threshold, ratio, attack, release):
    return compress_dynamic_range(
        audio_segment,
        threshold=threshold,
        ratio=ratio,
        attack=attack,
        release=release,
    )

def final_gain_adjustment(audio_segment, current_lufs, target_lufs):
    gain_difference = target_lufs - current_lufs
    adjusted_audio = audio_segment.apply_gain(gain_difference)

    # Peak normalize to -6 dBFS
    audio_data = np.array(adjusted_audio.get_array_of_samples(), dtype=np.float32)
    sample_rate = adjusted_audio.frame_rate

    # Normalize the audio data to be in the range of -1 to 1
    audio_data /= np.iinfo(np.int32).max

    if adjusted_audio.channels > 1:
        audio_data = audio_data.reshape(-1, adjusted_audio.channels)

    peak_normalized_audio = pyln.normalize.peak(audio_data, -6.0)
    peak_normalized_audio *= np.iinfo(np.int32).max
    peak_normalized_audio = peak_normalized_audio.astype(np.int32)

    adjusted_audio = AudioSegment(
        peak_normalized_audio.tobytes(),
        frame_rate=sample_rate,
        sample_width=adjusted_audio.sample_width,
        channels=adjusted_audio.channels,
    )

    return adjusted_audio
