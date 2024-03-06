from threading import Thread
from infrastructure.event_managers.consumers.create_game_consumer import CreateGameListener


def start_consumer():
    Thread(target=CreateGameListener).start()


if __name__ == "__main__":
    start_consumer()
