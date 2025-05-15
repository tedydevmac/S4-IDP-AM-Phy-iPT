# 01_msg_to_sound.py

# ===================
# INITIALIZATION
# ===================
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

# ================================
# SETTINGS AND GLOBAL VARIABLES
# ================================
msg = "  ethan goon  "  # Include 2 spaces before and after
total_msg_chars = len(msg)
pulse_duration = 0.1  # seconds (change according to your group)
sound_freq = 1760     # Hz (change according to your group)
samp_rate = 44100     # Hz
sound_amplitude = 10000  # Arbitrary units

# Morse key as [letter, morse_code]
key = [
    ['A', '.-'], ['B', '-...'], ['C', '-.-.'], ['D', '-..'], ['E', '.'], ['F', '..-.'],
    ['G', '--.'], ['H', '....'], ['I', '..'], ['J', '.---'], ['K', '-.-'], ['L', '.-..'],
    ['M', '--'], ['N', '-.'], ['O', '---'], ['P', '.--.'], ['Q', '--.-'], ['R', '.-.'],
    ['S', '...'], ['T', '-'], ['U', '..-'], ['V', '...-'], ['W', '.--'], ['X', '-..-'],
    ['Y', '-.--'], ['Z', '--..']
]

# ========================
# FUNCTION DEFINITIONS
# ========================
def morse_to_pulses(morse):
    pulses = ''
    for i, char in enumerate(morse):
        if char == '.':
            pulses += '1'
        elif char == '-':
            pulses += '111'
        if i < len(morse) - 1:
            pulses += '0'
    return pulses

def add_pulses_to_key(key):
    for i in range(len(key)):
        letter, morse = key[i]
        pulses = morse_to_pulses(morse)
        key[i].append(pulses)
    return key

def letter_to_pulses(letter, key):
    for item in key:
        if item[0] == letter:
            return item[2]
    raise ValueError(f"Letter '{letter}' not found in key")

def msg_to_pulses(msg, key):
    pulses = ''
    for i in range(len(msg)):
        if msg[i] == ' ':
            pulses += '0000000'
        else:
            pulses += letter_to_pulses(msg[i], key)
            if i < len(msg) - 1 and msg[i+1] != ' ':
                pulses += '000'  # interletter space
    return pulses

def t_to_samp_index(t):
    return int(round(t * samp_rate))

def samp_ts(start_t, end_t):
    start_idx = t_to_samp_index(start_t)
    end_idx = t_to_samp_index(end_t)
    indices = np.arange(start_idx, end_idx)
    return indices / samp_rate

def tone(start_t, end_t):
    ts = samp_ts(start_t, end_t)
    return sound_amplitude * np.sin(2 * np.pi * sound_freq * ts)

def pulse_index_to_start_t(j):
    return j * pulse_duration

def pulses_to_samps(pulses):
    samps = np.array([])
    for j, pulse in enumerate(pulses):
        start_t = pulse_index_to_start_t(j)
        end_t = start_t + pulse_duration
        if pulse == '1':
            segment = tone(start_t, end_t)
        else:
            segment = np.zeros(t_to_samp_index(end_t - start_t))
        samps = np.concatenate((samps, segment))
    return samps.astype(np.int16)

# =================
# EXECUTION
# =================
key = add_pulses_to_key(key)
pulses = msg_to_pulses(msg.strip().upper(), key)
samps = pulses_to_samps(pulses)
write("02_sound.wav", samp_rate, samps)

# Plot envelope
plt.figure(figsize=(10, 4))
plt.plot(np.linspace(0, len(samps)/samp_rate, len(samps)), samps)
plt.title("Transmitted sound envelope")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.tight_layout()
plt.savefig("03 Transmitted sound envelope.png")
plt.close()

# Plot zoomed-in waveform
zoom_start = t_to_samp_index(0.5)
zoom_end = t_to_samp_index(0.5 + 5/samp_rate)
plt.figure(figsize=(10, 4))
plt.plot(np.linspace(0, (zoom_end - zoom_start)/samp_rate, zoom_end - zoom_start), samps[zoom_start:zoom_end])
plt.title("Transmitted sound period")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.tight_layout()
plt.savefig("04 Transmitted sound period.png")
plt.close()
