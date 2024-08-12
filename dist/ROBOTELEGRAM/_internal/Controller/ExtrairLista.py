# Controller/ExtractMembersController.py

import datetime
import os
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import QtWidgets
from Views.ExtrairListaView import Ui_Dialog as Ui_ExtrairListaDialog
from Threads.ThreadExtrairLista import ThreadExtrairLista
from Database.Database import Database


class ExtractMembersController:
    def __init__(self, main_view):
        self.database = Database()
        self.main_view = main_view
        self.main_view.btnAddLista.clicked.connect(
            self.open_extract_members_dialog)
        self.main_view.btnRemoveLista.clicked.connect(self.remove_selected_row)

        self.load_listas()

    def open_extract_members_dialog(self):
        dialog = QDialog()
        self.ui = Ui_ExtrairListaDialog()
        licence = self.database.get_licence_local()
        expiration_date = datetime.datetime.strptime(licence['vencimento'], "%d-%m-%Y")
        
        if datetime.datetime.now() > expiration_date:
            QMessageBox.warning(dialog, 'Warning', 'Licença Expirada!')
            return
        self.ui.setupUi(dialog)
        self.populate_groups()
        self.ui.lineNomeLista.textChanged.connect(self.toggle_save_button)
        self.ui.btnSalvar.setEnabled(False)
        self.ui.btnSalvar.clicked.connect(self.start_extraction)
        dialog.exec_()

    def populate_groups(self):
        groups = self.database.get_all_groups()
        if groups:
            for group in groups:
                self.ui.comboGrupo.addItem(group['desc'], group)
            self.toggle_group_options(True)
        else:
            self.toggle_group_options(False)

    def toggle_group_options(self, enabled):
        self.ui.comboGrupo.setEnabled(enabled)
        self.ui.checkAtivos.setEnabled(enabled)
        self.ui.checkUsername.setEnabled(enabled)
        self.ui.checkTelefone.setEnabled(enabled)
        self.ui.checkFoto.setEnabled(enabled)
        self.ui.checkRemoverAdministradores.setEnabled(enabled)
        self.ui.spinDias.setEnabled(enabled)
        self.ui.lineNomeLista.setEnabled(enabled)

    def toggle_save_button(self):
        lists = self.database.get_all_files()
        lists = [list.split('/')[-1].split('.csv')[0] for list in lists]

        if self.ui.lineNomeLista.text().strip() in lists:
            self.ui.labelStatus.setStyleSheet('color:red')
            self.ui.labelStatus.setText("Nome de lista já existe.")
            self.ui.btnSalvar.setEnabled(False)
            return
        else:
            self.ui.labelStatus.setText("")
            self.ui.btnSalvar.setEnabled(
                bool(self.ui.lineNomeLista.text().strip()))

    def start_extraction(self):
        selected_group = self.ui.comboGrupo.currentData()

        if selected_group is None:
            self.ui.labelStatus.setStyleSheet('color:red')
            self.ui.labelStatus.setText("Por favor, selecione um grupo.")
            return

        options = {
            "ativos": self.ui.checkAtivos.isChecked(),
            "username": self.ui.checkUsername.isChecked(),
            "telefone": self.ui.checkTelefone.isChecked(),
            "foto": self.ui.checkFoto.isChecked(),
            "remover_administradores": self.ui.checkRemoverAdministradores.isChecked(),
            "dias": self.ui.spinDias.value(),
        }

        connected_account = self.get_connected_account()
        if connected_account is None:
            self.ui.labelStatus.setStyleSheet('color:red')
            self.ui.labelStatus.setText("Nenhuma conta conectada disponível.")
            return

        phone = connected_account['file_session']

        group_link = selected_group['link']

        self.thread = ThreadExtrairLista(
            self.ui.lineNomeLista.text(), phone, group_link, options)
        self.thread.sinalListaExtraida.connect(self.on_extraction_complete)
        self.thread.sinalMsg.connect(self.on_extraction_failed)
        self.thread.start()

    def get_connected_account(self):
        accounts = self.database.get_all_accounts()
        for account in accounts:
            if account['status_conta'] == 0:
                return account
        return None

    def on_extraction_complete(self, list):
        message, total_members, group_name, file_path = list
        self.ui.labelStatus.setStyleSheet('color:green')
        self.ui.labelStatus.setText(message)
        self.update_table(total_members, group_name, file_path)

    def update_table(self, total_members, group_name, file_path):
        row_position = self.main_view.tableListas.rowCount()
        self.main_view.tableListas.insertRow(row_position)

        # Cria um novo botão de abrir pasta para cada linha
        btn_abrirPasta = QtWidgets.QPushButton("Abrir Pasta")
        btn_abrirPasta.setStyleSheet("""
        QPushButton {
            background-color: rgb(44, 163, 222);
            color: white;
            border-radius: 5px;
            padding: 5px;
        }
        QPushButton:disabled {
            background-color: rgb(185, 185, 185);
            color: white;
            border-radius: 5px;
            padding: 5px;
        }
        """)
        btn_abrirPasta.clicked.connect(lambda: self.open_csv(file_path))
        self.main_view.tableListas.setCellWidget(
            row_position, 0, btn_abrirPasta)

        self.main_view.tableListas.setItem(
            row_position, 1, QtWidgets.QTableWidgetItem(str(row_position + 1)))
        self.main_view.tableListas.setItem(
            row_position, 2, QtWidgets.QTableWidgetItem(str(total_members)))
        self.main_view.tableListas.setItem(
            row_position, 3, QtWidgets.QTableWidgetItem(group_name))
        self.main_view.tableListas.setItem(
            row_position, 4, QtWidgets.QTableWidgetItem(file_path))

    def on_extraction_failed(self, message):
        self.ui.labelStatus.setStyleSheet('color:red')
        self.ui.labelStatus.setText(message)

    def open_csv(self, file_path):
        import subprocess
        import os
        try:
            directory = os.path.dirname(file_path)
            if os.name == 'nt':
                os.startfile(directory)
            else:
                subprocess.call(['open', directory])
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                None, "Erro", f"Não foi possível abrir o diretório: {str(e)}")

    def load_listas(self):
        listas = self.database.get_all_listas()

        for lista in listas:
            self.update_table(lista['total_members'],
                              lista['group_name'], lista['file_path'])

    def remove_selected_row(self):
        selected_row = self.main_view.tableListas.currentRow()
        if selected_row >= 0:
            file_path = self.main_view.tableListas.item(selected_row, 4).text()
            if file_path:
                
                os.remove(file_path)
                self.database.delete_lista(file_path)
                self.main_view.tableListas.removeRow(selected_row)
           
        else:
            QMessageBox.warning(None, "Seleção inválida",
                                "Por favor, selecione uma linha para remover.")
