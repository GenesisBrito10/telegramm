

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(846, 500)
        MainWindow.setMinimumSize(QtCore.QSize(846, 500))
        MainWindow.setMaximumSize(QtCore.QSize(846, 500))
        MainWindow.setWindowTitle("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("D:/Robô Telegram Pro/Views/UI\\../Icons/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QtCore.QSize(64, 64))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 841, 431))
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setObjectName("tabWidget")
        self.tabContas = QtWidgets.QWidget()
        self.tabContas.setObjectName("tabContas")
        self.tableContas = QtWidgets.QTableWidget(self.tabContas)
        self.tableContas.setGeometry(QtCore.QRect(10, 50, 821, 351))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tableContas.setFont(font)
        self.tableContas.setStyleSheet("QHeaderView::section {\n"
"    background-color: rgb(227, 227, 227);\n"
"    border:1px solid #D8D8D8;\n"
"    height: 32px;\n"
"}")
        self.tableContas.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableContas.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableContas.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableContas.setObjectName("tableContas")
        self.tableContas.setColumnCount(5)
        self.tableContas.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableContas.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableContas.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableContas.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableContas.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableContas.setHorizontalHeaderItem(4, item)
        self.tableContas.horizontalHeader().setDefaultSectionSize(140)
        self.tableContas.horizontalHeader().setStretchLastSection(True)
        self.tableContas.verticalHeader().setVisible(False)
        self.btnAddConta = QtWidgets.QPushButton(self.tabContas)

        self.btnAddConta.setEnabled(True)
        self.btnAddConta.setGeometry(QtCore.QRect(10, 10, 150, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnAddConta.setFont(font)
        self.btnAddConta.setStyleSheet("QPushButton:enabled {\n"
"    background-color: rgb(44, 163, 222);\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color:rgb(185, 185, 185);\n"
"    color: white;\n"
"}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("D:/Robô Telegram Pro/Views/UI\\../Icons/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAddConta.setIcon(icon1)
        self.btnAddConta.setObjectName("btnAddConta")
        self.btnRemoveConta = QtWidgets.QPushButton(self.tabContas)
        self.btnRemoveConta.setGeometry(QtCore.QRect(330, 10, 150, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnRemoveConta.setFont(font)
        self.btnRemoveConta.setStyleSheet("QPushButton:enabled {\n"
"    background-color: rgb(44, 163, 222);\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color:rgb(185, 185, 185);\n"
"    color: white;\n"
"}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("D:/Robô Telegram Pro/Views/UI\\../Icons/rubbish-bin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRemoveConta.setIcon(icon2)
        self.btnRemoveConta.setObjectName("btnRemoveConta")
        self.btnImportConta = QtWidgets.QPushButton(self.tabContas)
        self.btnImportConta.setGeometry(QtCore.QRect(170, 10, 150, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnImportConta.setFont(font)
        self.btnImportConta.setStyleSheet("QPushButton:enabled {\n"
"    background-color: rgb(44, 163, 222);\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color:rgb(185, 185, 185);\n"
"    color: white;\n"
"}")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("D:/Robô Telegram Pro/Views/UI\\../Icons/import.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnImportConta.setIcon(icon3)
        self.btnImportConta.setObjectName("btnImportConta")
        self.btnDesbloquearFlood = QtWidgets.QPushButton(self.tabContas)
        self.btnDesbloquearFlood.setEnabled(False)
        self.btnDesbloquearFlood.setGeometry(QtCore.QRect(489, 10, 161, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnDesbloquearFlood.setFont(font)
        self.btnDesbloquearFlood.setStyleSheet("QPushButton:enabled {\n"
"    background-color: rgb(255, 112, 10);\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color:rgb(185, 185, 185);\n"
"    color: white;\n"
"}")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("D:/Robô Telegram Pro/Views/UI\\../Icons/unlock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDesbloquearFlood.setIcon(icon4)
        self.btnDesbloquearFlood.setObjectName("btnDesbloquearFlood")
       
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("D:/Robô Telegram Pro/Views/UI\\../Icons/phone-call.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabContas, icon6, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tableGrupos = QtWidgets.QTableWidget(self.tab)
        self.tableGrupos.setGeometry(QtCore.QRect(10, 50, 821, 351))
        self.tableGrupos.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableGrupos.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableGrupos.setObjectName("tableGrupos")
        self.tableGrupos.setColumnCount(3)
        self.tableGrupos.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableGrupos.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableGrupos.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableGrupos.setHorizontalHeaderItem(2, item)
        self.tableGrupos.horizontalHeader().setDefaultSectionSize(150)
        self.tableGrupos.horizontalHeader().setStretchLastSection(True)
        self.tableGrupos.verticalHeader().setVisible(False)
        self.btnRemoveGrupo = QtWidgets.QPushButton(self.tab)
        self.btnRemoveGrupo.setGeometry(QtCore.QRect(680, 10, 150, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnRemoveGrupo.setFont(font)
        self.btnRemoveGrupo.setStyleSheet("QPushButton:enabled {\n"
"    background-color: rgb(44, 163, 222);\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color:rgb(185, 185, 185);\n"
"    color: white;\n"
"}")
        self.btnRemoveGrupo.setIcon(icon2)
        self.btnRemoveGrupo.setObjectName("btnRemoveGrupo")
        self.btnAddGrupo = QtWidgets.QPushButton(self.tab)
        self.btnAddGrupo.setEnabled(True)
        self.btnAddGrupo.setGeometry(QtCore.QRect(520, 10, 150, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnAddGrupo.setFont(font)
        self.btnAddGrupo.setStyleSheet("QPushButton:enabled {\n"
"    background-color: rgb(44, 163, 222);\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color:rgb(185, 185, 185);\n"
"    color: white;\n"
"}")
        self.btnAddGrupo.setIcon(icon1)
        self.btnAddGrupo.setObjectName("btnAddGrupo")
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(0, 0, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("D:/Robô Telegram Pro/Views/UI\\../Icons/add-group.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab, icon7, "")
        self.tabAquecerConta = QtWidgets.QWidget()
        self.tabAquecerConta.setObjectName("tabAquecerConta")
        self.tableAquecendo = QtWidgets.QTableWidget(self.tabAquecerConta)
        self.tableAquecendo.setGeometry(QtCore.QRect(10, 50, 811, 351))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tableAquecendo.setFont(font)
        self.tableAquecendo.setStyleSheet("QHeaderView::section {\n"
"    background-color: rgb(227, 227, 227);\n"
"    border:1px solid #D8D8D8;\n"
"    height: 32px;\n"
"}")
        self.tableAquecendo.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableAquecendo.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableAquecendo.setObjectName("tableAquecendo")
        self.tableAquecendo.setColumnCount(5)
        self.tableAquecendo.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableAquecendo.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableAquecendo.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableAquecendo.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableAquecendo.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableAquecendo.setHorizontalHeaderItem(4, item)
        self.tableAquecendo.horizontalHeader().setStretchLastSection(True)
        self.tableAquecendo.verticalHeader().setVisible(False)
        self.btnAddAquecendo = QtWidgets.QPushButton(self.tabAquecerConta)
        self.btnAddAquecendo.setEnabled(True)
        self.btnAddAquecendo.setGeometry(QtCore.QRect(510, 10, 150, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnAddAquecendo.setFont(font)
        self.btnAddAquecendo.setStyleSheet("QPushButton:enabled {\n"
"    background-color: rgb(44, 163, 222);\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color:rgb(185, 185, 185);\n"
"    color: white;\n"
"}")
        self.btnAddAquecendo.setIcon(icon1)
        self.btnAddAquecendo.setObjectName("btnAddAquecendo")
        self.btnRemoveAquecendo = QtWidgets.QPushButton(self.tabAquecerConta)
        self.btnRemoveAquecendo.setGeometry(QtCore.QRect(670, 10, 150, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnRemoveAquecendo.setFont(font)
        self.btnRemoveAquecendo.setStyleSheet("QPushButton:enabled {\n"
"    background-color: rgb(44, 163, 222);\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color:rgb(185, 185, 185);\n"
"    color: white;\n"
"}")
        self.btnRemoveAquecendo.setIcon(icon2)
        self.btnRemoveAquecendo.setObjectName("btnRemoveAquecendo")
        self.label_4 = QtWidgets.QLabel(self.tabAquecerConta)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 491, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("D:/Robô Telegram Pro/Views/UI\\../Icons/fire.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabAquecerConta, icon8, "")
        self.tabGrupos = QtWidgets.QWidget()
        self.tabGrupos.setObjectName("tabGrupos")
        self.label = QtWidgets.QLabel(self.tabGrupos)
        self.label.setGeometry(QtCore.QRect(10, 10, 341, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.tableTarefasGrupo = QtWidgets.QTableWidget(self.tabGrupos)
        self.tableTarefasGrupo.setGeometry(QtCore.QRect(10, 50, 821, 351))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tableTarefasGrupo.setFont(font)
        self.tableTarefasGrupo.setStyleSheet("QHeaderView::section {\n"
"    background-color: rgb(227, 227, 227);\n"
"    border:1px solid #D8D8D8;\n"
"    height: 32px;\n"
"}")
        self.tableTarefasGrupo.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableTarefasGrupo.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableTarefasGrupo.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableTarefasGrupo.setObjectName("tableTarefasGrupo")
        self.tableTarefasGrupo.setColumnCount(8)
        self.tableTarefasGrupo.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableTarefasGrupo.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableTarefasGrupo.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableTarefasGrupo.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableTarefasGrupo.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableTarefasGrupo.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableTarefasGrupo.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableTarefasGrupo.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableTarefasGrupo.setHorizontalHeaderItem(7, item)
        self.tableTarefasGrupo.horizontalHeader().setStretchLastSection(True)
        self.tableTarefasGrupo.verticalHeader().setVisible(False)
        self.btnAddTarefaGrupo = QtWidgets.QPushButton(self.tabGrupos)
        self.btnAddTarefaGrupo.setGeometry(QtCore.QRect(360, 10, 150, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnAddTarefaGrupo.setFont(font)
        self.btnAddTarefaGrupo.setStyleSheet("QPushButton:enabled {\n"
"    background-color: rgb(44, 163, 222);\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color:rgb(185, 185, 185);\n"
"    color: white;\n"
"}")
        self.btnAddTarefaGrupo.setIcon(icon1)
        self.btnAddTarefaGrupo.setObjectName("btnAddTarefaGrupo")
        self.btnRemoveTarefaGrupo = QtWidgets.QPushButton(self.tabGrupos)
        self.btnRemoveTarefaGrupo.setEnabled(False)
        self.btnRemoveTarefaGrupo.setGeometry(QtCore.QRect(520, 10, 150, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnRemoveTarefaGrupo.setFont(font)
        self.btnRemoveTarefaGrupo.setStyleSheet("QPushButton:enabled {\n"
"    background-color: rgb(44, 163, 222);\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color:rgb(185, 185, 185);\n"
"    color: white;\n"
"}")
        self.btnRemoveTarefaGrupo.setIcon(icon2)
        self.btnRemoveTarefaGrupo.setObjectName("btnRemoveTarefaGrupo")
        self.btnDetalhesTarefa = QtWidgets.QPushButton(self.tabGrupos)
        self.btnDetalhesTarefa.setEnabled(False)
        self.btnDetalhesTarefa.setGeometry(QtCore.QRect(680, 10, 150, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnDetalhesTarefa.setFont(font)
        self.btnDetalhesTarefa.setStyleSheet("QPushButton:enabled {\n"
"    background-color: rgb(44, 163, 222);\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color:rgb(185, 185, 185);\n"
"    color: white;\n"
"}")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("D:/Robô Telegram Pro/Views/UI\\../Icons/details.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDetalhesTarefa.setIcon(icon9)
        self.btnDetalhesTarefa.setObjectName("btnDetalhesTarefa")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("D:/Robô Telegram Pro/Views/UI\\../Icons/group.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabGrupos, icon10, "")
        self.tabListas = QtWidgets.QWidget()
        self.tabListas.setObjectName("tabListas")
        self.tableListas = QtWidgets.QTableWidget(self.tabListas)
        self.tableListas.setGeometry(QtCore.QRect(10, 50, 821, 351))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tableListas.setFont(font)
        self.tableListas.setStyleSheet("QHeaderView::section {\n"
"    background-color: rgb(227, 227, 227);\n"
"    border:1px solid #D8D8D8;\n"
"    height: 32px;\n"
"}")
        self.tableListas.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableListas.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableListas.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableListas.setObjectName("tableListas")
        self.tableListas.setColumnCount(5)
        self.tableListas.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableListas.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableListas.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableListas.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableListas.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableListas.setHorizontalHeaderItem(4, item)
        self.tableListas.horizontalHeader().setDefaultSectionSize(150)
        self.tableListas.horizontalHeader().setStretchLastSection(True)
        self.tableListas.verticalHeader().setVisible(False)
        self.label_2 = QtWidgets.QLabel(self.tabListas)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 501, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.btnAddLista = QtWidgets.QPushButton(self.tabListas)
        self.btnAddLista.setGeometry(QtCore.QRect(520, 10, 150, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnAddLista.setFont(font)
        self.btnAddLista.setStyleSheet("QPushButton:enabled {\n"
"    background-color: rgb(44, 163, 222);\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color:rgb(185, 185, 185);\n"
"    color: white;\n"
"}")
        self.btnAddLista.setIcon(icon1)
        self.btnAddLista.setObjectName("btnAddLista")
        self.btn_abrirPasta = QtWidgets.QPushButton("Abrir Pasta")
        self.btn_abrirPasta.setStyleSheet("""
        QPushButton {
            background-color: rgb(44, 163, 222);
            color: white;
        }
        QPushButton:disabled {
            background-color: rgb(185, 185, 185);
            color: white;
        }
    """)
        self.btnRemoveLista = QtWidgets.QPushButton(self.tabListas)
        self.btnRemoveLista.setGeometry(QtCore.QRect(680, 10, 150, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnRemoveLista.setFont(font)
        self.btnRemoveLista.setStyleSheet("QPushButton:enabled {\n"
"    background-color: rgb(44, 163, 222);\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color:rgb(185, 185, 185);\n"
"    color: white;\n"
"}")
        self.btnRemoveLista.setIcon(icon2)
        self.btnRemoveLista.setObjectName("btnRemoveLista")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("D:/Robô Telegram Pro/Views/UI\\../Icons/to-do-list.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tabListas, icon11, "")
        self.labelLicense = QtWidgets.QLabel(self.centralwidget)
        self.labelLicense.setGeometry(QtCore.QRect(410, 440, 251, 31))
        self.labelLicense.setText("")
        self.labelLicense.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelLicense.setObjectName("labelLicense")
        self.btnAlterarLicenca = QtWidgets.QPushButton(self.centralwidget)
        self.btnAlterarLicenca.setGeometry(QtCore.QRect(670, 440, 150, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnAlterarLicenca.setFont(font)
        self.btnAlterarLicenca.setStyleSheet("QPushButton:enabled {\n"
"    background-color: rgb(44, 163, 222);\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color:rgb(185, 185, 185);\n"
"    color: white;\n"
"}")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("D:/Robô Telegram Pro/Views/UI\\../Icons/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAlterarLicenca.setIcon(icon12)
        self.btnAlterarLicenca.setObjectName("btnAlterarLicenca")
        self.labelVersion = QtWidgets.QLabel(self.centralwidget)
        self.labelVersion.setGeometry(QtCore.QRect(10, 440, 381, 31))
        self.labelVersion.setText("")
        self.labelVersion.setObjectName("labelVersion")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 846, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.actionExportar = QtWidgets.QAction(MainWindow)
        self.actionExportar.setObjectName("actionExportar")
        self.actionArquivo = QtWidgets.QAction(MainWindow)
        self.actionArquivo.setObjectName("actionArquivo")
        self.actionNovo = QtWidgets.QAction(MainWindow)
        self.actionNovo.setObjectName("actionNovo")
        self.actionListar = QtWidgets.QAction(MainWindow)
        self.actionListar.setObjectName("actionListar")
        self.actionCadastrar = QtWidgets.QAction(MainWindow)
        self.actionCadastrar.setObjectName("actionCadastrar")
        self.actionGerar_Lista = QtWidgets.QAction(MainWindow)
        self.actionGerar_Lista.setObjectName("actionGerar_Lista")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        item = self.tableContas.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Cod."))
        item = self.tableContas.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Nº Telefone"))
        item = self.tableContas.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Status"))
        item = self.tableContas.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Apelido da Conta"))
        item = self.tableContas.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Detalhes"))
        self.btnAddConta.setText(_translate("MainWindow", "Adicionar"))
        self.btnRemoveConta.setText(_translate("MainWindow", "Remover"))
        self.btnImportConta.setText(_translate("MainWindow", "Importar"))
        self.btnDesbloquearFlood.setText(_translate("MainWindow", "Liberar Agora"))
        
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabContas), _translate("MainWindow", "Gerenciar Contas"))
        item = self.tableGrupos.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Cod."))
        item = self.tableGrupos.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Nome"))
        item = self.tableGrupos.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Link / ID"))
        self.btnRemoveGrupo.setText(_translate("MainWindow", "Remover"))
        self.btnAddGrupo.setText(_translate("MainWindow", "Adicionar"))
        self.label_5.setText(_translate("MainWindow", "Gerenciar Grupos"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Gerenciar Grupos"))
        item = self.tableAquecendo.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Cod."))
        item = self.tableAquecendo.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Data Inclusão"))
        item = self.tableAquecendo.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Conta"))
        item = self.tableAquecendo.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Status"))
        item = self.tableAquecendo.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Observação"))
        self.btnAddAquecendo.setText(_translate("MainWindow", "Adicionar"))
        self.btnRemoveAquecendo.setText(_translate("MainWindow", "Remover"))
        self.label_4.setText(_translate("MainWindow", "Aquecer Contas"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAquecerConta), _translate("MainWindow", "Aquecer Contas"))
        self.label.setText(_translate("MainWindow", "ENCHER GRUPO"))
        item = self.tableTarefasGrupo.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Cod."))
        item = self.tableTarefasGrupo.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Origem"))
        item = self.tableTarefasGrupo.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Destino"))
        item = self.tableTarefasGrupo.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Analisados"))
        item = self.tableTarefasGrupo.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Adicionados"))
        item = self.tableTarefasGrupo.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Nº Contas"))
        item = self.tableTarefasGrupo.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Status"))
        self.btnAddTarefaGrupo.setText(_translate("MainWindow", "Adicionar"))
        self.btnRemoveTarefaGrupo.setText(_translate("MainWindow", "Remover"))
        self.btnDetalhesTarefa.setText(_translate("MainWindow", "Detalhes"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabGrupos), _translate("MainWindow", "Encher Grupo"))
        item = self.tableListas.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Cod."))
        item = self.tableListas.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Total de Membros"))
        item = self.tableListas.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Grupo de Origem"))
        item = self.tableListas.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Descrição"))
        self.label_2.setText(_translate("MainWindow", "EXTRAIR LISTA"))
        self.btnAddLista.setText(_translate("MainWindow", "Adicionar"))
        self.btnRemoveLista.setText(_translate("MainWindow", "Remover"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabListas), _translate("MainWindow", "Extrair Lista"))
        self.btnAlterarLicenca.setText(_translate("MainWindow", "Alterar"))
        self.actionExportar.setText(_translate("MainWindow", "Exportar"))
        self.actionArquivo.setText(_translate("MainWindow", "Arquivo"))
        self.actionNovo.setText(_translate("MainWindow", "Novo Processo"))
        self.actionListar.setText(_translate("MainWindow", "Listar"))
        self.actionCadastrar.setText(_translate("MainWindow", "Cadastrar"))
        self.actionGerar_Lista.setText(_translate("MainWindow", "Gerar Lista"))


