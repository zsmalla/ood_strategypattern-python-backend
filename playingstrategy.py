# @copyright 한국기술교육대학교 컴퓨터공학부 객체지향개발론및실습
# @version 2021년도 2학기 
# @author 김상진
# @file playingstrategy.py
# PlayingStrategy
# 전략패턴: 전략 interface
# RandomStrategy 
# 전략패턴: 구체적인 전략 클래스

from abc import ABC, abstractmethod
from handtype import HandType
import random

class PlayingStrategy(ABC):
	@abstractmethod
	def computeNextHand(self):
		pass

class RandomStrategy(PlayingStrategy):
	def computeNextHand(self):
		return HandType.valueOf(random.randint(0,2))

'''
def test():
	strategy = RandomStrategy()
	print(strategy.computeNextHand())
	print(strategy.computeNextHand())
'''