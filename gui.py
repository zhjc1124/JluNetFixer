from sys import argv
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QLabel, QLineEdit, QGridLayout, QTabWidget, QTextEdit
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette, QColor, QTextCursor
import mac
import spider
from webbrowser import open as web_open
import time
import threading


class DispalyPanel(QWidget):
    def __init__(self):
        super().__init__()


class MainPanel(QTabWidget):
    def __init__(self):
        super().__init__()

        self.resize(250, 150)
        self.setWindowTitle('JluNetFixer@601040231')
        self.setWindowIcon(QIcon('py.ico'))

        self.login_box = QWidget()
        self.addTab(self.login_box, '登陆')
        self.usr_edit = QLineEdit()
        self.pwd_edit = QLineEdit()
        self.sc_edit = QLineEdit()

        self.login_panel()

        self.dis_box = QWidget()
        self.addTab(self.dis_box, '状态')

        self.text = QTextEdit()
        self.text.setReadOnly(True)

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinimizeButtonHint)
        self.setFixedSize(self.width(), self.height())
        self.ini()

    def login_panel(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        up_layout = QGridLayout()
        usr_label = QLabel('校园卡号：')
        pwd_label = QLabel('密    码：')
        sc_label = QLabel('验 证 码：')
        up_layout.addWidget(usr_label, 1, 0)
        up_layout.addWidget(pwd_label, 2, 0)
        up_layout.addWidget(sc_label, 3, 0)

        self.usr_edit.setToolTip('校园卡号为11位数字')

        self.pwd_edit.setEchoMode(QLineEdit.Password)
        self.pwd_edit.setToolTip('初始密码为身份证后六位，\n如果最后一位为字母则顺延一位')

        sc_layout = QGridLayout()
        sc_gif = QLabel()
        sc = QPixmap('code.gif')
        sc_gif.setPixmap(sc)
        sc_gif.resize(60, 25)
        sc_layout.addWidget(self.sc_edit, 1, 0)
        sc_layout.addWidget(sc_gif, 1, 5)

        up_layout.addWidget(self.usr_edit, 1, 1)
        up_layout.addWidget(self.pwd_edit, 2, 1)
        up_layout.addLayout(sc_layout, 3, 1)

        btn_layout = QGridLayout()
        login_btn = QPushButton('登陆', self.login_box)
        login_btn.clicked.connect(self.thread)
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

    def ini(self):
        lay = QGridLayout(self.dis_box)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        lay.addWidget(self.text, 1, 0)
        self.show()

    def display(self):
        self.setTabEnabled(0, False)
        self.text.setText('')
        self.setCurrentIndex(1)
        if not mac.FOUNDED:
            self.text.insertPlainText(u'未经检测到以太网网卡\n')
        else:
            self.text.insertPlainText('本机mac为: ' + mac.mac + '\n')
        self.text.insertPlainText('尝试进行登陆......\n')
        result = spider.login(self.usr_edit.text(), self.pwd_edit.text(), self.sc_edit.text())
        if result == 1:
            self.text.insertPlainText('图片验证码有误。\n')
        elif result == 2:
            self.text.insertPlainText('不存在此校园卡号：' + self.usr_edit.text() + '\n')
        elif result == 3:
            self.text.insertPlainText('账号或密码错误。\n')
        elif result == 4:
            self.text.insertPlainText('网络未开户。请登陆自助营业厅进行开户\n')
            time.sleep(5)
            web_open("https://ip.jlu.edu.cn/pay/")
        else:
            ip, mac_address = result
            mac_ = ''.join(mac.mac.split("-"))
            if mac_ != mac_address:
                self.text.insertPlainText('mac地址不符。尝试修改...\n')
                self.text.insertPlainText(spider.modify_mac(ip, mac_))
            gateway = ip.split('.')
            gateway[3] = '254'
            gateway = '.'.join(gateway)
            self.text.insertPlainText('尝试设置ip地址为: %s' % ip + '\n')
            self.text.insertPlainText('        子网掩码为: %s' % '255.255.255.0\n')
            self.text.insertPlainText('        默认网关为: %s' % gateway + '\n')
            self.text.insertPlainText(mac.execute(
                'netsh interface ipv4 set address '
                'name="%s" '
                'source=static '
                'addr=%s '
                'mask=255.255.255.0 '
                'gateway=%s' % (mac.FOUNDED, ip, gateway)))
            self.text.insertPlainText('尝试设置默认DNS为: 10.10.10.10(时间可能稍长请稍等)\n')
            self.text.insertPlainText(
                mac.execute(
                    'netsh interface ipv4 add dns '
                    'name="%s" '
                    'address=10.10.10.10 '
                    'index=1' % mac.FOUNDED))
            self.text.insertPlainText('尝试设置默认DNS为: 10.10.10.10(时间可能稍长请稍等)\n')
        self.text.insertPlainText('程序将在10秒后自动关闭。\n')
        time.sleep(10)
        QCoreApplication.quit()

    def thread(self):
        t = threading.Thread(target=self.display, args=())
        t.start()


if __name__ == '__main__':
    app = QApplication(argv)
    ex = MainPanel()
    app.exec_()
