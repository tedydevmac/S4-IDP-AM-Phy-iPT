import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# 07_analyse_received_sound.py
def load_received_sound(filename):
    """Load received WAV file and normalize to float in [-1,1]."""
    fs, data = wavfile.read(filename)
    # If stereo, take one channel
    if data.ndim > 1:
        data = data[:, 0]
    # normalize
    data = data.astype(np.float32)
    data /= np.max(np.abs(data))
    return fs, data


def plot_envelope(fs, data, title, xlim=None, ylim=None, savefile=None):
    """Plot the envelope (absolute amplitude) of the signal."""
    t = np.arange(len(data)) / fs
    env = np.abs(data)
    plt.figure(figsize=(10, 3))
    plt.plot(t, env)
    plt.title(title)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (arb. units)')
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    plt.tight_layout()
    if savefile:
        plt.savefig(savefile, dpi=300)
    plt.show()


def plot_raw_wave(fs, data, title, xlim=None, ylim=None, savefile=None):
    """Plot raw waveform of the signal."""
    t = np.arange(len(data)) / fs
    plt.figure(figsize=(6, 3))
    plt.plot(t, data)
    plt.title(title)
    plt.xlabel('Time (s)')
    plt.ylabel('Signal (arb. units)')
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    plt.tight_layout()
    if savefile:
        plt.savefig(savefile, dpi=300)
    plt.show()


def sound_wave_model(A, f, c, t):
    """Generate a sinusoidal model: y = A * sin(2*pi*f*(t - c))"""
    return A * np.sin(2 * np.pi * f * (t - c))


def plot_model_overlay(fs, data, A, f, c, title, xlim=None, ylim=None, savefile=None):
    """Plot raw data and overlay sinusoidal model on same axes."""
    t = np.arange(len(data)) / fs
    model = sound_wave_model(A, f, c, t)
    plt.figure(figsize=(6, 3))
    plt.plot(t, data, label='Received')
    plt.plot(t, model, label='Model', linestyle='--')
    plt.title(title)
    plt.xlabel('Time (s)')
    plt.ylabel('Signal (arb. units)')
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    plt.legend()
    plt.tight_layout()
    if savefile:
        plt.savefig(savefile, dpi=300)
    plt.show()


if __name__ == '__main__':
    # Load received sound
    fs, data = load_received_sound('/Volumes/T9/tedgoh/S4-IDP-AM-Phy-iPT/06a_received_sound.wav')

    # 1. Envelope of complete message
    plot_envelope(fs, data,
                  title='08 Received sound envelope - complete message',
                  savefile='08_received_envelope_complete.png')

    # 2. Envelope of first word (0 to 1 second)
    plot_envelope(fs, data,
                  title='08a Received sound envelope - 1st word',
                  xlim=(0.0, 1.0),  # limits reduced to 1s window
                  savefile='08a_received_envelope_1st.png')

    # 3. Envelope of second word (1 to 2 seconds)
    plot_envelope(fs, data,
                  title='08b Received sound envelope - 2nd word',
                  xlim=(1.0, 2.0),  # limits reduced to 1s window
                  savefile='08b_received_envelope_2nd.png')

    # 4. Raw waveform of one on-pulse for period analysis
    plot_raw_wave(fs, data,
                  title='09a Received sound period - Raw',
                  xlim=(0.5, 0.505),  # zoomed to 5 ms window
                  ylim=(-0.065, 0.065),  # limits to show the pulse
                  savefile='09a Received sound period - Raw.png')

    # 5. Model overlay
    A = 0.5  # example amplitude
    f = 440.0  # example frequency (Hz)
    c = 0.200  # example phase offset (s)
    plot_model_overlay(fs, data,
                       A, f, c,
                       title='09c Received sound period - Model',
                       xlim=(0.2, 0.205),  # matched to raw window
                       savefile='09c_received_period_model.png')
