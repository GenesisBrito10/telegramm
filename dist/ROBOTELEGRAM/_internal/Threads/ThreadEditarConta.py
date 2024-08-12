
from PyQt5.QtCore import QThread, pyqtSignal
from Database.Database import Database


class ThreadEditarConta(QThread):
    account_edited = pyqtSignal(str, int)

    def __init__(self, db_path, phone, new_apelido, row):
        super().__init__()
        self.db_path = db_path
        self.phone = phone
        self.new_apelido = new_apelido
        self.row = row

    def run(self):
        self.database = Database(self.db_path)
        self.database.update_account_apelido(self.phone, self.new_apelido)
        
        self.account_edited.emit(self.new_apelido, self.row)


