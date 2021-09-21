# @copyright 한국기술교육대학교 컴퓨터공학부 객체지향개발론및실습
# @version 2021년도 2학기 
# @author 임지수
# @studentnumber 2017136106
# @file playingstrategy.py
# PlayingStrategy
# 전략패턴: 전략 interface

from abc import ABC, abstractmethod
from handtype import HandType
import random


class PlayingStrategy(ABC):
	@abstractmethod
	def computeNextHand(self):
		pass

class RandomStrategy(PlayingStrategy):
	def computeNextHand(self, model):
		return HandType.valueOf(random.randint(0,2))

"""
LastHandBasedStrategy 전략
랜덤 전략에서 추가적으로 lastUserHand(직전 사용자의 손) 정보 필요, 이 정보는 해당 전략에서만 필요하다고 판단했기 때문에 해당 클래스 변수로 정의
또한 묵찌빠에서의 전략이기 때문에 가위바위보/묵찌빠 정보, 사용자의 공/수 정보 필요
이후에도 많은 매개변수가 필요할 수 있기 때문에 새로 재정의한 computeNextHand에서는 객체를 전달받기로 함

의사 난수 생성 -> random 모듈의 choices 메소드 사용, weight 인자에서 가중치를 조절함으로서 확률 조정
"""

class LastHandBasedStrategy(PlayingStrategy):
	def __init__(self):
		self.lastUserHand = None

	def computeNextHand(self, model):					# 객체를 전달 => 이후 전략이나 기능 추가 위해 모델 객체에 변수나 메소드를 추가해도 이 함수는 수정 불필요!
		if self.lastUserHand or model.playingMookJiBa:
			if self.lastUserHand == HandType.MOOK:		# 컴퓨터 공격일 때와 수비일 때의 확률이 다름 => LastHandBased전략에 의거, 컴퓨터가 유리한 쪽으로
				hand = HandType.valueOf(random.choices(range(0, 3), weights=[2, 1, 1] if model.isUserAttack else [1, 2, 2])[0])		# random.choices()의 반환타입은 list
			elif self.lastUserHand == HandType.JI:
				hand = HandType.valueOf(random.choices(range(0, 3), weights=[1, 2, 1] if model.isUserAttack else [2, 1, 2])[0])
			else:
				hand = HandType.valueOf(random.choices(range(0, 3), weights=[1, 1, 2] if model.isUserAttack else [2, 2, 1])[0])
		else:	# 가위바위보, 첫 묵찌빠 => RandomStrategy
			hand = HandType.valueOf(random.randint(0,2))
		self.lastUserHand = hand
		return hand

"""
UserAnalyzeStrategy 전략 설명
게임이 길어지면 사용자는 자주 내는 손을 더 내는 경향이 높을 것이라 가정한 전략
새로운 게임 시작 후 종료 시까지 유저의 사용한 손의 데이터를 저장하여
랜덤 전략을 기반으로 하되 묵 찌 빠의 확률을 지금까지 유저가 낸 손의 데이터를 기반으로 결정
추가 확률을 부여하는 방식은 random 모듈 choices메소드의 weight 인자를 통한 가중치를 부여하는 방식
1) 가위바위보에서는 사용자가 묵의 비율이 높으면 빠의 가중치를 높이는 방식
2) 묵찌빠에서는 컴퓨터 공격시 사용자가 묵의 비율이 높으면 묵의 가중치를 높이는 방식, 컴퓨터 수비시 사용자가 묵의 비율이 높으면 묵의 가중치를 줄이는 방식

GameModel클래스의 isUserAttack, playingMookJiBa, 새로 정의한 userdata 정보 필요
userdata 정보는 해당 전략에서만 필요할 것으로 판단했기 때문에 해당 클래스 변수로 정의
이후의 전략 유지 보수 측면과 많은 정보(매개변수)가 필요하다는 측면에서 각각의 data가 아닌 GameModel객체 자체를 받아와 활용하는 것이
더 효율적이라 판단

추가적으로 정의한 data_analyze 메소드는 가위바위보, 묵찌빠(공/수) 별로 다른 weight를 계산하기 위한 메소드
부여 가능한 가중치의 범위는 0 ~ 10, 이를 벗어나면 추가적으로 가중치를 부여하거나 감소시키지 않음
"""

class UserAnalyzeStrategy(PlayingStrategy):
	def __init__(self):
		self.userdata = [5, 5, 5] # default weight = 5 : 5 : 5

	def computeNextHand(self, model):		# 객체를 전달받음
		hand = HandType.valueOf(random.choices(range(0, 3), weights=self.data_analyze(model))[0])
		for i in range(3):			# 가중치 업데이트
			if model.currUserHand == HandType.valueOf(i) and self.userdata[i] < 10 : self.userdata[i] += 1	# 가중치 범위 제한
		return hand

	def data_analyze(self, model) -> list:		# weight 계산, 반환
		if model.playingMookJiBa:				# 묵찌빠의 경우
			return [10-self.userdata[0], 10-self.userdata[1], 10-self.userdata[2]] if model.isUserAttack else self.userdata	# 공수 별도 가중치 반환
		else:		# 가위바위보의 경우
			return [self.userdata[1], self.userdata[2], self.userdata[0]]	# 사용자가 묵 많이 냄 -> 컴퓨터 빠의 가중치 ↑


if __name__ == '__main__':		# 테스트 코드
	array = [1, 2, 3]
	for _ in range(10) : print(random.choices(array, weights=[1, 0, 1]))
	print(type(random.choices(array, weights=[5, 5, 5])[0]))
