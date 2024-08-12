
from PyQt5.QtCore import QThread, pyqtSignal
from Database.Database import Database


class ThreadRemoverGrupo(QThread):
    account_removed = pyqtSignal(int)

    def __init__(self, db_path, group, row):
        super().__init__()
        self.db_path = db_path
        self.group = group
        self.row = row

    def run(self):
        self.database = Database(self.db_path)
        self.database.remove_group(self.group)
        
        self.account_removed.emit(self.row)