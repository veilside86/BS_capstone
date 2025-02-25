from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QLabel
import school_api
import sys
from pathlib import Path

columns = ['area_title', 'occ_title', 'tot_emp', 'h_pct25', 'a_pct25', 'occ_code']


class Ui_MainWindow(QMainWindow):
    def update_data(self, filename):
        conn, cursor = school_api.open_db("school_db.sqlite")
        school_api.save_excel_db(filename, conn)
        school_api.setup_db(cursor)
        query = "SELECT * FROM states"
        result = conn.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        conn.commit()
        conn.close()

    def update_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Choose an excel file", "", "Excel(*.xls *.xlsx)")
        filename = Path(file).name
        self.update_data(filename)

    def setup_ui(self, mainwindow):
        mainwindow.setObjectName("MainWindow")
        mainwindow.resize(750, 650)

        # tablewidget to show data
        self.centralwidget = QtWidgets.QWidget(mainwindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 700, 500))
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(columns)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setStyleSheet("Color: green")

        # button to load excel file
        self.btn_update = QtWidgets.QPushButton(self.centralwidget)
        self.btn_update.setGeometry(QtCore.QRect(10, 540, 110, 40))
        self.btn_update.setObjectName("btn_update")
        self.btn_update.clicked.connect(self.update_file)

        # button to exit program
        self.btn_quit = QtWidgets.QPushButton(self.centralwidget)
        self.btn_quit.setGeometry(QtCore.QRect(600, 540, 110, 40))
        self.btn_quit.setObjectName("btn_quit")
        self.btn_quit.clicked.connect(QApplication.instance().quit)

        # Label to show sort method
        self.lb_ascending = QLabel(mainwindow)
        self.lb_ascending.setGeometry(QtCore.QRect(150, 540, 110, 20))
        self.lb_ascending.setObjectName("lb_ascending")

        # ascending combobox; let the user choose the column
        self.cb_ascending = QtWidgets.QComboBox(self.centralwidget)
        self.cb_ascending.setGeometry(QtCore.QRect(150, 560, 110, 20))
        self.cb_ascending.setObjectName("cb_ascending")
        self.cb_ascending.addItems(columns)
        # self.cb_ascending.activated.connect(self.do_something)
        self.cb_ascending.activated[str].connect(self.sort_by_ascending)

        # label to show sort method
        self.lb_descending = QLabel(mainwindow)
        self.lb_descending.setGeometry(QtCore.QRect(300, 540, 110, 20))
        self.lb_descending.setObjectName("lb_descending")

        # descending combobox; let the user choose the column
        self.cb_descending = QtWidgets.QComboBox(self.centralwidget)
        self.cb_descending.setGeometry(QtCore.QRect(300, 560, 110, 20))
        self.cb_descending.setObjectName("cb_descending")
        self.cb_descending.addItems(columns)
        self.cb_descending.activated[str].connect(self.sort_by_descending)

        mainwindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainwindow)
        self.statusbar.setObjectName("statusbar")
        mainwindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainwindow)
        QtCore.QMetaObject.connectSlotsByName(mainwindow)

    def sort_by_ascending(self, text):
        self.tableWidget.setStyleSheet("Color: green")
        conn, cursor = school_api.open_db("school_db.sqlite")
        query = f"SELECT * FROM states ORDER BY {text};"
        result = conn.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

    def sort_by_descending(self, text):
        self.tableWidget.setStyleSheet("Color: green")
        conn, cursor = school_api.open_db("school_db.sqlite")
        query = f"SELECT * FROM states ORDER BY {text} DESC;"
        result = conn.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

    def retranslateUi(self, mainwindow):
        _translate = QtCore.QCoreApplication.translate
        mainwindow.setWindowTitle(_translate("MainWindow", "Schools"))
        self.btn_update.setText(_translate("MainWindow", "Update"))
        self.btn_quit.setText(_translate("MainWindow", "Quit"))
        self.lb_ascending.setText(_translate("MainWindow", "Ascending"))
        self.lb_descending.setText(_translate("MainWindow", "Descending"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setup_ui(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())
