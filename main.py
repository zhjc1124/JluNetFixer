import os
import re

pattern = re.compile(r'(以太网适配器 (以太网|本地连接)).*?物理地址.*?: (.*?)' + '\n', re.DOTALL)
infos = os.popen("ipconfig /all").read()
match = pattern.search(infos)
FOUNDED = match.group(1)
mac = match.group(3)


def pressexit():
    input(u'按Enter键退出...')
    os._exit(1)


def execute(string):
    feedback = os.popen(string).readlines()
    if feedback in (['\n'], [], ['\n', '配置的 DNS 服务器不正确或不存在。\n', '\n']):
        print(u'修改成功')
    else:
        print(u'修改失败，配置已正确或者未以管理员身份运行')


def change():
    try:
        f = open('D:/ip_address.txt', 'r')           # 获取ip地址
        addr = f.read()
        f.close()
        print(u'检测到本地配置')
    except FileNotFoundError:
        print(u'未检测到本地配置')
        if not FOUNDED:  # 输出信息
            input(u'未经检测到以太网网卡，请手动检查是否禁用以太网或者电脑没有以太网网卡')
            pressexit()
        print(u'检测到以太网网卡地址为:', mac)
        input(u'请登录ip.jlu.edu/pay,然后将此网卡地址填入开网时所需的物理地址中(按Enter键继续): ')
        addr = input(u'请填入学校分配的ip地址: ')
        with open('D:/ip_address.txt', 'w') as f:
            f.write(addr)
            print(u'成功将ip地址保存到本地')

    gateway = addr.split('.')      # 得到网关
    gateway[3] = '254'
    gateway = '.'.join(gateway)

    print(u'尝试设置ip地址为: %s' % addr)
    print(u'        子网掩码为: %s' % '255.255.255.0')
    print(u'        默认网关为: %s' % gateway)
    execute('netsh interface ipv4 set address name="%s" source=static addr=%s mask=255.255.255.0 gateway=%s' % (FOUNDED, addr, gateway))

    print(u'尝试设置默认DNS为: %s' % '10.10.10.10(时间可能稍长请稍等)')
    execute('netsh interface ipv4 add dns name="%s" address=10.10.10.10 index=1' % FOUNDED)
    pressexit()


def reset():
    try:
        f = open('D:/ip_address.txt', 'r')
        f.close()
        print(u'检测到本地配置')
    except FileNotFoundError:
        print(u'未检测到本地配置')
        for line in os.popen("netsh -c interface dump").readlines():
            if 'add address name="%s"' % FOUNDED in line:
                addr = line.split(' ')[1].split('=')[1]
                print(u'读取到本机设置的ip地址为%s并存储到本地' % addr)
                with open('D:/ip_address.txt', 'w') as f:
                    f.write(addr)
                    print(u'成功将ip地址保存到本地')

    print(u'尝试设置自动获取ip地址')
    execute('netsh interface ipv4 set address "%s" dhcp' % FOUNDED)

    print(u'尝试设置自动静态DNS')
    execute('netsh interface ipv4 set dns "%s" dhcp' % FOUNDED)
    pressexit()


def main():
    print('请务必以右键管理员身份运行')
    print('请确保电脑连上JLU.PC来运行爬虫获取在线配置')
    print('获取的ip地址默认存储在D:/ip_address.txt, 可手动查看或修改')
    while True:
        print(u'请选择一项\n1.在学校  2.在家里')
        print(u'请输入序号(输入q退出): ')
        choice = input()
        if choice == '1':
            change()
        elif choice == '2':
            reset()
        elif choice == 'q':
            os._exit(0)
        else:
            print(u'输入错误请重新输入')
if __name__ == "__main__":
    main()
