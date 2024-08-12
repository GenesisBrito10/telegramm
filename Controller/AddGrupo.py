
import datetime
import sqlite3
from Database.Database import Database
from PyQt5.QtWidgets import QDialog, QMessageBox
from Views.AdicionarGrupoView import Ui_Dialog
from PyQt5 import  QtWidgets

class GroupController:
    def __init__(self, main_window):
        self.database = Database()
        self.main_window = main_window
        self.main_window.btnAddGrupo.clicked.connect(self.open_add_group_dialog)
        self.load_groups()

    def open_add_group_dialog(self):
        dialog = QDialog()
        ui = Ui_Dialog()
        
        licence = self.database.get_licence_local()
        expiration_date = datetime.datetime.strptime(licence['vencimento'], "%d-%m-%Y")
        
        if datetime.datetime.now() > expiration_date:
            QMessageBox.warning(dialog, 'Warning', 'Licença Expirada!')
            return
        ui.setupUi(dialog)
        
        ui.btnSalvar.clicked.connect(lambda: self.add_group(ui, dialog))
        
        dialog.exec_()

    def add_group(self, ui, dialog):
        group_desc = ui.lineNomeGrupo.text()
        group_link = ui.lineIDGrupo.text()

    
        if not group_desc or not group_link:
            QMessageBox.warning(dialog, 'Warning', 'Por favor, preencha todos os campos.')
            return

        valid_link_structures = ["https://t.me/+", "https://t.me/", "http://t.me/+", "http://t.me/", "t.me/+", "https://t.me/joinchat/", "t.me/joinchat/"]
        if not any(link_structure in group_link for link_structure in valid_link_structures):
            QMessageBox.warning(dialog, 'Erro', 'O link do grupo não possui uma estrutura válida.')
            return

        try:
            self.database.add_group(group_desc, group_link)
            QMessageBox.information(dialog, 'Successo', 'Grupo adicionado com sucesso!')
            self.insert_row_grupo(group_desc, group_link)
            dialog.accept()
        except sqlite3.IntegrityError:
            QMessageBox.warning(dialog, 'Erro', 'ID do grupo já existe.')
        except Exception as e:
            QMessageBox.warning(dialog, 'Erro', str(e))


   
    def insert_row_grupo(self,group_desc, group_link):
        row_position = self.main_window.tableGrupos.rowCount()
        self.main_window.tableGrupos.insertRow(row_position)
        self.main_window.tableGrupos.setItem(row_position, 0, QtWidgets.QTableWidgetItem(str(row_position + 1)))
        self.main_window.tableGrupos.setItem(row_position, 1, QtWidgets.QTableWidgetItem(group_desc))
        self.main_window.tableGrupos.setItem(row_position, 2, QtWidgets.QTableWidgetItem(group_link))

    def load_groups(self):
        groups = self.database.get_all_groups()
        for group in groups:
            self.insert_row_grupo(group['desc'], group['link'])