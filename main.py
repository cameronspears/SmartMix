import configparser
import calculate
import effects
import file_operations

def main():
    # Read the config.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')
    pre_compression_target_loudness = float(config.get('Gain', 'PreCompressionTargetLoudness'))
    final_target_loudness = float(config.get('Gain', 'FinalTargetLoudness'))
    threshold = float(config.get('Compressor', 'Threshold'))
    ratio = float(config.get('Compressor', 'Ratio'))
    attack = float(config.get('Compressor', 'Attack'))
    release = float(config.get('Compressor', 'Release'))

    # Load WAV files
    file_paths, audio_segments = file_operations.load()

    # Analyze WAV files and calculate gain adjustments
    wav_data, sample_rates, individual_loudness = calculate.analyze_wav_files(file_paths)
    gain_adjustments = calculate.calculate_gain_adjustment(individual_loudness, pre_compression_target_loudness)

    # Apply gain correction (first pass)
    gain_adjusted_audio = effects.first_gain_adjustment(wav_data, sample_rates, gain_adjustments)

    # Apply compression
    compressed_audio = effects.apply_compression(gain_adjusted_audio, threshold, ratio, attack, release)

    # Measure LUFS and peak level after compression
    current_lufs = calculate.calculate_lufs(compressed_audio)
    current_peak = calculate.calculate_peak_level(compressed_audio)

    # Adjust the final_target_loudness if necessary to ensure that peaks do not exceed -6 dBFS
    if current_peak + (final_target_loudness - current_lufs) > -6:
        final_target_loudness = current_lufs + (-6 - current_peak)

    # Perform the final gain adjustment
    mixed_audio = effects.final_gain_adjustment(compressed_audio, current_lufs, final_target_loudness)

    # Save the mixed audio
    file_operations.save(mixed_audio)

if __name__ == "__main__":
    main()
