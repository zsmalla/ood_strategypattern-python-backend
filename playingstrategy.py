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
		if model.lastUserHand or model.playingMookJiBa:
			if model.lastUserHand == HandType.MOOK:		# 컴퓨터 공격일 때와 수비일 때의 확률이 다름 => LastHandBased전략에 의거, 컴퓨터가 유리한 쪽으로
				return HandType.valueOf(random.choices(range(0, 3), weights=[2, 1, 1] if model.isUserAttack else [1, 2, 2])[0])
			elif model.lastUserHand == HandType.JI:
				return HandType.valueOf(random.choices(range(0, 3), weights=[1, 2, 1] if model.isUserAttack else [2, 1, 2])[0])
			else:
				return HandType.valueOf(random.choices(range(0, 3), weights=[1, 1, 2] if model.isUserAttack else [2, 2, 1])[0])
		else:
			return HandType.valueOf(random.randint(0,2))

"""
UserAnalyzeStrategy 전략 설명
게임이 길어지면 사용자는 자주 내는 손을 더 내는 경향이 높을 것이라 가정한 전략
새로운 게임 시작 후 종료 시까지 유저의 사용한 손의 데이터를 저장하여
랜덤 전략을 기반으로 하되 묵 찌 빠의 확률을 지금까지 유저가 낸 손의 데이터를 기반으로 결정
추가 확률을 부여하는 방식은 random 모듈 choices메소드의 weight 인자를 통한 가중치를 부여하는 방식
1) 가위바위보에서는 사용자가 묵의 비율이 높으면 빠의 가중치를 높이는 방식
2) 묵찌빠에서는 컴퓨터 공격시 사용자가 묵의 비율이 높으면 묵의 가중치를 높이는 방식, 컴퓨터 수비시 사용자가 묵의 비율이 높으면 묵의 가중치를 줄이는 방식

GameModel클래스의 isUserAttack, playingMookJiBa, 새로 정의한 userdata 정보 필요
이후의 전략 유지 보수 측면과 많은 정보(매개변수)가 필요하다는 측면에서 각각의 data가 아닌 GameModel객체 자체를 받아와 활용하는 것이
더 효율적이라 판단

추가적으로 정의한 data_analyze 메소드는 가위바위보, 묵찌빠(공/수) 별로 다른 weight를 계산하기 위한 메소드
"""

class UserAnalyzeStrategy(PlayingStrategy):
	def computeNextHand(self, model):
		hand = HandType.valueOf(random.choices(range(0, 3), weights=self.data_analyze(model))[0])
		for i in range(3):
			if model.currUserHand == HandType.valueOf(i) and model.userdata[i] < 10 : model.userdata[i] += 1
		return hand
	def data_analyze(self, model) -> list:
		if model.playingMookJiBa:
			return [10-model.userdata[0], 10-model.userdata[1], 10-model.userdata[2]] if model.isUserAttack else model.userdata
		else:
			return [model.userdata[2], model.userdata[0], model.userdata[1]]


if __name__ == '__main__':		# 테스트 코드
	array = [1, 2, 3]
	for _ in range(10) : print(random.choices(array, weights=[1, 0, 1]))
	print(type(random.choices(array, weights=[5, 5, 5])[0]))
