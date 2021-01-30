import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QApplication

def appWait(milliseconds=3000):
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(milliseconds, loop.quit)
    loop.exec_()

def setWaitCursor(funct):
    def wrapper(*args,**kwargs):
        QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        try:
            result = funct(*args,**kwargs)
            appWait(1000)
            return result
        finally:
            QApplication.restoreOverrideCursor()
    return wrapper