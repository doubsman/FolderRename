# #! /usr/bin/python
# coding: utf-8
from sys import argv
from os import path, getcwd
from json import load, dumps
from Ui_MainWindow import Ui_Dialog
from FoldersRename import FoldersRename
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem, QMouseEvent, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QStyle, QMenu, QComboBox



class FoldersRenameGUI(QMainWindow, Ui_Dialog):
	"""Init mini Gui constants."""
	DOWN 		= 1
	UP   		= -1

	def __init__(self, parent=None):
		super(FoldersRenameGUI, self).__init__(parent)

		self.parent = parent
		self.setupUi(self)

		# default config
		self.C_ROWHEIGHT = 30
		self.listcolumnsactions = {'-'       : ['Actions', 'Paramater', 'Paramater', 'Paramater', 'Paramater', 'Paramater'],
								   'move'    : ['Actions', 'Start', 'Length', 'Goal', 'Deco Left', 'Deco Right'],
								   'replace' : ['Actions', 'Replace', 'By', '---', '---', '---'],
								   'add'     : ['Actions', 'Text','Start', '---', '---', '---'],
								   'delete'  : ['Actions', 'Start','Length', '---', '---', '---']}
		self.defaultconfiguration = {  'General' : { 'Programs'  : 'Folders Rename Managment',
											  'Version'  : 0.7,
											  'Size Row Table'  : 30,
											  'Font' : "Calibri",
											  'Ico'  : 'FoldersRenameGUI.ico'
											},
										'Actions' : self.listcolumnsactions}
		
		# json file configuration ?
		file_configuration = path.join(path.dirname(path.abspath(__file__)), 'FoldersRenameGUI.json')
		if path.exists(file_configuration):
			data_file = open(file_configuration, 'r')
			self.configuration = load(data_file)
			data_file.close()
		else:
			self.configuration = self.defaultconfiguration

		self.setWindowIcon(QIcon(self.configuration['General']['Ico']))
		self.setWindowTitle(self.configuration['General']['Programs'] + ' ' + str(self.configuration['General']['Version']))
		self.arrayactions = []
		self.file_json = None
		self.C_ROWHEIGHT = int(self.configuration['General']['Size Row Table'])

		# define font tab
		self.fontbig = QFont()
		self.fontbig.setFamily(self.configuration['General']['Font'])
		self.fontbig.setFixedPitch(True)
		self.fontbig.setPointSize(12)
		self.tbl_viewactions.setFont(self.fontbig)
	
		# define buttons
		self.btn_selectfolder.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
		self.btn_rename.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
		self.btn_rename.setText('Rename')
		self.btn_sav.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
		self.btn_sav.setText('Save')
		self.btn_load.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
		self.btn_load.setText('Load')
		self.btn_test.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
		self.btn_test.setText('Test')

		# define lists
		self.listcolumnsresult = ['Actual','New']
		self.listsizeresult = [200, 200]
		self.listcolumnsactions = self.configuration['Actions']
		self.listcomboactions = self.listcolumnsactions.keys()
		self.listsizeactions = [200] + ([110] *5)
		
		# format tableviews
		self.prepareTable(self.tbl_viewresult, self.listsizeresult)
		self.modelfolder = self.prepareModel(self.tbl_viewresult, self.listsizeresult, self.listcolumnsresult)
		self.prepareTable(self.tbl_viewactions, self.listsizeactions)
		self.modelactions = self.prepareModel(self.tbl_viewactions, self.listsizeactions, self.listcolumnsactions['-'])

		# pop up
		self.menua = QMenu()
		self.action2 = self.menua.addAction("remove", self.remove_action)
		self.action3 = self.menua.addAction("up", lambda n=self.UP: self.move_action(n))
		self.action4 = self.menua.addAction("down", lambda n=self.DOWN: self.move_action(n))
		
		# events
		self.btn_selectfolder.clicked.connect(self.selectFolder)
		self.lin_pathfolder.returnPressed.connect(lambda: self.selectFolder(True))
		self.btn_sav.clicked.connect(self.saveListactions)
		self.btn_load.clicked.connect(self.loadListactions)
		self.btn_test.clicked.connect(self.testFoldersRename)
		self.btn_rename.clicked.connect(self.runFoldersRename)
		self.tbl_viewactions.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tbl_viewactions.customContextMenuRequested.connect(self.popUpTreeAlbums)
		self.tbl_viewactions.clicked.connect(self.onSelectAction)

		# init class FoldersRename
		self.pathfolder = None
		self.FoldersRename = FoldersRename()
		# init actions tab
		self.fillTableactions()

	def selectFolder(self, linpathfolder = False):
		if not linpathfolder:
			self.pathfolder = QFileDialog.getExistingDirectory(self, "Select Directory")
		else:
			self.pathfolder = self.lin_pathfolder.text()
		if path.isdir(self.pathfolder):
			self.lin_pathfolder.setText(self.pathfolder.replace('/','\\'))
			self.FoldersRename.folder_init(self.pathfolder)
			self.fillTablefolder()

	def runFoldersRename(self):
		# build list actions
		self.testFoldersRename()
		# Rename
		self.FoldersRename.folders_rename()
		# display results
		self.fillTablefolder()
	
	def testFoldersRename(self):
		# build list actions
		self.buildListactions()
		# Reinit list result
		self.FoldersRename.pathList = self.FoldersRename.backList
		# realise actions
		self.realiseListactions()
		# display results
		self.fillTablefolder()

	def saveListactions(self):
		"""Backup list actions to json file."""
		# build list actions
		self.buildListactions()
		self.file_json = QFileDialog.getSaveFileName(self,
										"Create file for save parameters",
										getcwd(),
										"Json (*.json)")
		self.file_json = self.file_json[0]
		# write file
		data_file = open(self.file_json, 'w+')
		data_file.write(dumps(self.arrayactions, indent=4))
		data_file.close()

	def loadListactions(self):
		"""Backup list actions to json file."""
		self.file_json = QFileDialog.getOpenFileName(self,
										"Load file for init parameters",
										getcwd(),
										"Json (*.json)")
		self.file_json = self.file_json[0]
		data_file = open(self.file_json, 'r')
		self.arrayactions = load(data_file)
		data_file.close()
		# refresh tab
		self.fillTableactions()
	
	def buildListactions(self):
		# build list actions
		self.arrayactions = []
		for row in range(self.modelactions.rowCount()):
			self.arrayaction = []
			for col in range(self.modelactions.columnCount()):
				value = self.getValueCellactions(self.modelactions, row, col)
				self.arrayaction.append(value)
			if self.arrayaction[0] != '-':
				self.arrayactions.append(self.arrayaction)

	def realiseListactions(self):
		# realise actions
		for action in self.arrayactions:
			if action[0] == 'move':
				par1 = self.trtparams(action[1])
				par2 = self.trtparams(action[2])
				par3 = self.trtparams(action[3])
				par4 = self.trtparams(action[4])
				par5 = self.trtparams(action[5])
				self.FoldersRename.move_characters(par1, par2, par3, par4, par5)
			elif action[0] == 'replace':
				par1 = self.trtparams(action[1])
				par2 = self.trtparams(action[2])
				self.FoldersRename.replace_characters(par1, par2)
			elif action[0] == 'add':
				par1 = self.trtparams(action[1])
				par2 = self.trtparams(action[2])
				par3 = self.trtparams(action[3])
				par4 = self.trtparams(action[4])
				if par3 == '':
					self.FoldersRename.add_characters(par1, par2)
				elif par4 == '':
					self.FoldersRename.add_characters(par1, par2, par3)
				else:
					self.FoldersRename.add_characters(par1, par2, par3, par4)
			elif action[0] == 'delete':
				par1 = self.trtparams(action[1])
				par2 = self.trtparams(action[2])
				self.FoldersRename.delete_characters(par1, par2)
	
	def trtparams(self, param):
		"""Convert String to int is numeric."""
		if param.isnumeric():
			param = int(param)
		return param

	def getValueCellactions(self, model, row, col):
		if col == 0:
			# combo cell value
			i = self.tbl_viewactions.model().index(row , col)
			combo = self.tbl_viewactions.indexWidget(i)
			value = combo.currentText()
		else:
			# cell value 
			value = model.data(model.index(row, col))
		return value
	
	def prepareTable(self, table, listsizecolumns):
		"""Define table format."""
		table.horizontalHeader().setStretchLastSection(True)
		table.verticalHeader().setVisible(False)
		table.setStyleSheet("QHeaderView::section { color: white; background-color: black;border-radius:1px;margin: 1px;padding: 2px;}")
		table.setAlternatingRowColors(True)
		table.setSortingEnabled(False)
		table.setSelectionBehavior(table.SelectRows)
		# columns width 
		for ind in range(len(listsizecolumns)):
			table.setColumnWidth(ind, listsizecolumns[ind])
		table.verticalHeader().setDefaultSectionSize(self.C_ROWHEIGHT)
	
	def prepareModel(self, table, listsizecolumns, listnamecolumns, defaultline = 26):
		"""Define table model : fill columns name."""
		model = QStandardItemModel(defaultline, len(listsizecolumns), self)
		model.setHorizontalHeaderLabels(listnamecolumns)
		table.setModel(model)
		return model

	def fillTableactions(self):
		"""Prepare combos."""
		# fill line actions
		for row in range(self.modelactions.rowCount()):
			# if present action
			if row < len(self.arrayactions):
				col = 0
				for params in self.arrayactions[row]:
					if col > 0:
						item = QStandardItem(params)
						self.modelactions.setItem(row, col, item)
					col += 1
				self.buildComboActions(row, self.arrayactions[row][0])
			else:
				self.buildComboActions(row)
		#self.tbl_viewactions.horizontalHeader().setStretchLastSection(False)
		#self.tbl_viewactions.resizeColumnsToContents()
		#self.tbl_viewactions.horizontalHeader().setStretchLastSection(True)			

	def fillTablefolder(self):
		"""Display columns list and transformation."""
		self.modelfolder = QStandardItemModel(len(self.FoldersRename.pathList), len(self.listcolumnsresult), self)
		self.modelfolder.setHorizontalHeaderLabels(self.listcolumnsresult)
		self.tbl_viewresult.setModel(self.modelfolder)
		counter = 0
		for row in range(self.modelfolder.rowCount()):
			item = QStandardItem(self.FoldersRename.backList[counter])
			self.modelfolder.setItem(row, 0, item)
			item = QStandardItem(self.FoldersRename.cleanlist[counter])
			self.modelfolder.setItem(row, 1, item)
			counter += 1
		self.tbl_viewresult.horizontalHeader().setStretchLastSection(False)
		self.tbl_viewresult.resizeColumnsToContents()
		self.tbl_viewresult.horizontalHeader().setStretchLastSection(True)
	
	def popUpTreeAlbums(self, position):
		self.menua.exec_(self.tbl_viewactions.viewport().mapToGlobal(position))
	
	def onComboChanged(self, row):
		i = self.tbl_viewactions.model().index(row , 0)
		combo = self.tbl_viewactions.indexWidget(i)
		value = combo.currentText()
		self.modelactions.setHorizontalHeaderLabels(self.listcolumnsactions[value])

	def onSelectAction(self):
		"""Modifie Header."""
		model = self.modelactions
		selModel = self.tbl_viewactions.selectionModel()
		selected = selModel.selectedRows()
		row = selected[0].row()
		i = self.tbl_viewactions.model().index(row , 0)
		combo = self.tbl_viewactions.indexWidget(i)
		value = combo.currentText()
		self.modelactions.setHorizontalHeaderLabels(self.listcolumnsactions[value])

	def remove_action(self):
		model = self.modelactions
		selModel = self.tbl_viewactions.selectionModel()
		selected = selModel.selectedRows()
		if not selected:
			return
		# in progress
		row = selected[0].row()
		self.modelactions.removeRow(row)
		# add end line
		self.modelactions.insertRow(self.modelactions.rowCount())
		# rebuild combo
		self.buildComboActions(self.modelactions.rowCount() - 1)

	def move_action(self, direction = DOWN):
		if direction not in (self.DOWN, self.UP):
			return
		model = self.modelactions
		selModel = self.tbl_viewactions.selectionModel()
		selected = selModel.selectedRows()
		if not selected:
			return
		row = selected[0].row()
		i = self.tbl_viewactions.model().index(row , 0)
		combo = self.tbl_viewactions.indexWidget(i)
		value = combo.currentText()
		items = []
		indexes = sorted(selected, key=lambda x: x.row(), reverse=(direction==self.DOWN))
		for idx in indexes:
			items.append(model.itemFromIndex(idx))
			rowNum = idx.row()
			newRow = rowNum+direction
			if not (0 <= newRow < model.rowCount()):
				continue
			rowItems = model.takeRow(rowNum)
			model.insertRow(newRow, rowItems)
		selModel.clear()
		for item in items:
			selModel.select(item.index(), selModel.Select|selModel.Rows)
		# rebuild combo
		self.buildComboActions(row + direction, value)
	
	def buildComboActions(self, row, value = None):
		# create combo
		combo_actions = QComboBox(self)
		combo_actions.addItems(self.listcomboactions)
		#combo_actions.currentIndexChanged.connect(lambda n=row: self.onComboChanged(row))
		i = self.tbl_viewactions.model().index( row, 0)
		self.tbl_viewactions.setIndexWidget(i, combo_actions)
		# select value
		if value is not None:
			index = combo_actions.findText(value, Qt.MatchFixedString)
			if index >= 0:
				combo_actions.setCurrentIndex(index)	



if __name__ == '__main__':
	app = QApplication(argv)
	DB = FoldersRenameGUI()
	DB.show()
	rc = app.exec_()
	exit(rc)
