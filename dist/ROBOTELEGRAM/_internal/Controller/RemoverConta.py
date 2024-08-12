import os
from PyQt5.QtWidgets import QMessageBox
from Database.Database import Database
from Model.ClientModel import ClientModel
from Model.TelegramModel import TelegramModel
from Threads.ThreadRemoverConta import ThreadRemoverConta

class RemoverContaController:
    def __init__(self, main_view):
        self.model = TelegramModel()
        self.client = ClientModel()
        self.database = Database()
        self.main_view = main_view
        self.main_view.btnRemoveConta.clicked.connect(self.remove_selected_account)
        
      

    def remove_selected_account(self):
        selected_row = self.main_view.tableContas.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self.main_view, 'Warning', 'Selecione uma conta para remover.')
            return
        
        phone = self.main_view.tableContas.item(selected_row, 1).text()
        message_box = QMessageBox(self.main_view)
        message_box.setWindowTitle('Confirmação')
        message_box.setText(f'Tem certeza que deseja excluir a conta {phone}?')
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.button(QMessageBox.Yes).setText('Sim')
        message_box.button(QMessageBox.No).setText('Não')
        reply = message_box.exec_()

        if reply == QMessageBox.Yes:
            os.remove(f'sessions/{phone}.session')
            self.remove_account_thread = ThreadRemoverConta(self.database.db_name, phone, selected_row)
            self.remove_account_thread.account_removed.connect(self.remove_table_row)
            self.remove_account_thread.start()

    def remove_table_row(self, row):
        self.main_view.tableContas.removeRow(row)
        QMessageBox.information(self.main_view, 'Info', 'Conta removida com sucesso!')
