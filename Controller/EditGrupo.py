import sqlite3
import traceback
from PyQt5.QtWidgets import QDialog,QMessageBox
from PyQt5 import QtWidgets
from Database.Database import Database
from Model.ClientModel import ClientModel
from Threads.ThreadEditarConta import ThreadEditarConta
from Views.AdicionarGrupoView import Ui_Dialog as Ui_EditGrupoDialog
from Model.TelegramModel import TelegramModel

class EditGrupoController:
    def __init__(self, main_view):
        self.model = TelegramModel()
        self.client = ClientModel()
        self.database = Database()
        self.main_view = main_view
        self.main_view.tableGrupos.cellDoubleClicked.connect(self.open_edit_account_dialog)
        
      
    def open_edit_account_dialog(self, row):
        
        dialog = QDialog()
        ui = Ui_EditGrupoDialog()
        ui.setupUi(dialog)

        name = self.main_view.tableGrupos.item(row, 1).text()
        link = self.main_view.tableGrupos.item(row, 2).text()

        ui.lineNomeGrupo.setText(name)
        ui.lineIDGrupo.setText(link)

        ui.btnSalvar.clicked.connect(lambda: self.edit( ui, link, dialog,row))

        dialog.exec_()

    def edit(self, ui,  link, dialog,row):

        new_name = ui.lineNomeGrupo.text()
        new_link = ui.lineIDGrupo.text()

        if not new_name or not new_link:
            QMessageBox.warning(dialog, 'Warning', 'Por favor, preencha todos os campos.')
            return
        
        try:
            self.database.update_group(new_name, new_link, link)
            QMessageBox.information(dialog, 'Successo', 'Grupo editado com sucesso!')

            dialog.accept()
            self.update_table(new_name, new_link, row)
        except sqlite3.IntegrityError:
            QMessageBox.warning(dialog, 'Erro', 'ID do grupo já existe.')
        except Exception as e:
            traceback.print_exc()   
            QMessageBox.warning(dialog, 'Erro', str(e))

    def update_table(self, new_name, new_link, row):
        self.main_view.tableGrupos.item(row, 1).setText(new_name)
        self.main_view.tableGrupos.item(row, 2).setText(new_link)


   