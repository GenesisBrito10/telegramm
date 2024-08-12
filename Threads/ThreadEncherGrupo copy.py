import asyncio
import re
from datetime import datetime, timezone
import traceback
from PyQt5.QtCore import QThread, pyqtSignal,QWaitCondition,QMutex,QMutexLocker
from telethon.errors import UserAlreadyParticipantError, ChatAdminRequiredError, FloodWaitError, PeerFloodError
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest, GetFullChannelRequest, GetParticipantRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, GetFullChatRequest, AddChatUserRequest
from telethon.tl.types import ChannelParticipantsAdmins, Chat, Channel, ChatParticipantAdmin, ChatParticipantCreator, ChannelForbidden, InputUser, InputPeerSelf, ChannelParticipantSelf, ChannelParticipantAdmin,ChannelParticipantCreator
from telethon import errors
from Model.ClientModel import ClientModel
from Database.Database import Database
from Enums.StatusTarefa import StatusTarefa
from Enums.StatusConta import StatusConta
from Enums.StatusAddMembro import StatusAddMembro
from Threads.ThreadCarregarContas import ThreadCarregarConta

class ThreadEncherGrupo(QThread):
    sinalMsg = pyqtSignal(str)
    sinalAdicionados = pyqtSignal(int)   
    sinalStatus = pyqtSignal(str)
    sinalAnalisados = pyqtSignal(int)
    sinalContaStatus = pyqtSignal(str)
    sinalQuit = pyqtSignal(bool)
    sinalInsertTable = pyqtSignal(bool)
    sinalDeleteTable = pyqtSignal(bool)
    sinalStart = pyqtSignal(bool)

    def __init__(self, id_tarefa, accounts, origin_group, target_group, options):
        super().__init__()
        self.client = ClientModel()
        self._client = None
        self.db = Database()
        self.load_accounts_thread = ThreadCarregarConta()
        self.id_tarefa = id_tarefa
        self.accounts = accounts
        self.session = accounts[0].get("file_session")
        self.origin_group = origin_group
        self.target_group = target_group
        self.options = options
        self.loop = None
        self.paused = False
        self.pause_cond = QWaitCondition()
        self.mutex = QMutex()

    def extract_hash(self, link):
        patterns = [
            "https://t.me/+", "https://t.me/", "http://t.me/+", "http://t.me/",
            "t.me/+", "https://t.me/joinchat/", "t.me/joinchat/"
        ]
        for pattern in patterns:
            link = link.replace(pattern, "")
        return link
    
    def pause(self):
        print("Pausando thread")
        self.paused = True
        self.db.update_campo_tarefa(self.id_tarefa, "status", StatusTarefa.PAUSADO_EXECUTANDO.value)
        self.sinalStatus.emit(StatusTarefa.PAUSADO_EXECUTANDO.name)
        

    def resume(self):
        print("Resumindo thread")
        self.paused = False
        self.db.update_campo_tarefa(self.id_tarefa, "status", StatusTarefa.EXECUTANDO.value)
        self.sinalStatus.emit(StatusTarefa.EXECUTANDO.name)
       
        with QMutexLocker(self.mutex):
            self.pause_cond.wakeAll()

    
    async def reconnect_client(self):
        print("Reconectando conta")
        try:
            await self._client.connect()
            if not await self._client.is_user_authorized():
                await self._client.disconnect()
                self.sinalMsg.emit("Erro: Usuário Banido ou não autorizado. Conecte Novamente.")
                self.db.update_account_status(self.session, StatusConta.NAO_AUTENTICADA.value)
                return False
            return True
        except Exception as e:
            self.sinalMsg.emit(f"Erro ao reconectar o cliente: {str(e)}")
            return False

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        self.loop.run_until_complete(self.encher_grupo())

    async def is_user_in_group(self,client,group_entity, user_entity):
        try:
            participant = await client(GetParticipantRequest(group_entity, user_entity))
            return participant is not None
        except errors.UserNotParticipantError:
            return False
        except Exception as e:
            print(f"Erro ao verificar a participação do usuário: {e}")
            return False
    
    async def verificar_entidades(self):
        for account in self.accounts:
            client = await self.get_client(account.get("file_session"))
            if not client:
                return False
            await client.connect()
         
            entity_origin = await self.get_entity(client, self.origin_group)
            entity_target = await self.get_entity(client, self.target_group)

            if isinstance(entity_target,Channel) and entity_target and entity_target.megagroup and not await self.is_user_in_group(client, entity_target, await client.get_me()):
                await self.join_group(client,'channel', self.extract_hash(self.target_group)) 

            if not entity_origin:
                await self.join_group(client, 'chat', self.extract_hash(self.origin_group))
                entity_origin = await self.get_entity(client, self.origin_group)

            if not entity_target:
                await self.join_group(client, 'chat', self.extract_hash(self.target_group))
                entity_target = await self.get_entity(client, self.target_group)

            if not entity_origin or not entity_target:
                await client.disconnect()
                return False
            
            await client.disconnect()
        
        return True

    async def encher_grupo(self):
        try:

            all_verified = await self.verificar_entidades()
            if not all_verified:
                self.sinalMsg.emit("Erro: Uma das contas selecionadas deu erro.")
                self.sinalQuit.emit(False)
                self.sinalDeleteTable.emit(True)
                self.loop.close()
                return
            
            client = await self.get_client(self.session)
            await client.connect()
            
            entity_origin = await self.get_entity(client, self.origin_group)
            entity_target = await self.get_entity(client, self.target_group)
            #print(entity_target)

            if isinstance(entity_target,Channel) and entity_target and entity_target.megagroup and not await self.is_user_in_group(client,entity_target, await client.get_me()):
                await self.join_group(client,'channel', self.extract_hash(self.target_group))      

            if not entity_origin:
                await self.join_group(client, 'chat', self.extract_hash(self.origin_group))
                entity_origin = await self.get_entity(client, self.origin_group)

            if not entity_target:
                await self.join_group(client, 'chat', self.extract_hash(self.target_group))
                entity_target = await self.get_entity(client, self.target_group)

            full_chat_origin = await self.get_full_chat(client, entity_origin) if entity_origin else None
            full_chat_target = await self.get_full_chat(client, entity_target) if entity_target else None

            if isinstance(entity_target, ChannelForbidden):
                await self.join_group(client, 'channel', self.extract_hash(self.target_group))

            if isinstance(entity_target, Channel) and not entity_target.megagroup:
                is_admin = await self.verify_admin(client, entity_target)
                if not is_admin:
                    await client.disconnect() if client else None
                    self.sinalQuit.emit(False)
                    self.sinalDeleteTable.emit(True)
                    self.loop.close()
                    return
            self.sinalInsertTable.emit(True)

            if full_chat_origin and full_chat_target:
                self.sinalStatus.emit(StatusTarefa.EXECUTANDO.name)

                participants = await self.extract_members(client, entity_origin, full_chat_origin)
                admins = await self.extract_admins(client, entity_origin, full_chat_origin)
                selected_participants = await self.filter_participants(client, participants, admins,entity_target)
                self.sinalAnalisados.emit(100)
                await client.disconnect() if client else None
                await self.add_members_to_group(selected_participants, entity_target)

        except Exception as e:
            traceback.print_exc()
            await client.disconnect() if client else None
            self.sinalMsg.emit(f"Erro ao adicionar membros: {str(e)}")
            self.sinalQuit.emit(False)
            self.loop.close()

   
    async def verify_admin(self, client, entity):
        me = await client.get_me()
        print(entity)
        try:
            participant = await client(GetParticipantRequest(entity, me))
            print(participant)

            if isinstance(participant.participant, ChannelParticipantSelf):
                #print('You are a member of this channel but is not admin.')
                self.sinalMsg.emit('Você é um membro deste canal, mas não é um administrador.')
                
                return False

            elif isinstance(participant.participant, ChannelParticipantAdmin) or isinstance(participant.participant, ChannelParticipantCreator):

                #print('You are an admin of this channel.') if participant.participant.admin_rights.invite_users else print('You are an admin of this channel, but dont have permissions to add users.')
                None if participant.participant.admin_rights.invite_users else self.sinalMsg.emit('Você é um administrador deste grupo, mas não tem permissão para adicionar usuários.')
                return True if participant.participant.admin_rights.invite_users else False
            else:
                #print('You are not a member of this channel.')
                self.sinalMsg.emit('Você não é um membro deste canal.')
                return False

                #await self.join_group('channel', self.extract_hash(self.target_group))
        except Exception as e:
            print('You are not a member of this channel. ',e)
            self.sinalMsg.emit('Você não é um membro deste canal.')
            return False
            #await self.join_group('channel', self.extract_hash(self.target_group))

    async def add_members_to_group(self, participants, group_entity):
        self.sinalStart.emit(True)

        self.total_added = 0
        tot_contas = len(self.accounts)
        tot_contas_usadas = 0
        i = 0  # Índice para rastrear o participante atual

        while i < len(participants):
            for account_index in range(tot_contas_usadas, tot_contas):
                client_atual = await self.get_client(self.accounts[account_index].get("file_session"))
                await client_atual.connect()


                try:
                    print(f"Conta atual: {self.accounts[account_index].get('file_session')}")
                    if not await client_atual.is_user_authorized():
                        await client_atual.disconnect()
                        self.sinalMsg.emit("Erro: Usuário Banido ou não autorizado. Conecte Novamente.")
                        self.db.update_account_status(self.accounts[account_index].get("file_session"), StatusConta.NAO_AUTENTICADA.value)
                        continue

                    while i < len(participants):
                        user = participants[i]
                        i += 1
                        try:
                            with QMutexLocker(self.mutex):
                                while self.paused:
                                    await client_atual.disconnect()
                                    self.pause_cond.wait(self.mutex)

                            if not client_atual.is_connected():
                                await client_atual.connect()

                            self.db.update_campo_tarefa(self.id_tarefa, "status", StatusTarefa.EXECUTANDO.value)
                            if user and not isinstance(user, InputPeerSelf):
                                await self.add_user_to_group(client_atual, user, group_entity, account_index)

                                if self.total_added >= self.options.get("limite_dia", 10):
                                    print(f"Limite diário atingido: {self.total_added} membros adicionados.")
                                    tot_contas_usadas += 1
                                    await client_atual.disconnect()
                                    break

                        except (FloodWaitError, PeerFloodError) as e:
                            tot_contas_usadas += 1
                            self.handle_flood_error(e, account_index, tot_contas)
                            print(f"Erro de Flood: {str(e)} na conta {self.accounts[account_index].get('file_session')}")
                            self.db.insert_membro(self.id_tarefa, user.id, StatusAddMembro.FALHA.value, self.accounts[account_index].get("apelido"), str(e), datetime.now().strftime("%d-%m-%Y"))
                            await self.load_accounts_thread.load_accounts()
                            await client_atual.disconnect()
                            break

                        except UserAlreadyParticipantError:
                            continue

                        except errors.InputUserDeactivatedError:
                            continue

                        except errors.UserPrivacyRestrictedError as e:
                            print(f"can't add {user} due to the user privacy setting")
                            self.db.insert_membro(self.id_tarefa, user.id, StatusAddMembro.FALHA.value, self.accounts[account_index].get("apelido"), str(e), datetime.now().strftime("%d-%m-%Y"))
                            continue
                        except errors.UserNotMutualContactError as e:
                            print(f'{user} probably was in this group early, but leave it')
                            self.db.insert_membro(self.id_tarefa, user.id, StatusAddMembro.FALHA.value, self.accounts[account_index].get("apelido"), str(e), datetime.now().strftime("%d-%m-%Y"))
                            continue
                        except errors.UserChannelsTooMuchError as e:
                            print(f'{user} is already in too many channels/supergroups.')
                            self.db.insert_membro(self.id_tarefa, user.id, StatusAddMembro.FALHA.value, self.accounts[account_index].get("apelido"), str(e), datetime.now().strftime("%d-%m-%Y"))
                            continue
                        except errors.UserKickedError as e:
                            print(f'{user} was kicked from this supergroup/channel')
                            self.db.insert_membro(self.id_tarefa, user.id, StatusAddMembro.FALHA.value, self.accounts[account_index].get("apelido"), str(e), datetime.now().strftime("%d-%m-%Y"))
                        except errors.UserBannedInChannelError as e:
                            print(f'{user} was banned from sending messages in supergroups/channels')
                            self.db.insert_membro(self.id_tarefa, user.id, StatusAddMembro.FALHA.value, self.accounts[account_index].get("apelido"), str(e), datetime.now().strftime("%d-%m-%Y"))
                            continue
                        except errors.UserBlockedError as e:
                            print(f'{user} User blocked')
                            self.db.insert_membro(self.id_tarefa, user.id, StatusAddMembro.FALHA.value, self.accounts[account_index].get("apelido"), str(e), datetime.now().strftime("%d-%m-%Y"))
                            continue
                        except errors.UserIdInvalidError as e:
                            print(f'{user} User id is invalid')
                            self.db.insert_membro(self.id_tarefa, user.id, StatusAddMembro.FALHA.value, self.accounts[account_index].get("apelido"), str(e), datetime.now().strftime("%d-%m-%Y"))
                            continue

                        except errors.ChatWriteForbiddenError as e:
                            self.sinalMsg.emit(f"Você não tem permissão para adicionar membros ao grupo {group_entity.title}.")
                            self.db.update_campo_tarefa(self.id_tarefa, "status", StatusTarefa.FALHA.value)
                            self.db.insert_membro(self.id_tarefa, user.id, StatusAddMembro.FALHA.value, self.accounts[account_index].get("apelido"), str(e), datetime.now().strftime("%d-%m-%Y"))
                            await client_atual.disconnect()
                            break

                        except Exception as e:
                            traceback.print_exc()
                            self.sinalMsg.emit(f"Erro ao adicionar membro: {str(e)}")
                            self.db.update_campo_tarefa(self.id_tarefa, "status", StatusTarefa.FALHA.value)
                            self.db.insert_membro(self.id_tarefa, user.id, StatusAddMembro.FALHA.value, self.accounts[account_index].get("apelido"), str(e), datetime.now().strftime("%d-%m-%Y"))
                            continue

                        await asyncio.sleep(self.options.get("intervalo", 0))

                except Exception as e:
                    traceback.print_exc()
                    self.sinalMsg.emit(f"Erro ao trocar de conta: {str(e)}")
                    self.db.update_account_status(self.accounts[account_index].get("file_session"), StatusConta.NAO_AUTENTICADA.value)
                    self.sinalStatus.emit(StatusTarefa.FALHA.name)
                    continue

            self.db.update_campo_tarefa(self.id_tarefa, "status", StatusTarefa.FINALIZADA.value)
            self.sinalStatus.emit(StatusTarefa.FINALIZADA.name)
            self.sinalStart.emit(True)
            await client_atual.disconnect()

        #self.sinalMsg.emit(f"{self.total_added} membros adicionados ao grupo {group_entity.title}.")

    

    async def add_user_to_group(self, client_atual, member, group_entity,tot_contas_usadas):

        if isinstance(group_entity, Channel):
            """  mm = InputUser(member.id,member.access_hash)
            print(f'Adicionando ao canal {mm}') """
            await client_atual(InviteToChannelRequest(group_entity.id, [member]))
        else:
            print(f'Adicionando ao grupo {group_entity}')
            await client_atual(AddChatUserRequest(group_entity.id, member.id, fwd_limit=10))
        
        self.total_added += 1
        self.sinalAdicionados.emit(self.total_added)
        self.db.insert_membro(self.id_tarefa,member.id,StatusAddMembro.SUCESSO.value,self.accounts[tot_contas_usadas].get("apelido"),StatusAddMembro.SUCESSO.name,datetime.now().strftime("%d-%m-%Y"))

    async def switch_client(self, client_atual, tot_contas_usadas):
        try:
            await client_atual.disconnect()
            self.sinalMsg.emit(f"Trocando para a conta {self.accounts[tot_contas_usadas].get('file_session')}")
            new_client = await self.get_client(self.accounts[tot_contas_usadas].get("file_session"))
            await new_client.connect()
            print(f"Conta {self.accounts[tot_contas_usadas].get('file_session')} conectada.")
            return new_client
        except Exception as e:
            self.sinalMsg.emit(f"Erro ao trocar de conta: {str(e)}")
            self.db.update_account_status(self.accounts[tot_contas_usadas].get("file_session"), StatusConta.NAO_AUTENTICADA.value)
            self.sinalStatus.emit(StatusTarefa.FALHA.name)
            return None

    def handle_flood_error(self, error, tot_contas_usadas, tot_contas):
        if isinstance(error, FloodWaitError):
            self.sinalMsg.emit(f"Erro de Flood: Aguarde {error.seconds} segundos.")
        else:
            self.sinalMsg.emit("Erro de Flood: Ação bloqueada temporariamente.")

        self.db.update_account_status(self.accounts[tot_contas_usadas].get("file_session"), StatusConta.FLOOD.value)
       
        #self.sinalContaStatus.emit(self.accounts[tot_contas_usadas].get("file_session"),StatusConta.FLOOD.name)
        

      

    async def get_client(self, session):
        client = self.client.get_client(session)
        await client.connect()

        if not await client.is_user_authorized():
            await client.disconnect()
            self.sinalMsg.emit("Erro: Usuário Banido ou não autorizado. Conecte Novamente.")
            self.db.update_account_status(session, StatusConta.NAO_AUTENTICADA.value)
            await self.load_accounts_thread.load_accounts()
            return None

        return client

    async def get_entity(self, client, invite_link):
        try:
            return await client.get_entity(invite_link)
        except Exception:
            return None

    async def get_full_chat(self, client, entity):
        chat_id = entity.id

        if isinstance(entity, Chat):
            full_chat = await client(GetFullChatRequest(chat_id))
            return full_chat.full_chat

        if isinstance(entity, Channel):
            full_chat = await client(GetFullChannelRequest(chat_id))
            return full_chat.full_chat

        return None

    async def extract_members(self, client, group_entity, full_chat):
        self.db.update_campo_tarefa(self.id_tarefa, "status", StatusTarefa.EXTRAINDO.value)
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

    async def filter_participants(self, client, participants, admins,entity):
        selected_participants = []
        
        for user in participants:
            try:
               
                #print(f'Userrrr: {user}')
                #member = await client.get_entity(user)

                if self.is_valid_member(user, admins):
                    selected_participants.append(InputUser(user.id,user.access_hash) if isinstance(entity, Channel) else user)
                    
                    percent = len(selected_participants) / len(participants) * 100
                    self.sinalAnalisados.emit(int(percent))
            except errors.FloodWaitError as e:
                self.sinalMsg.emit(f"Erro de Flood, aguardando {str(e.seconds)} segundos.")
                await asyncio.sleep(e.seconds)
                continue

        return selected_participants

    def is_valid_member(self, member, admins):
        #print(f'Validando membro: {member}')
        if member.bot:
            return False

        if self.options.get("ativos") and (not member.status or self.is_inactive_member(member)):
            return False

        if self.options.get("telefone") and not member.phone:
            return False

        if self.options.get("foto") and not member.photo:
            return False

        if self.options.get("remover_administradores") and member.id in admins:
            return False

        return True

    def is_inactive_member(self, member):
        last_seen = member.status.was_online if hasattr(member.status, 'was_online') else None
        return last_seen and (datetime.now(timezone.utc) - last_seen).days > self.options.get("intervalo_dia", 0)

    async def join_group(self, client, entity, invite):
        try:
            if entity == 'chat':
                await client(ImportChatInviteRequest(invite))
            else:
                await client(JoinChannelRequest(invite))
        except Exception as e:
            print(e)
            self.sinalMsg.emit(f"Erro ao entrar no grupo: {str(e)}")

