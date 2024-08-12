from PyQt5.QtWidgets import QDialog,QMessageBox
from Database.Database import Database
from Model.ClientModel import ClientModel
from Threads.ThreadEditarConta import ThreadEditarConta
from Views.EditarImportarContaView import Ui_Dialog as Ui_EditarImportarContaDialog
from Model.TelegramModel import TelegramModel

class EditContaController:
    def __init__(self, main_view):
        self.model = TelegramModel()
        self.client = ClientModel()
        self.database = Database()
        self.main_view = main_view
        self.main_view.tableContas.cellDoubleClicked.connect(self.open_edit_account_dialog)
        
      
    def open_edit_account_dialog(self, row):
        
        dialog = QDialog()
        ui = Ui_EditarImportarContaDialog()
        ui.setupUi(dialog)

        phone = self.main_view.tableContas.item(row, 1).text()
        current_apelido = self.main_view.tableContas.item(row, 3).text()

        ui.label_conta.setText(phone)
        ui.line_apelido.setText(current_apelido)

        ui.btnSalvar.clicked.connect(lambda: self.start_edit_account_thread(ui, phone, row, dialog))

        dialog.exec_()

    def start_edit_account_thread(self, ui, phone, row, dialog):
        new_apelido = ui.line_apelido.text()

        self.edit_account_thread = ThreadEditarConta(self.database.db_name, phone, new_apelido, row)
        self.edit_account_thread.account_edited.connect(self.update_table_apelido)
        self.edit_account_thread.finished.connect(lambda: self.on_edit_account_finished(ui, dialog))
        self.edit_account_thread.start()

    def on_edit_account_finished(self, ui, dialog):
        QMessageBox.information(ui.btnSalvar, 'Info', 'Apelido atualizado com sucesso!')
        dialog.accept()

    def update_table_apelido(self, new_apelido, row):
        self.main_view.tableContas.item(row, 3).setText(new_apelido)
