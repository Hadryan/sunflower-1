from .song_loader import Song
import librosa


class SongAnalyzer:
    def __init__(self, song: Song):
        """Creates a SongAnalyzer object.
        """

        ######################
        # Loaded song

        self.song = song

        #################
        # Features

        self.tempo = None
        self.beat_frames = None

    def detect_tempo(self):
        """Detects tempo of a track.
        """

        if (self.song.sr is None) or (self.song.waveform is None):
            raise ValueError("No song was loaded.")

        # Detect tempo
        tempo, beat_frames = librosa.beat.beat_track(
            y=self.song.mono_waveform, sr=self.song.sr, tightness=100
        )

        self.tempo = adjust_tempo(tempo)
        self.beat_frames = beat_frames


def adjust_tempo(bpm: float, mode="chill") -> float:
    """Adjusts the BPM for more coherence (e.g. turning 160 BPM into 80 BPM)

    :param bpm: BPM of the song
    :param mode: Type of song to analyse.
    Setting the mode to 'chill' ensures to have a BPM lower to a threshold (110 BPM)
    """

    THRESOLD = 110

    if mode == "chill":

        while bpm > THRESOLD:
            bpm = bpm / 2

    bpm = round(bpm, 0)

    return bpm
