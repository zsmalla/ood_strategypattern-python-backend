# @copyright 한국기술교육대학교 컴퓨터공학부 객체지향개발론및실습
# @version 2021년도 2학기 
# @author 김상진
# @file GameModel.py
# 묵찌바 게임에 필요한 데이터를 유지하고 게임 로직 제공

from handtype import HandType, GameResult
from playingstrategy import PlayingStrategy, RandomStrategy
from computerplayer import ComputerPlayer
from handtype import HandType, GameResult

class GameModel:
	def __init__(self):
		# 전략을 바꾸고 싶으면
		self.computer = ComputerPlayer(RandomStrategy())
		self.currUserHand = HandType.MOOK
		self.playingMookJiBa = False
		self.isUserAttack = False

	# 새 게임을 할 때마다 객체를 생성하는 대신 사용 (상태 초기화)
	def init(self):
		self.playingMookJiBa = False
		self.isUserAttack = False

	# 다음 컴퓨터 손 계산함
	def getComputerNextHand(self):
		return self.computer.nextHand()

	# 묵찌바 게임 결과 판단
	def playMookJiBa(self):
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
