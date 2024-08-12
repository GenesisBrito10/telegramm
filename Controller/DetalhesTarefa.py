from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from Database.Database import Database
from Views.DetalhesTarefaView import Ui_Dialog
from PyQt5 import QtCore
from Enums.StatusAddMembro import StatusAddMembro
from Enums.StatusConta import StatusConta
from PyQt5.QtGui import QColor, QBrush

class DetalhesTarefaController:
        
    def __init__(self, main_window):
        self.database = Database()
        self.main_window = main_window
        self.main_window.btnDetalhesTarefa.clicked.connect(self.open_add_group_dialog)
        self.main_window.tableTarefasGrupo.itemClicked.connect(self.enable_detalhes_tarefa_button)
        
    def open_add_group_dialog(self):
        dialog = QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(dialog)
        
        selected_row = self.main_window.tableTarefasGrupo.currentRow()
        if selected_row >= 0:
            selected_item = self.main_window.tableTarefasGrupo.item(selected_row, 1)
            tarefa_id = selected_item.text()
            self.info_data = self.database.get_tarefa_info(tarefa_id)
            self.members_data = self.database.get_membros_by_tarefa(tarefa_id)
            self.table_info(self.info_data)
            self.update_membros_table()
            self.update_contas_table()
            
            self.ui.comboFiltroMembros.currentIndexChanged.connect(self.update_membros_table)
            self.ui.comboFiltroContas.currentIndexChanged.connect(self.update_contas_table)
        else:
            QMessageBox.warning(dialog, "Warning", "No row selected.")
        dialog.exec_()

    def enable_detalhes_tarefa_button(self):
        self.main_window.btnDetalhesTarefa.setEnabled(True)

    def table_info(self, info_data):
        self.ui.labelOrigem.setText(info_data['grupo_origem'])
        self.ui.labelDestino.setText(info_data['grupo_destino'])
        self.ui.labelAtivos.setText(info_data['membros_ativos'])
        self.ui.labelLimiteDiario.setText(info_data['limite_diario_conta'])
        self.ui.labelIntervalo.setText(info_data['intervalo'])
        self.ui.labelVistoUltimo.setText(info_data['dias'])

    def update_membros_table(self):
        filtro = self.ui.comboFiltroMembros.currentText()
        self.ui.tableMembros.setRowCount(0)
        filtered_data = self.filter_data(self.members_data, filtro, 'membros')
        self.table_membros(filtered_data)

    def update_contas_table(self):
        filtro = self.ui.comboFiltroContas.currentText()
        self.ui.tableContas.setRowCount(0)
        filtered_data = self.filter_contas_data(self.members_data, filtro)
        self.table_contas(filtered_data)

    def filter_data(self, data, filtro, tipo):
        if filtro == "Todos":
            return data
        elif tipo == 'membros':
            status_map = {
                "Sucesso": StatusAddMembro.SUCESSO.value,
                "Falha": StatusAddMembro.FALHA.value,
                "Flood": StatusAddMembro.FLOOD.value
            }
            return [item for item in data if int(item['status']) == status_map.get(filtro)]

    def filter_contas_data(self, data, filtro):
        if filtro == "Todos":
            return data
        status_map = {
            "Conectada": StatusConta.CONECTADA.value,
            "Não Autenticada": StatusConta.NAO_AUTENTICADA.value,
            "Falha": StatusConta.FALHA.value,
            "Flood": StatusConta.FLOOD.value
        }
        filtered_accounts = [item for item in data if self.database.get_account_by_apelido(item['conta']) and self.database.get_account_by_apelido(item['conta'])['status_conta'] == status_map.get(filtro)]
        return filtered_accounts

    def table_membros(self, members_data):
        self.ui.labelTotal.setText(str(len(members_data)))
        self.ui.labelAdicionados.setText(str(sum([1 for member in members_data if member['status'] == str(StatusAddMembro.SUCESSO.value)])))
        self.ui.labelFalha.setText(str(sum([1 for member in members_data if member['status'] in [str(StatusAddMembro.FALHA.value), str(StatusAddMembro.FLOOD.value)]])))

        for member in members_data:
            rowPosition = self.ui.tableMembros.rowCount()
            self.ui.tableMembros.insertRow(rowPosition)
            self.ui.tableMembros.setItem(rowPosition, 0, QTableWidgetItem(member['user_id']))
            status = StatusAddMembro(int(member['status'])).name
            item = QTableWidgetItem(status)
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            if status == StatusAddMembro.SUCESSO.name:
                item.setForeground(QColor('green'))
            elif status ==  StatusAddMembro.FALHA.name:
                item.setForeground(QColor('red'))
            elif status ==  StatusAddMembro.FLOOD.name:
                item.setForeground(QColor('orange'))
            self.ui.tableMembros.setItem(rowPosition, 1, item)
            self.ui.tableMembros.setItem(rowPosition, 2, QTableWidgetItem(member['conta']))
            self.ui.tableMembros.setItem(rowPosition, 3, QTableWidgetItem(member['data']))
            self.ui.tableMembros.setItem(rowPosition, 4, QTableWidgetItem(member['observacao']))

            # Center align the text in each cell
            for column in range(self.ui.tableMembros.columnCount()):
                item = self.ui.tableMembros.item(rowPosition, column)
                item.setTextAlignment(QtCore.Qt.AlignCenter)

    def table_contas(self, members_data):
        nomes_sem_repetir = list(set([member['conta'] for member in members_data]))

        for i, conta in enumerate(nomes_sem_repetir):
            rowPosition = self.ui.tableContas.rowCount()
            self.ui.tableContas.insertRow(rowPosition)
            item = QTableWidgetItem(nomes_sem_repetir[i])
            item.setTextAlignment(QtCore.Qt.AlignCenter)  
            self.ui.tableContas.setItem(rowPosition, 0, item)
            
            status = self.database.get_account_by_apelido(nomes_sem_repetir[i])
            
            item = QTableWidgetItem(str(StatusConta(status['status_conta']).name if status else 'Desconhecido'))

            if status:
                if StatusConta(status['status_conta']).name == StatusConta.CONECTADA.name:
                    item.setForeground(QColor('green'))
                elif StatusConta(status['status_conta']).name ==  StatusConta.FALHA.name:
                    item.setForeground(QColor('red'))
                elif StatusConta(status['status_conta']).name ==  StatusConta.FLOOD.name:
                    item.setForeground(QColor('orange'))
            else:
                item.setForeground(QColor('black'))

            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.tableContas.setItem(rowPosition, 1, item)

            count_status_0 = sum(1 for member in members_data if member['status'] == str(StatusAddMembro.SUCESSO.value) and member['conta'] == nomes_sem_repetir[i])

            item = QTableWidgetItem(str(count_status_0))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.tableContas.setItem(rowPosition, 2, item)
