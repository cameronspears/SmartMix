from pydub import AudioSegment
from pydub.effects import compress_dynamic_range

def first_gain_adjustment(wav_data, sample_rates, gain_adjustments):
    mixed_audio = AudioSegment.silent(duration=0)

    for data, sample_rate, gain_adjustment in zip(wav_data, sample_rates, gain_adjustments):
        audio = AudioSegment(data.tobytes(), frame_rate=sample_rate, sample_width=data.dtype.itemsize, channels=len(data.shape))
        adjusted_audio = audio + gain_adjustment
        mixed_audio = mixed_audio.overlay(adjusted_audio)

    return mixed_audio

def apply_compression(audio_segment, threshold, ratio, attack, release):
    return compress_dynamic_range(
        audio_segment,
        threshold=threshold,
        ratio=ratio,
        attack_time=attack,
        release_time=release,
    )

def final_gain_adjustment(audio_segment, current_lufs, target_lufs):
    gain_difference = target_lufs - current_lufs
    adjusted_audio = audio_segment + gain_difference
    return adjusted_audio
