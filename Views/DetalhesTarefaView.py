

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(850, 500)
        Dialog.setMinimumSize(QtCore.QSize(850, 500))
        Dialog.setMaximumSize(QtCore.QSize(8500, 5000))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("D:/Robô Telegram Pro/Views/UI\\../Icons/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(180, 10, 491, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.btnAtualizar = QtWidgets.QPushButton(Dialog)
        self.btnAtualizar.setEnabled(False)
        self.btnAtualizar.setGeometry(QtCore.QRect(690, 10, 150, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnAtualizar.setFont(font)
        self.btnAtualizar.setStyleSheet("QPushButton:enabled {\n"
"    background-color: rgb(44, 163, 222);\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color:rgb(185, 185, 185);\n"
"    color: white;\n"
"}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("D:/Robô Telegram Pro/Views/UI\\../Icons/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAtualizar.setIcon(icon1)
        self.btnAtualizar.setObjectName("btnAtualizar")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 60, 831, 431))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.btnPageAnteriorMembro = QtWidgets.QPushButton(self.tab_3)
        self.btnPageAnteriorMembro.setEnabled(False)
        self.btnPageAnteriorMembro.setGeometry(QtCore.QRect(294, 370, 75, 23))
        self.btnPageAnteriorMembro.setObjectName("btnPageAnteriorMembro")
        self.labelPageMembro = QtWidgets.QLabel(self.tab_3)
        self.labelPageMembro.setGeometry(QtCore.QRect(370, 372, 81, 21))
        self.labelPageMembro.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPageMembro.setObjectName("labelPageMembro")
        self.comboFiltroMembros = QtWidgets.QComboBox(self.tab_3)
        self.comboFiltroMembros.setGeometry(QtCore.QRect(710, 10, 111, 22))
        self.comboFiltroMembros.setObjectName("comboFiltroMembros")
        self.comboFiltroMembros.addItem("")
        self.comboFiltroMembros.addItem("")
        self.comboFiltroMembros.addItem("")
        #self.comboFiltroMembros.addItem("")
        self.label_3 = QtWidgets.QLabel(self.tab_3)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.tableMembros = QtWidgets.QTableWidget(self.tab_3)
        self.tableMembros.setGeometry(QtCore.QRect(10, 40, 811, 311))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tableMembros.setFont(font)
        self.tableMembros.setStyleSheet("QHeaderView::section {\n"
"    background-color: rgb(227, 227, 227);\n"
"    border:1px solid #D8D8D8;\n"
"    height: 32px;\n"
"}")
        self.tableMembros.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableMembros.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableMembros.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableMembros.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableMembros.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableMembros.setObjectName("tableMembros")
        self.tableMembros.setColumnCount(5)
        self.tableMembros.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableMembros.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableMembros.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableMembros.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableMembros.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableMembros.setHorizontalHeaderItem(4, item)
        self.tableMembros.horizontalHeader().setCascadingSectionResizes(False)
        self.tableMembros.horizontalHeader().setDefaultSectionSize(100)
        self.tableMembros.horizontalHeader().setMinimumSectionSize(50)
        self.tableMembros.horizontalHeader().setStretchLastSection(True)
        self.tableMembros.verticalHeader().setVisible(False)
        self.tableMembros.verticalHeader().setSortIndicatorShown(False)
        self.label_10 = QtWidgets.QLabel(self.tab_3)
        self.label_10.setGeometry(QtCore.QRect(600, 10, 101, 20))
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.btnPageProximaMembro = QtWidgets.QPushButton(self.tab_3)
        self.btnPageProximaMembro.setEnabled(False)
        self.btnPageProximaMembro.setGeometry(QtCore.QRect(454, 370, 75, 23))
        self.btnPageProximaMembro.setObjectName("btnPageProximaMembro")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.btnPageProximaConta = QtWidgets.QPushButton(self.tab_2)
        self.btnPageProximaConta.setEnabled(False)
        self.btnPageProximaConta.setGeometry(QtCore.QRect(460, 370, 75, 23))
        self.btnPageProximaConta.setObjectName("btnPageProximaConta")
        self.tableContas = QtWidgets.QTableWidget(self.tab_2)
        self.tableContas.setGeometry(QtCore.QRect(10, 40, 811, 311))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tableContas.setFont(font)
        self.tableContas.setStyleSheet("QHeaderView::section {\n"
"    background-color: rgb(227, 227, 227);\n"
"    border:1px solid #D8D8D8;\n"
"    height: 32px;\n"
"}")
        self.tableContas.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableContas.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableContas.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableContas.setObjectName("tableContas")
        self.tableContas.setColumnCount(4)
        self.tableContas.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableContas.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableContas.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableContas.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableContas.setHorizontalHeaderItem(3, item)
        self.tableContas.horizontalHeader().setDefaultSectionSize(120)
        self.tableContas.horizontalHeader().setStretchLastSection(True)
        self.tableContas.verticalHeader().setVisible(False)
        self.tableContas.verticalHeader().setSortIndicatorShown(False)
        self.btnPageAnteriorConta = QtWidgets.QPushButton(self.tab_2)
        self.btnPageAnteriorConta.setEnabled(False)
        self.btnPageAnteriorConta.setGeometry(QtCore.QRect(300, 370, 75, 23))
        self.btnPageAnteriorConta.setObjectName("btnPageAnteriorConta")
        self.labelPageConta = QtWidgets.QLabel(self.tab_2)
        self.labelPageConta.setGeometry(QtCore.QRect(376, 372, 81, 21))
        self.labelPageConta.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPageConta.setObjectName("labelPageConta")
        self.comboFiltroContas = QtWidgets.QComboBox(self.tab_2)
        self.comboFiltroContas.setGeometry(QtCore.QRect(720, 10, 101, 22))
        self.comboFiltroContas.setObjectName("comboFiltroContas")
        self.comboFiltroContas.addItem("")
        self.comboFiltroContas.addItem("")
        self.comboFiltroContas.addItem("")
        #self.comboFiltroContas.addItem("")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.label_15 = QtWidgets.QLabel(self.tab_2)
        self.label_15.setGeometry(QtCore.QRect(610, 10, 101, 20))
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 20, 801, 191))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(460, 20, 61, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(10, 20, 51, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setGeometry(QtCore.QRect(10, 80, 111, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setGeometry(QtCore.QRect(460, 80, 101, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.groupBox_2)
        self.label_13.setGeometry(QtCore.QRect(460, 130, 111, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.groupBox_2)
        self.label_14.setGeometry(QtCore.QRect(10, 130, 121, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.labelOrigem = QtWidgets.QLabel(self.groupBox_2)
        self.labelOrigem.setGeometry(QtCore.QRect(10, 40, 191, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelOrigem.setFont(font)
        self.labelOrigem.setText("")
        self.labelOrigem.setObjectName("labelOrigem")
        self.labelDestino = QtWidgets.QLabel(self.groupBox_2)
        self.labelDestino.setGeometry(QtCore.QRect(460, 40, 181, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelDestino.setFont(font)
        self.labelDestino.setText("")
        self.labelDestino.setObjectName("labelDestino")
        self.labelAtivos = QtWidgets.QLabel(self.groupBox_2)
        self.labelAtivos.setGeometry(QtCore.QRect(10, 100, 91, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelAtivos.setFont(font)
        self.labelAtivos.setText("")
        self.labelAtivos.setObjectName("labelAtivos")
        self.labelVistoUltimo = QtWidgets.QLabel(self.groupBox_2)
        self.labelVistoUltimo.setGeometry(QtCore.QRect(10, 150, 81, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelVistoUltimo.setFont(font)
        self.labelVistoUltimo.setText("")
        self.labelVistoUltimo.setObjectName("labelVistoUltimo")
        self.labelIntervalo = QtWidgets.QLabel(self.groupBox_2)
        self.labelIntervalo.setGeometry(QtCore.QRect(460, 150, 71, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelIntervalo.setFont(font)
        self.labelIntervalo.setText("")
        self.labelIntervalo.setObjectName("labelIntervalo")
        self.labelLimiteDiario = QtWidgets.QLabel(self.groupBox_2)
        self.labelLimiteDiario.setGeometry(QtCore.QRect(460, 100, 91, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelLimiteDiario.setFont(font)
        self.labelLimiteDiario.setText("")
        self.labelLimiteDiario.setObjectName("labelLimiteDiario")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(10, 230, 801, 161))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(10, 80, 131, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 30, 131, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(460, 30, 171, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(460, 80, 171, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.labelTotal = QtWidgets.QLabel(self.groupBox)
        self.labelTotal.setGeometry(QtCore.QRect(10, 50, 121, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelTotal.setFont(font)
        self.labelTotal.setText("")
        self.labelTotal.setObjectName("labelTotal")
        self.labelAdicionados = QtWidgets.QLabel(self.groupBox)
        self.labelAdicionados.setGeometry(QtCore.QRect(10, 100, 121, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelAdicionados.setFont(font)
        self.labelAdicionados.setText("")
        self.labelAdicionados.setObjectName("labelAdicionados")
        self.labelFalha = QtWidgets.QLabel(self.groupBox)
        self.labelFalha.setGeometry(QtCore.QRect(460, 50, 171, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelFalha.setFont(font)
        self.labelFalha.setText("")
        self.labelFalha.setObjectName("labelFalha")
        self.labelPendente = QtWidgets.QLabel(self.groupBox)
        self.labelPendente.setGeometry(QtCore.QRect(460, 100, 171, 21))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelPendente.setFont(font)
        self.labelPendente.setText("")
        self.labelPendente.setObjectName("labelPendente")
        self.tabWidget.addTab(self.tab, "")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Detalhes de Tarefa"))
        self.label.setText(_translate("Dialog", "DETALHES DA TAREFA"))
        self.btnAtualizar.setText(_translate("Dialog", "Atualizar Tela"))
        self.btnPageAnteriorMembro.setText(_translate("Dialog", "<"))
        self.labelPageMembro.setText(_translate("Dialog", "0 de 0"))
        self.comboFiltroMembros.setItemText(0, _translate("Dialog", "Todos"))
        self.comboFiltroMembros.setItemText(1, _translate("Dialog", "Sucesso"))
        self.comboFiltroMembros.setItemText(2, _translate("Dialog", "Falha"))
        #self.comboFiltroMembros.setItemText(3, _translate("Dialog", "Pendente"))
        self.label_3.setText(_translate("Dialog", "Membros:"))
        self.tableMembros.setSortingEnabled(False)
        item = self.tableMembros.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Membro ID"))
        item = self.tableMembros.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Status"))
        item = self.tableMembros.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Conta"))
        item = self.tableMembros.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Data Adição"))
        item = self.tableMembros.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Observação"))
        self.label_10.setText(_translate("Dialog", "Filtro:"))
        self.btnPageProximaMembro.setText(_translate("Dialog", ">"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "Membros"))
        self.btnPageProximaConta.setText(_translate("Dialog", ">"))
        self.tableContas.setSortingEnabled(False)
        item = self.tableContas.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Conta"))
        item = self.tableContas.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Status"))
        item = self.tableContas.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Adicionado (Dia)"))
        item = self.tableContas.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Observação"))
        self.btnPageAnteriorConta.setText(_translate("Dialog", "<"))
        self.labelPageConta.setText(_translate("Dialog", "0 de 0"))
        self.comboFiltroContas.setItemText(0, _translate("Dialog", "Todos"))
        self.comboFiltroContas.setItemText(1, _translate("Dialog", "Conectada"))
        self.comboFiltroContas.setItemText(2, _translate("Dialog", "Flood"))
        #self.comboFiltroContas.setItemText(3, _translate("Dialog", "Limite Diário"))
        self.label_2.setText(_translate("Dialog", "Contas:"))
        self.label_15.setText(_translate("Dialog", "Filtro:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Contas"))
        self.groupBox_2.setTitle(_translate("Dialog", "Detalhes"))
        self.label_5.setText(_translate("Dialog", "Destino:"))
        self.label_4.setText(_translate("Dialog", "Origem:"))
        self.label_11.setText(_translate("Dialog", "Apenas ativos:"))
        self.label_12.setText(_translate("Dialog", "Limite Diário:"))
        self.label_13.setText(_translate("Dialog", "Intervalo (seg):"))
        self.label_14.setText(_translate("Dialog", "Visto por último:"))
        self.groupBox.setTitle(_translate("Dialog", "Estatísticas"))
        self.label_7.setText(_translate("Dialog", "Total Adicionados:"))
        self.label_6.setText(_translate("Dialog", "Total de Membros:"))
        self.label_8.setText(_translate("Dialog", "Total Falha:"))
        self.label_9.setText(_translate("Dialog", "Total Pendentes:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Informações Gerais"))

