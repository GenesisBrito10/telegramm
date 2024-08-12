import asyncio
import csv
import os
from datetime import datetime, timezone
import re
import traceback
from PyQt5.QtCore import QThread, pyqtSignal
from telethon import errors
from telethon.tl.functions.channels import JoinChannelRequest,GetFullChannelRequest,JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest,GetFullChatRequest
from telethon.tl.types import ChannelParticipantsAdmins,Chat,ChatParticipantAdmin,ChatParticipantCreator,Channel
from Model.ClientModel import ClientModel
from Database.Database import Database  

class ThreadExtrairLista(QThread):
    sinalListaExtraida = pyqtSignal(list)
    sinalMsg = pyqtSignal(str)

    def __init__(self, group, phone, group_link, options):
        super().__init__()
        self.client_model = ClientModel()
        self.db_model = Database()  
        self.group = group
        self.phone = phone
        self.group_link = group_link
        self.options = options
        print(self.options)

    def extrair_codigo_grupo(self, link):
        link = link.replace("https://t.me/+", "")
        link = link.replace("https://t.me/", "")
        link = link.replace("http://t.me/+", "")
        link = link.replace("http://t.me/", "")
        link = link.replace("t.me/+", "")
        link = link.replace("https://t.me/joinchat/", "")
        link = link.replace("t.me/joinchat/", "")
        return link

    def run(self):
        self.sinalMsg.emit("Iniciando Extração...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.main())

    async def main(self):
        try:
            client = self.client_model.get_client(self.phone)
            await client.connect()

            if not await client.is_user_authorized():
                self.sinalMsg.emit("Erro: Usuário não autorizado.")
                await client.disconnect()
                return

            group_code = self.extrair_codigo_grupo(self.group_link)
            
            entity = await self.get_entity(client, self.group_link)
            if not entity:
                await self.join_group(client, 'chat', group_code)
                entity = await self.get_entity(client, self.group_link)

            if entity:
                full_chat = await self.get_full_chat(client, entity, self.group_link)
                
                participants = await self.extract_members(client, entity, full_chat)
                #print(participants)
                
                admins = await self.extract_admins(client, entity, full_chat) if self.options.get("remover_administradores") else []
                selected_participants = await self.filter_participants(client,participants, admins)
                await self.save_to_csv(client,selected_participants, entity.title)
            else:
                self.sinalMsg.emit("Grupo não encontrado")

        except Exception as e:
            self.sinalMsg.emit(f"Erro: {str(e)}")
            traceback.print_exc()
            if client:
                await client.disconnect()

        finally:
            if client:
                await client.disconnect()

    async def extract_members(self, client, group_entity, full_chat):
        try:
            if isinstance(group_entity, Chat):
                return [await client.get_entity(participant.user_id) for participant in full_chat.participants.participants]

            if isinstance(group_entity, Channel):
                return [user for user in await client.get_participants(group_entity.id)]

        except errors.FloodWaitError as e:
            self.sinalMsg.emit(f"Erro de Flood extract: {str(e)}")
            print(f"Erro de Flood extract: {str(e)}")
        except errors.ChatAdminRequiredError:
            self.sinalMsg.emit("Erro: Administração do chat requerida.")
            print("Erro: Administração do chat requerida.")
        except Exception as e:
            self.sinalMsg.emit(f"Erro ao extrair membros: {str(e)}")
            print(f"Erro ao extrair membros: {str(e)}")

        return []

    async def extract_admins(self, client, group_entity, full_chat):
        try:
            if isinstance(group_entity, Chat):
                return [participant.user_id for participant in full_chat.participants.participants
                        if isinstance(participant, (ChatParticipantAdmin, ChatParticipantCreator))]

            if isinstance(group_entity, Channel):
                return [user for user in await client.get_participants(group_entity.id, filter=ChannelParticipantsAdmins)]

        except Exception as e:
            self.sinalMsg.emit(f"Erro ao extrair administradores: {str(e)}")
            print(f"Erro ao extrair administradores: {str(e)}")

        return []

    async def get_entity(self, client, group_code):
        try:
            entity = await client.get_entity(group_code)
            return entity
        except:
            return None
    
    async def get_full_chat(self,client,entity, chat_id):
        chat_id = entity.id

        if isinstance(entity, Chat):  # já é membro do grupo
            full_chat = await client(GetFullChatRequest(chat_id))
            #print(f'Informações do grupo: {full_chat.to_json()}')
            return full_chat.full_chat

        elif isinstance(entity, Channel):  # é um canal ou supergrupo
            
            full_chat: GetFullChannelRequest = await client(GetFullChannelRequest(chat_id))
            
            #print(f'Informações do canal/supergrupo: {full_chat.to_json()}')
            
            return full_chat.full_chat
            
    
        
    async def join_group(self, client, entity, chat_id):
        try:
            if entity == 'chat':
                await client(ImportChatInviteRequest(chat_id))
            else:
                await client(JoinChannelRequest(chat_id))
        except Exception as e:
            print(f"Erro: {e}")

    async def filter_participants(self, client, participants, admins):
        selected_participants = []
        for member in participants:
            
            try:
                #member = await client.get_entity(user)
                if member.bot:
                    continue
                if self.options.get("ativos"):
                    if not member.status:
                        continue
                    last_seen = member.status.was_online if hasattr(member.status, 'was_online') else None
                    if last_seen and (datetime.now(timezone.utc) - last_seen).days > self.options.get("dias", 0):
                    
                        continue
                if self.options.get("username") and not member.username:
                    continue
                if self.options.get("telefone") and not member.phone:
                    continue
                if self.options.get("foto") and not member.photo:
                    continue
                if self.options.get("remover_administradores") and member.id in admins:
                    continue
                selected_participants.append(member)
            except errors.FloodWaitError as e:
                self.sinalMsg.emit(f"Erro de Flood, aguardando {str(e.seconds)} segundos.")
                await asyncio.sleep(e.seconds)
                continue
        return selected_participants

    async def save_to_csv(self, client,participants, group_name):
        if not os.path.exists('Lista'):
            os.makedirs('Lista')

        filename = f"Lista/{self.group}.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Hash', 'Telefone'])
            for user in participants:
                print(f'User: {user}')
                #member = await client.get_entity(user)
                writer.writerow([
                    user.id,
                    user.access_hash if hasattr(user, 'access_hash') else 'N/A',
                    user.phone or ''
                ])
        self.sinalMsg.emit(f"Arquivo CSV salvo em: {filename}")
        
        self.save_to_database(len(participants), group_name, filename)

    def save_to_database(self, total_members, group_name, file_path):
        try:
            self.db_model.insert_lista(total_members, group_name, file_path)
            self.sinalListaExtraida.emit(["Extração concluída.", total_members, group_name, file_path])
        except Exception as e:
            print(e)
            self.sinalMsg.emit(f"Erro ao salvar no banco de dados: {str(e)}")
