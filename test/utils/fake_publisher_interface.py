from domain.interfaces.publisher import Publisher


class FakePublisherInterface(Publisher):


    def send_message(self, message: dict, topic: str):
        pass