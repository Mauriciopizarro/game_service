class FakeWalletServiceHttpClient:

    def __init__(self):
        self.calls = []

    def set_money(self, user_id: str, amount):
        self.calls.append({"user_id": user_id, "amount": amount})