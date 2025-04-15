# 07_analyse_received_sound.py

# ===================
# INITIALIZATION
# ===================
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.optimize import curve_fit

# ================================
# SETTINGS AND GLOBAL VARIABLES
# ================================
filename = "06a_received_sound.wav"
samp_rate, samps = wavfile.read(filename)
samps = samps / np.max(np.abs(samps))  # Normalize amplitude

# ========================
# FUNCTION DEFINITIONS
# ========================
def samp_index_to_t(n, samp_rate):
    return n / samp_rate

def samp_ts(samps, samp_rate):
    return np.array([samp_index_to_t(n, samp_rate) for n in range(len(samps))])

def sound_wave_model(t, A, f, phi):
    return A * np.sin(2 * np.pi * f * t + phi)

def plot_envelope(samps, samp_rate, start_time, end_time, filename):
    start_idx = int(start_time * samp_rate)
    end_idx = int(end_time * samp_rate)
    subset = samps[start_idx:end_idx]
    t = samp_ts(subset, samp_rate)

    plt.figure(figsize=(10, 4))
    plt.plot(t, subset)
    plt.title("Sound Envelope")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def fit_and_plot_sinusoid(samps, samp_rate, start_time, end_time, filename):
    start_idx = int(start_time * samp_rate)
    end_idx = int(end_time * samp_rate)
    subset = samps[start_idx:end_idx]
    t = samp_ts(subset, samp_rate)

    guess_amplitude = np.max(np.abs(subset))
    guess_frequency = 1000  # Can be updated based on known value
    guess_phase = 0

    popt, _ = curve_fit(sound_wave_model, t, subset, p0=[guess_amplitude, guess_frequency, guess_phase])

    fit = sound_wave_model(t, *popt)

    plt.figure(figsize=(10, 4))
    plt.plot(t, subset, label='Original')
    plt.plot(t, fit, '--', label='Fitted')
    plt.title("Fitted Sinusoidal Wave")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return popt

# =================
# EXECUTION
# =================
plot_envelope(samps, samp_rate, start_time=0.0, end_time=1.0, filename="08a Received sound envelope - 1st word.png")
plot_envelope(samps, samp_rate, start_time=1.0, end_time=2.0, filename="08b Received sound envelope - 2nd word.png")

# Plot period segment
plot_envelope(samps, samp_rate, start_time=0.5, end_time=0.505, filename="09a Received sound period.png")

# Plot fitted sinusoid
fit_and_plot_sinusoid(samps, samp_rate, start_time=0.5, end_time=0.505, filename="09b Received sound period - Fitted sinusoid.png")
