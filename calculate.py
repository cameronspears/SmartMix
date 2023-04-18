from scipy.io import wavfile
from pydub import AudioSegment
from pyloudnorm import Meter

def calculate_lufs(audio_segment):
    meter = Meter(audio_segment.frame_rate)
    return meter.integrated_loudness(audio_segment.get_array_of_samples().astype(float))

def analyze_wav_files(filepaths):
    wav_data = []
    sample_rates = []
    individual_loudness = []

    for filepath in filepaths:
        sample_rate, data = wavfile.read(filepath)
        sample_rates.append(sample_rate)
        wav_data.append(data)

        audio = AudioSegment(data.tobytes(), frame_rate=sample_rate, sample_width=data.dtype.itemsize, channels=len(data.shape))
        individual_loudness.append(calculate_lufs(audio))

    return wav_data, sample_rates, individual_loudness

def calculate_gain_adjustment(individual_loudness, target_loudness):
    gain_adjustments = [target_loudness - loudness for loudness in individual_loudness]

    scaling_factor = min(1, target_loudness / max(gain_adjustments))
    adjusted_gains = [gain * scaling_factor for gain in gain_adjustments]

    return adjusted_gains

def calculate_peak_level(audio_segment):
    return audio_segment.max_dBFS
