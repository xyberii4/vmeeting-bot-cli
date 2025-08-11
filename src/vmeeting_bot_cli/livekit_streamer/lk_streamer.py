from vmeeting_bot_cli.config import (
    LIVEKIT_URL,
    LIVEKIT_ROOM,
    LIVEKIT_PARTICIPANT_ID,
    LIVEKIT_PARTICIPANT_NAME,
    LIVEKIT_TOKEN,
    SAMPLE_RATE,
    FRAME_DURATION,
)

from livekit import rtc
from livekit.rtc import AudioFrame
import threading
import queue
import numpy as np
import asyncio

livekit_running = threading.Event()
livekit_running.set()


class LiveKitStreamer:
    def __init__(self, audio_queue: queue.Queue):
        self.url = LIVEKIT_URL
        self.room_name = LIVEKIT_ROOM
        self.participant_id = LIVEKIT_PARTICIPANT_ID
        self.participant_name = LIVEKIT_PARTICIPANT_NAME
        self.token = LIVEKIT_TOKEN

        self.sample_rate = SAMPLE_RATE
        self.frame_duration = FRAME_DURATION
        self.samples_per_frame = int(self.sample_rate * self.frame_duration)

        self.audio_queue = audio_queue
        self.room = None
        self.audio_source = None

    async def connect(self):
        try:
            print("Connecting to LiveKit...")
            self.room = rtc.Room()
            self.audio_source = rtc.AudioSource(self.sample_rate, 1)

            await self.room.connect(url=self.url, token=self.token)

            track = rtc.LocalAudioTrack.create_audio_track(
                "meeting_audio", self.audio_source
            )
            options = rtc.TrackPublishOptions()
            options.source = rtc.TrackSource.SOURCE_MICROPHONE
            await self.room.local_participant.publish_track(track, options)
            print("Connected to LiveKit. Streaming audio...")

            await asyncio.sleep(1)

            await self._stream_audio()

        except Exception as e:
            raise RuntimeError(f"Failed to connect to LiveKit: {e}")
        finally:
            print("Disconnecting from LiveKit...")
            await self.room.disconnect()

    async def _stream_audio(self):
        while livekit_running.is_set():
            try:
                audio_data = self.audio_queue.get_nowait()

                for i in range(0, len(audio_data), self.samples_per_frame):
                    if not livekit_running.is_set():
                        break

                    # get next audio chunk
                    chunk = audio_data[i : i + self.samples_per_frame]
                    if len(chunk) < self.samples_per_frame:
                        # pad with zeros to maintain frame size
                        chunk = np.pad(
                            chunk,
                            (0, self.samples_per_frame - len(chunk)),
                            "constant",
                        )
                    # clamp the values to the range [-1.0, 1.0] and convert to int16
                    clamped = np.clip(chunk, -1.0, 1.0)
                    int16_chunk = (clamped * 32767).astype(np.int16)

                    frame = AudioFrame(
                        int16_chunk.tobytes(),
                        self.sample_rate,
                        1,
                        self.samples_per_frame,
                    )

                    await self.audio_source.capture_frame(frame)

                    await asyncio.sleep(0.001)

            except queue.Empty:
                await asyncio.sleep(0.01)
            except Exception as e:
                raise RuntimeError(f"Failed to stream audio: {e}")

    def execute(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.connect())
        except Exception as e:
            raise RuntimeError(f"LiveKit streaming failed: {e}")
        finally:
            loop.close()
