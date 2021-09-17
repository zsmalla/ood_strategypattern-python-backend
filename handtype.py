# @copyright 한국기술교육대학교 컴퓨터공학부 객체지향개발론및실습
# @version 2021년도 2학기 
# @author 김상진
# @file handtype.py
# HandType 열거형: 가위바위보, 묵찌바 개임의 손 모습 
# GameResult 열거형: 묵찌바, 가위바위보 게임 결과 
# 묵찌바에서 공격실패는 DRAW로 나타냄

from enum import Enum
from PyQt5.QtGui import QPixmap

class HandType(Enum):
	MOOK=(0, "주먹.jpeg")
	JI=(1, "가위.jpeg")
	BA=(2, "보.jpeg")

	def __init__(self, value, imagesrc):
		self._value = value
		self.imagesrc = imagesrc

	def winValueOf(self) -> 'HandType':
		if self==HandType.MOOK: return HandType.BA
		elif self==HandType.JI: return HandType.MOOK
		else: return HandType.JI

	def getImage(self):
		return QPixmap(self.imagesrc)

	@classmethod
	def valueOf(cls, index: int) -> 'HandType':
		if index==0: return HandType.MOOK
		elif index==1: return HandType.JI
		else: return HandType.BA

class GameResult(Enum):
	USERWIN=0
	COMPUTERWIN=1
	DRAW=2


# def test():
# 	x = HandType.MOOK
# 	print(x)
# 	print(x.winValueOf())
# 	print(HandType.valueOf(0))
#
# test()