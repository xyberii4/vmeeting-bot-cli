from vmeeting_bot_cli.config import SAMPLE_RATE, MAX_SAMPLES

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import Deque


class Visualizer:
    def __init__(self, audio_buffer: Deque):
        self.max_samples = MAX_SAMPLES
        self.sample_rate = SAMPLE_RATE

        self.fig = None
        self.ax = None
        self.line = None
        self.ani = None

        self.audio_buffer = audio_buffer

        self._setup()

    def _setup(self):
        plt.ioff()

        print("Setting up audio visualizer...")
        self.fig, self.ax = plt.subplots(figsize=(12, 6))

        (self.line,) = self.ax.plot(
            np.arange(self.max_samples) / self.sample_rate,
            self.audio_buffer,
            color="blue",
            linewidth=0.8,
        )

        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        self.ax.set_ylim(-1.0, 1.0)
        self.ax.grid(True, alpha=0.3)
        plt.tight_layout()

        self.fig.canvas.mpl_connect("key_press_event", self.on_key_press)
        self.fig.canvas.mpl_connect("close_event", self.on_close)

        # animation
        self.ani = animation.FuncAnimation(
            self.fig, self.update_plot, interval=50, blit=True, cache_frame_data=False
        )
        print("Visualizer setup complete. Press 'q' to quit.")

    def update_plot(self, frame):
        self.line.set_ydata(self.audio_buffer)
        return (self.line,)

    def on_key_press(self, event):
        if event.key == "q":
            plt.close("all")

    def on_close(self, event):
        print("Plot window closed. Exiting...")

    def show(self):
        plt.show()
