# @copyright 한국기술교육대학교 컴퓨터공학부 객체지향개발론및실습
# @version 2021년도 2학기 
# @author 임지수
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

class LastHandBasedStrategy(PlayingStrategy):
	def computeNextHand(self, model):
		if model.lastUserHand:
			if model.lastUserHand == HandType.MOOK:
				return HandType.valueOf(random.choices(range(0, 3), weights=[2, 1, 1] if model.isUserAttack else [1, 2, 2]))
			elif model.lastUserHand == HandType.JI:
				return HandType.valueOf(random.choices(range(0, 3), weights=[1, 2, 1] if model.isUserAttack else [2, 1, 2]))
			else:
				return HandType.valueOf(random.choices(range(0, 3), weights=[1, 1, 2] if model.isUserAttack else [2, 2, 1]))
		else:
			return HandType.valueOf(random.randint(0,2))

		# if lastUserHand == HandType.MOOK:
		# 	return HandType.valueOf(random.choices(range(0, 3), weights=[1,2,2]))
		# elif lastUserHand == HandType.JI:
		# 	return HandType.valueOf(random.choices(range(0, 3), weights=[2,1,2]))
		# else:
		# 	return HandType.valueOf(random.choices(range(0, 3), weights=[2,2,1]))




if __name__ == '__main__':
	strategy = RandomStrategy()
	for _ in range(10):
		print(strategy.computeNextHand())
		# print(LastHandBasedStrategy.computeNextHand())

