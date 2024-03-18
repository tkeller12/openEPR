from PyQt5 import QtWidgets
import sys

# Local Module Imports
import openEPR

# Create GUI application
app = QtWidgets.QApplication(sys.argv)
main = openEPR.MyWindow()
main.show()
sys.exit(app.exec_())
