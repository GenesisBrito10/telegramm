import asyncio
import datetime
import random
from PyQt5.QtCore import QThread, pyqtSignal
from Database.Database import Database
from Enums.StatusAquecimento import StatusAquecimento
from Enums.StatusConta import StatusConta
from Model.ClientModel import ClientModel
from telethon.errors import UserAlreadyParticipantError, ChatAdminRequiredError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

class ThreadAquecerConta(QThread):
    message = pyqtSignal(str)
    table = pyqtSignal(int, str, str, str, str)  
    
    def __init__(self, conta_id, row_position):
        super().__init__()
        self.file_session = conta_id.split('|')[0].strip()
        self.apelido = ' (' +  conta_id.split('|')[1].strip() + ')'
        self.row_position = row_position
        self.client = ClientModel()
       

    def extract_group_code(self, link:str):
        link = link.replace("https://t.me/+", "")
        link = link.replace("https://t.me/", "")
        link = link.replace("http://t.me/+", "")
        link = link.replace("http://t.me/", "")
        link = link.replace("t.me/+", "")
        link = link.replace("https://t.me/joinchat/", "")
        link = link.replace("t.me/joinchat/", "")
        return link
            
    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.aquecer_conta())

    async def aquecer_conta(self):
        db = Database()
        status_before = db.get_account_by_file_session(self.file_session).get('status_conta')
        db.update_account_status(self.file_session, StatusConta.TAREFA.value)
        conta = f"{self.file_session}\n{self.apelido}"
        
        data_inicio = datetime.datetime.now().strftime('%d/%m/%Y')
        status = StatusAquecimento.AQUECENDO
        observacoes = ''

        try:
            db.insert_aquecimento(conta, data_inicio, status.value, observacoes)
            client = self.client.get_client(self.file_session)
            await client.connect()

            if not await client.is_user_authorized():
                #self.message.emit("Erro: Usuário não autorizado.")
                await client.disconnect()
                observacoes = "Erro: Usuário Banido ou não autorizado. Conecte Novamente."
                status = StatusAquecimento.FALHA.value
                db.update_aquecimento_status(conta, status, observacoes)
                self.table.emit(self.row_position, conta, data_inicio, StatusAquecimento.FALHA.name, observacoes)

                return
            
            group_links = db.fetch_links()
            messages = db.fetch_messages()

            

            for link in group_links:
                
                group_code = self.extract_group_code(link['link'])
                try:
                    try:
                        await client(JoinChannelRequest(group_code))
                        print('1 - Entrando no grupo com o código:', group_code)
                    except:
                        await client(ImportChatInviteRequest(group_code))
                        print('2 - Entrando no grupo com o código:', group_code)
                    #print(f"Entrou no grupo com o código: {group_code}")  
                except UserAlreadyParticipantError:
                    #print(f"Já está no grupo com o código: {group_code}")  
                    pass
                except ChatAdminRequiredError:
                    #print(f"Erro: Administração do chat requerida para o grupo {link}.")
                    observacoes = f"Erro: Administração do chat requerida para o grupo {link}."
                    status = StatusAquecimento.FALHA.value
                    db.update_account_status(self.file_session, status_before)
                    db.update_aquecimento_status(conta, status, observacoes)
                    self.table.emit(self.row_position, conta, data_inicio, StatusAquecimento.FALHA.name, observacoes)
                    #self.message.emit(f"Erro: Administração do chat requerida para o grupo {link}.")
                    await client.disconnect()
                    return
                except Exception as e:
                    #print(f"Erro ao entrar no grupo {link}: {str(e)}")
                    observacoes = f"Erro: {str(e)}"
                    status = StatusAquecimento.FALHA.value
                    db.update_account_status(self.file_session, status_before)
                    db.update_aquecimento_status(conta, status, observacoes)
                    self.table.emit(self.row_position, conta, data_inicio, StatusAquecimento.FALHA.name, observacoes)

                    #self.message.emit(f"Erro ao entrar no grupo primeiro for {link}: {str(e)}")
                    await client.disconnect()
                    return
                time = random.uniform(60*2, 60*4)
                print(f'Aguardando {time} segundos')
                await asyncio.sleep(time)

            # Enviar mensagens
            
            group_links = random.sample(group_links, len(group_links))
            for link in group_links:
                group_code = int(link['telegram_id']) if '-100' in link['telegram_id'] else link['telegram_id']
                group_entity = await client.get_entity(group_code)
                message = random.choice(messages)
                await client.send_message(group_entity, message)
                print(f"Mensagem enviada para o grupo {group_code}: {message}")
                time = random.uniform(60*2, 60*4)
                print(f'Aguardando {time} segundos')
                await asyncio.sleep(time)
            
            status = StatusAquecimento.FINALIZADO
            observacoes = f'Recomendamos usar a conta para extração a partir do dia: {(datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%d/%m/%Y %H:%M")}.\nFaça esse mesmo aquecimento ao menos 03 dias seguidos'
            db.update_account_status(self.file_session, status_before)
            db.update_aquecimento_status(conta, status.value, observacoes)
            self.table.emit(self.row_position, conta, data_inicio, status.name, observacoes)

            await client.disconnect()
            
            #self.message.emit("Finalizado")
        except Exception as e:
            print(e)
            observacoes = f"Erro durante o aquecimento: {str(e)}"
            status = StatusAquecimento.FALHA.value
            db.update_account_status(self.file_session, status_before)
            db.update_aquecimento_status(conta, status, observacoes)
            self.table.emit(self.row_position, conta, data_inicio, StatusAquecimento.FALHA.name, observacoes)
            if client:
                await client.disconnect()

