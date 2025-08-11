# Virtual Meeting Bot

CLI tool that creates a bot that joins meetings and streams audio to LiveKit. Currently only supports Google Meet.

## Installation

First ensure these are installed:

- Python 3.10+
- uv
- Chrome

1. Clone the repo and activate virtual environment.

```bash
git clone https://github.com/xyberii4/vmeeting-bot-cli.git && cd vmeeting-bot-cli
uv venv
source .venv/bin/activate #Windows: .venv\Scripts\activate

```

3. Install dependencies

```bash
uv pip install -r requirements.txt
```

4. Install the CLI

```bash
uv tool install .
```

## Usage

1. Make sure you have a LiveKit server running and have the URL, API key, and API secret.
2. Customize `.env` and `config.yaml` file with your own values by using the templates provided.

```bash
cp .env.example .env
cp config.yaml.example config.yaml
```

- `LIVEKIT_PARTICIPANT_ID` and `LIVEKIT_PARTICIPANT_NAME` should be a unique string for each bot instance.
- `LIVEKIT_ROOM` can be anything, and will be automatically created if it doesn't exist.

3. Run the bot within the virtual environment.

```bash
uv run vmb-cli --visualizer <MEETS_URL>
```

- \<MEETS_URL> - The meeting URL
- --visualizer - optional flag to enable the visualizer. Looks cool.
