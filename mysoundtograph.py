import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav

# Load the WAV file
sample_rate, data = wav.read("/Volumes/T9/tedgoh/S4-IDP-AM-Phy-iPT/02_sound.wav")

# If stereo, convert to mono
if len(data.shape) == 2:
    data = data.mean(axis=1)

# Time axis
time = np.linspace(0, len(data) / sample_rate, num=len(data))

# --- Zoom into an on-pulse segment ---
# Manually adjust the time window to zoom into a short pulse (~0.1 s duration)
start_time = 1.40   # adjust this to where an on-pulse is in your signal
end_time = 1.41     # start_time + pulse_duration (e.g., 0.1s)

# Create mask for time window
mask = (time >= start_time) & (time <= end_time)

# Plot the zoomed-in pulse
plt.figure(figsize=(10, 4))
plt.plot(time[mask], data[mask])
plt.xlabel("Time (s)")
plt.ylabel("Signal (arbitrary units)")
plt.title("Zoom into an On-Pulse Segment")
plt.grid(True)

# Set axis limits
plt.xlim(start_time, end_time)
plt.ylim(data[mask].min() * 1.1, data[mask].max() * 1.1)  # Add some padding
plt.tight_layout()

# Save the plot
plt.savefig("04 Received sound period.png", dpi=300)
plt.show()