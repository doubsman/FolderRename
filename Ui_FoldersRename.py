# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'R:\Python\FoldersRename\FoldersRename.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from FolderRenameDnd import QLineEditDnd


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lab_pathfolder = QtWidgets.QLabel(self.centralwidget)
        self.lab_pathfolder.setObjectName("lab_pathfolder")
        self.horizontalLayout.addWidget(self.lab_pathfolder)
        self.lin_pathfolder = QLineEditDnd(self)
        self.lin_pathfolder.setObjectName("lin_pathfolder")
        self.horizontalLayout.addWidget(self.lin_pathfolder)
        self.btn_selectfolder = QtWidgets.QPushButton(self.centralwidget)
        self.btn_selectfolder.setText("")
        self.btn_selectfolder.setObjectName("btn_selectfolder")
        self.horizontalLayout.addWidget(self.btn_selectfolder)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lin_filter = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lin_filter.sizePolicy().hasHeightForWidth())
        self.lin_filter.setSizePolicy(sizePolicy)
        self.lin_filter.setObjectName("lin_filter")
        self.horizontalLayout.addWidget(self.lin_filter)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tbl_viewactions = QtWidgets.QTableView(self.centralwidget)
        self.tbl_viewactions.setObjectName("tbl_viewactions")
        self.horizontalLayout_2.addWidget(self.tbl_viewactions)
        self.tbl_viewresult = QtWidgets.QTableView(self.centralwidget)
        self.tbl_viewresult.setObjectName("tbl_viewresult")
        self.horizontalLayout_2.addWidget(self.tbl_viewresult)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_load = QtWidgets.QPushButton(self.centralwidget)
        self.btn_load.setText("")
        self.btn_load.setObjectName("btn_load")
        self.horizontalLayout_3.addWidget(self.btn_load)
        self.btn_save = QtWidgets.QPushButton(self.centralwidget)
        self.btn_save.setText("")
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout_3.addWidget(self.btn_save)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.btn_cancel = QtWidgets.QPushButton(self.centralwidget)
        self.btn_cancel.setText("")
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout_3.addWidget(self.btn_cancel)
        self.btn_test = QtWidgets.QPushButton(self.centralwidget)
        self.btn_test.setText("")
        self.btn_test.setObjectName("btn_test")
        self.horizontalLayout_3.addWidget(self.btn_test)
        self.btn_run = QtWidgets.QPushButton(self.centralwidget)
        self.btn_run.setText("")
        self.btn_run.setObjectName("btn_run")
        self.horizontalLayout_3.addWidget(self.btn_run)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lab_pathfolder.setText(_translate("MainWindow", "Path"))
        self.label.setText(_translate("MainWindow", "Filter"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
