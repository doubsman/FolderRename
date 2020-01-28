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
		self.pathfolder = pathfolder
		self.parent = parent
		# build list
		self.pathList = self.list_folders(pathfolder)
		self.backList = self.pathList
		self.cleanlist = []
		self.counter = 0
		self.logFileName = QDateTime.currentDateTime().toString('yyMMddhhmmss') + "_ManageFolders.log"
		self.logFileName = path.join(path.dirname(path.abspath(__file__)), "LOG", self.logFileName)

	def folders_rename(self):
		"""Rename folders list and write log."""
		self.write_log_file('START OPERATIONS', self.pathfolder, False)
		self.counter = 0
		for folderName in self.backList:
			# clean name
			self.write_log_file('FOLDER NAME', folderName)
			self.write_log_file('CLEAN NAME', self.cleanlist[self.counter])
			#rename(path.join(pathList, self.folderName), path.join(pathList, self.cleanName))
		self.write_log_file('END OPERATIONS.',"", False)
		startfile(self.logFileName)

	def folders_control(self):
		self.counter = 0
		for folderName in self.backList:
				print(folderName)
				print(self.cleanlist[self.counter]+"\n")
				self.counter += 1
	
	def folders_replace_character(self, startC, goalC):
		self.cleanlist = []
		for folderName in self.pathList:
			self.cleanlist.append(folderName.replace(startC, goalC))
		self.pathList = self.cleanlist

	def folders_add_character(self, wordC, goalC, decoCL ="", decoCR =""):
		self.cleanlist = []
		if isinstance(goalC, str):
			if goalC == 'max':
				goalC = int(len(word))
		for folderName in self.pathList:
			self.cleanlist.append(folderName[:goalC] + decoCL + wordC + decoCR + folderName[goalC:])
		self.pathList = self.cleanlist

	def folders_delete_characters(self, startC, lenghtC):
		self.cleanlist = []
		for folderName in self.pathList:
			self.cleanlist.append(folderName[:startC] + folderName[lenghtC + startC:])
		self.pathList = self.cleanlist

	def folders_move_characters(self, startC, lenghtC, goalC, decoCL ="", decoCR =""):
		self.cleanlist = []
		for folderName in self.pathList:
			self.cleanlist.append(self.func_mov_characters(folderName, startC, lenghtC, goalC, decoCL , decoCR))
		self.pathList = self.cleanlist
	
	def func_mov_characters(self, word, startC, lenghtC, goalC, decoCL ="", decoCR =""):
		moveC = word[startC:lenghtC]
		tempC = word[:startC] + word[startC + lenghtC:]
		if isinstance(goalC, str):
			if goalC == 'max':
				goalC = int(len(word))
		return tempC[:goalC] + decoCL + moveC.strip() + decoCR + tempC[goalC:]

	def list_folders(self, path):
		"""Build list folders."""
		for _, dirs, _ in walk(path):
			break
		return dirs

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
		myfolder = "T:\\work\\Fila Brazillia NT\\\Compilations"
	# class
	BuildProcess = ManageFolders(myfolder)
	BuildProcess.folders_replace_character('(', '[')
	BuildProcess.folders_replace_character(')', ']')
	BuildProcess.folders_replace_character(' [Web]', '')
	BuildProcess.folders_move_characters(0, 5, 'max',' (',')')
	BuildProcess.folders_add_character('VA - ',0)
	#BuildProcess.folders_delete_characters(5,3)
	BuildProcess.folders_control()
	BuildProcess.folders_rename()
	# download list
	#BuildProcess.processManageFolders(myfolder)
