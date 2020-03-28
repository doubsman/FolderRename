#! /usr/bin/python
# coding: utf-8

from PyQt5.QtWidgets import QApplication
from sys import argv
from FoldersRename import FoldersRename


if __name__ == '__main__':
	app = QApplication(argv)
	if len(argv)>1:
		# prod
		myfolder = argv[1]
	else:
		# test envt
		myfolder = r'D:\WorkDev\MP3TrtFiles'
	# build class process
	BuildProcess = FoldersRename()
	BuildProcess.folder_init(myfolder)
	BuildProcess.add_characters('Omiki ', 0)
	BuildProcess.move_characters(0, 5, 'max',' (',')')
	BuildProcess.replace_characters(' [320]', '')
	#BuildProcess.delete_characters(5,3)
	BuildProcess.folders_control()
	# processing
	BuildProcess.folders_rename()
