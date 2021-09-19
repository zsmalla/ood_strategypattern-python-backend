# @copyright 한국기술교육대학교 컴퓨터공학부 객체지향개발론및실습
# @version 2021년도 2학기 
# @author 임지수
# @studentnumber 2017136106
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
	def computeNextHand(self, model):		# self를 전달 => 이후 전략이나 기능 추가 위해 모델 객체에 변수나 메소드를 추가해도 이 함수는 수정 불필요!
		if model.lastUserHand:
			if model.lastUserHand == HandType.MOOK:		# 컴퓨터 공격일 때와 수비일 때의 확률이 다름 => LastHandBased전략에 의거, 컴퓨터가 유리한 쪽으로
				return HandType.valueOf(random.choices(range(0, 3), weights=[2, 1, 1] if model.isUserAttack else [1, 2, 2]))
			elif model.lastUserHand == HandType.JI:
				return HandType.valueOf(random.choices(range(0, 3), weights=[1, 2, 1] if model.isUserAttack else [2, 1, 2]))
			else:
				return HandType.valueOf(random.choices(range(0, 3), weights=[1, 1, 2] if model.isUserAttack else [2, 2, 1]))
		else:
			return HandType.valueOf(random.randint(0,2))

if __name__ == '__main__':		# 테스트 코드
	strategy = RandomStrategy()
	for _ in range(10):
		print(strategy.computeNextHand())

