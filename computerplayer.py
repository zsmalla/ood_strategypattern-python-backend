# @copyright 한국기술교육대학교 컴퓨터공학부 객체지향개발론및실습
# @version 2021년도 2학기 
# @author 임지수
# @file computerplayer.py
# 묵찌바, 가위바위보에서 컴퓨터 역할을 하는 클래스
# 전략패턴: 전략을 활용하는 클라이언트 클래스

from handtype import HandType
import random

class ComputerPlayer():
	def __init__(self, strategy):
		self.setStrategy(strategy)
		# self.hand = HandType.MOOK		=> 기존 코드 수정 : 처음에 컴퓨터가 무조건 묵만 냄
		self.hand = HandType.valueOf(random.randint(0,2))
	# 관계 주입
	def setStrategy(self, strategy):
		self.strategy = strategy

	def nextHand(self, model):
		self.hand = self.strategy.computeNextHand(model)
		return self.hand
