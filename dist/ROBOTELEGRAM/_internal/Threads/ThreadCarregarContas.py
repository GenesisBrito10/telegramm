import asyncio
import os
from PyQt5.QtCore import QThread, pyqtSignal
from Database.Database import Database
from Enums.StatusConta import StatusConta
from Enums.TipoConta import TipoConta
from Model.ClientModel import ClientModel
from Database.Database import Database


class ThreadCarregarConta(QThread):
    account_loaded = pyqtSignal(str, TipoConta, str, StatusConta)

    def __init__(self):
        super().__init__()
      
        self.client = ClientModel()
        self.database = Database()
        self.remove_invalid_sessions()
       
        

    async def check_account_status(self, phone):
        client = self.client.get_client(phone)
        try:
            await client.connect()
            if not await client.is_user_authorized():
                return StatusConta.NAO_AUTENTICADA
            else:
                return StatusConta.CONECTADA
        except Exception as e:
            return StatusConta.FALHA
        finally:
            await client.disconnect()

    async def load_accounts(self):
        

        accounts = self.database.get_all_accounts()
        for account in accounts:
            phone = account['file_session']
            tipo_conta = TipoConta(account['tipo_conta'])
            apelido_conta = account['apelido_conta']
            session_file = f'sessions/{phone}.session'
            status = StatusConta(account['status_conta'])

            if not os.path.exists(session_file):
                self.database.remove_account(phone)
                continue

            if status == StatusConta.FLOOD:
                self.account_loaded.emit(phone, tipo_conta, apelido_conta, status)
                continue

                

            status_conta = await self.check_account_status(phone)
            if status_conta == StatusConta.FALHA:
                self.database.remove_account(phone)
                os.remove(session_file)
                continue
          
            self.database.update_account_status(phone, status_conta.value)
            self.account_loaded.emit(phone, tipo_conta, apelido_conta, status_conta)
        

    def remove_invalid_sessions(self):
        

        session_folder = 'sessions'
        
        for session_file in os.listdir(session_folder):
            if session_file.endswith('.session'):
                phone = session_file.split('.session')[0]
                session_file_path = os.path.join(session_folder, session_file)
                if not self.database.get_account_by_file_session(phone):
                    os.remove(session_file_path)
        

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.load_accounts())



