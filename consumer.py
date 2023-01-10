import time
from threading import Thread
import infrastructure.injector # no remove this dependecy
from infrastructure.event_managers.create_game_listener import CreateGameListener


def start_consumer():
    time.sleep(15)
    Thread(target=CreateGameListener).start()


if __name__ == "__main__":
    start_consumer()
