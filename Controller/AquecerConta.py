import datetime
from PyQt5.QtWidgets import QDialog, QMessageBox, QListWidgetItem, QTableWidgetItem
from PyQt5.QtGui import QColor
from Database.Database import Database
from Enums.StatusAquecimento import StatusAquecimento
from Enums.StatusConta import StatusConta
from Views.AdicionarContaAquecerView import Ui_Dialog
from Threads.ThreadAquecerConta import ThreadAquecerConta

class AquecerContaController:
    
    def __init__(self, main_window):
        self.main_window = main_window
        #self.main_window.closeEvent = self.handle_close_event
        self.database = Database()
        self.threads = []  
        self.main_window.btnAddAquecendo.clicked.connect(self.open_add_group_dialog)
        self.main_window.btnRemoveAquecendo.clicked.connect(self.remove_selected_row)

        self.load_aquecimentos()
        
    def open_add_group_dialog(self):
        self.dialog = QDialog()
        self.ui = Ui_Dialog()
        
        licence = self.database.get_licence_local()
        expiration_date = datetime.datetime.strptime(licence['vencimento'], "%d-%m-%Y")
        
        if datetime.datetime.now() > expiration_date:
            QMessageBox.warning(self.dialog, 'Warning', 'Licença Expirada!')
            return
        self.ui.setupUi(self.dialog)
        
        self.load_contas()
        
        self.dialog.exec_()

    def load_contas(self):
        contas = self.database.get_accounts_by_status(0)
        self.ui.comboContas.clear()
        for conta in contas:
            item = QListWidgetItem(f"{conta['file_session']} | {conta['apelido']}")
            self.ui.comboContas.addItem(item)
        self.ui.labelStatus.setText("")
        self.ui.btnSalvar.setEnabled(True)
        self.ui.btnSalvar.clicked.connect(self.on_save_clicked)

    def load_aquecimentos(self):
        aquecimentos = self.database.get_all_aquecimentos()
        self.main_window.tableAquecendo.setRowCount(0)
        for aquecimento in aquecimentos:
            self.add_aquecimento_to_table(aquecimento)

    def add_aquecimento_to_table(self, aquecimento):
        row_position = self.main_window.tableAquecendo.rowCount()
        self.main_window.tableAquecendo.insertRow(row_position)
        
        self.main_window.tableAquecendo.setItem(row_position, 0, QTableWidgetItem(str(row_position + 1)))
        self.main_window.tableAquecendo.setItem(row_position, 1, QTableWidgetItem(aquecimento['data_inicio']))
        
        status_item = QTableWidgetItem(StatusAquecimento(aquecimento['status']).name)
        status_color = QColor(0, 255, 0) if aquecimento['status'] == StatusAquecimento.FINALIZADO.value else QColor(255, 0, 0)
        status_item.setForeground(status_color)
        
        self.main_window.tableAquecendo.setItem(row_position, 2, QTableWidgetItem(aquecimento['conta_id']))
        self.main_window.tableAquecendo.setItem(row_position, 3, status_item)
        self.main_window.tableAquecendo.setItem(row_position, 4, QTableWidgetItem(aquecimento['observacoes']))

    def on_save_clicked(self):
        selected_items = self.ui.comboContas.selectedItems()

        licence = self.database.get_licence_local()
        expiration_date = datetime.datetime.strptime(licence['vencimento'], "%d-%m-%Y")
        
        if datetime.datetime.now() > expiration_date:
            QMessageBox.warning(self.ui.comboContas, 'Warning', 'Licença Expirada!')
            return
        
        if not selected_items:
            QMessageBox.warning(None, "Nenhuma conta selecionada", "Por favor, selecione pelo menos uma conta.")
            return

        for item in selected_items:
            conta_id = item.text()
            file_session, apelido = conta_id.split('|')[0].strip(), conta_id.split('|')[1].strip()
            if self.is_duplicate_account(file_session):
                QMessageBox.warning(None, "Conta duplicada", f"A conta {file_session} já está sendo aquecida.")
                continue
            
            """ if not self.is_disponible_account(file_session):
                QMessageBox.warning(None, "Conta indisponível", f"A conta {file_session} está em uso.")
                continue """

            
            
            row_position = self.main_window.tableAquecendo.rowCount()
            self.add_new_aquecimento_to_table(row_position, file_session, apelido)
            
            self.thread = ThreadAquecerConta(conta_id, row_position)
            self.thread.message.connect(self.on_save_finished)
            self.thread.table.connect(self.update_table_aquecendo)
            self.threads.append(self.thread)  
            self.thread.start()
            self.dialog.close()

    def is_duplicate_account(self, file_session):
        for row in range(self.main_window.tableAquecendo.rowCount()):
            existing_file_session = self.main_window.tableAquecendo.item(row, 2).text().split('|')[0].strip()
            if existing_file_session == file_session:
                return True
        return False
    
    def is_disponible_account(self, file_session):
        status = self.database.get_account_by_file_session(file_session)
        return True if status['status_conta'] != StatusConta.TAREFA.value else False

    def add_new_aquecimento_to_table(self, row_position, file_session, apelido):
        self.main_window.tableAquecendo.insertRow(row_position)
        self.main_window.tableAquecendo.setItem(row_position, 0, QTableWidgetItem(str(row_position + 1)))
        self.main_window.tableAquecendo.setItem(row_position, 1, QTableWidgetItem(datetime.datetime.now().strftime('%d/%m/%Y')))
        
        conta_id = f"{file_session} | {apelido}"
        self.main_window.tableAquecendo.setItem(row_position, 2, QTableWidgetItem(conta_id))
        
        status_item = QTableWidgetItem(StatusAquecimento.AQUECENDO.name)
        status_item.setForeground(QColor(255, 165, 0))
        self.main_window.tableAquecendo.setItem(row_position, 3, status_item)
        self.main_window.tableAquecendo.setItem(row_position, 4, QTableWidgetItem(''))

    def on_save_finished(self, message):
        self.ui.labelStatus.setStyleSheet('color:green' if message == "Finalizado" else 'color:red')
        self.ui.labelStatus.setText(message)
            
    def update_table_aquecendo(self, row_position, conta, data_inicio, status, observacoes):
        self.main_window.tableAquecendo.setItem(row_position, 1, QTableWidgetItem(data_inicio))
        self.main_window.tableAquecendo.setItem(row_position, 2, QTableWidgetItem(conta))
        
        status_item = QTableWidgetItem(status)
        status_color = QColor(0, 255, 0) if status == StatusAquecimento.FINALIZADO.name else QColor(255, 0, 0)
        status_item.setForeground(status_color)
        self.main_window.tableAquecendo.setItem(row_position, 3, status_item)
        
        self.main_window.tableAquecendo.setItem(row_position, 4, QTableWidgetItem(observacoes))

    def remove_selected_row(self):
        selected_row = self.main_window.tableAquecendo.currentRow()
        if selected_row >= 0:
            conta_id_item = self.main_window.tableAquecendo.item(selected_row, 2)
            if conta_id_item:
                conta_id = conta_id_item.text().split('|')[0].strip()
                self.database.delete_aquecimento(conta_id)
                self.main_window.tableAquecendo.removeRow(selected_row)
                
                # Stop the corresponding thread if it is running
                for thread in self.threads:
                    if thread.row_position == selected_row and thread.isRunning():
                        conta_id = f"{thread.file_session}\n{thread.apelido}"
                        self.database.update_account_status(thread.file_session, StatusConta.CONECTADA.value)
                        self.database.delete_aquecimento(conta_id)
                        print("Thread terminated.")
                        thread.terminate()
        else:
            QMessageBox.warning(None, "Seleção inválida", "Por favor, selecione uma linha para remover.")


    def handle_close_event(self, event):
        print("Closing2...")
        for thread in self.threads:
            print(thread.isRunning())
            if thread.isRunning():
                thread.terminate()
                conta_id = f"{thread.file_session}\n{thread.apelido}"
                print(conta_id)
                self.database.update_account_status(conta_id, StatusConta.CONECTADA.value)
                self.database.update_aquecimento_status(conta_id, StatusAquecimento.FALHA.value, "Aplicativo fechado inesperadamente")
        event.accept()