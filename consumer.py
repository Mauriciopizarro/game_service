import time
import infrastructure.injector # no remove this dependecy
from infrastructure.event_managers.create_game_listener import CreateGameListener


def start_consumer():
    time.sleep(15)
    create_game_listener = CreateGameListener()
    create_game_listener.start_consuming()


if __name__ == "__main__":
    start_consumer()
