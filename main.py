import subprocess
import socket
import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QPushButton, QLineEdit, QWidget, QTextEdit


class MainWindow(QWidget):
    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):
        ap_name_label = QLabel('Hotspot SSID')
        ap_password_label = QLabel("Hotspot password")
        self.ap_name_entry = QLineEdit()
        self.ap_password_entry = QLineEdit()

        self.ap_name_entry.setText(socket.gethostname())
        self.ap_password_entry.setText('12345678')

        '''ap_password_entry.setEchoMode()'''
        self.ap_start_button = QPushButton("Start")
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        grid_layout.addWidget(ap_name_label, 0, 0)
        grid_layout.addWidget(self.ap_name_entry, 0, 1)
        grid_layout.addWidget(ap_password_label, 1, 0)
        grid_layout.addWidget(self.ap_password_entry, 1, 1)
        grid_layout.addWidget(self.ap_start_button, 2, 0, 1, 2)
        grid_layout.addWidget(self.log_area, 3, 0, 1, 2)

        self.ap_start_button.clicked.connect(self.on_start_button_clicked)

        self.setLayout(grid_layout)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle("Easy Hotspot")
        app_icon = QtGui.QIcon()
        app_icon.addFile('img/icon_16.png', QtCore.QSize(16, 16))
        app_icon.addFile('img/icon_24.png', QtCore.QSize(24, 24))
        app_icon.addFile('img/icon_32.png', QtCore.QSize(32, 32))
        app_icon.addFile('img/icon_48.png', QtCore.QSize(48, 48))
        app_icon.addFile('img/icon_64.png', QtCore.QSize(64, 64))
        app_icon.addFile('img/icon_256.png', QtCore.QSize(256, 256))

        self.setWindowIcon(app_icon)
        self.show()

    def on_start_button_clicked(self):
        if self.ap_start_button.text() == 'Start':
            ssid = self.ap_name_entry.text();
            password = self.ap_password_entry.text();

            if len(ssid) == 0 or len(password) < 8:
                self.log_area.setText(
                    'The network ssid cannot be empty and the password must be at least 8 digits long')
            else:
                self.create_ap(ssid, password)
        else:
            self.stop_ap()

    def create_ap(self, ssid, password):
        try:
            output = subprocess.check_output('netsh wlan set hostednetwork mode=allow ssid=' + ssid + ' key=' + password, shell=True).decode('utf-8')
            self.log_area.setText(output)
            self.start_ap()
        except:
            self.showErrorMessage();

    def start_ap(self):
        try:
            output = subprocess.check_output('netsh wlan start hostednetwork', shell=True).decode('utf-8')
            self.log_area.setText(self.log_area.toPlainText() + output)
            self.ap_start_button.setText('Stop')
        except:
            self.showErrorMessage()

    def stop_ap(self):
        try:
            output = subprocess.check_output('netsh wlan stop hostednetwork', shell=True).decode('utf-8')
            self.log_area.setText(output)
            self.ap_start_button.setText('Start')
        except:
            self.showErrorMessage()

    def restore_credentials(self):

        with open('credentials') as credentials:
            data = credentials.read()
            if 'name' in data:
                pass

    def save_credentials(self):

        with open('credentials', 'w') as credentials:
            credentials.write('')

    def showErrorMessage(self):

        self.log_area.setText(
            'Oops something went wrong! \n \nPlease make sure that: \n- Your wireless adapter is on \n- Wi-Fi is turned on in Settings \n- .NET Framework 3.5 is installed \n- This app was launched with admin privileges')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_windows = MainWindow()
    sys.exit(app.exec_())
