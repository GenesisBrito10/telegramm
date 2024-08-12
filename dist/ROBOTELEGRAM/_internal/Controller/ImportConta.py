import datetime
import os
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush
from Database.Database import Database
from Enums.StatusConta import StatusConta
from Model.ClientModel import ClientModel
from Views.ImportarContaView import Ui_Dialog as Ui_ImportarContaDialog
from Threads.ThreadImportarConta import ThreadImportarConta


class ImportContaController:
    def __init__(self, main_view):
        
        self.client = ClientModel()
        self.database = Database()
        self.import_threads = [] 
        self.main_view = main_view
        self.main_view.btnImportConta.clicked.connect(self.open_import_account_dialog)
      
    def open_import_account_dialog(self):
        dialog = QDialog()
        ui = Ui_ImportarContaDialog()
        licence = self.database.get_licence_local()
        expiration_date = datetime.datetime.strptime(licence['vencimento'], "%d-%m-%Y")
        
        if datetime.datetime.now() > expiration_date:
            QMessageBox.warning(dialog, 'Warning', 'Licença Expirada!')
            return
        
        ui.setupUi(dialog)
        ui.btnProcurar.clicked.connect(lambda: self.load_session_file(ui))
        ui.btnSalvar.clicked.connect(lambda: self.save_imported_sessions(ui))

        dialog.exec_()

    def load_session_file(self, ui):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_names, _ = QFileDialog.getOpenFileNames(self.main_view, "Open Session Files", "", "Session Files (*.session);;All Files (*)", options=options)
        if file_names:
            self.session_files = []
            for file_name in file_names:
                destination = os.path.join("sessions", os.path.basename(file_name))
                if os.path.exists(destination):
                    ui.labelStatus.setStyleSheet('color:red')
                    ui.labelStatus.setText(f'Conta {os.path.basename(file_name)} já adicionada!')
                    ui.btnSalvar.setEnabled(False)
                else:
                    self.session_files.append((file_name, destination))
                    self.update_session_table(ui, destination)

    def update_session_table(self, ui, file_name):
        phone_number = os.path.basename(file_name).replace(".session", "")
        row_position = ui.tableSessions.rowCount()
        ui.tableSessions.insertRow(row_position)

        item_account = QTableWidgetItem(phone_number)
        item_account.setTextAlignment(Qt.AlignCenter)
        ui.tableSessions.setItem(row_position, 0, item_account)

        item_status = QTableWidgetItem("Pending")
        item_status.setTextAlignment(Qt.AlignCenter)
        item_status.setForeground(QBrush(QColor(255, 125, 0)))
        ui.tableSessions.setItem(row_position, 1, item_status)

    def save_imported_sessions(self, ui):
        for index, (file, destination) in enumerate(self.session_files):
            import_thread = ThreadImportarConta(file, destination, self.database.db_name, index, ui)
            import_thread.account_imported.connect(self.on_account_imported)
            import_thread.update_status.connect(self.on_update_status)
            self.import_threads.append(import_thread)  # Adicionar a thread à lista de threads
            import_thread.start()

        ui.btnSalvar.setEnabled(False)

    def on_account_imported(self, phone, tipo_conta, apelido_conta, status_conta, note):
        self.database.add_account(phone, tipo_conta, apelido_conta, status_conta)
        self.inserirTableConta(phone, tipo_conta, apelido_conta, status_conta)
        print(note)

    def on_update_status(self, status, note, row, ui):
        item_status = ui.tableSessions.item(row, 1)
        item_status.setText(status)
        if status == "Erro":
            item_status.setForeground(QBrush(QColor(255, 0, 0)))
        elif status == "Sucesso":
            item_status.setForeground(QBrush(QColor(0, 125, 25)))
        item_note = QTableWidgetItem(note)
        item_note.setTextAlignment(Qt.AlignCenter)
        ui.tableSessions.setItem(row, 2, item_note)

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