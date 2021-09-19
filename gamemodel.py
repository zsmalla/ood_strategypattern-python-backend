# @copyright 한국기술교육대학교 컴퓨터공학부 객체지향개발론및실습
# @version 2021년도 2학기 
# @author 임지수
# @studentnumber 2017136106
# @file GameModel.py
# 묵찌바 게임에 필요한 데이터를 유지하고 게임 로직 제공

from handtype import HandType, GameResult
from playingstrategy import *
from computerplayer import ComputerPlayer
from handtype import HandType, GameResult
import random


class GameModel:
	def __init__(self):
		# 전략을 바꾸고 싶으면
		# self.computer = ComputerPlayer(RandomStrategy())
		# self.computer = ComputerPlayer(LastHandBasedStrategy())
		self.computer = ComputerPlayer(UserAnalyzeStrategy())
		self.currUserHand = HandType.MOOK
		self.playingMookJiBa = False
		self.isUserAttack = False
		self.lastUserHand = None
		self.userdata = [5, 5, 5]		# default weight 5 : 5 : 5

	# 새 게임을 할 때마다 객체를 생성하는 대신 사용 (상태 초기화)
	def init(self):
		self.playingMookJiBa = False
		self.isUserAttack = False
		self.lastUserHand = None
		self.userdata = [5, 5, 5]

	# 다음 컴퓨터 손 계산함
	def getComputerNextHand(self):		# 가위바위보 -> RandomStarategy / 묵찌빠 -> LastHandBasedStrategy
		return self.computer.nextHand(self) # 매개로 self 전달

	# 묵찌바 게임 결과 판단
	def playMookJiBa(self):
		self.lastUserHand = self.currUserHand
		if self.currUserHand == self.computer.hand:
			return GameResult.USERWIN if self.isUserAttack else GameResult.COMPUTERWIN
		else:
			self.isUserAttack = self.computer.hand.winValueOf() == self.currUserHand
			return GameResult.DRAW

	# 가위바위보 게임 결과 판단, winValueOf() 반환값 ==> handtype.묵or찌or빠
	def playGawiBawiBo(self):
		if self.currUserHand == self.computer.hand : return GameResult.DRAW
		else:
			self.isUserAttack = self.computer.hand.winValueOf() == self.currUserHand
			self.playingMookJiBa = True
			return GameResult.USERWIN if self.isUserAttack else GameResult.COMPUTERWIN


if __name__ == '__main__': # 테스트 코드
	model = GameModel()
	# for _ in range(5) : print(model.getComputerNextHand())
	for _ in range(10) : print(HandType.valueOf(random.randint(0, 2)))