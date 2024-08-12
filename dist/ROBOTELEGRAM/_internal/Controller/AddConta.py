import asyncio
import datetime
from PyQt5.QtWidgets import QDialog, QMessageBox,QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush
from Enums.StatusConta import StatusConta
from Enums.TipoConta import TipoConta
from Views.AddConta import Ui_Dialog
from Model.TelegramModel import TelegramModel
from Threads.ThreadCarregarContas import ThreadCarregarConta
from Database.Database import Database

class AddContaController:
    def __init__(self,main_view):
        self.model = TelegramModel()
        self.database = Database()
        self.main_view = main_view
        self.main_view.btnAddConta.clicked.connect(self.open_add_account_dialog)
        self.main_view.btnDesbloquearFlood.setEnabled(True)
        self.main_view.btnDesbloquearFlood.clicked.connect(self.desbloquear_flood)
        self.load_accounts_thread = ThreadCarregarConta()
        self.load_accounts_thread.account_loaded.connect(self.inserirTableConta)
        self.load_accounts_thread.start()



    def open_add_account_dialog(self):
        dialog = QDialog()
        ui = Ui_Dialog()
        
        licence = self.database.get_licence_local()
        expiration_date = datetime.datetime.strptime(licence['vencimento'], "%d-%m-%Y")
        
        if datetime.datetime.now() > expiration_date:
            QMessageBox.warning(dialog, 'Warning', 'Licença Expirada!')
            return
        
        ui.setupUi(dialog)

        ui.btnEnviarToken.clicked.connect(lambda: self.send_code(ui))
        ui.btnSalvar.clicked.connect(lambda: self.verify_code(ui))

        dialog.exec_()

    def send_code(self, ui):
        phone = ui.lineCodPais.text() + ui.lineTelefone.text()

        if not ui.lineTelefone.text():
            QMessageBox.warning(ui.lineTelefone, 'Warning', 'Digite o número de telefone.')
            return

        loop = asyncio.get_event_loop()
        error_message = loop.run_until_complete(self.model.send_code(phone))
        
        if error_message is None:
            ui.lineToken.setEnabled(True)
            ui.btnSalvar.setEnabled(True)
            QMessageBox.information(ui.lineTelefone, 'Info', 'Código Enviado com Sucesso!')
        else:
            QMessageBox.warning(ui.lineTelefone, 'Warning', f'{error_message}')


    def verify_code(self, ui):
        phone = ui.lineCodPais.text() + ui.lineTelefone.text()
        code = ui.lineToken.text()
        password = ''  # Implement if you need to handle passwords
        if not phone or not code:
            QMessageBox.warning(ui.lineToken, 'Warning', 'Por favor, preencha todos os campos.')
            return

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.model.verify_code(phone, code, password))
        tipo_conta = TipoConta.ADICIONADA

        
        if 'Conta Adicionada com Sucesso !' in result:
            apelido_conta = ui.lineApelidoConta.text() if ui.lineApelidoConta.text() else result.split('! ')[1]
            status_conta = StatusConta.CONECTADA  

            # Save to database
            self.database.add_account(phone, tipo_conta, apelido_conta, status_conta)
            self.inserirTableConta(phone, tipo_conta, apelido_conta, status_conta)
            QMessageBox.information(ui.lineToken, 'Info', result.split('! ')[0])
         
        else:
            status_conta = StatusConta.FALHA 
            
            # Save to daabase with failure status
            """ self.database.add_account(phone, tipo_conta, "N/A", status_conta)
            self.inserirTableConta(phone, tipo_conta, "N/A", status_conta) """
            QMessageBox.warning(ui.lineToken, 'Warning', result)
        
        

    def inserirTableConta(self, phone, tipo_conta, apelido_conta, status_conta):
        rowPosition = self.main_view.tableContas.rowCount()
        self.main_view.tableContas.insertRow(rowPosition)

        itemCodigo = QTableWidgetItem(str(rowPosition + 1))
        itemCodigo.setTextAlignment(Qt.AlignCenter)
        self.main_view.tableContas.setItem(rowPosition, 0, itemCodigo)
        
        itemSession = QTableWidgetItem(phone)
        itemSession.setTextAlignment(Qt.AlignCenter)
        self.main_view.tableContas.setItem(rowPosition, 1, itemSession)
        
        itemStatus = QTableWidgetItem('')
        if status_conta == StatusConta.CONECTADA:
            itemStatus = QTableWidgetItem('Conectada')
            itemStatus.setForeground(QBrush(QColor(0, 125, 25)))
        elif status_conta == StatusConta.NAO_AUTENTICADA:
            itemStatus = QTableWidgetItem('Não Autenticada')
            itemStatus.setForeground(QBrush(QColor(255, 0, 0)))
        elif status_conta == StatusConta.FALHA:
            itemStatus = QTableWidgetItem('Falha')
            itemStatus.setForeground(QBrush(QColor(255, 0, 0)))
        elif status_conta == StatusConta.FLOOD:
            itemStatus = QTableWidgetItem('Flood')
            itemStatus.setForeground(QBrush(QColor(255, 125, 0)))
        self.main_view.tableContas.setItem(rowPosition, 2, itemStatus)
        itemStatus.setTextAlignment(Qt.AlignCenter)
        
        itemApelidoConta = QTableWidgetItem(apelido_conta if apelido_conta else '')
        itemApelidoConta.setTextAlignment(Qt.AlignCenter)
        self.main_view.tableContas.setItem(rowPosition, 3, itemApelidoConta)
        
        itemTipoConta = QTableWidgetItem(tipo_conta.name)
        itemTipoConta.setTextAlignment(Qt.AlignCenter)
        self.main_view.tableContas.setItem(rowPosition, 4, itemTipoConta)


    def desbloquear_flood(self):
        row = self.main_view.tableContas.currentRow()
        if row >= 0:
            phone = self.main_view.tableContas.item(row, 1).text()
            status = self.main_view.tableContas.item(row, 2).text()
            if status == 'Flood':
                self.database.update_account_status(phone, StatusConta.CONECTADA.value)
                self.main_view.tableContas.item(row, 2).setText('Conectada')
                self.main_view.tableContas.item(row, 2).setForeground(QBrush(QColor(0, 125, 25)))
                QMessageBox.information(self.main_view.tableContas, 'Info', 'Flood Desbloqueado com Sucesso!')
                
        return None
