class GameFinishedError(Exception):
    pass


class GamePendingBetError(Exception):
    pass


class InvalidBetAmountException(Exception):
    pass


class GameStartedImpossibleBet(Exception):
    pass


class IncorrectGameID(Exception):
    pass


class UserExistent(Exception):
    pass


class NotExistentUser(Exception):
    pass


class IncorrectObjectID(Exception):
    pass


class EmptyHistory(Exception):
    pass


class EmptyPlayersList(Exception):
    pass
