from pydub import AudioSegment
from pydub.silence import detect_nonsilent


def get_dBFS(file_path):
    audio = AudioSegment.from_wav(file_path)
    return audio.dBFS

def normalize_volume(file_path, target_dBFS = -20.0) -> AudioSegment:
    audio = AudioSegment.from_wav(file_path)
    change_in_dBFS = target_dBFS - audio.dBFS
    audio.apply_gain(change_in_dBFS)
    return audio

def detect_nonsilent(file_path, min_silence_len=100):
    audio = normalize_volume(file_path)
    return detect_nonsilent(audio, min_silence_len=min_silence_len)