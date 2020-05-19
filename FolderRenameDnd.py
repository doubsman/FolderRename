from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit


class QLineEditDnd(QLineEdit):
	# signal
	signalchgtfolder = pyqtSignal(str)		# add path

	def __init__ (self, parent):
		"""Init QLineEdit Dnd."""
		super(QLineEdit, self).__init__(parent)
		self.setAcceptDrops(True)

	def dragEnterEvent (self, event):
		"""Accept url"""
		if event.mimeData().hasUrls():
			event.acceptProposedAction()

	def dropEvent (self, event):
		event.setAccepted(True)
		if event.mimeData().hasUrls():
			url = event.mimeData().urls()[0]
			urlpath = url.toLocalFile()
			self.setText(urlpath)
			self.signalchgtfolder.emit(urlpath)