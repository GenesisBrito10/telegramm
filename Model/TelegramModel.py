
from Model.ClientModel import ClientModel
from telethon.errors import AuthRestartError,SessionPasswordNeededError

class TelegramModel:
    def __init__(self):
        
        self.client = ClientModel()
        
    async def send_code(self, phone):
        try:
            self._client = self.client.get_client(phone)
            await self._client.connect()
            await self._client.send_code_request(phone)
            return None  # Sucesso
        except AuthRestartError:
            return "Erro interno do Telegram: reinicie o processo de autorização."
       
        except Exception as e:
            return f"{str(e)}"



    async def verify_code(self, phone, code, password=None):
        
        try:
            if password:
                await self._client.sign_in(phone=phone, code=code, password=password)
            else:
                await self._client.sign_in(phone=phone, code=code)
            me = await self._client.get_me()
            nome = f"{me.first_name} {me.last_name}"
            
            await self._client.disconnect()
            return f'Conta Adicionada com Sucesso ! {nome}'
        except SessionPasswordNeededError:
            return 'Senha necessária! Por favor, insira sua senha.'
        except AuthRestartError:
            return "Erro interno do Telegram: reinicie o processo de autorização."
        
    
