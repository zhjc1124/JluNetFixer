from sys import argv
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QLabel, QLineEdit, QGridLayout, QTabWidget, QTextEdit
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette, QColor, QTextCursor


class DispalyPanel(QWidget):
    def __init__(self):
        super().__init__()


class MainPanel(QTabWidget):
    def __init__(self):
        super().__init__()

        self.resize(250, 150)
        self.setWindowTitle('@601040231')
        self.setWindowIcon(QIcon('py.ico'))

        self.login_box = QWidget()
        self.addTab(self.login_box, '登陆')
        self.login_panel()

        self.dis_box = QWidget()
        self.addTab(self.dis_box, '状态')

        self.text = QTextEdit()

        self.setTabEnabled(1, False)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinimizeButtonHint)
        self.setFixedSize(self.width(), self.height())
        self.show()
        self.display()

    def login_panel(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        up_layout = QGridLayout()
        usr_label = QLabel('校园卡号：')
        pwd_label = QLabel('密    码：')
        sc_label = QLabel('验 证 码：')
        up_layout.addWidget(usr_label, 1, 0)
        up_layout.addWidget(pwd_label, 2, 0)
        up_layout.addWidget(sc_label, 3, 0)

        usr_edit = QLineEdit()
        usr_edit.setToolTip('校园卡号为11位数字')

        pwd_edit = QLineEdit()
        pwd_edit.setEchoMode(QLineEdit.Password)
        pwd_edit.setToolTip('初始密码为身份证后六位，\n如果最后一位为字母则顺延一位')

        sc_layout = QGridLayout()
        sc_edit = QLineEdit()
        sc_gif = QLabel()
        sc = QPixmap('code.gif')
        sc_gif.setPixmap(sc)
        sc_gif.resize(60, 25)
        sc_layout.addWidget(sc_edit, 1, 0)
        sc_layout.addWidget(sc_gif, 1, 5)

        up_layout.addWidget(usr_edit, 1, 1)
        up_layout.addWidget(pwd_edit, 2, 1)
        up_layout.addLayout(sc_layout, 3, 1)

        btn_layout = QGridLayout()
        login_btn = QPushButton('登陆', self.login_box)
        login_btn.clicked.connect(self.display)
        quit_btn = QPushButton('退出', self.login_box)
        quit_btn.clicked.connect(QCoreApplication.quit)
        btn_layout.setSpacing(60)
        btn_layout.addWidget(login_btn, 1, 0)
        btn_layout.addWidget(quit_btn, 1, 1)

        main_layout = QGridLayout(self.login_box)
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(10)
        main_layout.addLayout(up_layout, 1, 0)
        main_layout.addLayout(btn_layout, 2, 0)

    def display(self):
        self.setCurrentIndex(1)
        self.setTabEnabled(1, True)

        lay = QGridLayout(self.dis_box)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        lay.addWidget(self.text, 1, 0)

    def checkButton(self):
        self.text.moveCursor(QTextCursor.End)
        self.text.insertPlainText(self.IPHostnameEdit.text())

if __name__ == '__main__':
    app = QApplication(argv)
    ex = MainPanel()
    app.exec_()
