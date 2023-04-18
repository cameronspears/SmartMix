import configparser
import calculate
import gain
import file

def main():
    # Read the config.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')
    target_gain = float(config.get('DEFAULT', 'TargetGain'))

    # Load WAV files
    file_paths, audio_segments = file.load()

    # Analyze WAV files and calculate gain adjustments
    wav_data, sample_rates, individual_gains = calculate.analyze_wav_files(file_paths)
    gain_adjustments = calculate.calculate_gain_adjustment(individual_gains, target_gain)

    # Apply gain adjustments and mix
    mixed_audio = gain.apply_gain_and_mix(wav_data, sample_rates, gain_adjustments)

    # Save the mixed audio
    file.save(mixed_audio)

if __name__ == "__main__":
    main()
