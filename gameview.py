# @copyright 한국기술교육대학교 컴퓨터공학부 객체지향개발론및실습
# @version 2021년도 2학기 
# @author 임지수
# @studentnumber 2017136106
# @file gameview.py
# View와 Controller가 결합되어 있는 형태
# 사용자에게 보여지는 부분과 사용자의 입력 처리

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QLabel, QRadioButton, QPushButton, QLineEdit
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer
from gamemodel import GameModel
from handtype import HandType, GameResult
import sys

class GameView(QMainWindow):
	def __init__(self):
		super().__init__()
		self.gamemodel = GameModel()

		self.gameStatus = QLineEdit()
		self.gameStatus.setReadOnly(True)
		self.gameStatus.setText('가위바위보로 누가 공격할지 결정하세요!!!')

		layout = QVBoxLayout()
		layout.addWidget(self.gameStatus)
		layout.addLayout(self.constructGamePaneView())
		layout.addLayout(self.constructButtonPaneView())

		centralWidget = QWidget()
		centralWidget.setLayout(layout)
		self.setCentralWidget(centralWidget)
		
		self.setWindowTitle('묵찌바 게임')
		self.show()
		self.setFixedSize(centralWidget.size())
	
	def newgame(self):
		self.userView.setPixmap(HandType.MOOK.getImage())
		self.computerView.setPixmap(HandType.MOOK.getImage())
		self.gameStatus.setText('가위바위보로 누가 공격할지 결정하세요!!!')
		self.gamemodel.init()
		self.selectButton.setDisabled(False)
		self.newgameButton.setDisabled(True)

	# 사용자가 선택 버튼(사용자 손을 선택한 후)을 눌렀을 때 실행되는 메소드
	def nextTurn(self):
		self.selectButton.setDisabled(True)
		self.gamemodel.getComputerNextHand()
		self.animateComputerHand()
	
	def finalizeComputerTurn(self):
		self.setComputerHandImage(self.gamemodel.computer.hand)
		if self.gamemodel.playingMookJiBa:
			self.playMookJiBa()
		else: self.playGawiBawiBo()
	
	def setComputerHandImage(self, hand):
		self.computerView.setPixmap(hand.getImage())

	def changeComputerHand(self):
		self.setComputerHandImage(HandType.valueOf(self.current))
		self.current = (self.current+1) % 3
		if self.current==0: self.timeout += 1
		if self.timeout==3: 
			self.handEffect.stop()
			self.finalizeComputerTurn()

	# 묵찌바가 순환적으로 표시되기 위한 코드
	def animateComputerHand(self):
		self.current = 0
		self.timeout = 0
		self.handEffect = QTimer()
		self.handEffect.setInterval(150)
		self.handEffect.timeout.connect(self.changeComputerHand)
		self.handEffect.start()

	# 사용자가 선택한 손과 컴퓨터가 선택한 손을 가지고 가위바위보를 진행
	def playGawiBawiBo(self):
		self.selectButton.setDisabled(False)							# 선택 버튼 비활성화
		gameresult = self.gamemodel.playGawiBawiBo()	# 가위바위보의 결과를 gameresult변수에 저장
		if gameresult==GameResult.USERWIN:								# USERWIN = 0, COMPUTERWIN = 1, DRAW = 2
			self.gameStatus.setText('사용자 승: 사용자 공격 차례')
		elif gameresult==GameResult.COMPUTERWIN:
			self.gameStatus.setText('컴퓨터 승: 컴퓨터 공격 차례')
		else: self.gameStatus.setText('비김: 가위바위보를 다시')

	# 사용자가 선택한 손과 컴퓨터가 선택한 손을 가지고 묵지빠를 진행
	def playMookJiBa(self):
		if self.gamemodel.playMookJiBa()==GameResult.DRAW:
			if self.gamemodel.isUserAttack:
				self.gameStatus.setText('사용자 공격 차례')
			else: self.gameStatus.setText('컴퓨터 공격 차례')
			self.selectButton.setDisabled(False)
		else:
			if self.gamemodel.isUserAttack:
				self.gameStatus.setText('사용자 승')
			else: self.gameStatus.setText('컴퓨터 승')
			self.selectButton.setDisabled(True)
			self.newgameButton.setDisabled(False)

	# 사용자가 선택한 손에 따라 이미지 변경 및 사용자 손 정보 변경
	def userSelected(self):
		selectedButton = self.sender()
		if selectedButton==self.mookButton:
			self.gamemodel.currUserHand = HandType.MOOK	
		elif selectedButton==self.jiButton:
			self.gamemodel.currUserHand = HandType.JI
		else:
			self.gamemodel.currUserHand = HandType.BA
		self.userView.setPixmap(self.gamemodel.currUserHand.getImage())

	def constructGamePaneView(self):
		gamePane = QGridLayout()
		gamePane.addWidget(QLabel("사용자"),0,0,Qt.AlignCenter)
		gamePane.addWidget(QLabel("컴퓨터"),0,1,Qt.AlignCenter)
		
		self.userView = QLabel()
		self.computerView = QLabel()
		self.userView.setPixmap(HandType.MOOK.getImage())
		self.computerView.setPixmap(HandType.MOOK.getImage())
		gamePane.addWidget(self.userView,1,0,Qt.AlignCenter)
		gamePane.addWidget(self.computerView,1,1,Qt.AlignCenter)
		return gamePane

	def constructButtonPaneView(self):
		buttonPane = QHBoxLayout()
		self.mookButton = QRadioButton('묵')
		self.jiButton = QRadioButton('찌')
		self.baButton = QRadioButton('바')
		self.mookButton.toggled.connect(self.userSelected)
		self.jiButton.toggled.connect(self.userSelected)
		self.baButton.toggled.connect(self.userSelected)
		self.newgameButton = QPushButton('새 게임')
		self.selectButton = QPushButton('선택')
		self.mookButton.setChecked(True)
		self.selectButton.clicked.connect(self.nextTurn)
		self.newgameButton.setDisabled(True)
		self.newgameButton.clicked.connect(self.newgame)

		buttonPane.addWidget(self.mookButton)
		buttonPane.addWidget(self.jiButton)
		buttonPane.addWidget(self.baButton)
		buttonPane.addWidget(self.selectButton)
		buttonPane.addWidget(self.newgameButton)	
		return buttonPane

def main():
	app = QApplication(sys.argv)
	view = GameView()
	sys.exit(app.exec())

main()