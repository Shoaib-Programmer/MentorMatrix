import librosa  # type: ignore
import numpy as np  # type: ignore
from icecream import ic  # type: ignore


def is_audio_usable(audio_file, silence_threshold=-50.0, noise_threshold=0.2) -> bool:
    """
    Analyzes an audio file to determine if it is suitable for transcription based on
    its loudness and noise levels.

    Parameters:
        audio_file (str): Path to the audio file to analyze.
        silence_threshold (float): Threshold for detecting mostly silent audio,
                                   measured in dBFS (default is -50.0 dBFS).
        noise_threshold (float): Threshold for spectral flatness to determine excessive noise
                                 (default is 0.2). Values close to 1 indicate high noise levels.

    Returns:
        bool: True if the audio is suitable for transcription; False if it is too noisy or silent.
    """

    try:
        # Load audio data for both loudness and noise analysis
        y, sr = librosa.load(audio_file, sr=None)

        # Calculate loudness (RMS energy) in decibels
        rms = librosa.feature.rms(y=y)
        rms_db = librosa.amplitude_to_db(rms)

        # Calculate average loudness across the entire file
        avg_loudness = np.mean(rms_db)

        # Check if the audio is mostly silent based on average loudness
        if avg_loudness < silence_threshold:
            return False

        # Calculate spectral flatness (used to detect noisiness)
        spectral_flatness = librosa.feature.spectral_flatness(y=y).mean()
        if spectral_flatness > noise_threshold:
            return False

        # Audio is usable
        return True

    except Exception as e:
        ic(f"Error analyzing audio file {audio_file}: {e}")
        return False
