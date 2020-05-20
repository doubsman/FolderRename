# #! /usr/bin/python
# coding: utf-8
from sys import argv
from os import path, getcwd
from json import load, dumps
from Ui_FoldersRename import Ui_MainWindow
#from Ui_MainWindow import Ui_Dialog
from FoldersRename import FoldersRename
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem, QMouseEvent, QFont, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QStyle, QMenu, QComboBox, QLineEdit, QMessageBox

""" add file Ui_FoldersRename.py after regeneration
		line 11: from FolderRenameDnd import QLineEditDnd
        line 25: 	# add for Dnd
        			#self.lin_pathfolder = QtWidgets.QLineEdit(self.centralwidget)
        			self.lin_pathfolder = QLineEditDnd(self)
"""


class FoldersRenameGUI(QMainWindow, Ui_MainWindow):
	"""Init mini Gui constants."""
	DOWN 		= 1
	UP   		= -1

	def __init__(self, parent=None):
		super(FoldersRenameGUI, self).__init__(parent)
		self.parent = parent
		self.path_prog = path.dirname(path.abspath(__file__))
		self.setupUi(self)

		# default config
		self.listcolumnsactions = {'-'       : ['Actions'] + ['Parameter']*5,
								   'move'    : ['Actions', 'Start', 'Length', 'Goal', 'Deco Left', 'Deco Right'],
								   'replace' : ['Actions', 'Replace', 'By', '---', '---', '---'],
								   'add'     : ['Actions', 'Text','Start', 'Deco Left', 'Deco Right', '---'],
								   'delete'  : ['Actions', 'Start','Length', '---', '---', '---'],
								   'title'  : ['Actions', '---','---', '---', '---', '---']}
		self.defaultconfiguration = {  'General' : { 'Programs'  : 'Folders Rename Managment',
											  'Version'  : 0.7,
											  'Size Row Table'  : 30,
											  'Font' : "Calibri",
											  'Ico'  : 'FoldersRenameGUI.ico',
											  'Width': 1350,
        									  'Height': 850
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
		
		self.setMinimumSize(600, 600)
		self.resize(self.configuration['General']['Width'], self.configuration['General']['Height'])
		icofile = path.join(self.path_prog, self.configuration['General']['Ico'])
		self.setWindowIcon(QIcon(icofile))
		self.setWindowTitle(self.configuration['General']['Programs'] + ' ' + str(self.configuration['General']['Version']))
		self.arrayactions = []
		self.file_json = None
		self.boolaction = False

		# define font tab
		self.fontbig = QFont()
		self.fontbig.setFamily(self.configuration['General']['Font'])
		self.fontbig.setFixedPitch(True)
		self.fontbig.setPointSize(12)
		self.tbl_viewactions.setFont(self.fontbig)
	
		# define buttons
		self.btn_selectfolder.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
		self.btn_run.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
		self.btn_run.setText('Rename Folders')
		self.btn_run.setEnabled(False)
		self.btn_save.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
		self.btn_save.setText('Save Actions')
		self.btn_load.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
		self.btn_load.setText('Load Actions')
		self.btn_test.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
		self.btn_test.setText('Test Actions')
		self.btn_test.setEnabled(False)
		self.btn_cancel.setIcon(self.style().standardIcon(QStyle.SP_DialogCancelButton))
		self.btn_cancel.setText('Cancel Actions')
		self.btn_cancel.setEnabled(False)
		
		# define lists
		self.listcolumnsresult = ['Current Name','New Name']
		self.listsizeresult = [200, 200]
		self.listcolumnsactions = self.configuration['Actions']
		self.listcomboactions = self.listcolumnsactions.keys()
		self.listsizeactions = [200] + ([110] *5)
		
		# format tableviews
		self.C_ROWHEIGHT = int(self.configuration['General']['Size Row Table'])
		self.NBLINES = int((self.frameGeometry().height() - 130) / self.C_ROWHEIGHT)
		self.prepareTable(self.tbl_viewresult, self.listsizeresult)
		self.modelfolder = self.prepareModel(self.tbl_viewresult, self.listsizeresult, self.listcolumnsresult, self.NBLINES)
		self.prepareTable(self.tbl_viewactions, self.listsizeactions)
		self.modelactions = self.prepareModel(self.tbl_viewactions, self.listsizeactions, self.listcolumnsactions['-'], self.NBLINES)

		# pop up
		self.menua = QMenu()
		self.action2 = self.menua.addAction("remove", self.remove_action)
		self.action3 = self.menua.addAction("up", lambda n=self.UP: self.move_action(n))
		self.action4 = self.menua.addAction("down", lambda n=self.DOWN: self.move_action(n))
		
		# events
		self.btn_selectfolder.clicked.connect(self.selectFolder)
		self.lin_pathfolder.signalchgtfolder.connect(self.selectFolder)
		self.lin_pathfolder.returnPressed.connect(lambda: self.selectFolder(True))
		self.lin_filter.returnPressed.connect(lambda: self.selectFolder(True))
		self.btn_save.clicked.connect(self.saveListactions)
		self.btn_load.clicked.connect(self.loadListactions)
		self.btn_test.clicked.connect(self.testFoldersRename)
		self.btn_run.clicked.connect(self.runFoldersRename)
		self.btn_cancel.clicked.connect(self.cancelRename)
		self.tbl_viewactions.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tbl_viewactions.customContextMenuRequested.connect(self.popUpTreeActions)
		self.tbl_viewactions.clicked.connect(self.onSelectAction)

		# init class FoldersRename
		self.pathfolder = None
		self.FoldersRename = FoldersRename(self)
		# init actions tab
		self.fillTableactions()
	
	@pyqtSlot()
	def resizeEvent(self, event):
		"""Widget size move."""
		newnumberlines = int((self.frameGeometry().height() - 140) / self.C_ROWHEIGHT)
		if newnumberlines != self.NBLINES:
			self.buildListactions()
			self.NBLINES = int((self.frameGeometry().height() - 140) / self.C_ROWHEIGHT)
			if self.NBLINES > len(self.arrayactions):
				self.modelactions = self.prepareModel(self.tbl_viewactions, self.listsizeactions, self.listcolumnsactions['-'], self.NBLINES)
				self.fillTableactions()

	def selectFolder(self, linpathfolder = False):
		if not linpathfolder:
			self.pathfolder = QFileDialog.getExistingDirectory(self, "Select Directory")
		else:
			self.pathfolder = self.lin_pathfolder.text()
		if path.isdir(self.pathfolder):
			self.lin_pathfolder.setText(self.pathfolder.replace('/','\\'))
			self.FoldersRename.folder_init(self.pathfolder, self.lin_filter.text())
			self.fillTablefolder()

	def runFoldersRename(self):
		response = QMessageBox.question(self, "Confirmation", "Rename Folders ?", QMessageBox.Yes, QMessageBox.No)
		if response == QMessageBox.Yes:		
			# build list actions
			self.testFoldersRename()
			# Rename
			self.FoldersRename.folders_rename()
			# display results
			self.fillTablefolder()
			# display cancel Actions
			self.btn_cancel.setEnabled(True)
	
	def cancelRename(self):
		"""Cancel all actions and Rename folders."""
		self.FoldersRename.folders_cancelrename()
	
	def testFoldersRename(self):
		# build list actions
		self.buildListactions()
		# Reinit list result
		self.FoldersRename.cancel_actions()
		# realise actions
		self.realiseListactions()
		# display results
		self.fillTablefolder()

	def saveListactions(self):
		"""Backup list actions to json file."""
		# build list actions
		self.buildListactions()
		self.file_json = QFileDialog.getSaveFileName(self,
										"Create file for save Actions",
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
										"Load file for init Actions",
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
			self.boolaction = True
			if action[0] == 'move':
				par1 = self.trtparams(action[1], 'mix')
				par2 = self.trtparams(action[2], 'mix')
				par3 = self.trtparams(action[3], 'mix')
				par4 = self.trtparams(action[4], 'str')
				par5 = self.trtparams(action[5], 'str')
				if self.boolaction:
					self.FoldersRename.move_characters(par1, par2, par3, par4, par5)
			elif action[0] == 'replace':
				par1 = self.trtparams(action[1], 'str')
				par2 = self.trtparams(action[2], 'str')
				if self.boolaction:
					self.FoldersRename.replace_characters(par1, par2)
			elif action[0] == 'add':
				par1 = self.trtparams(action[1], 'str')
				par2 = self.trtparams(action[2], 'mix')
				par3 = self.trtparams(action[3], 'str')
				par4 = self.trtparams(action[4], 'str')
				if self.boolaction:
					self.FoldersRename.add_characters(par1, par2, par3, par4)
			elif action[0] == 'delete':
				par1 = self.trtparams(action[1], 'mix')
				par2 = self.trtparams(action[2], 'mix')
				if self.boolaction:
					self.FoldersRename.delete_characters(par1, par2)
			elif action[0] == 'title':
				if self.boolaction:
					self.FoldersRename.format_tittle()
	
	def trtparams(self, param, type = None):
		"""Convert String to int function type param."""
		if param is None and (type == 'int' or type == 'mix'):
			param = 0
			self.boolaction = False
		elif param is None and type == 'str':
			param = ''
		elif type == 'int':
			param = int(param)
		elif type == 'str':
			param = str(param)
		elif type == 'mix':
			if param.isnumeric():
				param = int(param)
			else:
				param = str(param)
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
	
	def prepareModel(self, table, listsizecolumns, listnamecolumns, defaultline = 20):
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

	def fillTablefolder(self):
		"""Display columns list and transformation."""
		self.modelfolder = self.prepareModel(self.tbl_viewresult, self.listsizeresult, self.listcolumnsresult, len(self.FoldersRename.pathList))
		counter = 0
		for row in range(self.modelfolder.rowCount()):
			item = QStandardItem(self.FoldersRename.backList[counter])
			self.modelfolder.setItem(row, 0, item)
			item = QStandardItem(self.FoldersRename.pathList[counter])
			if self.FoldersRename.backList[counter] != self.FoldersRename.pathList[counter]:
				item.setData(QColor(146, 42, 232), Qt.ForegroundRole)
			self.modelfolder.setItem(row, 1, item)
			counter += 1
		self.tbl_viewresult.horizontalHeader().setStretchLastSection(False)
		self.tbl_viewresult.resizeColumnsToContents()
		self.tbl_viewresult.horizontalHeader().setStretchLastSection(True)
		self.btn_run.setEnabled(len(self.FoldersRename.backList) > 0)
		self.btn_test.setEnabled(len(self.FoldersRename.backList) > 0)
	
	def popUpTreeActions(self, position):
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
		column = 1
		for itemlist in self.listcolumnsactions[value]:
			if itemlist == '---':
				# no params
				item = QStandardItem('-')
				#item.setData(QColor(166, 153, 152), Qt.BackgroundRole)
				self.modelactions.setItem(row, column - 1, item)
			column += 1

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
		# build list actions
		self.buildListactions()

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
			newRow = rowNum + direction
			if not (0 <= newRow < model.rowCount()):
				continue
			rowItems = model.takeRow(rowNum)
			model.insertRow(newRow, rowItems)
		selModel.clear()
		for item in items:
			selModel.select(item.index(), selModel.Select|selModel.Rows)
		# rebuild combo
		self.buildComboActions(row + direction, value)
		# build list actions
		self.buildListactions()

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
