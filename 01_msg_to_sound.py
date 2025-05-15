# Same structure as original
import numpy as np
import wave
import matplotlib.pyplot as plt

FREQUENCY = 1760 // 2  # Halved frequency
AMPLITUDE = 32767
DURATION_UNIT = 0.1
SAMPLE_RATE = 44100

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..',
    'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    ' ': ' '  # for word space
}  # (same dictionary as before)
MESSAGE = "  ethan goon  "   # Replace with your group message

def text_to_morse(message):
    return [MORSE_CODE_DICT.get(c, '') if c != ' ' else ' ' for c in message.upper()]

def morse_to_wave(morse_sequence):
    signal = np.array([], dtype=np.int16)

    def append_tone(duration_sec):
        t = np.linspace(0, duration_sec, int(SAMPLE_RATE * duration_sec), False)
        tone = AMPLITUDE * np.sin(2 * np.pi * FREQUENCY * t)
        return tone.astype(np.int16)

    def append_silence(duration_sec):
        return np.zeros(int(SAMPLE_RATE * duration_sec), dtype=np.int16)

    for symbol in morse_sequence:
        if symbol == ' ':
            signal = np.concatenate((signal, append_silence(7 * DURATION_UNIT)))
        else:
            for i, s in enumerate(symbol):
                if s == '.':
                    signal = np.concatenate((signal, append_tone(DURATION_UNIT)))
                elif s == '-':
                    signal = np.concatenate((signal, append_tone(3 * DURATION_UNIT)))
                if i < len(symbol) - 1:
                    signal = np.concatenate((signal, append_silence(DURATION_UNIT)))
            signal = np.concatenate((signal, append_silence(3 * DURATION_UNIT)))
    return signal

morse_sequence = text_to_morse(MESSAGE)
waveform = morse_to_wave(morse_sequence)

with wave.open('02_sound_half_freq.wav', 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(waveform.tobytes())

# Plot
t = np.linspace(0, len(waveform)/SAMPLE_RATE, len(waveform))
plt.plot(t, waveform)
plt.title("Frequency Halved – Sound Envelope")
plt.xlabel("Time (s)")
plt.ylabel("Signal")
plt.grid(True)
plt.savefig("04 Received sound period - half freq.png")
plt.show()