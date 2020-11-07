import librosa
import io
import pydub
import numpy as np
import soundfile as sf

ALLOWED_EXTENSIONS = {"mp3", "wav"}


class Song:
    def __init__(self, filelike, extension):
        """Creates a Song object.
        """

        ######################
        # Basic audio features

        self.waveform = None
        self.extension = None
        self.channels = None
        self.sr = None
        self.sample_width = None

        self.mono_waveform = None  # to remove ?

        self.load_from_filelike(filelike, extension)

        #################
        # Processing song

        self.process_song()

        # Features
        self.tempo = None
        self.beat_frames = None

    def load_from_filelike(self, filelike, extension: str):
        """Filelike to librosa."""

        self.extension = extension

        if extension == "mp3":
            a = pydub.AudioSegment.from_mp3(filelike)
        elif extension == "wav":
            a = pydub.AudioSegment.from_wav(filelike)
        else:
            raise ValueError("Wrong extension: Format not supported.")

        # Converting to float32 for librosa
        waveform = np.array(a.get_array_of_samples())

        self.sample_width = a.sample_width
        self.channels = 1

        if a.channels == 2:

            self.channels = 2
            waveform = waveform.reshape((-1, 2)).astype("float32")

        # Normalization
        waveform = waveform / self.channels ** 15
        self.waveform = waveform
        self.mono_waveform = np.array(a.set_channels(1).get_array_of_samples()).astype(
            "float32"
        )
        self.sr = a.frame_rate

    def print_attributes(self) -> None:
        """Print attributes of the object."""

        attrs = vars(song)
        print(", ".join("%s: %s" % item for item in attrs.items()))

    def process_song(self) -> None:
        """Removes silence at the beginning of the song."""

        self.waveform, _ = librosa.effects.trim(self.waveform)

    def detect_tempo(self):
        """Detects tempo of a track.
        """

        if (self.sr is None) or (self.waveform is None):
            raise ValueError("No song was loaded.")

        # Detect tempo
        self.tempo, self.beat_frames = librosa.beat.beat_track(
            y=self.mono_waveform, sr=self.sr, tightness=100
        )

    def export_wav(self):
        sf.write(
            "data/processedfile.wav",
            self.waveform.astype(np.float32, order="C") / 32768.0,
            self.sr,
        )


def allowed_file(filename: str) -> (bool, str):
    """Check if the file extension is allowed."""

    extension = ""
    allowed = False

    if "." in filename:

        extension = filename.rsplit(".", 1)[1].lower()

        allowed = filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    return (allowed, extension)


def load_from_disk(file_path: str):
    """Load a song from disk to emulate a GET request"""

    f = open(file_path, "rb")
    filename = f.name

    allowed, extension = allowed_file(filename)

    if not allowed:
        raise ValueError(
            f"File extension not allowed. Allowed extensions :{ALLOWED_EXTENSIONS}"
        )

    data_song = io.BytesIO(f.read())

    return data_song, extension


raw_audio, extension = load_from_disk("data/examplesong.wav")

song = Song(raw_audio, extension)

song.print_attributes()
