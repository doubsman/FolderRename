# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'r:\Python\FoldersRename\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1400, 900)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(5, 6, 1391, 891))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lin_pathfolder = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lin_pathfolder.setObjectName("lin_pathfolder")
        self.horizontalLayout_2.addWidget(self.lin_pathfolder)
        self.btn_selectfolder = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_selectfolder.setText("")
        self.btn_selectfolder.setObjectName("btn_selectfolder")
        self.horizontalLayout_2.addWidget(self.btn_selectfolder)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tbl_viewactions = QtWidgets.QTableView(self.verticalLayoutWidget)
        self.tbl_viewactions.setObjectName("tbl_viewactions")
        self.horizontalLayout.addWidget(self.tbl_viewactions)
        self.tbl_viewresult = QtWidgets.QTableView(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbl_viewresult.sizePolicy().hasHeightForWidth())
        self.tbl_viewresult.setSizePolicy(sizePolicy)
        self.tbl_viewresult.setObjectName("tbl_viewresult")
        self.horizontalLayout.addWidget(self.tbl_viewresult)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.btn_load = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_load.setObjectName("btn_load")
        self.horizontalLayout_4.addWidget(self.btn_load)
        self.btn_sav = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_sav.setObjectName("btn_sav")
        self.horizontalLayout_4.addWidget(self.btn_sav)
        self.btn_test = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_test.setObjectName("btn_test")
        self.horizontalLayout_4.addWidget(self.btn_test)
        self.btn_rename = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_rename.setObjectName("btn_rename")
        self.horizontalLayout_4.addWidget(self.btn_rename)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn_load.setText(_translate("Dialog", "Load"))
        self.btn_sav.setText(_translate("Dialog", "Save"))
        self.btn_test.setText(_translate("Dialog", "Test"))
        self.btn_rename.setText(_translate("Dialog", "Run"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
