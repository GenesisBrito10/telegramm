import datetime
from PyQt5.QtWidgets import QDialog, QListWidgetItem, QTableWidgetItem, QPushButton, QMessageBox,QAbstractItemView
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon,QColor,QBrush
from Enums.TipoConta import TipoConta
from Views.EncherGrupoView import Ui_Dialog as Ui_EncherGrupoDialog
from Database.Database import Database
from Threads.ThreadEncherGrupo import ThreadEncherGrupo
from Enums.StatusTarefa import StatusTarefa
from Enums.StatusConta import StatusConta

class EncherGrupoController():
    def __init__(self, main_window):
        self.main_window = main_window
        #self.main_window.closeEvent = self.handle_close_event

        self.main_window.btnAddTarefaGrupo.clicked.connect(self.open_encher_grupo_dialog)
        self.main_window.btnRemoveTarefaGrupo.setEnabled(True)
        self.main_window.btnRemoveTarefaGrupo.clicked.connect(self.remove_selected_row)
        self.database = Database()
        self.threads = {}
        self.load_tarefas()

    def open_encher_grupo_dialog(self):
        self.dialog = QDialog()
        self.ui = Ui_EncherGrupoDialog()
        licence = self.database.get_licence_local()
        expiration_date = datetime.datetime.strptime(licence['vencimento'], "%d-%m-%Y")
        
        if datetime.datetime.now() > expiration_date:
            QMessageBox.warning(self.dialog, 'Warning', 'Licença Expirada!')
            return
        self.ui.setupUi(self.dialog)
        self.load_data()
        self.ui.btnSalvar.clicked.connect(self.start_encher_grupo_thread)
        self.dialog.exec_()

    def load_tarefas(self):
        tarefas = self.database.get_all_tarefas()
        for tarefa in tarefas:
            members = self.database.get_membros_by_tarefa(tarefa['id'])
            count = len(set([member['conta'] for member in members]))
            adicionados = sum([1 for member in members if member['status'] == '0'])

            self.insert_table_tarefa(tarefa['id'], tarefa['grupo_origem'], tarefa['grupo_destino'], 0, adicionados if adicionados else 0, count if count else 0, StatusTarefa(tarefa['status']).name)

    def remove_selected_row(self):
        row = self.main_window.tableTarefasGrupo.currentRow()
        if row >= 0:
            id_tarefa = self.main_window.tableTarefasGrupo.item(row, 1).text()
            self.database.delete_tarefa(id_tarefa)
            self.database.delete_membros_by_tarefa(id_tarefa)
            self.main_window.tableTarefasGrupo.removeRow(row)
            if id_tarefa in self.threads:
                self.threads[id_tarefa].terminate()
                del self.threads[id_tarefa]

    def load_data(self):
        groups = self.database.get_all_groups()
        self.ui.comboExtrair.clear()
        self.ui.comboAdicionar.clear()
        for group in groups:
            self.ui.comboExtrair.addItem(f"{group['desc']}", group)
            self.ui.comboAdicionar.addItem(f"{group['desc']}", group)

        accounts = self.database.get_accounts_by_status(0)
        self.ui.listContasWidget.clear()
        for account in accounts:
            item = QListWidgetItem(f"{account['file_session']} | {account['apelido']}")
            item.setData(QtCore.Qt.UserRole, account)
            self.ui.listContasWidget.addItem(item)

    def start_encher_grupo_thread(self):
        origin_group = self.ui.comboExtrair.currentData()
        target_group = self.ui.comboAdicionar.currentData()

        selected_items = self.ui.listContasWidget.selectedItems()
        accounts = [item.data(QtCore.Qt.UserRole) for item in selected_items]

        options = {
            'limite_dia': self.ui.spinLimiteDia.value(),
            'intervalo_dia': self.ui.spinDias.value(),
            'intervalo': self.ui.spinIntevalo.value(),
            "ativos": self.ui.checkAtivos.isChecked(),
            "remover_administradores": self.ui.checkAdministrador.isChecked(),
            "telefone": self.ui.checkTelefone.isChecked(),
            "foto": self.ui.checkFoto.isChecked()
        }

        options_db = {
            'limite_diario': self.ui.spinLimiteDia.value(),
            'intervalo_dia': self.ui.spinDias.value(),
            'intervalo': self.ui.spinIntevalo.value(),
            "ativos": 'Sim' if self.ui.checkAtivos.isChecked() else 'Não',
            "remover_administradores": 'Sim' if self.ui.checkAdministrador.isChecked() else 'Não',
            "telefone": 'Sim' if self.ui.checkTelefone.isChecked() else 'Não',
            "foto": 'Sim' if self.ui.checkFoto.isChecked() else 'Não'
        }
        print(options)

        if origin_group.get("link") == target_group.get("link"):
            self.ui.labelStatus.setText("<font color='red'>Os grupos de origem e destino não podem ser iguais.</font>")
            return
        if len(accounts) == 0:
            self.ui.labelStatus.setText("<font color='red'>Selecione ao menos uma conta.</font>")
            return
        
        id_tarefa = self.database.insert_tarefa(origin_group.get('desc'), target_group.get('desc'), StatusTarefa.PAUSADO_EXTRAINDO.value, options_db.get('intervalo'), options_db.get('ativos'), options_db.get('foto'), options_db.get('intervalo_dia'), options_db.get('limite_diario'), options_db.get('remover_administradores'), options_db.get('telefone'))

        self.thread = ThreadEncherGrupo(id_tarefa, accounts, origin_group.get('link'), target_group.get('link'), options)
        self.threads[id_tarefa] = self.thread
        self.thread.sinalMsg.connect(self.update_status)
        self.thread.sinalAdicionados.connect(self.update_adicionados)
        self.thread.sinalStart.connect(self.start_pause_thread)
        self.thread.sinalStatus.connect(self.update_status)
        self.thread.sinalFlood.connect(self.set_flood)
        self.thread.sinalAnalisados.connect(self.update_analisados)
        self.thread.sinalContaStatus.connect(self.change_status)
        self.thread.sinalQuit.connect(self.quit_thread)
        self.thread.sinalInsertTable.connect(lambda: self.insert_table_tarefa(id_tarefa, origin_group.get('desc'), target_group.get('desc'), 0, 0, len(accounts), 'Pausado'))
        self.thread.sinalDeleteTable.connect(lambda: self.database.delete_tarefa(id_tarefa))
        self.thread.start()
        self.ui.btnSalvar.setEnabled(False)
        self.dialog.close()


    def set_flood(self, session):
        for row in range(self.main_window.tableContas.rowCount()):
            status_item = self.main_window.tableContas.item(row, 1)
            print(status_item.text())
            if status_item.text() == str(session):
                itemStatus = QTableWidgetItem('Flood')
                itemStatus.setForeground(QBrush(QColor(255, 125, 0)))
                self.main_window.tableContas.setItem(row, 2, itemStatus)
                itemStatus.setTextAlignment(QtCore.Qt.AlignCenter)
        
                
    def insert_table_tarefa(self, id_tarefa, origin_group, target_group, analisados, adicionados, num_contas, status):
        
        self.main_window.tableTarefasGrupo.insertRow(0)

        items = [
            QTableWidgetItem(str(id_tarefa)),
            QTableWidgetItem(str(origin_group)),
            QTableWidgetItem(str(target_group)),
            QTableWidgetItem(str(f'{analisados}%')),
            QTableWidgetItem(str(adicionados)),
            QTableWidgetItem(str(num_contas)),
            QTableWidgetItem(str(status.split('_')[0])) if '_' in status else QTableWidgetItem(str(status))
        ]

        self.button = QPushButton("Iniciar")
        self.button.setEnabled(False)
        self.button.setIcon(QIcon("D:/Robô Telegram Pro/Views/UI\\../Icons/start.png"))
        self.button.clicked.connect(lambda: self.toggle_thread(id_tarefa))

        self.main_window.tableTarefasGrupo.setCellWidget(0, 0, self.button)
        self.main_window.tableTarefasGrupo.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for column, item in enumerate(items, start=1):  
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.main_window.tableTarefasGrupo.setItem(0, column, item)

    def toggle_thread(self, id_tarefa):

        for row in range(self.main_window.tableTarefasGrupo.rowCount()):
            if self.main_window.tableTarefasGrupo.item(row, 1).text() == str(id_tarefa):
                button = self.main_window.tableTarefasGrupo.cellWidget(row, 0)
                thread = self.threads.get(id_tarefa)
                if thread:
                    if button.text() == "Pausar":
                        button.setText("Iniciar")
                        button.setIcon(QIcon("D:/Robô Telegram Pro/Views/UI\\../Icons/start.png"))
                        thread.pause()
                    else:
                        button.setText("Pausar")
                        button.setIcon(QIcon("D:/Robô Telegram Pro/Views/UI\\../Icons/stop.png"))
                        thread.resume()
               


        

    def start_pause_thread(self,id_tarefa):
        """ if self.button.text() == "Pausar":
            self.button.setEnabled(False)
            self.button.setText("Iniciar")
            self.button.setIcon(QIcon("D:/Robô Telegram Pro/Views/UI\\../Icons/start.png"))
        else:
            self.button.setEnabled(True)
            self.button.setText("Pausar")
            self.button.setIcon(QIcon("D:/Robô Telegram Pro/Views/UI\\../Icons/stop.png")) """

        for row in range(self.main_window.tableTarefasGrupo.rowCount()):
            if self.main_window.tableTarefasGrupo.item(row, 1).text() == str(id_tarefa):
                button = self.main_window.tableTarefasGrupo.cellWidget(row, 0)
                thread = self.threads.get(id_tarefa)
                if thread:
                    if button.text() == "Pausar":
                        button.setEnabled(False)
                        button.setText("Iniciar")
                        button.setIcon(QIcon("D:/Robô Telegram Pro/Views/UI\\../Icons/start.png"))
                        
                    else:
                        button.setText("Pausar")
                        button.setEnabled(True)
                        button.setIcon(QIcon("D:/Robô Telegram Pro/Views/UI\\../Icons/stop.png"))
                        

        

    def update_adicionados(self, adicionados):
        self.main_window.tableTarefasGrupo.item(0, 5).setText(str(adicionados))

    def update_status(self, status):
        msgs = ['Você é um membro deste canal, mas não é um administrador.', 'Você é um membro deste grupo, mas não é um administrador.', 'Você não é um membro deste grupo.', 'Você não é um membro deste canal.']
        if status in msgs:
            self.ui.labelStatus.setText(f"<font color='red'>{status}</font>")
        else:
            #self.main_window.tableTarefasGrupo.item(0, 7).setText(status) 
            self.ui.labelStatus.setText(status)
            self.ui.labelStatus.setStyleSheet('color:green' if status in ["Finalizado","Iniciando a extração dos membros..."] else 'color:red')

    def quit_thread(self, status):
        print(self.thread.isRunning())
        if not status:
            print('Deu erro')
            self.thread.terminate()
            print('Terminando thread')
            
            self.ui.labelStatus.setStyleSheet('color:red')

    def update_analisados(self, value):
        self.main_window.tableTarefasGrupo.item(0, 4).setText(f"{value}%")

    def get_account_info(self, row, status):
        status_conta = self.main_view.tableContas.item(row, 2)
        status_conta.setText(status)

    def change_status(self, id_tarefa, status):
        for row in range(self.main_window.tableTarefasGrupo.rowCount()):
            if self.main_window.tableTarefasGrupo.item(row, 1).text() == str(id_tarefa):
                self.main_window.tableTarefasGrupo.item(row, 7).setText(status)
                break
       

    def handle_close_event(self, event):
        print("Closing...")
        for thread in self.threads.values():
            if thread.isRunning():
                thread.terminate()
                id_tarefa = thread.id_tarefa
                self.database.update_campo_tarefa(id_tarefa, "status", StatusTarefa.FALHA.value)
        
        tarefas = self.database.get_all_tarefas()
        for tarefa in tarefas:
            if tarefa['status'] not in [StatusTarefa.FINALIZADA.value, StatusTarefa.FALHA.value]:
                self.database.update_campo_tarefa(tarefa['id'], "status", StatusTarefa.FALHA.value)

        event.accept()

