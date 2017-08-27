import os
import re

pattern = re.compile(r'(以太网适配器 (以太网|本地连接)).*?物理地址.*?: (.*?)' + '\n', re.DOTALL)
infos = os.popen("ipconfig /all").read()
match = pattern.search(infos)
FOUNDED = match.group(1)
mac = match.group(3)


def execute(string):
    feedback = os.popen(string).readlines()
    if feedback in (['\n'], [], ['\n', '配置的 DNS 服务器不正确或不存在。\n', '\n']):
        return '修改成功\n'
    else:
        return '修改失败，配置已正确或者未以管理员身份运行\n'


def change(addr):
    gateway = addr.split('.')
    gateway[3] = '254'
    gateway = '.'.join(gateway)

    print(u'尝试设置ip地址为: %s' % addr)
    print(u'        子网掩码为: %s' % '255.255.255.0')
    print(u'        默认网关为: %s' % gateway)
    execute('netsh interface ipv4 set address name="%s" source=static addr=%s mask=255.255.255.0 gateway=%s' % (FOUNDED, addr, gateway))

    print(u'尝试设置默认DNS为: %s' % '10.10.10.10(时间可能稍长请稍等)')
    execute('netsh interface ipv4 add dns name="%s" address=10.10.10.10 index=1' % FOUNDED)