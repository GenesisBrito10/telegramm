import datetime
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore
import requests
from Views.LicenseView import Ui_Dialog as Ui_LicenseDialog
from Database.Database import Database
 
class LicenseController(QDialog):
    license_validated = QtCore.pyqtSignal()

    def __init__(self,main_view):
        super().__init__()
        self.ui = Ui_LicenseDialog()
        self.ui.setupUi(self)
        self.main_window = main_view
        self.ui.btnValidar.clicked.connect(self.validate_license)
        self.main_window.btnAlterarLicenca.clicked.connect(self.change_license)
        self.db = Database()
        self.check_license()

    def check_license(self):
        local_license = self.db.get_licence_local()
        if local_license:
            remote_license = self.db.get_license_remote(local_license['codigo_acesso'])
            if remote_license['uuid'] and remote_license['uuid'] == self.db.get_uuid():
                if self.is_license_valid(local_license['codigo_acesso']):
                    self.main_window.labelLicense.setText(f"Licença expira em : {local_license['vencimento'].replace('-', '/')}")
                    self.show_license_info(local_license['codigo_acesso'])
            else:
                self.db.delete_license_local(local_license['codigo_acesso'])

    def show_license_info(self, license_code):
        # Exibe informações sobre a licença e prepara para abrir o aplicativo principal
        self.ui.lineCodigoAcesso.setText(license_code)
        self.ui.lineCodigoAcesso.setEnabled(False)
        self.ui.labelStatus.setText("<font color='green'>Licença validada com sucesso!</font>")
        QtCore.QTimer.singleShot(1000, self.show_next_message)  # Aguarda 3 segundos

    def show_next_message(self):
        # Exibe mensagem final antes de abrir o aplicativo principal
        self.ui.labelStatus.setText("<font color='green'>Abrindo o aplicativo...</font>")
        QtCore.QTimer.singleShot(1000, self.proceed_to_main_app)  # Aguarda mais 3 segundos

    def proceed_to_main_app(self):
        # Emite sinal para abrir o aplicativo principal
        self.license_validated.emit()
        self.accept()

    def validate_license(self):
        # Valida a licença fornecida pelo usuário
        license_code = self.ui.lineCodigoAcesso.text()
        if self.is_license_valid(str(license_code)):

            self.license_validated.emit()
            self.accept()
        else:
            self.ui.labelStatus.setText(self.message)

    def is_license_valid(self, license_code):
        if license_code:
            try:
                remote_license = self.db.get_license_remote(license_code)
                local_license = self.db.get_licence_local()
                if remote_license:
                    if not remote_license['uuid']:
                        # Se a licença é válida mas não está associada a nenhum UUID, associa ao UUID local 
                        if local_license:
                            expiration_date = remote_license['vencimento']
                            if local_license:
                                self.db.delete_license_local(local_license['codigo_acesso'])

                            self.db.insert_license_local(license_code, expiration_date)
                            self.db.update_license_remote(license_code, self.db.get_uuid())
                            self.main_window.labelLicense.setText(f"Licença expira em : {expiration_date.replace('-', '/')}")

                            return True
                        else:

                            expiration_date = remote_license['vencimento']
                            self.db.insert_license_local(license_code, expiration_date)
                            self.db.update_license_remote(license_code, self.db.get_uuid())
                            self.main_window.labelLicense.setText(f"Licença expira em : {expiration_date.replace('-', '/')}")

                            return True
                    elif remote_license['uuid']:
                        # Se a licença está associada a outro UUID, retorna erro
                        if remote_license['uuid'] != self.db.get_uuid():
                            self.message = "<font color='red'>Código de licença já utilizado. Por favor, tente novamente.</font>"
                            return False
                        else:
                            # Se a licença está associada ao UUID local, verifica a validade
                            if local_license:
                                expiration_date = datetime.datetime.strptime(local_license['vencimento'], "%d-%m-%Y")
                                if datetime.datetime.now() > expiration_date:
                                    self.message = "<font color='red'>Licença expirada. Por favor, tente novamente.</font>"
                                    return False
                            else:
                                expiration_date = datetime.datetime.strptime(remote_license['vencimento'], "%d-%m-%Y")
                                self.db.insert_license_local(license_code, remote_license['vencimento'])
                            
                            self.main_window.labelLicense.setText(f"Licença expira em : {str(expiration_date).replace('-', '/')}")
                            return True
                    
                else:
                    self.message = "<font color='red'>Código de licença inválido. Por favor, tente novamente.</font>"
                    return False
            except requests.exceptions.RequestException as e:
                print("Error:", e)
                self.message = "<font color='red'>Erro ao validar a licença. Por favor, tente novamente.</font>"
                return False
        else:
            self.message = "<font color='red'>Por favor, insira um código de acesso válido.</font>"
            return False
        
    def change_license(self):
        self.ui.labelStatus.setText("")
        self.ui.setupUi(self)
        self.ui.btnValidar.clicked.connect(self.validate_license)
        self.exec_()
