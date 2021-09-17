from abc import ABC, abstractmethod
from handtype import HandType, GameResult

class IUserHand(ABC):
    @abstractmethod
    def judge(self):
        pass

class User_MOOK(IUserHand):
    def judge(self, comHand):
        if comHand == HandType.MOOK:
            return GameResult.DRAW
        elif comHand == HandType.JI:
            return GameResult.USERWIN
        else : return GameResult.COMPUTERWIN

class User_JI(IUserHand):
    def judge(self, comHand):
        if comHand == HandType.MOOK:
            return GameResult.COMPUTERWIN
        elif comHand == HandType.JI:
            return GameResult.DRAW
        else : return GameResult.USERWIN

class User_BA(IUserHand):
    def judge(self, comHand):
        if comHand == HandType.MOOK:
            return GameResult.USERWIN
        elif comHand == HandType.JI:
            return GameResult.COMPUTERWIN
        else:
            return GameResult.DRAW
