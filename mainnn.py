import sys
from PyQt5 import QtWidgets
from Views.ViewMain import Ui_MainWindow
from Controller.AddConta import AddContaController
from Controller.ImportConta import ImportContaController
from Controller.EditConta import EditContaController
from Controller.RemoverConta import RemoverContaController
from Controller.AddGrupo import GroupController
from Controller.RemoverGrupo import RemoverGrupoController
from Controller.ExtrairLista import ExtractMembersController
from Controller.AquecerConta import AquecerContaController
from Controller.License import LicenseController
from Controller.EncherGrupo import EncherGrupoController
from Controller.EditGrupo import EditGrupoController
from Controller.DetalhesTarefa import DetalhesTarefaController

class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        

    def init_controllers(self):
        self.add_controller = AddContaController(self)
        self.import_controller = ImportContaController(self)
        self.edit_controller = EditContaController(self)
        self.remove_controller = RemoverContaController(self)
        self.group_controller = GroupController(self)
        self.remove_group_controller = RemoverGrupoController(self)
        self.extract_controller = ExtractMembersController(self)
        self.aquecer_controller = AquecerContaController(self)
        self.encher_grupo_controller = EncherGrupoController(self)
        self.edit_group_controller = EditGrupoController(self)
        self.detalhes_tarefa_controller = DetalhesTarefaController(self)

    def closeEvent(self, event):
        # Executa ações de fechamento específicas para cada controlador, se necessário
        self.aquecer_controller.handle_close_event(event)
        self.encher_grupo_controller.handle_close_event(event)
        event.accept()

def main():
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainApp()
    main_window.init_controllers()

    license_dialog = LicenseController(main_window)

    def show_main_window():
        main_window.show()

    license_dialog.license_validated.connect(show_main_window)

    if license_dialog.exec_() == QtWidgets.QDialog.Accepted:
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()
