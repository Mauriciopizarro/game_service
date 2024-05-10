from threading import Thread
from infrastructure.event_managers.consumers.create_game_consumer import CreateGameListener
import time


def start_consumer():
    time.sleep(5)
    Thread(target=CreateGameListener).start()


if __name__ == "__main__":
    start_consumer()
