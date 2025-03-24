import wave
import struct
import numpy as np

# Morse code dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', ', ': '--..--', '.': '.-.-.-',
    '?': '..--..', '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-', ' ': '/'
}

def encode_to_morse(message):
    return ' '.join(MORSE_CODE_DICT.get(char.upper(), '') for char in message)

def decode_from_morse(morse_code):
    reverse_dict = {v: k for k, v in MORSE_CODE_DICT.items()}
    return ''.join(reverse_dict.get(code, '') for code in morse_code.split())

def generate_morse_wav(morse_code, filename='morse_code.wav', framerate=44100):
    dot_duration = 0.1  # seconds
    dash_duration = 0.3  # seconds
    space_duration = 0.1  # seconds

    amplitude = 32767  # max amplitude for 16-bit audio
    frequency = 800  # frequency in Hz

    def generate_tone(duration):
        t = np.linspace(0, duration, int(framerate * duration), False)
        tone = amplitude * np.sin(2 * np.pi * frequency * t)
        return tone

    dot = generate_tone(dot_duration)
    dash = generate_tone(dash_duration)
    space = np.zeros(int(framerate * space_duration))

    signal = []

    for char in morse_code:
        if char == '.':
            signal.extend(dot)
        elif char == '-':
            signal.extend(dash)
        else:
            signal.extend(space)
        signal.extend(space)  # space between parts of the same letter

    signal = np.array(signal, dtype=np.int16)

    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)  # 2 bytes for 16-bit audio
        wav_file.setframerate(framerate)
        wav_file.writeframes(signal.tobytes())

if __name__ == '__main__':
    message = input("Enter the message to encode: ")
    morse_code = encode_to_morse(message)
    print(f"Morse Code: {morse_code}")

    generate_morse_wav(morse_code)

    decoded_message = decode_from_morse(morse_code)
    print(f"Decoded Message: {decoded_message}")
