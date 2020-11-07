import matplotlib.pyplot as plt
import librosa.display


def visualize_waveform(song):
    """Waveform visualization.
    """

    plt.figure(figsize=(16, 4))
    librosa.display.waveplot(song.mono_waveform, sr=song.sr)
    plt.title("Waveform Visualizer (mono)")
    plt.show()
