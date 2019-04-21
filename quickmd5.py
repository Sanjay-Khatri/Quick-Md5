# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'genrator.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
import os
import re
import hashlib
import time
import threading


from PyQt5 import QtCore, QtGui, QtWidgets

global ext
global path
global fname
fname = []
global chksum
chksum = []


def name():
    print("helllo")

class Ui_MainWindow(object):

    def checker(self):
        try:
            global fname, chksum, path

            fname = []
            chksum = []
            self.tableWidget.setRowCount(0)
            chk = QtWidgets.QFileDialog().getOpenFileName()
            print(chk)
            print(chk[0])
            print(chk[0].rfind('/'))
            with open(chk[0], 'r') as reader:
                for rea in reader:
                    if rea == "CHECKSUMS>>>\n":
                        break
                    fname.append(rea)
                for rea in reader:
                    chksum.append(rea)

            print(chksum)
            print(fname)
            count = 0

            if len(fname) == len(chksum):
                MainWindow.setWindowTitle("Don't Panic if it stuck....")
                self.statusbar.showMessage("Comparing Checksums")
                print(fname)
                print(chksum)
                for file in fname:
                    numrow = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(numrow)
                    self.tableWidget.setItem(numrow, 0, QtWidgets.QTableWidgetItem(file))
                    self.tableWidget.setItem(numrow, 1, QtWidgets.QTableWidgetItem("Unknown"))
                    self.tableWidget.setItem(numrow, 2, QtWidgets.QTableWidgetItem(chksum[count]))
                    count += 1

                dirt = chk[0].rfind('/')
                dirt1 = chk[0]
                path = dirt1[:dirt]

                print(path)

                count = 0
                for fi in fname:
                    self.tableWidget.setItem(count, 1, QtWidgets.QTableWidgetItem("GENRATING"))
                    count += 1
                genra = ''
                count = 0
                print(fname)
                for file in fname:
                    name = path + '/' + file[:len(file) - 1]
                    print("NAME==" + name)
                    md = hashlib.md5()
                    with open(name, "rb") as reader:
                        while True:
                            data = reader.read(1024)
                            if not data:
                                break
                            md.update(data)
                            genra = md.hexdigest()

                    print(genra)
                    comp = chksum[count]
                    # print("comp===" + comp)
                    if genra == comp[:len(comp) - 1]:

                        self.tableWidget.setItem(count, 1, QtWidgets.QTableWidgetItem("MATCHED"))
                        self.tableWidget.item(count,1).setForeground(QtGui.QColor(0,255,0))


                    else:
                        self.tableWidget.setItem(count, 1, QtWidgets.QTableWidgetItem("UNMATCHED"))
                        self.tableWidget.item(count, 1).setForeground(QtGui.QColor(255, 0, 0))

                    count += 1
                self.save.setEnabled(False)
                self.load.setEnabled(False)
                self.genrate.setEnabled(False)
                MainWindow.setWindowTitle("QuickMD5©")
                self.statusbar.showMessage("")

            else:
                QtWidgets.QMessageBox.about(QtWidgets.QMessageBox(), "OOPS!",
                                            "FILE NOT RECOGNIZE\t\n ")
                fname = []
                chksum = []
                path = ''


        except IOError:
            print("no file")

        except Exception as e:
            QtWidgets.QMessageBox.about(QtWidgets.QMessageBox(), "OOPS!",
                                        "Problem occur in CHECKER.\t\n ")
            self.statusbar.showMessage(e)
            print(e)



    def saved(self):
        try:
            name = path + '/CheckSum.md5'
            with open(name, 'w') as writer:
                for f in fname:
                    print(f, file=writer)
                print("CHECKSUMS>>>", file=writer)
                for ch in chksum:
                    print(ch, file=writer)

                self.statusbar.showMessage("CHECKSUMs save.")

        except:
            QtWidgets.QMessageBox.about(QtWidgets.QMessageBox(), "OOPS!",
                                        "Problem occur in SAVED\t")
            self.statusbar.showMessage(e)

    def resetter(self):

        try:
            global path, ext, fname, chksum
            path = ''
            ext = []
            fname = []
            chksum = []
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.tableWidget.setRowCount(0)
            self.save.setDisabled(True)
            self.genrate.setDisabled(True)
            self.lineEdit.setEnabled(True)
            self.statusbar.showMessage("")
            print(chksum)
            print(fname)


        except:
            QtWidgets.QMessageBox.about(QtWidgets.QMessageBox(), "OOPS!",
                                        "Problem occur in RESETTER\t")
            self.statusbar.showMessage(e)

    def gen(self):
        try:

            global fname
            self.tableWidget.setRowCount(0)
            fname=[]
            def multi_find(patterns, phrase):
                global ext
                for pattern in patterns:
                    print("searching for pattern {}".format(pattern))
                    ext = re.findall(pattern, phrase)
                    print("\n")

            test_phrase = self.lineEdit_2.text()
            test_pattern = ['.[a-z 0-9]+']
            multi_find(test_pattern, test_phrase.lower())
            print(ext)

            def searcher():
                filename = os.listdir(path)
                count = 0
                for e in ext:

                    for file in filename:
                        if re.findall(e, file):
                            fname.append(file)
                            numrow = self.tableWidget.rowCount()
                            self.tableWidget.insertRow(numrow)
                            self.tableWidget.setItem(numrow, 0, QtWidgets.QTableWidgetItem(file))
                            self.tableWidget.setItem(numrow, 1, QtWidgets.QTableWidgetItem("..."))
                            self.tableWidget.setItem(numrow, 2, QtWidgets.QTableWidgetItem("..."))
                            count += 1
                self.statusbar.showMessage(str(count) + " Files are LOADED")

            searcher()

            self.genrate.setDisabled(False)
            print(chksum)
            print(fname)
            if fname == []:
                self.genrate.setDisabled(True)
                QtWidgets.QMessageBox.about(QtWidgets.QMessageBox(), "OOPS!",
                                            "No file present for the given EXTENSION in the given DIRECTORY\t")


        except Exception as e:
            QtWidgets.QMessageBox.about(QtWidgets.QMessageBox(), "OOPS!",
                                        "Something went wrong.\t\n Either DIRECTORY or EXTENSION are not given. ")
            self.statusbar.showMessage(e)

    def checksum(self):

        try:
            MainWindow.setWindowTitle("Don't Panic if it stuck....")
            QtWidgets.QMessageBox.about(QtWidgets.QMessageBox(), "Warning",
                                        "Sometimes the application became NOT RESPONDING due to large files\t\n so Don't WORRY.")
            count = 0
            for fi in fname:
                self.tableWidget.setItem(count, 1, QtWidgets.QTableWidgetItem("GENRATING"))
                self.tableWidget.setItem(count, 2, QtWidgets.QTableWidgetItem("WAIT"))

                count += 1
            genra=''
            count = 0
            msg = "Genrating Checksum please WAIT... "
            starttime = time.time()
            self.statusbar.showMessage(msg)
            totalsize = 0
            for file in fname:

                name = path + '/' + file
                filesize = os.path.getsize(name)
                totalsize += filesize
                print(name)
                md = hashlib.md5()
                with open(name, "rb") as reader:

                    while True:
                        data = reader.read(1024)

                        if not data:
                            break
                        md.update(data)
                        genra = md.hexdigest()

                print(genra)
                chksum.append(genra)
                self.tableWidget.setItem(count, 1, QtWidgets.QTableWidgetItem("GENRATED"))
                self.tableWidget.item(count, 1).setForeground(QtGui.QColor(0, 255, 0))
                self.tableWidget.setItem(count, 2, QtWidgets.QTableWidgetItem(genra))
                count += 1

            endtime = time.time()
            msg = str(count) + " Checksums Are Genrated" + "         "+"Total Size: "+str(round(totalsize/(1024*1024),2))+"MB"+ "         "+" Time Required: "+str(round(endtime-starttime,2))+"sec"
            self.statusbar.showMessage(msg)
            MainWindow.setWindowTitle("QuickMD5©")
            self.save.setDisabled(False)
            print(chksum)
            print(fname)


        except:
            QtWidgets.QMessageBox.about(QtWidgets.QMessageBox(), "OOPS!",
                                        "Problem occur in CHECKSUM\t")
            self.statusbar.showMessage(e)

    def openFileNameDialog(self):
        try:
            global path
            fname = QtWidgets.QFileDialog().getExistingDirectory()
            if fname != '':
                path = fname
                self.lineEdit.setText(fname)
                self.lineEdit_2.setDisabled(False)
                self.load.setDisabled(False)

        except Exception as e:
            QtWidgets.QMessageBox.about(QtWidgets.QMessageBox(), "OOPS!",
                                        "Problem occur in OPEN-FILE\t")

            print(e)
            self.statusbar.showMessage(e)



    def aboutmenu(self):
        QtWidgets.QMessageBox.about(QtWidgets.QMessageBox(), "ABOUT",
                                    "This is the BETA-PHASE of this application which is only for        \t \n                                     Testing PURPOSE.\n\n                        Develop By :  SANJAY KHATRI (*_*)\n")

    def helper(self):
        print("help")

    def fileopener(self):
        try:
            global fname, path,chksum

            fname = []
            chksum = []
            self.tableWidget.setRowCount(0)
            filenames = QtWidgets.QFileDialog().getOpenFileNames()
            count = 0
            for file in filenames[0]:
                print(file)
                indx = file.rfind('/')
                path =file[:indx]
                filename = file[indx+1:len(file)]
                fname.append(filename)
                numrow = self.tableWidget.rowCount()
                self.tableWidget.insertRow(numrow)
                self.tableWidget.setItem(numrow, 0, QtWidgets.QTableWidgetItem(filename))
                self.tableWidget.setItem(numrow, 1, QtWidgets.QTableWidgetItem("..."))
                self.tableWidget.setItem(numrow, 2, QtWidgets.QTableWidgetItem("..."))
                count +=1
            self.statusbar.showMessage(str(count) + " Files are LOADED")
            print(path)
            print(fname)
            self.load.setEnabled(False)
            self.genrate.setEnabled(True)
            self.lineEdit.setEnabled(False)
            self.lineEdit_2.setEnabled(False)


        except Exception as e:
            print(e)
            fname = []
            path = ''
            self.statusbar.showMessage(e)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        self.app = QtWidgets.QApplication(sys.argv)
        screen = app.primaryScreen()
        screen_width = screen.size().width()
        screen_height = screen.size().height()


        MainWindow.resize(screen_width*0.44, screen_height*0.65)
        MainWindow.setFixedHeight(screen_height*0.65)
        MainWindow.setFixedWidth(screen_width*0.447)

        MainWindow.setWindowIcon(QtGui.QIcon("D:\original.png"))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_3.addWidget(self.lineEdit_2)

        self.reset = QtWidgets.QPushButton(self.centralwidget)
        self.reset.setObjectName("reset")
        self.horizontalLayout_3.addWidget(self.reset)
        self.reset.clicked.connect(self.resetter)

        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_2.addWidget(self.line_2)
        self.lineEdit_2.setDisabled(True)

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setObjectName("tableWidget")
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.tableWidget.setHorizontalHeaderLabels(['Name', 'Status', 'MD5'])
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setColumnWidth(0, screen_width*0.17)
        self.tableWidget.setColumnWidth(1, screen_width*0.06)
        self.tableWidget.setColumnWidth(2, screen_width*0.17)
        self.tableWidget.horizontalScrollBar()

        self.gridLayout.addLayout(self.verticalLayout_2, 4, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.load = QtWidgets.QPushButton(self.centralwidget)
        self.load.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.load)
        self.load.clicked.connect(self.gen)
        self.load.setEnabled(False)

        self.genrate = QtWidgets.QPushButton(self.centralwidget)
        self.genrate.setObjectName("genrate")
        self.horizontalLayout.addWidget(self.genrate)
        self.genrate.clicked.connect(self.checksum)
        self.genrate.setDisabled(True)

        self.check = QtWidgets.QPushButton(self.centralwidget)
        self.check.setObjectName("check")
        self.horizontalLayout.addWidget(self.check)
        self.check.clicked.connect(self.checker)

        self.save = QtWidgets.QPushButton(self.centralwidget)
        self.save.setObjectName("save")
        self.horizontalLayout.addWidget(self.save)
        self.save.clicked.connect(self.saved)
        self.save.setDisabled(True)

        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)


        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.open = QtWidgets.QPushButton(self.centralwidget)
        self.open.setObjectName("open")
        self.horizontalLayout_2.addWidget(self.open)
        self.open.clicked.connect(self.openFileNameDialog)

        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 442, 21))
        self.menubar.setObjectName("menubar")
        self.menuAbout_2 = QtWidgets.QMenu(self.menubar)
        self.menuAbout_2.setObjectName("menuAbout_2")

        self.about = self.menuAbout_2.addAction("Open...")
        self.about.triggered.connect(self.fileopener)

        self.about = self.menuAbout_2.addAction("About")
        self.about.triggered.connect(self.aboutmenu)


        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuAbout_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QuickMD5©"))
        self.label_2.setText(_translate("MainWindow", "Extension"))
        self.reset.setText(_translate("MainWindow", "Reset"))
        self.load.setText(_translate("MainWindow", "Load"))
        self.genrate.setText(_translate("MainWindow", "Genrate"))
        self.check.setText(_translate("MainWindow", "Check"))
        self.save.setText(_translate("MainWindow", "Save"))
        self.label.setText(_translate("MainWindow", "Directory "))
        self.open.setText(_translate("MainWindow", "Open"))
        self.menuAbout_2.setTitle(_translate("MainWindow", "Menu"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
