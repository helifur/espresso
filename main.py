import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QHeaderView, QTableWidgetItem, QDialog


class Add(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.setWindowTitle('Эспрессо')

        self.goBtn.clicked.connect(self.add)

    def add(self):
        cur = self.con.cursor()

        cur1 = self.con.cursor()
        idd = max(i[0] for i in cur.execute("SELECT ID FROM coffee").fetchall()) + 1
        cur1.close()

        data = [idd, self.titleEdit.text(), self.roastingEdit.text(), self.groundEdit.currentText(),
                self.descEdit.text(),
                self.priceEdit.text(), self.volumeEdit.text()]

        cur.execute("INSERT INTO coffee VALUES (?, ?, ?, ?, ?, ?, ?)", data)
        cur.close()
        self.con.commit()
        self.accept()


class Update(QDialog):
    def __init__(self, current, output):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.setWindowTitle('Эспрессо')
        self.output = output
        self.current = current

        self.fill_fields()
        self.goBtn.clicked.connect(self.update_data)

    def fill_fields(self):
        cur = self.con.cursor()

        obj = self.current[0]
        self.idd = self.output.item(obj.row(), 0).text()

        result = cur.execute(f"SELECT * FROM coffee WHERE id = {self.idd}").fetchone()
        print(result)
        cur.close()

        self.titleEdit.setText(result[1])
        self.roastingEdit.setText(result[2])
        self.groundEdit.setCurrentIndex(self.groundEdit.findText(result[3]))
        self.descEdit.setText(result[4])
        self.priceEdit.setValue(int(result[5]))
        self.volumeEdit.setValue(int(result[6]))

    def update_data(self):
        cur = self.con.cursor()

        new_data = [self.idd, self.titleEdit.text(), self.roastingEdit.text(), self.groundEdit.currentText(),
                    self.descEdit.text(),
                    self.priceEdit.text(), self.volumeEdit.text(), self.idd]

        cur.execute(
            "UPDATE coffee SET ID = '{}', title = '{}', degree_roasting = '{}', ground = '{}', "
            "description = '{}', price = '{}', volume = '{}' "
            "WHERE id = {}".format(*new_data))
        self.con.commit()
        self.accept()


class Main(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.setWindowTitle('Эспрессо')

        self.fill_work_table()

        self.addButton.clicked.connect(self.add)
        self.updateBtn.clicked.connect(self.update_data)

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

    def add(self):
        dlg = Add()
        dlg.exec()
        if dlg.result():
            self.fill_work_table()

    def update_data(self):
        dlg = Update(self.outputCoffee.selectedItems(), self.outputCoffee)
        dlg.exec()
        if dlg.result():
            self.fill_work_table()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
