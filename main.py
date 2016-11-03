import os
def pressexit():
    input('按Enter键退出...')
    os._exit(1)
def SMS(str):
    feedback = os.popen(str).readlines()
    if feedback != ['\n']:
        print('修改失败，请将该程序右键以管理员身份运行')
        pressexit()
    else:
        print('修改成功')
def change():
    FOUNDED = False                                                                             #网卡是否找到

    #dos运行ipconfig/all
    for line in os.popen("ipconfig /all").readlines():  # 找出里面的以太网网卡
        if FOUNDED:
            if '物理地址' in line:
                print('检测到以太网网卡地址为:', line.split(':')[1].strip())
            if '适配器' in line:
                break
        if (('以太网适配器 本地连接') in line):
            FOUNDED = '本地连接'
        if (('以太网适配器 以太网')) in line:
            FOUNDED = '以太网'

    try:
        f = open('D:/ip_address.txt','r')           #获取ip地址
        addr = f.read()
        f.close()
        print('检测到本地配置')
    except Exception:
        print('未检测到本地配置')
        if FOUNDED:  # 输出信息
            input('请登录ip.jlu.edu/pay,然后将此网卡地址填入开网时所需的物理地址中(按Enter键继续): ')
        else:
            input('未经检测到以太网网卡，请手动检查是否禁用以太网或者电脑没有以太网网卡')
            pressexit()
        addr = input('请填入学校分配的ip地址: ')
        with open('D:/ip_address.txt', 'w') as f:
            f.write(addr)
            print('成功将ip地址保存到本地')

    gateway = addr.split('.')#得到网关
    gateway[3]='254'
    gateway='.'.join(gateway)

    print('尝试设置ip地址为: %s'% addr)
    print('    子网掩码为: %s'% '255.255.255.0')
    print('    默认网关为: %s'% gateway)
    SMS('netsh interface ipv4 set address name="%s" source=static addr=%s mask=255.255.255.0 gateway=%s' % (FOUNDED,addr,gateway))

    print('尝试设置默认DNS为: %s' % '10.10.10.10')
    SMS('netsh interface ipv4 set address name="%s" source=static addr=%s mask=255.255.255.0 gateway=%s' % (FOUNDED,addr,gateway))
    pressexit()

def reset():
    try:
        f = open('D:/ip_address.txt','r')           #获取ip地址
        f.close()
        print('检测到本地配置')
    except Exception:
        print('未检测到本地配置')
        for line in os.popen("netsh -c interface dump").readlines():
            if 'add address name="以太网"' in line:
                addr = line.split(' ')[1].split('=')[1]
                print('读取到本机设置的ip地址为%s并存储到本地' % addr)
                with open('D:/ip_address.txt', 'w') as f:
                    f.write(addr)
                    print('成功将ip地址保存到本地')

    print('尝试设置成动态获取ip地址')
    SMS('set address name = "以太网" source = dhcp')

    print('尝试设置成动态获取DNS')
    SMS('set dns name = "以太网" source = dhcp')

    pressexit()

def main():
    print('本程序面向不会改ip地址的纯小白')
    print('因为由python编写,打包成exe的文件略大,不喜勿用')
    print('注意:此脚本需要右键以管理员身份运行!!')
    print('如有建议或者bug请联系qq2991320574')
    print('能满足的功能：')
    print('尝试读取本地存储的ip配置(存储在D盘的ip_address.txt文件中，请不要随意修改)')
    print('电脑没保存过配置文件的情况下能引导进行校园有线网ip地址等的修改')
    print('电脑保存过配置的情况下能够自动设置ip地址等')
    print('能将有线网的设置恢复成默认并存储配置文件')
    print('默认设置DNS为10.10.10.10，不提供其他dns，如有需要请自行更改')

    while 1:
        print('请选择一项\n1.将有线网设置成校园网登录状态  2.将有线网恢复成初始状态')
        choice = input('请输入序号(输入q退出): ')
        if choice == '1':
            change()
        elif choice == '2':
            reset()
        elif choice == 'q':
            os._exit(0)
        else:
            print('输入错误请重新输入')
main()