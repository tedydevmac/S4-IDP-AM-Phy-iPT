import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# --- Load WAV file ---
file_path = "/Volumes/T9/tedgoh/S4-IDP-AM-Phy-iPT/06a_received_sound.wav"
rate, data = wavfile.read(file_path)

# --- Prepare signal data ---
if data.ndim > 1:
    data = data[:, 0]  # use 1st channel if stereo
time = np.arange(len(data)) / rate
signal = data / np.max(np.abs(data))  # normalize

# --- Plot full signal ---
plt.figure(figsize=(12, 4))
plt.plot(time, signal)
plt.title("08 Full Received Sound Signal")
plt.xlabel("Time (s)")
plt.ylabel("Signal (normalized)")
plt.grid(True)
plt.tight_layout()
plt.savefig("08_full_signal.png")
plt.show()

# --- Zoom in to examine one pulse (adjust these limits based on the graph above) ---
t_start = 0.50
t_end = 0.505
plt.figure(figsize=(10, 3))
plt.plot(time, signal)
plt.title("09a Received Sound Period")
plt.xlabel("Time (s)")
plt.ylabel("Signal (normalized)")
plt.xlim([t_start, t_end])
plt.ylim([-1.1, 1.1])
plt.grid(True)
plt.tight_layout()
plt.savefig("09a_received_sound_period.png")
plt.show()

# --- Extract region of interest for analysis ---
mask = (time > t_start) & (time < t_end)
t_zoom = time[mask]
y_zoom = signal[mask]

# --- Pick 2 points for amplitude and frequency measurement (update manually!) ---
# Example: Manually find two peaks in the signal from the zoomed graph
t1 = 0.50015  # time of peak 1
y1 = 0.0618    # signal at peak 1

t2 = 0.5045664  # time of peak 2
y2 = 0.0621    # signal at peak 2
# (x, y) = (0.50054422,  0.06180)
# --- Calculate amplitude and frequency ---
amplitude = round((y1 + y2) / 2, 2)
period = abs(t2 - t1)
frequency = round(1 / period)

# --- Print calculated values ---
print(f"Amplitude (A) ≈ {amplitude}")
print(f"Frequency (f) ≈ {frequency} Hz")
print(f"Period (T) ≈ {period:.6f} s")

# --- Plot with X marks and values ---
plt.figure(figsize=(10, 3))
plt.plot(t_zoom, y_zoom, label="Signal")
plt.plot(t1, y1, 'ro')
plt.text(t1, y1 + 0.05, f"X1 ({t1:.4f}, {y1})")
plt.plot(t2, y2, 'ro')
plt.text(t2, y2 + 0.05, f"X2 ({t2:.4f}, {y2})")
plt.title("09b Received Sound Period with Points")
plt.xlabel("Time (s)")
plt.ylabel("Signal (normalized)")
plt.grid(True)
plt.tight_layout()
plt.savefig("09b_received_points_labeled.png")
plt.show()

# --- Define sine wave model using results ---
def sound_wave_model(t, A, f, c, t0):
    return 0.0619*np.cos(2*np.pi*2538*(t - 0.50015))+ 0.00456

# --- Estimate vertical center (c) and phase alignment (t0) ---
c = 0
t0 = t1  # peak at t1
y_model = sound_wave_model(t_zoom, amplitude, frequency, c, t0)

# --- Overlay model on graph ---
plt.figure(figsize=(10, 3))
plt.plot(t_zoom, y_zoom, label="Signal")
plt.plot(t_zoom, y_model, '--', label="Sine Model")
plt.title("09c Received Sound with Model")
plt.xlabel("Time (s)")
plt.ylabel("Signal (normalized)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("09c_received_sound_period_model.png")
plt.show()