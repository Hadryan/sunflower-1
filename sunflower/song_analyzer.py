from .song_loader import Song


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
        self.tempo, self.beat_frames = librosa.beat.beat_track(
            y=self.song.mono_waveform, sr=self.song.sr, tightness=100
        )
