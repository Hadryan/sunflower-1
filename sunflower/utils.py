from .song_loader import Song
import soundfile as sf
import numpy as np


def export_wav(song: Song):
    """TO DO: Move this function somewhere else. 
    
    --- Just used for tests atm ---
    """

    sf.write("../data/processedfile.wav", song.waveform, song.sr, subtype="FLOAT")
