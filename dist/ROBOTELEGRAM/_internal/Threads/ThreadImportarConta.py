import asyncio
import os
import shutil
from PyQt5.QtCore import QThread, pyqtSignal
from Enums.StatusConta import StatusConta
from Enums.TipoConta import TipoConta
from Model.ClientModel import ClientModel


class ThreadImportarConta(QThread):
    account_imported = pyqtSignal(str, TipoConta, str, StatusConta, str)
    update_status = pyqtSignal(str, str, int, object)

    def __init__(self, file, destination, db_path, row,ui):
        super().__init__()
        self.file = file
        self.destination = destination
        self.db_path = db_path
        self.row = row
        self.ui = ui
        self.client = ClientModel()

    async def import_account(self, phone_number):
        shutil.copy(self.file, self.destination)
        client = self.client.get_client(phone_number)
        
        try:
            await client.connect()
            if not await client.is_user_authorized():
                status_conta = StatusConta.NAO_AUTENTICADA
                note = f"Conta {phone_number} Banida/ não autenticada"
                self.update_status.emit("Erro", note, self.row, self.ui)
            else:
                status_conta = StatusConta.CONECTADA
                note = f"Conta {phone_number} conectada com sucesso"
                me = await client.get_me()
                nome = f"{me.first_name} {me.last_name}"
                self.account_imported.emit(phone_number, TipoConta.IMPORTADA, nome, status_conta, note)
        except Exception as e:
            status_conta = StatusConta.FALHA
            note = f"Erro ao importar conta {phone_number}: {str(e)}"
            self.update_status.emit("Erro", note, self.row, self.ui)
            
        finally:
            await client.disconnect()
            if status_conta in [StatusConta.NAO_AUTENTICADA, StatusConta.FALHA]:
                try:
                    os.remove(f'sessions/{phone_number}.session')
                except Exception as e:
                    print(f"Erro ao tentar remover {phone_number}.session: {str(e)}")
            else:
                self.update_status.emit("Sucesso", note, self.row, self.ui)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        phone_number = os.path.basename(self.file).replace(".session", "")
        loop.run_until_complete(self.import_account(phone_number))