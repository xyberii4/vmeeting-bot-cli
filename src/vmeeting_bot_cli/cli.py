import time
import threading
import click

from vmeeting_bot_cli.selenium_bot.google_meets import (
    Bot,
    audio_queue,
    audio_buffer,
    selenium_running,
)
from vmeeting_bot_cli.visualizer.visualizer import Visualizer
from vmeeting_bot_cli.livekit_streamer.lk_streamer import (
    LiveKitStreamer,
    livekit_running,
)


def quit(quit_event):
    while not quit_event.is_set():
        user_input = input()
        if user_input.lower() == "q":
            print("Quitting...")
            quit_event.set()
            selenium_running.clear()
            livekit_running.clear()


@click.command()
@click.argument("meeting_link", type=str)
@click.option(
    "--visualizer", is_flag=True, default=False, help="Enables audio visualizer."
)
def main(meeting_link, visualizer):
    bot = Bot(meeting_link)
    lks = LiveKitStreamer(audio_queue)

    quit_event = threading.Event()
    quit_thread = threading.Thread(target=quit, args=(quit_event,))
    quit_thread.daemon = True
    quit_thread.start()

    # start bot
    selenium_thread = threading.Thread(target=bot.execute)
    selenium_thread.daemon = True
    selenium_thread.start()

    time.sleep(2)

    # Start LiveKit streamer
    livekit_thread = threading.Thread(target=lks.execute)
    livekit_thread.daemon = True
    livekit_thread.start()

    time.sleep(3)
    try:
        if visualizer:
            # looks cool
            vl = Visualizer(audio_buffer)

            vl.show()

        print("Press 'q' and Enter to exit.")
        while not quit_event.is_set():
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt. Quitting...")
        quit_event.set()
    finally:
        # cleanup
        selenium_running.clear()
        livekit_running.clear()
        quit_event.clear()

        if selenium_thread and selenium_thread.is_alive():
            print("Waiting for bot to shutdown...")
            selenium_thread.join(timeout=5)

        if livekit_thread and livekit_thread.is_alive():
            livekit_thread.join(timeout=5)


if __name__ == "__main__":
    main()
