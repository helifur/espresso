import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QHeaderView, QTableWidgetItem


class Main(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.setWindowTitle('Эспрессо')

        self.fill_work_table()

    def fill_work_table(self):
        sql = "SELECT * FROM coffee"

        cur = self.con.cursor()
        data = cur.execute(sql).fetchall()
        headers = cur.description
        headers = [headers[i][0] for i in range(len(headers))]
        cur.close()

        self.outputCoffee.setColumnCount(len(headers))
        self.outputCoffee.setHorizontalHeaderLabels(headers)
        header = self.outputCoffee.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.outputCoffee.setRowCount(0)

        for i, row in enumerate(data):
            self.outputCoffee.setRowCount(self.outputCoffee.rowCount() + 1)
            for j, elem in enumerate(row):
                self.outputCoffee.setItem(i, j, QTableWidgetItem(str(elem)))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
