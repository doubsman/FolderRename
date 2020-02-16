#! /usr/bin/python
# coding: utf-8

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, qDebug
from os import walk, rename, path
from sys import argv, path as syspath
syspath.append(path.dirname(path.dirname(path.abspath(__file__))))
from LogPrintFile.LogPrintFile import LogPrintFile


class ManageFolders(QObject):
	"""Rename list folders."""
						
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
		self.logProcess = LogPrintFile(path.join(path.dirname(path.abspath(__file__)), 'LOG'), 'ManageFolders', True, 30)

	def folders_rename(self):
		"""Rename folders list and write log."""
		self.logProcess.write_log_file('START OPERATIONS', self.pathfolder, False)
		counter = 0
		for folderName in self.backList:
			# clean name
			self.logProcess.write_log_file('FOLDER FOLDER', folderName)
			self.logProcess.write_log_file('CLEAN FOLDER', self.cleanlist[counter])
			rename(path.join(self.pathfolder, folderName), path.join(self.pathfolder, self.cleanlist[counter]))
			counter += 1
		self.logProcess.write_log_file('END OPERATIONS.',"", False)
		self.logProcess.view_log_file()

	def folders_control(self):
		"""Display results."""
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
			posiC = self.convert_position_character(goalC, folderName)
			self.cleanlist.append(folderName[:posiC] + decoCL + wordadd + decoCR + folderName[posiC:])
		self.pathList = self.cleanlist

	def delete_characters(self, startC, lenghtC):
		self.cleanlist = []
		for folderName in self.pathList:
			self.cleanlist.append(folderName[:startC] + folderName[lenghtC + startC:])
		self.pathList = self.cleanlist

	def move_characters(self, startC, lenghtC, goalC, decoCL ="", decoCR =""):
		self.cleanlist = []
		for folderName in self.pathList:
			posiC = self.convert_position_character(goalC, folderName)
			moveC = folderName[startC:lenghtC]
			tempC = folderName[:startC] + folderName[startC + lenghtC:]
			self.cleanlist.append(tempC[:posiC] + decoCL + moveC.strip() + decoCR + tempC[posiC:])
		self.pathList = self.cleanlist
	
	def convert_position_character(self, posi, item):
		"""conversion max to len()."""
		if isinstance(posi, str):
			# str
			if posi == 'max':
				posiC = int(len(item))
		else:
			# int
			posiC = posi
		return posiC


if __name__ == '__main__':
	app = QApplication(argv)
	if len(argv)>1:
		# prod
		myfolder = argv[1]
	else:
		# test envt
		myfolder = r'T:\work\Tiken Jah Fakoly - Discographie [mp3-320]'
	# build class process
	BuildProcess = ManageFolders(myfolder)
	BuildProcess.move_characters(0, 5, 'max',' (',')')
	BuildProcess.replace_characters(' [320]', '')
	BuildProcess.add_characters('Tiken Jah Fakoly - ', 0)
	#BuildProcess.delete_characters(5,3)
	BuildProcess.folders_control()
	# processing
	BuildProcess.folders_rename()
