#! /usr/bin/python
# coding: utf-8

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, qDebug, QDateTime
from os import walk, rename, path, mkdir, remove, rmdir, startfile
from sys import argv
from codecs import open


class ManageFolders(QObject):
	"""build list folders name, search youtube and download first video find format mp4."""
						
	def __init__(self, pathfolder, parent=None):
		"""Init."""
		super(ManageFolders, self).__init__(parent)
		self.parent = parent
		self.pathfolder = pathfolder
		# build list
		self.pathList = self.folders_list()
		self.backList = self.pathList
		self.cleanlist = []
		# log
		self.logFileName = QDateTime.currentDateTime().toString('yyMMddhhmmss') + "_ManageFolders.log"
		self.logFileName = path.join(path.dirname(path.abspath(__file__)), "LOG", self.logFileName)

	def folders_rename(self):
		"""Rename folders list and write log."""
		self.write_log_file('START OPERATIONS', self.pathfolder, False)
		counter = 0
		for folderName in self.backList:
			# clean name
			self.write_log_file('FOLDER FOLDER', folderName)
			self.write_log_file('CLEAN FOLDER', self.cleanlist[counter])
			rename(path.join(self.pathfolder, folderName), path.join(self.pathfolder, self.cleanlist[counter]))
			counter += 1
		self.write_log_file('END OPERATIONS.',"", False)
		startfile(self.logFileName)

	def folders_control(self):
		counter = 0
		for folderName in self.backList:
			print(folderName)
			print(self.cleanlist[counter]+"\n")
			counter += 1

	def folders_list(self):
		"""Build list folders."""
		listdirs = []
		for _, listdirs, _ in walk(self.pathfolder):
			break
		return listdirs

	def replace_characters(self, startC, goalC):
		self.cleanlist = []
		for folderName in self.pathList:
			self.cleanlist.append(folderName.replace(startC, goalC))
		self.pathList = self.cleanlist

	def add_characters(self, wordadd, goalC, decoCL ="", decoCR =""):
		self.cleanlist = []
		for folderName in self.pathList:
			if isinstance(goalC, str):
				if goalC == 'max':
					goalC = int(len(folderName))
			self.cleanlist.append(folderName[:goalC] + decoCL + wordadd + decoCR + folderName[goalC:])
		self.pathList = self.cleanlist

	def delete_characters(self, startC, lenghtC):
		self.cleanlist = []
		for folderName in self.pathList:
			self.cleanlist.append(folderName[:startC] + folderName[lenghtC + startC:])
		self.pathList = self.cleanlist

	def move_characters(self, startC, lenghtC, goalC, decoCL ="", decoCR =""):
		self.cleanlist = []
		for folderName in self.pathList:
			if isinstance(goalC, str):
				if goalC == 'max':
					goalC = int(len(folderName))
			moveC = folderName[startC:lenghtC]
			tempC = folderName[:startC] + folderName[startC + lenghtC:]
			self.cleanlist.append(tempC[:goalC] + decoCL + moveC.strip() + decoCR + tempC[goalC:])
		self.pathList = self.cleanlist
	
	def write_log_file(self, operation, line, modification = True, writeconsole = True):
		"""Write log file."""
		if modification:
			logline = '{:>22} : {}  '.format(operation, line)
		else:
			if line == "":
				logline = operation + "\n"
			else:
				logline = '{} "{}"'.format(operation, line)
		text_file = open(self.logFileName, "a", 'utf-8')
		text_file.write(logline+"\n")
		text_file.close()
		if writeconsole:
			print(logline)

if __name__ == '__main__':
	app = QApplication(argv)
	if len(argv)>1:
		# prod
		myfolder = argv[1]
	else:
		# test envt
		myfolder = "T:\\work\\Fila Brazillia NT\\\Singles & EPs"
	# build class process
	BuildProcess = ManageFolders(myfolder)
	BuildProcess.replace_characters('(', '[')
	BuildProcess.replace_characters(')', ']')
	BuildProcess.replace_characters(' [Web]', '')
	BuildProcess.move_characters(0, 5, 'max',' (',')')
	#BuildProcess.add_characters('VA - ',0)
	#BuildProcess.delete_characters(5,3)
	BuildProcess.folders_control()
	# processing
	BuildProcess.folders_rename()
