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
	def playMookJiBa(self, userhand):
		self.currUserHand = userhand
		if self.currUserHand == HandType.MOOK:
			if self.computer.hand == HandType.JI:
				self.isUserAttack = True
				return GameResult.DRAW
			elif self.computer.hand == HandType.BA:
				self.isUserAttack = False
				return GameResult.DRAW
			else:
				return GameResult.USERWIN if self.isUserAttack else GameResult.COMPUTERWIN
		elif self.currUserHand == HandType.JI:
			if self.computer.hand == HandType.BA:
				self.isUserAttack = True
				return GameResult.DRAW
			elif self.computer.hand == HandType.MOOK:
				self.isUserAttack = False
				return GameResult.DRAW
			else:
				return GameResult.USERWIN if self.isUserAttack else GameResult.COMPUTERWIN
		else:
			if self.computer.hand == HandType.MOOK:
				self.isUserAttack = True
				return GameResult.DRAW
			elif self.computer.hand == HandType.JI:
				self.isUserAttack = False
				return GameResult.DRAW
			else:
				return GameResult.USERWIN if self.isUserAttack else GameResult.COMPUTERWIN

	# 가위바위보 게임 결과 판단
	def playGawiBawiBo(self, userhand):		# userhand 정보가 들어오면 어떻게 처리?
		self.currUserHand = userhand
		if self.currUserHand == HandType.MOOK:
			if self.computer.hand == HandType.MOOK :
				return GameResult.DRAW		# 비김
			elif self.computer.hand == HandType.JI :
				self.playingMookJiBa, self.isUserAttack = True, True
				return GameResult.USERWIN		# 이김
			else :
				self.playingMookJiBa, self.isUserAttack = True, False
				return GameResult.COMPUTERWIN							# 짐
		elif self.currUserHand == HandType.JI:
			if self.computer.hand == HandType.MOOK :
				self.playingMookJiBa, self.isUserAttack = True, False
				return GameResult.COMPUTERWIN
			elif self.computer.hand == HandType.JI :
				return GameResult.DRAW
			else :
				self.playingMookJiBa, self.isUserAttack = True, True
				return GameResult.USERWIN
		else:
			if self.computer.hand == HandType.MOOK :
				self.playingMookJiBa, self.isUserAttack = True, True
				return GameResult.USERWIN
			elif self.computer.hand == HandType.JI :
				self.playingMookJiBa, self.isUserAttack = True, False
				return GameResult.COMPUTERWIN
			else :
				return GameResult.DRAW
