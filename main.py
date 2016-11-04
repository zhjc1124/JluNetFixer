import os

FOUNDED = False  # 网卡是否找到
# dos运行ipconfig/all
for line in os.popen("ipconfig /all").readlines():  # 找出里面的以太网网卡
    if FOUNDED:
        if u'物理地址' in line:
            mac = line.split(':')[1].strip()
        if u'适配器' in line:
            break
    if ((u'以太网适配器 本地连接') in line):
        FOUNDED = u'本地连接'
    if ((u'以太网适配器 以太网')) in line:
        FOUNDED = u'以太网'
def pressexit():
    print(u'按Enter键退出...')
    input()
    os._exit(1)
def SMS(str):
    #print(str)
    feedback = os.popen(str).readlines()
    #for i in feedback:print(i)
    if feedback in (['\n'],[],['\n', '配置的 DNS 服务器不正确或不存在。\n', '\n']):
        print(u'修改成功')
    else:
        print(u'修改失败，配置已正确或者未以管理员身份运行')

def change():
    try:
        f = open('D:/ip_address.txt','r')           #获取ip地址
        addr = f.read()
        f.close()
        print(u'检测到本地配置')
    except Exception:
        print(u'未检测到本地配置')
        if FOUNDED:  # 输出信息
            print(u'检测到以太网网卡地址为:', mac)
            input(u'请登录ip.jlu.edu/pay,然后将此网卡地址填入开网时所需的物理地址中(按Enter键继续): ')
        else:
            input(u'未经检测到以太网网卡，请手动检查是否禁用以太网或者电脑没有以太网网卡')
            pressexit()
        addr = input(u'请填入学校分配的ip地址: ')
        with open('D:/ip_address.txt', 'w') as f:
            f.write(addr)
            print(u'成功将ip地址保存到本地')

    gateway = addr.split('.')#得到网关
    gateway[3]='254'
    gateway='.'.join(gateway)

    print(u'尝试设置ip地址为: %s'% addr)
    print(u'        子网掩码为: %s'% '255.255.255.0')
    print(u'        默认网关为: %s'% gateway)
    SMS('netsh interface ipv4 set address name="%s" source=static addr=%s mask=255.255.255.0 gateway=%s' % (FOUNDED,addr,gateway))

    print(u'尝试设置默认DNS为: %s' % '10.10.10.10(时间可能稍长请稍等)')
    SMS('netsh interface ipv4 add dns name="%s" address=10.10.10.10 index=1' % FOUNDED)
    pressexit()

def reset():
    try:
        f = open('D:/ip_address.txt','r')           #获取ip地址
        addr = f.read()
        f.close()
        print(u'检测到本地配置')
    except Exception:
        print(u'未检测到本地配置')
        for line in os.popen("netsh -c interface dump").readlines():
            if 'add address name="%s"' % FOUNDED in line:
                addr = line.split(' ')[1].split('=')[1]
                print(u'读取到本机设置的ip地址为%s并存储到本地' % addr)
                with open('D:/ip_address.txt', 'w') as f:
                    f.write(addr)
                    print(u'成功将ip地址保存到本地')

    print(u'尝试设置自动获取ip地址')
    SMS('netsh interface ipv4 set address "%s" dhcp' % FOUNDED)

    print(u'尝试设置自动静态DNS')
    SMS('netsh interface ipv4 set dns "%s" dhcp' %FOUNDED)
    pressexit()

def main():
    print(u'本程序面向不会改ip地址的纯小白')
    print(u'因为由python编写,打包成exe的文件略大,不喜勿用')
    print(u'注意:此脚本需要右键以管理员身份运行!!')
    print(u'如有建议或者bug请联系qq2991320574')
    print(u'能满足的功能：')
    print(u'尝试读取本地存储的ip配置(存储在D盘的ip_address.txt文件中，请不要随意修改)')
    print(u'电脑没保存过配置文件的情况下能引导进行校园有线网ip地址等的修改')
    print(u'电脑保存过配置的情况下能够自动设置ip地址等')
    print(u'能将有线网的设置恢复成默认并存储配置文件')
    print(u'默认设置DNS为10.10.10.10，不提供其他dns，如有需要请自行更改')

    while 1:
        print(u'请选择一项\n1.将有线网设置成校园网登录状态  2.将有线网恢复成初始状态')
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
main()