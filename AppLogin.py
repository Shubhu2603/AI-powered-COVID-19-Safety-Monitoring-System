from PyQt5 import QtWidgets, QtSql, QtCore, uic, QtGui
from PyQt5.QtCore import QPoint, Qt, pyqtSignal, pyqtSlot, Qt, QThread, QSize
from PyQt5.QtGui import QPixmap, QColor, QMovie
from PyQt5.QtGui import QColor, QKeySequence, QImage
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QGraphicsDropShadowEffect, QLabel, QMainWindow, QDesktopWidget, QSizePolicy
from welcome import Ui_Dialog
import sqlite3
import sys
import os
os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/bin")

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from os.path import dirname, join
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream, FPS
import numpy as np
import imutils
import time
import cv2

from mylib import config, thread
from mylib.mailer import Mailer
from mylib.detection import detect_people
from scipy.spatial import distance as dist
import argparse,schedule

import smtplib

s = smtplib.SMTP('smtp.gmail.com', 587)

counter=0
flag=0

class SplashScreen(QMainWindow):
	def __init__(self):
		super(SplashScreen,self).__init__()
		uic.loadUi('splash_screen.ui',self)
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.progress)
		self.timer.start(35)
		self.progressBar.setValue(0)
		QtCore.QTimer.singleShot(1500, lambda: self.label_description.setText("<strong>LOADING</strong> DATABASE"))
		QtCore.QTimer.singleShot(3000, lambda: self.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))
		QtCore.QTimer.singleShot(4500, lambda: self.label_description.setText("<strong>LOADING</strong> MODELS"))

		self.shadow = QGraphicsDropShadowEffect(self)
		self.shadow.setBlurRadius(20)
		self.shadow.setXOffset(0)
		self.shadow.setYOffset(0)
		self.shadow.setColor(QColor(0, 0, 0, 60))
		self.dropShadowFrame.setGraphicsEffect(self.shadow)
		self.setFixedHeight(400)
		self.setFixedWidth(680)
		self.center()

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def progress(self):

		global counter
		self.progressBar.setValue(counter)


		if counter > 100:
			self.timer.stop()

			main=myApp()
			widget.addWidget(main)
			widget.setCurrentIndex(widget.currentIndex()+1)

		counter += 1


class myApp(QDialog):
	def __init__(self):
		super(myApp,self).__init__()
		uic.loadUi('welcomescreen.ui',self)
		self.pushButton_4.clicked.connect(self.gotologin)
		self.pushButton_3.clicked.connect(self.gotosignup)
		self.face.clicked.connect(self.gotofaceinfo)
		self.social.clicked.connect(self.gotosocialinfo)
		self.close.clicked.connect(self.gotoclose)
		self.min.clicked.connect(self.gotomin)
		self.max.clicked.connect(self.gotomax)
		print(flag)
		if flag==1:
			self.frame.move(365,100)
			self.titlebar.move(720,0)
			self.face.move(self.face.x()-100,self.face.y())
			self.face.setFixedSize(430,380)
			self.social.setFixedSize(430,380)
			self.pushButton_3.move(self.pushButton_3.x(),self.pushButton_3.y()+80)
			self.pushButton_4.move(self.pushButton_4.x(),self.pushButton_4.y()+80)
			self.pushButton_3.setFixedSize(130,50)
			self.pushButton_4.setFixedSize(130,50)
			self.label.move(self.label.x(),self.label.y()-50)
			self.label_2.move(self.label_2.x(),self.label_2.y()-40)
			self.label.setStyleSheet('font: 55pt "MS Shell Dlg 2";color:black;')
			self.label_2.setStyleSheet('font: 14pt "MS Shell Dlg 2";color:black')



	def gotomin(self):
		widget.showMinimized()

	def gotomax(self):
		if widget.isMaximized():
			widget.showNormal()
			#widget.showMaximized()
			self.frame.move(self.frame.x()-365,self.frame.y()-100)
			self.face.setFixedSize(320,300)
			self.social.setFixedSize(320,300)
			self.face.move(self.face.x()+100,self.face.y())
			self.titlebar.move(self.titlebar.x()-720,0)
			self.pushButton_3.move(self.pushButton_3.x(),self.pushButton_3.y()-80)
			self.pushButton_4.move(self.pushButton_4.x(),self.pushButton_4.y()-80)
			self.pushButton_3.setFixedSize(120,40)
			self.pushButton_4.setFixedSize(120,40)
			self.label.move(self.label.x(),self.label.y()+50)
			self.label_2.move(self.label_2.x(),self.label_2.y()+40)
			self.label.setStyleSheet('font: 45pt "MS Shell Dlg 2";color:black;')
			self.label_2.setStyleSheet('font: 12pt "MS Shell Dlg 2";color:black')

		else:
			widget.showMaximized()
			self.frame.move(365,100)
			self.titlebar.move(720,0)
			self.face.move(self.face.x()-100,self.face.y())
			self.face.setFixedSize(430,380)
			self.social.setFixedSize(430,380)
			self.pushButton_3.move(self.pushButton_3.x(),self.pushButton_3.y()+80)
			self.pushButton_4.move(self.pushButton_4.x(),self.pushButton_4.y()+80)
			self.pushButton_3.setFixedSize(130,50)
			self.pushButton_4.setFixedSize(130,50)
			self.label.move(self.label.x(),self.label.y()-50)
			self.label_2.move(self.label_2.x(),self.label_2.y()-40)
			self.label.setStyleSheet('font: 55pt "MS Shell Dlg 2";color:black;')
			self.label_2.setStyleSheet('font: 14pt "MS Shell Dlg 2";color:black')


	def gotoclose(self):
		exit(1)

	def gotofaceinfo(self):
		global flag
		if widget.isMaximized():
			flag=1
		if self.frame.x()==0:
			flag=0
		print(flag)
		face=facemaskinfo()
		widget.addWidget(face)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def gotosocialinfo(self):
		global flag
		if widget.isMaximized():
			flag=1
		if self.frame.x()==0:
			flag=0
		print(flag)
		social=socialinfo()
		widget.addWidget(social)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def gotologin(self):
		global flag
		if widget.isMaximized():
			flag=1
		if self.frame.x()==0:
			flag=0
		print(flag)
		login=LoginScreen()
		widget.addWidget(login)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def gotosignup(self):
		global flag
		if widget.isMaximized():
			flag=1
		if self.frame.x()==0:
			flag=0
		print(flag)
		signup=SignupScreen()
		widget.addWidget(signup)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def keyPressEvent(self,event):
		if event.key() == Qt.Key_Escape:
			exit(1)

	'''def mousePressEvent(self,event):
		self.oldPosition=event.globalPos()

	def mouseMoveEvent(self,event):
		delta=QPoint(event.globalPos()-self.oldPosition)
		self.move(self.x()+delta.x(),self.y()+delta.y())
		self.oldPosition=event.globalPos()'''

class LoginScreen(QDialog):
	def __init__(self):
		super(LoginScreen,self).__init__()
		uic.loadUi('loginscreen.ui',self)
		self.pushButton_4.clicked.connect(self.loginfunction)
		self.close_6.clicked.connect(self.gotoclose)
		self.min_6.clicked.connect(self.gotomin)
		self.max_6.clicked.connect(self.gotomax)
		print(flag)
		if flag==1:
			self.frame.move(365,0)
			self.frame_buttons.move(self.frame_buttons.x()+720,0)
			self.widget_2.setFixedSize(450,280)
			self.widget_2.move(self.widget_2.x()-50,self.widget_2.y()+150)
			self.error.setFixedSize(370,30)
			self.pushButton_4.move(self.pushButton_4.x(),self.pushButton_4.y()+250)
			self.pushButton_4.setFixedSize(130,50)
			self.label_3.move(40,25)
			self.lineEdit.move(40,60)
			self.lineEdit.setFixedSize(370,50)
			self.lineEdit_2.setFixedSize(370,50)
			self.label_4.move(40,135)
			self.lineEdit_2.move(40,170)
			self.error.move(40,230)
			self.label_3.setStyleSheet('font: 14pt "Segoe UI";')
			self.label_4.setStyleSheet('font: 14pt "Segoe UI";')
			self.lineEdit.setStyleSheet('background-color:rgba(0,0,0,0);font: 15pt "Arial Rounded MT Bold";')
			self.lineEdit_2.setStyleSheet('background-color:rgba(0,0,0,0);font: 15pt "Arial Rounded MT Bold";')
			self.error.setStyleSheet('color:red;font: 16pt "Segoe UI";')
		if flag==0 and self.frame.x()==365:
			self.frame.move(self.frame.x()-365,self.frame.y())
			self.frame_buttons.move(self.frame_buttons.x()-720,0)
			self.widget_2.setFixedSize(350,210)
			self.widget_2.move(self.widget_2.x()+50,self.widget_2.y()-150)
			self.error.setFixedSize(280,30)
			self.pushButton_4.move(self.pushButton_4.x(),self.pushButton_4.y()-250)
			self.pushButton_4.setFixedSize(120,40)
			self.label_3.move(40,20)
			self.lineEdit.move(40,50)
			self.lineEdit.setFixedSize(280,40)
			self.lineEdit_2.setFixedSize(280,40)
			self.label_4.move(40,100)
			self.lineEdit_2.move(40,130)
			self.error.move(40,172)
			self.label_3.setStyleSheet('font: 11pt "Segoe UI";')
			self.label_4.setStyleSheet('font: 11pt "Segoe UI";')
			self.lineEdit.setStyleSheet('background-color:rgba(0,0,0,0);font: 12pt "Arial Rounded MT Bold";')
			self.lineEdit_2.setStyleSheet('background-color:rgba(0,0,0,0);font: 12pt "Arial Rounded MT Bold";')
			self.error.setStyleSheet('color:red;font: 11pt "Segoe UI";')



	def gotomin(self):
		widget.showMinimized()

	def gotomax(self):
		if widget.isMaximized():
			widget.showNormal()
			#widget.showMaximized()
			self.frame.move(self.frame.x()-365,self.frame.y())
			self.frame_buttons.move(self.frame_buttons.x()-720,0)
			self.widget_2.setFixedSize(350,210)
			self.widget_2.move(self.widget_2.x()+50,self.widget_2.y()-150)
			self.error.setFixedSize(280,30)
			self.pushButton_4.move(self.pushButton_4.x(),self.pushButton_4.y()-250)
			self.pushButton_4.setFixedSize(120,40)
			self.label_3.move(40,20)
			self.lineEdit.move(40,50)
			self.lineEdit.setFixedSize(280,40)
			self.lineEdit_2.setFixedSize(280,40)
			self.label_4.move(40,100)
			self.lineEdit_2.move(40,130)
			self.error.move(40,172)
			self.label_3.setStyleSheet('font: 11pt "Segoe UI";')
			self.label_4.setStyleSheet('font: 11pt "Segoe UI";')
			self.lineEdit.setStyleSheet('background-color:rgba(0,0,0,0);font: 12pt "Arial Rounded MT Bold";')
			self.lineEdit_2.setStyleSheet('background-color:rgba(0,0,0,0);font: 12pt "Arial Rounded MT Bold";')
			self.error.setStyleSheet('color:red;font: 11pt "Segoe UI";')

		else:
			widget.showMaximized()
			self.frame.move(365,0)
			self.frame_buttons.move(self.frame_buttons.x()+720,0)
			self.widget_2.setFixedSize(450,280)
			self.widget_2.move(self.widget_2.x()-50,self.widget_2.y()+150)
			self.error.setFixedSize(370,30)
			self.pushButton_4.move(self.pushButton_4.x(),self.pushButton_4.y()+250)
			self.pushButton_4.setFixedSize(130,50)
			self.label_3.move(40,25)
			self.lineEdit.move(40,60)
			self.lineEdit.setFixedSize(370,50)
			self.lineEdit_2.setFixedSize(370,50)
			self.label_4.move(40,135)
			self.lineEdit_2.move(40,170)
			self.error.move(40,230)
			self.label_3.setStyleSheet('font: 14pt "Segoe UI";')
			self.label_4.setStyleSheet('font: 14pt "Segoe UI";')
			self.lineEdit.setStyleSheet('background-color:rgba(0,0,0,0);font: 15pt "Arial Rounded MT Bold";')
			self.lineEdit_2.setStyleSheet('background-color:rgba(0,0,0,0);font: 15pt "Arial Rounded MT Bold";')
			self.error.setStyleSheet('color:red;font: 16pt "Segoe UI";')


	def gotoclose(self):
		exit(1)	

	def keyPressEvent(self,event):
		global flag
		if event.key() == Qt.Key_Escape:
			if widget.isMaximized():
				flag=1
			else:
				flag=0
			main=myApp()
			widget.addWidget(main)
			widget.setCurrentIndex(widget.currentIndex()+1)

	def loginfunction(self):
		user=self.lineEdit.text()
		password=self.lineEdit_2.text()

		if len(user)==0 or len(password)==0:
			self.error.setText("Please input all Fields.")
			self.error.setStyleSheet(
                "color:red")
	

		else:
			conn=sqlite3.connect("Admin.db")
			cur=conn.cursor()
			query='SELECT password FROM login_info WHERE username =\''+user+"\'"
			cur.execute(query)
			result_pass=cur.fetchone()
			if result_pass is not None:
				result_pass = result_pass[0]
			if(result_pass==password):
				print("Successfully logged in")
				#self.error.setText("Login Successful")
				#self.error.setStyleSheet(
                #"color:green")
				global flag
				if widget.isMaximized():
					flag=1
				if self.frame.x()==0:
					flag=0
				print(flag)
				mainscreen=MainScreen()
				widget.addWidget(mainscreen)
				widget.setCurrentIndex(widget.currentIndex()+1)
				
			else:
				self.error.setText("Invalid Username or Password")
				self.error.setStyleSheet(
                "color:red")


class facemaskinfo(QDialog):
	def __init__(self):
		super(facemaskinfo,self).__init__()
		uic.loadUi('facemaskinfo.ui',self)
		self.movie=QMovie('maskgif.gif')
		self.label.setMovie(self.movie)
		self.movie.start()
		self.close.clicked.connect(self.gotoclose)
		self.max.clicked.connect(self.gotomax)
		self.min.clicked.connect(self.gotomin)
		if flag==1:
			self.frame.setFixedSize(1920,800)
			self.label.move(self.label.x()+365,self.label.y()+100)
			self.frame_buttons.move(self.frame_buttons.x()+720,self.frame_buttons.y())
			self.label_2.move(self.label_2.x()+365,self.label_2.y()+100)
			self.label_3.move(self.label_3.x()+365,self.label_3.y()+100)
			self.widget_2.move(self.widget_2.x()+365,self.widget_2.y()+100)	
		if flag==0 and self.label_2.x()==709:
			self.frame.setFixedSize(1200,800)
			self.label_2.move(self.label_2.x()-365,self.label_2.y()-100)
			self.frame_buttons.move(self.frame_buttons.x()-720,self.frame_buttons.y())
			self.label.move(self.label.x()-365,self.label.y()-100)
			self.label_3.move(self.label_3.x()-365,self.label_3.y()-100)
			self.widget_2.move(self.widget_2.x()-365,self.widget_2.y()-100)


	def gotoclose(self):
		exit(1)

	def gotomin(self):
		widget.showMinimized()

	def gotomax(self):
		if widget.isMaximized():
			widget.showNormal()
			self.frame.setFixedSize(1200,800)
			self.label_2.move(self.label_2.x()-365,self.label_2.y()-100)
			self.frame_buttons.move(self.frame_buttons.x()-720,self.frame_buttons.y())
			self.label.move(self.label.x()-365,self.label.y()-100)
			self.label_3.move(self.label_3.x()-365,self.label_3.y()-100)
			self.widget_2.move(self.widget_2.x()-365,self.widget_2.y()-100)

		else:
			widget.showMaximized()
			self.frame.setFixedSize(1920,800)
			self.label.move(self.label.x()+365,self.label.y()+100)
			self.frame_buttons.move(self.frame_buttons.x()+720,self.frame_buttons.y())
			self.label_2.move(self.label_2.x()+365,self.label_2.y()+100)
			self.label_3.move(self.label_3.x()+365,self.label_3.y()+100)
			self.widget_2.move(self.widget_2.x()+365,self.widget_2.y()+100)	


	def keyPressEvent(self,event):
		global flag
		if event.key() == Qt.Key_Escape:
			if widget.isMaximized():
				flag=1
			else:
				flag=0
			main=myApp()
			widget.addWidget(main)
			widget.setCurrentIndex(widget.currentIndex()+1)




class socialinfo(QDialog):
	def __init__(self):
		super(socialinfo,self).__init__()
		uic.loadUi('socialinfo.ui',self)
		self.movie=QMovie('socialgif.gif')
		self.label.setMovie(self.movie)
		self.movie.start()
		self.close.clicked.connect(self.gotoclose)
		self.max.clicked.connect(self.gotomax)
		self.min.clicked.connect(self.gotomin)
		if flag==1:
			self.frame.setFixedSize(1920,800)
			self.label.move(self.label.x()+365,self.label.y()+100)
			self.frame_buttons.move(self.frame_buttons.x()+720,self.frame_buttons.y())
			self.label_2.move(self.label_2.x()+365,self.label_2.y()+100)
			self.label_3.move(self.label_3.x()+365,self.label_3.y()+100)
			self.widget_2.move(self.widget_2.x()+365,self.widget_2.y()+100)	
		if flag==0 and self.label_2.x()==779:
			self.frame.setFixedSize(1200,800)
			self.label_2.move(self.label_2.x()-365,self.label_2.y()-100)
			self.frame_buttons.move(self.frame_buttons.x()-720,self.frame_buttons.y())
			self.label.move(self.label.x()-365,self.label.y()-100)
			self.label_3.move(self.label_3.x()-365,self.label_3.y()-100)
			self.widget_2.move(self.widget_2.x()-365,self.widget_2.y()-100)


	def gotoclose(self):
		exit(1)

	def gotomin(self):
		widget.showMinimized()

	def gotomax(self):
		if widget.isMaximized():
			widget.showNormal()
			self.frame.setFixedSize(1200,800)
			self.label_2.move(self.label_2.x()-365,self.label_2.y()-100)
			self.frame_buttons.move(self.frame_buttons.x()-720,self.frame_buttons.y())
			self.label.move(self.label.x()-365,self.label.y()-100)
			self.label_3.move(self.label_3.x()-365,self.label_3.y()-100)
			self.widget_2.move(self.widget_2.x()-365,self.widget_2.y()-100)

		else:
			widget.showMaximized()
			self.frame.setFixedSize(1920,800)
			self.label.move(self.label.x()+365,self.label.y()+100)
			self.frame_buttons.move(self.frame_buttons.x()+720,self.frame_buttons.y())
			self.label_2.move(self.label_2.x()+365,self.label_2.y()+100)
			self.label_3.move(self.label_3.x()+365,self.label_3.y()+100)
			self.widget_2.move(self.widget_2.x()+365,self.widget_2.y()+100)	


	def keyPressEvent(self,event):
		global flag
		if event.key() == Qt.Key_Escape:
			if widget.isMaximized():
				flag=1
			else:
				flag=0
			main=myApp()
			widget.addWidget(main)
			widget.setCurrentIndex(widget.currentIndex()+1)


class MainScreen(QDialog):
	def __init__(self):
		super(MainScreen,self).__init__()
		uic.loadUi('Mainscreen.ui',self)
		effect = QGraphicsDropShadowEffect(offset=QPoint(2, 2), blurRadius=10, color=QColor("#111"))
		self.frame_2.setGraphicsEffect(effect)
		self.logout.clicked.connect(self.logoutfunction)
		self.face.clicked.connect(self.facemaskfunction)
		self.social.clicked.connect(self.socialdistfunction)
		self.close_2.clicked.connect(self.gotoclose)
		self.min_2.clicked.connect(self.gotomin)
		self.max_2.clicked.connect(self.gotomax)
		if flag==1:
			self.frame_2.setFixedSize(1920,60)
			self.frame.move(365,100)
			self.label_2.move(self.label_2.x()+360,self.label_2.y())
			self.frame_buttons_2.move(self.frame_buttons_2.x()+720,self.frame_buttons_2.y())
			self.face.move(self.face.x()-100,self.face.y())
			self.face.setFixedSize(430,380)
			self.social.setFixedSize(430,380)
			self.logout.move(self.logout.x()-10,self.logout.y()+80)
			self.error.move(self.error.x()-5,self.error.y()+80)
			self.logout.setFixedSize(130,50)
			self.frame_2.setStyleSheet('QFrame#frame_2{background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0.210227 rgba(5, 177, 106, 255), stop:1 rgba(0, 85, 0, 255));border-top-left-radius:0px;border-bottom-right-radius:0px;border-top-right-radius:0px;border-bottom-left-radius:0px}')
		if flag==0 and self.frame.x()==365:
			self.frame_2.setFixedSize(1200,60)
			self.frame.move(0,0)
			self.label_2.move(self.label_2.x()-360,self.label_2.y())
			self.frame_buttons_2.move(self.frame_buttons_2.x()-720,self.frame_buttons_2.y())
			self.face.move(self.face.x()+100,self.face.y())
			self.face.setFixedSize(320,300)
			self.social.setFixedSize(320,300)
			self.logout.move(self.logout.x()+10,self.logout.y()-80)
			self.logout.setFixedSize(120,40)
			self.error.move(self.error.x()+5,self.error.y()-80)
			self.frame_2.setStyleSheet('QFrame#frame_2{background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0.210227 rgba(5, 177, 106, 255), stop:1 rgba(0, 85, 0, 255));border-top-left-radius:15px;border-bottom-right-radius:0px;border-top-right-radius:15px;border-bottom-left-radius:0px}')

	def gotomin(self):
		widget.showMinimized()

	def gotomax(self):
		if widget.isMaximized():
			widget.showNormal()
			self.frame_2.setFixedSize(1200,60)
			self.frame.move(0,0)
			self.label_2.move(self.label_2.x()-360,self.label_2.y())
			self.frame_buttons_2.move(self.frame_buttons_2.x()-720,self.frame_buttons_2.y())
			self.face.move(self.face.x()+100,self.face.y())
			self.face.setFixedSize(320,300)
			self.social.setFixedSize(320,300)
			self.logout.move(self.logout.x()+10,self.logout.y()-80)
			self.logout.setFixedSize(120,40)
			self.error.move(self.error.x()+5,self.error.y()-80)
			self.frame_2.setStyleSheet('QFrame#frame_2{background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0.210227 rgba(5, 177, 106, 255), stop:1 rgba(0, 85, 0, 255));border-top-left-radius:15px;border-bottom-right-radius:0px;border-top-right-radius:15px;border-bottom-left-radius:0px}')
		else:
			widget.showMaximized()
			self.frame_2.setFixedSize(1920,60)
			self.frame.move(365,100)
			self.label_2.move(self.label_2.x()+360,self.label_2.y())
			self.frame_buttons_2.move(self.frame_buttons_2.x()+720,self.frame_buttons_2.y())
			self.face.move(self.face.x()-100,self.face.y())
			self.face.setFixedSize(430,380)
			self.social.setFixedSize(430,380)
			self.logout.move(self.logout.x()-10,self.logout.y()+80)
			self.logout.setFixedSize(130,50)
			self.error.move(self.error.x()-5,self.error.y()+80)
			self.frame_2.setStyleSheet('QFrame#frame_2{background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0.210227 rgba(5, 177, 106, 255), stop:1 rgba(0, 85, 0, 255));border-top-left-radius:0px;border-bottom-right-radius:0px;border-top-right-radius:0px;border-bottom-left-radius:0px}')

	def gotoclose(self):
		exit(1)

	def facemaskfunction(self):
		global flag
		if widget.isMaximized():
			flag=1
		else:
			flag=0
		trial=TrialScreen()
		widget.addWidget(trial)
		widget.setCurrentIndex(widget.currentIndex()+1)
		trial.mainfunc()

	def socialdistfunction(self):
		global flag
		if widget.isMaximized():
			flag=1
		else:
			flag=0
		sc=SocialDist()
		widget.addWidget(sc)
		widget.setCurrentIndex(widget.currentIndex()+1)
		sc.mainfunc()

	def logoutfunction(self):
		global flag
		if widget.isMaximized():
			flag=1
		else:
			flag=0
		main=myApp()
		widget.addWidget(main)
		widget.setCurrentIndex(widget.currentIndex()+1)

	def keyPressEvent(self,event):
		if event.key() == Qt.Key_Escape:
			self.error.setText("Log out to exit")	


class VideoThread(QThread):
	change_pixmap_signal = pyqtSignal(np.ndarray)

	def __init__(self):
		super().__init__()
		self._run_flag = True

	def run(self):
		count=0
		maskNet = load_model("mask_detector.model")
		prototxtPath = r"deploy.protext"
		weightsPath = r"res10_300x300_ssd_iter_140000.caffemodel"
		faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
		cap = cv2.VideoCapture(0)
		if not cap.isOpened():
			raise IOError("Cannot open webcam")
		while self._run_flag:
			ret, cv_img = cap.read()
			if ret:

				(locs, preds) = self.detect_and_predict_mask(cv_img, faceNet, maskNet)

				for (box, pred) in zip(locs, preds):
					(startX, startY, endX, endY) = box
					(mask, withoutMask) = pred
					if mask>withoutMask:
						count+=1
					else:
						count=0

					label = "Mask" if mask > withoutMask else "No Mask"
					color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
					print(mask,withoutMask)

					label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

					cv2.putText(cv_img, label, (startX, startY - 10),
			                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
					cv2.rectangle(cv_img, (startX, startY), (endX, endY), color, 5)

				if count>=25:
					cv2.rectangle(cv_img, (0, 450), (650, 500), color, -1)
					cv2.putText(cv_img, "MASK DETECTED", (270,467),
				                    cv2.FONT_HERSHEY_DUPLEX, 0.45, (255,255,255), 1)

				self.change_pixmap_signal.emit(cv_img)

				
				key = cv2.waitKey(1) & 0xFF
				if key == ord("q"):
					self._run_flag = False
			
	
		
	def detect_and_predict_mask(self,frame, faceNet, maskNet):
				(h, w) = frame.shape[:2]
				blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
			                             (104.0, 177.0, 123.0))

				faceNet.setInput(blob)
				detections = faceNet.forward()
				print(detections.shape)

				faces = []
				locs = []
				preds = []

				for i in range(0, detections.shape[2]):
					confidence = detections[0, 0, i, 2]
					if confidence > 0.5:
						box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
						(startX, startY, endX, endY) = box.astype("int")

						(startX, startY) = (max(0, startX), max(0, startY))
						(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

						face = frame[startY:endY, startX:endX]
						face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
						face = cv2.resize(face, (224, 224))
						face = img_to_array(face)
						face = preprocess_input(face)

						faces.append(face)
						locs.append((startX, startY, endX, endY))


				if len(faces) > 0:
					faces = np.array(faces, dtype="float32")
					preds = maskNet.predict(faces, batch_size=32)
				return (locs, preds)

	def stop(self):
		self._run_flag = False

class VideoThread1(QThread):
	change_pixmap_signal = pyqtSignal(np.ndarray)

	def __init__(self,url):
		super().__init__()
		self._run_flag = True
		self.url=url
		self.MAX_DISTANCE= 400
		self.MIN_DISTANCE = 250
		self.mail_flag=0


	def run(self):
		# load the COCO class labels our YOLO model was trained on
		labelsPath = os.path.sep.join([config.MODEL_PATH, "coco.names"])
		LABELS = open(labelsPath).read().strip().split("\n")
		
		# derive the paths to the YOLO weights and model configuration
		weightsPath = os.path.sep.join([config.MODEL_PATH, "yolov4.weights"])
		configPath = os.path.sep.join([config.MODEL_PATH, "yolov4.cfg"])

		# load our YOLO object detector trained on COCO dataset (80 classes)
		net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

		#use GPU
		if config.USE_GPU:
			# set CUDA as the preferable backend and target
			net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
			net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

		# determine only the *output* layer names that we need from YOLO
		ln = net.getLayerNames()
		ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

		print("Starting the live stream")
		vs = cv2.VideoCapture(self.url)
		if config.Thread:
			cap = thread.ThreadingClass(self.url)
		time.sleep(2.0)

		print(self.url)
		if self.url==0:
			self.MAX_DISTANCE= 400
			self.MIN_DISTANCE = 250
		else:
			self.MAX_DISTANCE= 140
			self.MIN_DISTANCE = 100
		'''while(True):
			try:
				cap = cv2.VideoCapture(self.url)
				break
			except:
				print("Invalid Entry")
				self.url= 0'''
		print(self.MAX_DISTANCE)
		while self._run_flag:
			# read the next frame from the file
			if config.Thread:
				frame = cap.read()

			else:
				(grabbed, frame) = vs.read()
				# if the frame was not grabbed, then we have reached the end of the stream
				if not grabbed:
					break

			# resize the frame and then detect people (and only people) in it
			#frame = imutils.resize(frame, width=700)
			results = detect_people(frame, net, ln,
			personIdx=LABELS.index("person"))

			# initialize the set of indexes that violate the max/min social distance limits
			serious = set()
			abnormal = set()

			# ensure there are *at least* two people detections (required in
			# order to compute our pairwise distance maps)
			if len(results) >= 2:
				# extract all centroids from the results and compute the
				# Euclidean distances between all pairs of the centroids
				centroids = np.array([r[2] for r in results])
				D = dist.cdist(centroids, centroids, metric="euclidean")

				# loop over the upper triangular of the distance matrix
				for i in range(0, D.shape[0]):
					for j in range(i + 1, D.shape[1]):
					# check to see if the distance between any two
					# centroid pairs is less than the configured number of pixels
						if D[i, j] < self.MIN_DISTANCE:
							# update our violation set with the indexes of the centroid pairs
							serious.add(i)
							serious.add(j)
               			# update our abnormal set if the centroid distance is below max distance limit
						if (D[i, j] < self.MAX_DISTANCE) and not serious:
							abnormal.add(i)
							abnormal.add(j)

			# loop over the results
			for (i, (prob, bbox, centroid)) in enumerate(results):
				# extract the bounding box and centroid coordinates, then
				# initialize the color of the annotation
				(startX, startY, endX, endY) = bbox
				(cX, cY) = centroid
				color = (0, 255, 0)

				# if the index pair exists within the violation/abnormal sets, then update the color
				if i in serious:
					color = (0, 0, 255)
				elif i in abnormal:
					color = (0, 255, 255) #orange = (0, 165, 255)

				# draw (1) a bounding box around the person and (2) the
				# centroid coordinates of the person,
				cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
				cv2.circle(frame, (cX, cY), 5, color, 2)


		
		    # draw the total number of social distancing violations on the output frame
			text = "Total serious violations: {}".format(len(serious))
			cv2.putText(frame, text, (10, frame.shape[0] - 55),
			cv2.FONT_HERSHEY_SIMPLEX, 0.70, (0, 0, 255), 2)

			text1 = "Total abnormal violations: {}".format(len(abnormal))
			cv2.putText(frame, text1, (10, frame.shape[0] - 25),
			cv2.FONT_HERSHEY_SIMPLEX, 0.70, (0, 255, 255), 2)
			self.change_pixmap_signal.emit(frame)
			if len(serious)>10 and self.mail_flag==0:
				s.starttls()
  
				# Authentication
				s.login("shubhu2603@gmail.com", "Shubhankar123#")
  
				# message to be sent
				message = "Social Distancing Violation Alert"
  
				# sending the mail
				s.sendmail("shubhu2603@gmail.com", "hingneshubhankar@gmail.com", message)
  
				# terminating the session
				s.quit()
				self.mail_flag=1
			if len(serious)<2:
				self.mail_flag=0
	
		
	def stop(self):
		self._run_flag = False

class SocialDist(QDialog):
	def __init__(self):
		super(SocialDist,self).__init__()
		uic.loadUi('social.ui',self)
		effect = QGraphicsDropShadowEffect(offset=QPoint(2, 2), blurRadius=10, color=QColor("#111"))
		self.frame_2.setGraphicsEffect(effect)
		self.disply_width = 1000
		self.display_height = 650
		self.image_label = QLabel(self)
		self.image_label.setStyleSheet("border-radius: 25px; border: 2px white;")
		self.image_label.setMinimumSize(QSize(self.disply_width, self.display_height))
		self.image_label.move(170,90)
		self.url=0
		self.movie=QMovie('loading.gif')
		self.image.setMovie(self.movie)
		self.image.resize(865,650)
		self.movie.start()
		self.close.clicked.connect(self.gotoclose)
		self.min.clicked.connect(self.gotomin)
		self.max.clicked.connect(self.gotomax)
		self.change.clicked.connect(self.gotochange)
		self.cc.clicked.connect(self.takeinputs)

		if flag==1:
			self.frame_2.setFixedSize(1920,60)
			self.frame.move(365,100)
			self.label_2.move(self.label_2.x()+360,self.label_2.y())
			self.frame_buttons.move(self.frame_buttons.x()+720,self.frame_buttons.y())
			self.image_label.move(self.image.x()+365,self.image.y()+100)

		if flag==0 and self.frame.x()==365:
			self.frame_2.setFixedSize(1200,60)
			self.frame.move(0,0)
			self.label_2.move(self.label_2.x()-360,self.label_2.y())
			self.frame_buttons.move(self.frame_buttons.x()-720,self.frame_buttons.y())
			self.image_label.move(170,90)

	def gotomin(self):
		widget.showMinimized()

	def gotomax(self):
		if widget.isMaximized():
			widget.showNormal()
			self.frame_2.setFixedSize(1200,60)
			self.frame.move(0,0)
			self.label_2.move(self.label_2.x()-360,self.label_2.y())
			self.frame_buttons.move(self.frame_buttons.x()-720,self.frame_buttons.y())
			if self.url==1 or self.url==0:
				self.image_label.move(170,90)
			else:
				self.image_label.move(100,90)

		else:
			widget.showMaximized()
			self.frame_2.setFixedSize(1920,60)
			self.frame.move(365,100)
			self.label_2.move(self.label_2.x()+360,self.label_2.y())
			self.frame_buttons.move(self.frame_buttons.x()+720,self.frame_buttons.y())
			if self.url==1 or self.url==0:
				self.image_label.move(535,190)
			else:
				self.image_label.move(465,190)			
			


	def takeinputs(self):
		inp,rec= QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter Device ID:')
		self.url=str(inp)
		self.thread.stop()
		if self.frame.x()==365:
			self.image_label.move(465,190)
		else:
			self.image_label.move(100,90)
		self.image_label.hide()
		self.image.hide()
		self.thread=VideoThread1(self.url)
		self.thread.change_pixmap_signal.connect(self.update_image)
		self.thread.start()
		time.sleep(5.0)
		self.image_label.show()
		#self.image_label.show()

	def gotoclose(self):
		exit(1)		

	def keyPressEvent(self,event):
		if event.key() == Qt.Key_Escape:
			self.thread.stop()
			global flag
			if widget.isMaximized():
				flag=1
			else:
				flag=0
			main=MainScreen()
			widget.addWidget(main)
			widget.setCurrentIndex(widget.currentIndex()+1)


	def gotochange(self):

		self.thread.stop()
		if self.frame.x()==365:
			self.image_label.move(535,190)
		else:
			self.image_label.move(170,90)
		if self.url==0:
			self.url=1
		else:
			self.url=0
		self.image.show()
		self.image_label.hide()
		self.thread=VideoThread1(self.url)
		self.thread.change_pixmap_signal.connect(self.update_image)
		self.thread.start()
		time.sleep(5.0)
		self.image_label.show()
		#self.image_label.show()


	def mainfunc(self):
	
		self.thread=VideoThread1(self.url)
		self.thread.change_pixmap_signal.connect(self.update_image)
		self.thread.start()

	def closeEvent(self, event):
		self.thread.stop()
		event.accept()


	def update_image(self, cv_img):
		qt_img = self.convert_cv_qt(cv_img)
		self.image_label.setPixmap(qt_img) 
		self.image_label.setStyleSheet("border-radius: 25px; border: 2px white;")

	def convert_cv_qt(self, cv_img):
		rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
		h, w, ch = rgb_image.shape
		bytes_per_line = ch * w
		convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
		p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
		return QPixmap.fromImage(p)

	def smooth_gif_resize(gif, frameWidth, frameHeight):
	    gif = Image.open(gif)
	    gifWidth0, gifHeight0 = gif.size

	    widthRatio = frameWidth / gifWidth0
	    heightRatio = frameHeight / gifHeight0

	    if widthRatio >= heightRatio:
	        gifWidth1 = gifWidth0 * heightRatio
	        gifHeight1 = frameHeight
	        return gifWidth1, gifHeight1

	    gifWidth1 = frameWidth
	    gifHeight1 = gifHeight0 * widthRatio
	    return gifWidth1, gifHeight1


class TrialScreen(QDialog):
	def __init__(self):
		super(TrialScreen,self).__init__()
		uic.loadUi('trial.ui',self)
		effect = QGraphicsDropShadowEffect(offset=QPoint(2, 2), blurRadius=10, color=QColor("#111"))
		self.frame_2.setGraphicsEffect(effect)
		self.disply_width = 1000
		self.display_height = 650
		self.image_label = QLabel(self)
		self.image_label.setStyleSheet("border-radius: 25px; border: 2px white;")
		self.image_label.setMinimumSize(QSize(self.disply_width, self.display_height))
		self.image_label.move(170,90)

		self.movie=QMovie('loading.gif')
		self.image.setMovie(self.movie)
		self.image.resize(865,650)
		self.movie.start()
		self.close.clicked.connect(self.gotoclose)
		self.min.clicked.connect(self.gotomin)
		self.max.clicked.connect(self.gotomax)

		if flag==1:
			self.frame_2.setFixedSize(1920,60)
			self.frame.move(365,100)
			self.label_2.move(self.label_2.x()+360,self.label_2.y())
			self.frame_buttons.move(self.frame_buttons.x()+720,self.frame_buttons.y())
			self.image_label.move(self.image.x()+365,self.image.y()+100)

		if flag==0 and self.frame.x()==365:
			self.frame_2.setFixedSize(1200,60)
			self.frame.move(0,0)
			self.label_2.move(self.label_2.x()-360,self.label_2.y())
			self.frame_buttons.move(self.frame_buttons.x()-720,self.frame_buttons.y())
			self.image_label.move(170,90)

	def gotomin(self):
		widget.showMinimized()

	def gotomax(self):
		if widget.isMaximized():
			widget.showNormal()
			self.frame_2.setFixedSize(1200,60)
			self.frame.move(0,0)
			self.label_2.move(self.label_2.x()-360,self.label_2.y())
			self.frame_buttons.move(self.frame_buttons.x()-720,self.frame_buttons.y())
			self.image_label.move(170,90)

		else:
			widget.showMaximized()
			self.frame_2.setFixedSize(1920,60)
			self.frame.move(365,100)
			self.label_2.move(self.label_2.x()+360,self.label_2.y())
			self.frame_buttons.move(self.frame_buttons.x()+720,self.frame_buttons.y())
			self.image_label.move(self.image.x()+365,self.image.y()+100)


	def gotoclose(self):
		exit(1)		

	def keyPressEvent(self,event):
		if event.key() == Qt.Key_Escape:
			self.thread.stop()
			global flag
			if widget.isMaximized():
				flag=1
			else:
				flag=0
			main=MainScreen()
			widget.addWidget(main)
			widget.setCurrentIndex(widget.currentIndex()+1)


	def mainfunc(self):
	
		self.thread=VideoThread()
		self.thread.change_pixmap_signal.connect(self.update_image)
		self.thread.start()


	def closeEvent(self, event):
		self.thread.stop()
		event.accept()


	def update_image(self, cv_img):
		qt_img = self.convert_cv_qt(cv_img)
		self.image_label.setPixmap(qt_img) 
		self.image_label.setStyleSheet("border-radius: 25px; border: 2px white;")

	def convert_cv_qt(self, cv_img):
		rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
		h, w, ch = rgb_image.shape
		bytes_per_line = ch * w
		convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
		p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
		return QPixmap.fromImage(p)

	def smooth_gif_resize(gif, frameWidth, frameHeight):
	    gif = Image.open(gif)
	    gifWidth0, gifHeight0 = gif.size

	    widthRatio = frameWidth / gifWidth0
	    heightRatio = frameHeight / gifHeight0

	    if widthRatio >= heightRatio:
	        gifWidth1 = gifWidth0 * heightRatio
	        gifHeight1 = frameHeight
	        return gifWidth1, gifHeight1

	    gifWidth1 = frameWidth
	    gifHeight1 = gifHeight0 * widthRatio
	    return gifWidth1, gifHeight1


class SignupScreen(QDialog):
	def __init__(self):
		super(SignupScreen,self).__init__()
		uic.loadUi('signupscreen.ui',self)
		self.signup.clicked.connect(self.signupfunction)
		self.close_2.clicked.connect(self.gotoclose)
		self.min_2.clicked.connect(self.gotomin)
		self.max_2.clicked.connect(self.gotomax)
		if flag==1:
			self.frame.move(365,0)
			self.frame_buttons.move(self.frame_buttons.x()+720,0)
			self.widget_2.setFixedSize(450,440)
			self.widget_2.move(self.widget_2.x()-50,self.widget_2.y()+120)
			self.error.setFixedSize(370,30)
			self.signup.move(self.signup.x(),self.signup.y()+240)
			self.signup.setFixedSize(130,50)
			self.label_5.move(40,25)
			self.email.move(40,60)
			self.email.setFixedSize(370,50)
			self.us.move(40,120)
			self.username.setFixedSize(370,50)
			self.username.move(40,150)
			self.label_4.move(40,210)
			self.password.move(40,240)
			self.password.setFixedSize(370,50)
			self.label_6.move(40,300)
			self.cpass.move(40,330)
			self.cpass.setFixedSize(370,50)
			self.error.move(40,390)
			self.label_5.setStyleSheet('font: 14pt "Segoe UI";')
			self.us.setStyleSheet('font: 14pt "Segoe UI";')
			self.label_4.setStyleSheet('font: 14pt "Segoe UI";')
			self.label_6.setStyleSheet('font: 14pt "Segoe UI";')
			self.email.setStyleSheet('background-color:rgba(0,0,0,0);font: 15pt "Arial Rounded MT Bold";')
			self.username.setStyleSheet('background-color:rgba(0,0,0,0);font: 15pt "Arial Rounded MT Bold";')
			self.password.setStyleSheet('background-color:rgba(0,0,0,0);font: 15pt "Arial Rounded MT Bold";')
			self.cpass.setStyleSheet('background-color:rgba(0,0,0,0);font: 15pt "Arial Rounded MT Bold";')
			self.error.setStyleSheet('color:red;font: 16pt "Segoe UI";')

		if flag==0 and self.frame.x()==365:
			self.frame.move(self.frame.x()-365,self.frame.y())
			self.frame_buttons.move(self.frame_buttons.x()-720,0)
			self.widget_2.setFixedSize(350,330)
			self.widget_2.move(self.widget_2.x()+50,self.widget_2.y()-120)
			self.error.setFixedSize(280,30)
			self.signup.move(self.signup.x(),self.signup.y()-240)
			self.signup.setFixedSize(120,40)
			self.label_5.move(40,10)
			self.email.move(40,40)
			self.email.setFixedSize(280,40)
			self.us.move(40,80)
			self.username.setFixedSize(280,40)
			self.username.move(40,110)
			self.label_4.move(40,150)
			self.password.move(40,180)
			self.password.setFixedSize(280,40)
			self.label_6.move(40,220)
			self.cpass.move(40,250)
			self.cpass.setFixedSize(280,40)
			self.error.move(40,290)
			self.label_5.setStyleSheet('font: 11pt "Segoe UI";')
			self.us.setStyleSheet('font: 11pt "Segoe UI";')
			self.label_4.setStyleSheet('font: 11pt "Segoe UI";')
			self.label_6.setStyleSheet('font: 141t "Segoe UI";')
			self.email.setStyleSheet('background-color:rgba(0,0,0,0);font: 12pt "Arial Rounded MT Bold";')
			self.username.setStyleSheet('background-color:rgba(0,0,0,0);font: 12pt "Arial Rounded MT Bold";')
			self.password.setStyleSheet('background-color:rgba(0,0,0,0);font: 12pt "Arial Rounded MT Bold";')
			self.cpass.setStyleSheet('background-color:rgba(0,0,0,0);font: 12pt "Arial Rounded MT Bold";')
			self.error.setStyleSheet('color:red;font: 11pt "Segoe UI";')




	def gotomin(self):
		widget.showMinimized()

	def gotomax(self):
		if widget.isMaximized():
			widget.showNormal()
			self.frame.move(self.frame.x()-365,self.frame.y())
			self.frame_buttons.move(self.frame_buttons.x()-720,0)
			self.widget_2.setFixedSize(350,330)
			self.widget_2.move(self.widget_2.x()+50,self.widget_2.y()-120)
			self.error.setFixedSize(280,30)
			self.signup.move(self.signup.x(),self.signup.y()-240)
			self.signup.setFixedSize(120,40)
			self.label_5.move(40,10)
			self.email.move(40,40)
			self.email.setFixedSize(280,40)
			self.us.move(40,80)
			self.username.setFixedSize(280,40)
			self.username.move(40,110)
			self.label_4.move(40,150)
			self.password.move(40,180)
			self.password.setFixedSize(280,40)
			self.label_6.move(40,220)
			self.cpass.move(40,250)
			self.cpass.setFixedSize(280,40)
			self.error.move(40,290)
			self.label_5.setStyleSheet('font: 11pt "Segoe UI";')
			self.us.setStyleSheet('font: 11pt "Segoe UI";')
			self.label_4.setStyleSheet('font: 11pt "Segoe UI";')
			self.label_6.setStyleSheet('font: 141t "Segoe UI";')
			self.email.setStyleSheet('background-color:rgba(0,0,0,0);font: 12pt "Arial Rounded MT Bold";')
			self.username.setStyleSheet('background-color:rgba(0,0,0,0);font: 12pt "Arial Rounded MT Bold";')
			self.password.setStyleSheet('background-color:rgba(0,0,0,0);font: 12pt "Arial Rounded MT Bold";')
			self.cpass.setStyleSheet('background-color:rgba(0,0,0,0);font: 12pt "Arial Rounded MT Bold";')
			self.error.setStyleSheet('color:red;font: 11pt "Segoe UI";')


		else:
			widget.showMaximized()
			self.frame.move(365,0)
			self.frame_buttons.move(self.frame_buttons.x()+720,0)
			self.widget_2.setFixedSize(450,440)
			self.widget_2.move(self.widget_2.x()-50,self.widget_2.y()+120)
			self.error.setFixedSize(370,30)
			self.signup.move(self.signup.x(),self.signup.y()+240)
			self.signup.setFixedSize(130,50)
			self.label_5.move(40,25)
			self.email.move(40,60)
			self.email.setFixedSize(370,50)
			self.us.move(40,120)
			self.username.setFixedSize(370,50)
			self.username.move(40,150)
			self.label_4.move(40,210)
			self.password.move(40,240)
			self.password.setFixedSize(370,50)
			self.label_6.move(40,300)
			self.cpass.move(40,330)
			self.cpass.setFixedSize(370,50)
			self.error.move(40,390)
			self.label_5.setStyleSheet('font: 14pt "Segoe UI";')
			self.us.setStyleSheet('font: 14pt "Segoe UI";')
			self.label_4.setStyleSheet('font: 14pt "Segoe UI";')
			self.label_6.setStyleSheet('font: 14pt "Segoe UI";')
			self.email.setStyleSheet('background-color:rgba(0,0,0,0);font: 15pt "Arial Rounded MT Bold";')
			self.username.setStyleSheet('background-color:rgba(0,0,0,0);font: 15pt "Arial Rounded MT Bold";')
			self.password.setStyleSheet('background-color:rgba(0,0,0,0);font: 15pt "Arial Rounded MT Bold";')
			self.cpass.setStyleSheet('background-color:rgba(0,0,0,0);font: 15pt "Arial Rounded MT Bold";')
			self.error.setStyleSheet('color:red;font: 16pt "Segoe UI";')


	def gotoclose(self):
		exit(1)

	def keyPressEvent(self,event):
		global flag
		if event.key() == Qt.Key_Escape:
			if widget.isMaximized():
				flag=1
			else:
				flag=0
			main=myApp()
			widget.addWidget(main)
			widget.setCurrentIndex(widget.currentIndex()+1)

	def signupfunction(self):
		email=self.email.text()
		username=self.username.text()
		password=self.password.text()
		cpass=self.cpass.text()

		if len(username)==0 or len(password)==0 or len(email)==0 or len(cpass)==0:
			self.error.setText("Please input all Fields.")
			self.error.setStyleSheet("color:red")

		elif '@' not in email and '.' not in email:
			self.error.setText("Enter valid email.")
			self.error.setStyleSheet("color:red")

		elif len(password)<8:
			self.error.setText("Password too short")
			self.error.setStyleSheet("color:red")

		elif password!=cpass:
			self.error.setText("Passwords do not match.")
			self.error.setStyleSheet("color:red")

		else:
			conn=sqlite3.connect("Admin.db")
			cur=conn.cursor()
			user_info=[username,password,email]
			cur.execute('INSERT INTO login_info(username,password,email) VALUES (?,?,?)', user_info)
			conn.commit()

			welcome=myApp()
			widget.addWidget(welcome)
			widget.setCurrentIndex(widget.currentIndex()+1)


app=QtWidgets.QApplication(sys.argv)
Dialog=SplashScreen()
widget=QtWidgets.QStackedWidget()
widget.addWidget(Dialog)
widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
try:
	sys.exit(app.exec_())
except:
	print("Exiting")