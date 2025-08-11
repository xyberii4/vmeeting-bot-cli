from dotenv import load_dotenv
import yaml
from livekit import api
import os


# generate livekit token
def get_livekit_token(
    api_key: str,
    api_secret: str,
    room_name: str,
    participant_id: str,
    participant_name: str,
):
    token = (
        api.AccessToken(api_key, api_secret)
        .with_identity(participant_id)
        .with_name(participant_name)
        .with_grants(api.VideoGrants(room_join=True, room=room_name))
    )
    return token.to_jwt()


load_dotenv()

with open("config.yaml", "r") as f:
    yaml_config = yaml.safe_load(f)

# LiveKit configuration
LIVEKIT_API_KEY = os.environ.get("LIVEKIT_API_KEY", "")
LIVEKIT_API_SECRET = os.environ.get("LIVEKIT_API_SECRET", "")
LIVEKIT_URL = os.environ.get("LIVEKIT_URL", "")
LIVEKIT_ROOM = os.environ.get("LIVEKIT_ROOM", "")
LIVEKIT_PARTICIPANT_ID = os.environ.get("LIVEKIT_PARTICIPANT_ID", "")
LIVEKIT_PARTICIPANT_NAME = os.environ.get("LIVEKIT_PARTICIPANT_NAME", "")
LIVEKIT_TOKEN = get_livekit_token(
    LIVEKIT_API_KEY,
    LIVEKIT_API_SECRET,
    LIVEKIT_ROOM,
    LIVEKIT_PARTICIPANT_ID,
    LIVEKIT_PARTICIPANT_NAME,
)

# audio configuration
MAX_SAMPLES = yaml_config.get("audio_visualizer", {}).get("max_samples", 96000)
SAMPLE_RATE = yaml_config.get("audio_visualizer", {}).get("sample_rate", 48000)
FRAME_DURATION = yaml_config.get("audio_visualizer", {}).get(
    "frame_duration", 0.01
)  # in seconds

# bot configuration
BROWSER_EXECUTABLE = yaml_config.get("selenium_bot", {}).get(
    "browser_executable", "/usr/bin/chromium"
)
DRIVER_EXECUTABLE = yaml_config.get("selenium_bot", {}).get(
    "driver_executable", "/usr/bin/chromedriver"
)
BOT_NAME = yaml_config.get("selenium_bot", {}).get("name", "Bot")
WAIT_TIME = yaml_config.get("selenium_bot", {}).get(
    "wait_time", 30
)  # time to wait to be let in the meeting, in secs
