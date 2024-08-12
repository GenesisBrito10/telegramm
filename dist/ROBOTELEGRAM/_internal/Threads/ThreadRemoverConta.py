
from PyQt5.QtCore import QThread, pyqtSignal
from Database.Database import Database


class ThreadRemoverConta(QThread):
    account_removed = pyqtSignal(int)

    def __init__(self, db_path, phone, row):
        super().__init__()
        self.db_path = db_path
        self.phone = phone
        self.row = row

    def run(self):
        self.database = Database(self.db_path)
        self.database.remove_account(self.phone)
        
        self.account_removed.emit(self.row)