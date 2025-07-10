import sys
from PyQt5.QtWidgets import QApplication
from database import Database
from ui_main import MainWindow

app = QApplication(sys.argv)
db = Database()
window = MainWindow(db)
window.show()
sys.exit(app.exec_())