import sqlite3
import uuid
import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, db_name='database.db'):
        self.db_name = db_name
        self.create_table_conta()
        self.create_table_grupo()
        self.create_table_lista()
        self.create_table_aquecimento()
        self.create_table_license()
        self.create_table_tarefa()
        self.create_table_membro()

    def get_uuid(self):
       
        mac_address = uuid.getnode()

        
        mac_address_str = ':'.join(('%012X' % mac_address)[i:i+2] for i in range(0, 12, 2))

       
        namespace = uuid.NAMESPACE_DNS
        machine_uuid = uuid.uuid5(namespace, mac_address_str)

       
        machine_uuid_upper = str(machine_uuid).upper()

        return machine_uuid_upper

    def create_table_conta(self):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            CREATE TABLE IF NOT EXISTS conta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_session TEXT NOT NULL,
                tipo_conta INTEGER,
                apelido_conta TEXT,
                status_conta INTEGER
            )
            '''
            conn.execute(query)
            conn.commit()

    def create_table_grupo(self):
        with sqlite3.connect(self.db_name) as conn:
            query = """
            CREATE TABLE IF NOT EXISTS grupo (
                id INTEGER PRIMARY KEY,
                desc TEXT NOT NULL,
                link TEXT NOT NULL UNIQUE
            );
            """
            conn.execute(query)
            conn.commit()

    def create_table_lista(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS lista (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    total_members INTEGER,
                    group_name TEXT,
                    file_path TEXT
                )
            ''')
            conn.commit()

    def create_table_aquecimento(self):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            CREATE TABLE IF NOT EXISTS aquecimento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conta_id INTEGER,
                data_inicio TEXT,
                status INTEGER,
                observacoes TEXT DEFAULT '',
                FOREIGN KEY(conta_id) REFERENCES conta(id)
            )
            '''
            conn.execute(query)
            conn.commit()

    def create_table_license(self):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            CREATE TABLE IF NOT EXISTS license (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_acesso TEXT NOT NULL,
                vencimento TEXT NOT NULL
            )
            '''
            conn.execute(query)
            conn.commit()

    def create_table_tarefa(self):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            CREATE TABLE IF NOT EXISTS tarefa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                grupo_origem TEXT NOT NULL,
                grupo_destino TEXT NOT NULL,
                status INTEGER NOT NULL,
                intervalo TEXT NOT NULL,
                membros_ativos TEXT NOT NULL,
                apenas_foto TEXT NOT NULL,
                dias TEXT NOT NULL,
                limite_diario_conta TEXT NOT NULL,
                remover_administradores TEXT NOT NULL,
                apenas_telefone TEXT NOT NULL
            )
            '''
            conn.execute(query)
            conn.commit()

    def create_table_membro(self):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            CREATE TABLE IF NOT EXISTS membro (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_tarefa INTEGER NOT NULL,
                user_id TEXT NOT NULL,
                status TEXT NOT NULL,
                conta TEXT NOT NULL,
                observacao TEXT NOT NULL,
                data TEXT NOT NULL
            )
            '''
            conn.execute(query)
            conn.commit()
    
    def insert_tarefa(self, grupo_origem, grupo_destino, status, intervalo, membros_ativos, apenas_foto, dias, limite_diario_conta, remover_administradores, apenas_telefone):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            INSERT INTO tarefa (grupo_origem, grupo_destino, status, intervalo, membros_ativos, apenas_foto, dias, limite_diario_conta, remover_administradores, apenas_telefone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            conn.execute(query, (grupo_origem, grupo_destino, status, intervalo, membros_ativos, apenas_foto, dias, limite_diario_conta, remover_administradores, apenas_telefone))
            conn.commit()

            # Get the last inserted row id
            tarefa_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            
            return tarefa_id

    def update_campo_tarefa(self,id,campo,valor):
        with sqlite3.connect(self.db_name) as conn:
            query = f'''
            UPDATE tarefa
            SET {campo} = ?
            WHERE id = ?
            '''
            conn.execute(query, (valor, id))
            conn.commit()

  

    def insert_license_local(self, codigo_acesso, vencimento):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            INSERT INTO license (codigo_acesso, vencimento)
            VALUES (?, ?)
            '''
            conn.execute(query, (codigo_acesso, vencimento))
            conn.commit()

    def delete_license_local(self, codigo_acesso):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            DELETE FROM license
            WHERE codigo_acesso = ?
            '''
            conn.execute(query, (codigo_acesso,))
            conn.commit()

    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
            host='108.167.151.99',
            database='specim38_gruposecreto',
            user='specim38_teste',
            password='lokodebala123'
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None
        
    def fetch_links(self):
        try:
            with self.connect_to_database() as connection:
                if connection:
                    cursor = connection.cursor()
                    query = "SELECT link,telegram_id FROM specim38_gruposecreto.grupos;"
                    cursor.execute(query)
                    result = cursor.fetchall()
                    accounts = []

                    for row in result:
                        accounts.append({
                            'link': row[0],
                            'telegram_id': row[1]
                        })

                    return accounts
                        
                    
                else:
                    print("Erro ao conectar ao banco de dados")
                    return None
        except Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return None
        
    def fetch_messages(self):
        try:
            with self.connect_to_database() as connection:
                if connection:
                    cursor = connection.cursor()
                    query = "SELECT `desc` FROM specim38_gruposecreto.mensagems;"
                    cursor.execute(query)
                    result = cursor.fetchall()
                    
                    return [link[0] for link in result]
                else:
                    print("Erro ao conectar ao banco de dados")
                    return None
        except Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return None
        
    def get_license_remote(self, license):
        try:
            with self.connect_to_database() as connection:
                if connection:
                    cursor = connection.cursor()
                    query = f"""
                    SELECT 
                        ca.uuid,
                        DATE_FORMAT(up.vencimento, '%d-%m-%Y') as vencimento
                    FROM 
                        specim38_gruposecreto.codigo_acessos ca
                    JOIN 
                        specim38_gruposecreto.usuario_produtos up
                    ON 
                        ca.user_id = up.user_id
                    WHERE 
                        ca.codigo_acesso = '{license}' and up.vencimento is not null and up.produto_id = 9;
                    """
                    cursor.execute(query)
                    result = cursor.fetchone()
                    if result:
                        return {
                            'uuid': result[0],
                            'vencimento': result[1]
                        }
                    else:
                        return None
                else:
                    print("Erro ao conectar ao banco de dados")
                    return None
        except Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return None
    
    def update_license_remote(self, license, new_uuid):
        try:
            with self.connect_to_database() as connection:
                if connection:
                    cursor = connection.cursor()
                    query = f"""
                    UPDATE 
                        specim38_gruposecreto.codigo_acessos
                    SET 
                        uuid = '{new_uuid}'
                    WHERE 
                        codigo_acesso = '{license}';
                    """
                    cursor.execute(query)
                    connection.commit()
                    return True
                else:
                    print("Erro ao conectar ao banco de dados")
                    return False
        except Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return False
        

    def get_licence_local(self):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            SELECT codigo_acesso, vencimento
            FROM license
            '''
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            if row:
                result = {
                    'codigo_acesso': row[0],
                    'vencimento': row[1]
                }
                return result
            else:
                return None


    def add_account(self, file_session, tipo_conta, apelido_conta, status_conta):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            INSERT INTO conta (file_session, tipo_conta, apelido_conta, status_conta)
            VALUES (?, ?, ?, ?)
            '''
            conn.execute(query, (file_session, tipo_conta.value, apelido_conta, status_conta.value))
            conn.commit()

    def update_account_status(self, file_session, status_conta):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            UPDATE conta
            SET status_conta = ?
            WHERE file_session = ?
            '''
            conn.execute(query, (status_conta, file_session))
            conn.commit()

    def update_account_apelido(self, file_session, new_apelido):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            UPDATE conta
            SET apelido_conta = ?
            WHERE file_session = ?
            '''
            conn.execute(query, (new_apelido, file_session))
            conn.commit()

    def remove_account(self, file_session):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            DELETE FROM conta
            WHERE file_session = ?
            '''
            conn.execute(query, (file_session,))
            conn.commit()

    def get_all_accounts(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT file_session, tipo_conta, apelido_conta, status_conta FROM conta")
            rows = cursor.fetchall()
            accounts = []
            for row in rows:
                accounts.append({
                    'file_session': row[0],
                    'tipo_conta': row[1],
                    'apelido_conta': row[2],
                    'status_conta': row[3]
                })
            return accounts

    def get_account_by_file_session(self, file_session):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            SELECT file_session, tipo_conta, apelido_conta, status_conta
            FROM conta
            WHERE file_session = ?
            '''
            cursor = conn.cursor()
            cursor.execute(query, (file_session,))
            row = cursor.fetchone()
            if row:
                account = {
                    'file_session': row[0],
                    'tipo_conta': row[1],
                    'apelido_conta': row[2],
                    'status_conta': row[3]
                }
                return account
            else:
                return None
    def get_account_by_apelido(self, apelido):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            SELECT file_session, tipo_conta, apelido_conta, status_conta
            FROM conta
            WHERE apelido_conta = ?
            '''
            cursor = conn.cursor()
            cursor.execute(query, (apelido,))
            row = cursor.fetchone()
            if row:
                account = {
                    'file_session': row[0],
                    'tipo_conta': row[1],
                    'apelido_conta': row[2],
                    'status_conta': row[3]
                }
                return account
            else:
                return None
            

    def add_group(self, group_desc, group_link):
        with sqlite3.connect(self.db_name) as conn:
            query = """
            INSERT INTO grupo (desc, link)
            VALUES (?, ?)
            """
            conn.execute(query, (group_desc, group_link))
            conn.commit()
    
    def update_group(self, new_desc,new_link, group_link):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            UPDATE grupo
            SET desc = ?,
            link = ?
            WHERE link = ?
            '''
            conn.execute(query, (new_desc, new_link,group_link))
            conn.commit()

    def get_all_groups(self):
        with sqlite3.connect(self.db_name) as conn:
            query = "SELECT id, desc, link FROM grupo"
            cursor = conn.execute(query)
            groups = []
            for row in cursor.fetchall():
                groups.append({
                    'id': row[0],
                    'desc': row[1],
                    'link': row[2]
                })
            return groups

    def remove_group(self, group):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            DELETE FROM grupo
            WHERE desc = ?
            '''
            conn.execute(query, (group,))
            conn.commit()

    def insert_lista(self, total_members, group_name, file_path):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO lista (total_members, group_name, file_path)
                VALUES (?, ?, ?)
            ''', (total_members, group_name, file_path))
            conn.commit()

    def get_all_listas(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT total_members, group_name, file_path FROM lista")
            rows = cursor.fetchall()
            listas = []
            for row in rows:
                listas.append({
                    'total_members': row[0],
                    'group_name': row[1],
                    'file_path': row[2]
                })
            return listas
        
    
    def get_accounts_by_status(self, status):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, file_session,apelido_conta FROM conta WHERE status_conta = ?", (status,))
            rows = cursor.fetchall()
            accounts = []
            for row in rows:
                accounts.append({
                    'id': row[0],
                    'file_session': row[1],
                    'apelido' : row[2]
                })
            return accounts
        
    def get_account_id_by_file_session(self, file_session):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM conta WHERE file_session = ?", (file_session,))
            row = cursor.fetchone()
            return row[0] if row else None

    def insert_aquecimento(self, conta_id, data_inicio, status, observacoes=''):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            INSERT INTO aquecimento (conta_id, data_inicio, status, observacoes)
            VALUES (?, ?, ?, ?)
            '''
            conn.execute(query, (conta_id, data_inicio, status, observacoes))
            conn.commit()

    def update_aquecimento_status(self, conta_id, status, observacoes):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            UPDATE aquecimento
            SET status = ?, observacoes = ?
            WHERE conta_id = ?
            '''
            conn.execute(query, (status, observacoes, conta_id))
            conn.commit()

    def delete_aquecimento(self, conta_id):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            DELETE FROM aquecimento
            WHERE conta_id = ?
            '''
            conn.execute(query, (conta_id,))
            conn.commit()

    def delete_lista(self, file_path):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            DELETE FROM lista
            WHERE file_path = ?
            '''
            conn.execute(query, (file_path,))
            conn.commit()

    def get_all_files(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT file_path FROM lista")
            rows = cursor.fetchall()
            files = []
            for row in rows:
                files.append(row[0])
            return files

    def get_all_aquecimentos(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, conta_id, data_inicio, status, observacoes FROM aquecimento")
            rows = cursor.fetchall()
            aquecimentos = []
            for row in rows:
                aquecimentos.append({
                    'id': row[0],
                    'conta_id': row[1],
                    'data_inicio': row[2],
                    'status': row[3],
                    'observacoes': row[4]
                })
            return aquecimentos
        
    def get_all_tarefas(self):
        with sqlite3.connect(self.db_name) as conn:
            query = "SELECT id, grupo_origem, grupo_destino, status, intervalo, membros_ativos, apenas_foto, dias, limite_diario_conta, remover_administradores, apenas_telefone FROM tarefa"
            cursor = conn.execute(query)
            tarefas = []
            for row in cursor.fetchall():
                tarefas.append({
                    'id': row[0],
                    'grupo_origem': row[1],
                    'grupo_destino': row[2],
                    'status': row[3],
                    'intervalo': row[4],
                    'membros_ativos': row[5],
                    'apenas_foto': row[6],
                    'dias': row[7],
                    'limite_diario_conta': row[8],
                    'remover_administradores': row[9],
                    'apenas_telefone': row[10]
                })
            return tarefas
    
    def get_tarefa_info(self, tarefa_id):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            SELECT grupo_origem, grupo_destino, status, intervalo, membros_ativos, apenas_foto, dias, limite_diario_conta, remover_administradores, apenas_telefone
            FROM tarefa
            WHERE id = ?
            '''
            cursor = conn.cursor()
            cursor.execute(query, (tarefa_id,))
            row = cursor.fetchone()
            if row:
                tarefa = {
                    'grupo_origem': row[0],
                    'grupo_destino': row[1],
                    'status': row[2],
                    'intervalo': row[3],
                    'membros_ativos': row[4],
                    'apenas_foto': row[5],
                    'dias': row[6],
                    'limite_diario_conta': row[7],
                    'remover_administradores': row[8],
                    'apenas_telefone': row[9]
                }
                return tarefa
            else:
                return None
    def delete_tarefa(self, tarefa_id):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            DELETE FROM tarefa
            WHERE id = ?
            '''
            conn.execute(query, (tarefa_id,))
            conn.commit()
            
    def insert_membro(self, id_tarefa,user_id, status, conta, observacao, data):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            INSERT INTO membro (id_tarefa,user_id, status, conta, observacao, data)
            VALUES (?, ?, ?, ?, ?, ?)
            '''
            conn.execute(query, (id_tarefa,user_id, status, conta, observacao, data))
            conn.commit()
    
    def get_membros_by_tarefa(self, id_tarefa):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            SELECT user_id, status, conta, observacao, data
            FROM membro
            WHERE id_tarefa = ?
            '''
            cursor = conn.cursor()
            cursor.execute(query, (id_tarefa,))
            rows = cursor.fetchall()
            membros = []
            for row in rows:
                membros.append({
                    'user_id': row[0],
                    'status': row[1],
                    'conta': row[2],
                    'observacao': row[3],
                    'data': row[4]
                })
            return membros
        
    def get_all_membros(self):
        with sqlite3.connect(self.db_name) as conn:
            query = "SELECT id_tarefa, user_id, status, conta, observacao, data FROM membro"
            cursor = conn.execute(query)
            membros = []
            for row in cursor.fetchall():
                membros.append({
                    'id_tarefa': row[0],
                    'user_id': row[1],
                    'status': row[2],
                    'conta': row[3],
                    'observacao': row[4],
                    'data': row[5]
                })
            return membros
    
    def delete_membros_by_tarefa(self, id_tarefa):
        with sqlite3.connect(self.db_name) as conn:
            query = '''
            DELETE FROM membro
            WHERE id_tarefa = ?
            '''
            conn.execute(query, (id_tarefa,))
            conn.commit()
        