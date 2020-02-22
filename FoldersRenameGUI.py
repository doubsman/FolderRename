# #! /usr/bin/python
# coding: utf-8
from sys import argv
from Ui_MainWindow import Ui_Dialog
from FoldersRename import FoldersRename
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QStyle, QMenu, QComboBox



class FoldersRenameGUI(QMainWindow, Ui_Dialog):
	"""Init mini Gui constants."""
	DOWN = 1
	UP   = -1

	def __init__(self, parent=None):
		super(FoldersRenameGUI, self).__init__(parent)

		self.parent = parent
		self.setupUi(self)
		self.setWindowIcon(QIcon('FoldersRenameGUI.ico'))
		self.setWindowTitle('Folders Rename Managment 1.0')
		self.btn_selectfolder.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
		self.btn_selectfolder.clicked.connect(self.selectFolder)
		self.btn_rename.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
		self.btn_rename.setText('Rename')
		self.btn_test.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
		self.btn_test.setText('Test')
		self.tbl_viewresult.horizontalHeader().setStretchLastSection(True)
		self.tbl_viewresult.verticalHeader().setVisible(False)
		self.tbl_viewresult.setStyleSheet("QHeaderView::section { background-color:black; color:white}")
		self.tbl_viewresult.setAlternatingRowColors(True)

		self.tbl_viewactions.horizontalHeader().setStretchLastSection(True)
		self.tbl_viewactions.verticalHeader().setVisible(False)
		self.tbl_viewactions.setStyleSheet("QHeaderView::section { background-color:black; color:white}")
		self.tbl_viewactions.setSelectionBehavior(self.tbl_viewactions.SelectRows)
		self.tbl_viewactions.setAlternatingRowColors(True)
		self.tbl_viewactions.setSortingEnabled(True)
		
		# combo actions
		self.listeactions = ['-', 'move_characters', 'replace_characters','add_characters','delete_characters']

		# pop up
		self.menua = QMenu()
		self.action1 = self.menua.addAction("add", self.add_action)
		self.action2 = self.menua.addAction("remove", self.remove_action)
		self.action3 = self.menua.addAction("up", lambda n=self.UP: self.move_action(n))
		self.action4 = self.menua.addAction("down", lambda n=self.DOWN: self.move_action(n))
		self.tbl_viewactions.setContextMenuPolicy(Qt.CustomContextMenu)
		self.tbl_viewactions.customContextMenuRequested.connect(self.popUpTreeAlbums)

		# init
		self.pathfolder = None
		self.initTables()
		self.FoldersRename = FoldersRename()

	def selectFolder(self):
		self.pathfolder = QFileDialog.getExistingDirectory(self, "Select Directory")
		self.lin_pathfolder.setText(self.pathfolder.replace('/','\\'))
		self.FoldersRename.folder_init(self.pathfolder)
		self.fillTablefolder()
	
	def testFoldersRename(self):
		self.FoldersRename.folders_control()

	def runFoldersRename(self):
		self.FoldersRename.folders_rename()
	
	def initTables(self):
		# columns name
		self.modelactions = QStandardItemModel(20, 2, self)
		self.modelactions.setHorizontalHeaderLabels(['Actions','Params1','Params2','Params3','Params4','Params5'])
		self.tbl_viewactions.setModel(self.modelactions)
		# combos actions
		for row in range(self.modelactions.rowCount()):
			combo_actions = QComboBox(self)
			combo_actions.addItems(self.listeactions)
			i = self.tbl_viewactions.model().index(row , 0)
			self.tbl_viewactions.setIndexWidget(i, combo_actions)
		# columns width 
		sizecol = [150, 100, 100, 100, 100, 100]
		for ind in range(len(sizecol)):
			self.tbl_viewactions.setColumnWidth(ind, sizecol[ind])
		# format result
		self.modelfolder = QStandardItemModel(20, 2, self)
		self.modelfolder.setHorizontalHeaderLabels(['Actual','New'])
		self.tbl_viewresult.setModel(self.modelfolder)

	def fillTablefolder(self):
		self.modelfolder = QStandardItemModel(len(self.FoldersRename.pathList), 2, self)
		self.modelfolder.setHorizontalHeaderLabels(['Actual','New'])
		self.tbl_viewresult.setModel(self.modelfolder)
		counter = 0
		for row in range(self.modelfolder.rowCount()):
			item = QStandardItem(self.FoldersRename.backList[counter])
			self.modelfolder.setItem(row, 0, item)
			item = QStandardItem(self.FoldersRename.backList[counter])
			self.modelfolder.setItem(row, 1, item)
			counter += 1
	
	def popUpTreeAlbums(self, position):
		self.menua.exec_(self.tbl_viewactions.viewport().mapToGlobal(position))

	def add_action(self):
		pass

	def remove_action(self):
		pass

	def move_action(self, direction = DOWN):
		if direction not in (self.DOWN, self.UP):
			return
		model = self.modelactions
		selModel = self.tbl_viewactions.selectionModel()
		selected = selModel.selectedRows()
		if not selected:
			return
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


if __name__ == '__main__':
	app = QApplication(argv)
	DB = FoldersRenameGUI()
	DB.show()
	rc = app.exec_()
	exit(rc)
