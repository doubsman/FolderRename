#! /usr/bin/python
# coding: utf-8

from PyQt5.QtCore import QObject
from os import walk, rename, path
from sys import path as syspath
from copy import deepcopy
syspath.append(path.dirname(path.dirname(path.abspath(__file__))))
from LogPrintFile.LogPrintFile import LogPrintFile


class FoldersRename(QObject):
	"""Rename list folders."""
						
	def __init__(self, parent=None):
		"""Init."""
		super(FoldersRename, self).__init__(parent)
		self.parent = parent
		self.pathfolder = None
		self.pathList = None
		self.backList = None
		# log
		self.logProcess = LogPrintFile(path.join(path.dirname(path.abspath(__file__)), 'LOG'), 'FoldersRename', True, 30)

	def folder_init(self, pathfolder, pathfilter = None):
		# build list
		self.pathfolder = pathfolder
		self.backList = self.folders_list(pathfilter)
		self.pathList = deepcopy(self.backList)
	
	def cancel_actions(self):
		"""Reinit list."""
		self.pathList = deepcopy(self.backList)

	def folders_rename(self):
		"""Rename folders list and write log."""
		self.logProcess.write_log_file('START OPERATIONS', self.pathfolder, False)
		counter = 0
		for folderName in self.backList:
			# clean name
			self.logProcess.write_log_file('FOLDER FOLDER', folderName)
			if folderName != self.pathList[counter]:
				self.logProcess.write_log_file('CLEAN FOLDER', self.pathList[counter])
				rename(path.join(self.pathfolder, folderName), path.join(self.pathfolder, self.pathList[counter]))
			else:
				self.logProcess.write_log_file('NO MODIFICATION', self.pathList[counter])
			counter += 1
		self.logProcess.write_log_file('END OPERATIONS.',"", False)
		self.logProcess.view_log_file()

	def folders_cancelrename(self):
		"""Rename folders list and write log."""
		self.logProcess.write_log_file('START CANCEL OPERATIONS', self.pathfolder, False)
		counter = 0
		for folderName in self.backList:
			# clean name
			self.logProcess.write_log_file('FOLDER FOLDER', folderName)
			if folderName != self.pathList[counter]:
				self.logProcess.write_log_file('CANCEL NAME FOLDER', self.pathList[counter])
				rename(path.join(self.pathfolder, self.pathList[counter]), path.join(self.pathfolder, folderName))
			else:
				self.logProcess.write_log_file('NO MODIFICATION', self.pathList[counter])
			counter += 1
		self.logProcess.write_log_file('END OPERATIONS.',"", False)
		self.logProcess.view_log_file()

	def folders_control(self):
		"""Display results."""
		for counter in range(0, len(self.pathList)):
			print( self.backList[counter])
			print(self.pathList[counter]+"\n")

	def folders_list(self, pathfilter):
		"""Build list folders."""
		listdirs = []
		for _, listdirs, _ in walk(self.pathfolder):
			break
		if pathfilter:
			listdirs = [f for f in listdirs if pathfilter in f]
		return listdirs

	def replace_characters(self, startC, goalC):
		for counter in range(0, len(self.pathList)):
			self.pathList[counter] = self.pathList[counter].replace(startC, goalC)

	def add_characters(self, wordadd, goalC, decoCL ="", decoCR =""):
		for counter in range(0, len(self.pathList)):
			folderName = self.pathList[counter]
			posiC = self.convert_position_character(goalC, folderName)
			self.pathList[counter] = folderName[:posiC] + decoCL + wordadd + decoCR + folderName[posiC:]

	def delete_characters(self, startC, lenghtC):
		for counter in range(0, len(self.pathList)):
			folderName = self.pathList[counter]
			posiC = self.convert_position_character(startC, folderName)
			self.pathList[counter] = folderName[:posiC] + folderName[lenghtC + posiC:]

	def move_characters(self, startC, lenghtC, goalC, decoCL ="", decoCR =""):
		for counter in range(0, len(self.pathList)):
			folderName = self.pathList[counter]
			starC = self.convert_position_character(startC, folderName)
			posiC = self.convert_position_character(goalC, folderName)
			moveC = folderName[starC:lenghtC + starC]
			tempC = folderName[:starC] + folderName[starC + lenghtC:]
			self.pathList[counter] = tempC[:posiC] + decoCL + moveC.strip() + decoCR + tempC[posiC:]
	
	def format_tittle(self):
		for counter in range(0, len(self.pathList)):
			self.pathList[counter] = self.pathList[counter].title()

	def convert_position_character(self, posi, item):
		"""conversion 
				max 	: end of the string
				pos(n:s): find position occurence:string
		"""
		if isinstance(posi, str):
			# str
			if posi.startswith('max'):
				posiC = int(len(item))
			elif posi.startswith('pos'):
				params = posi.replace('pos(','').replace(')','')
				number = int(params.split(":")[0])
				string = params.split(":")[1]
				posiC = self.find_nth(item, string, number)
				print(posi, number, string, posiC)
		else:
			# int
			posiC = posi
		return posiC

	def find_nth(self, haystack, needle, n):
		"""https://stackoverflow.com/questions/1883980/find-the-nth-occurrence-of-substring-in-a-string."""
		start = haystack.find(needle)
		while start >= 0 and n > 1:
			start = haystack.find(needle, start+len(needle))
			n -= 1
		return start