from requests import Session
from bs4 import BeautifulSoup
from random import randint
from webbrowser import open as web_open
session = Session()
# 获取验证码和phpsession
safecode_url = r'https://ip.jlu.edu.cn/pay/img_safecode.php'
response = session.get(safecode_url)
phpsession = list(response.cookies)[0].value
with open('code.gif', 'wb') as f:
    f.write(response.content)


card = '20160100531'
pwd = '240112'
safecode = input()

login_url = r'https://ip.jlu.edu.cn/pay/?'
login_data = 'menu=chklogin&card=' + card + '&pwd=' + pwd + '&imgcode=' + safecode + '&x=' \
             + str(randint(1, 43)) + '&y=' + str(randint(1, 23))
login_data = login_data.encode()
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://ip.jlu.edu.cn/pay/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
response = session.post(login_url, data=login_data, headers=headers, verify=False)
content = response.text
login_info = ''
if '验证码有误' in content:
    login_info = '图片验证码有误，请返回重新输入。'
elif '不存在此校园卡号' in content:
    login_info = '不存在此校园卡号：%s。' % card
elif '密码验证失败' in content:
    login_info = '账号或密码错误，请检查。'
print(login_info)
headers['Referer'] = login_url
index_url = 'https://ip.jlu.edu.cn/pay/index.php'
session.get(index_url, headers=headers, verify=False)

headers['Referer'] = index_url
menu_url = 'https://ip.jlu.edu.cn/pay/index.php?menu=menu'
session.get(menu_url, headers=headers, verify=False)

headers['Referer'] = menu_url
modify_mac_url = 'https://ip.jlu.edu.cn/pay/modify_mac.php'
response = session.get(modify_mac_url, headers=headers, verify=False)

soup = BeautifulSoup(response.text, "html5lib")
content = soup.find('div', {'id': 'xy_info'})
if content:
    content = content.find_all('li')[1].text
else:
    info = '网络未开户。请登陆<a href="ip.jlu.edu.cn/pay/">自助营业厅</a>'
    web_open('ip.jlu.edu.cn/pay/', new=1)
ip_address = content.split('-')[0][1:]
mac = content.split('：')[-1]
print([ip_address, mac])

headers['Referer'] = modify_mac_url
set_mac_url = 'https://ip.jlu.edu.cn/pay/modify_mac.php?menu=set_mac&ip=' + ip_address
session.get(set_mac_url, headers=headers, verify=False)

headers['Referer'] = set_mac_url
final_url = 'https://ip.jlu.edu.cn/pay/modify_mac.php?'
mac = [mac[2*i:2*i+2] for i in range(6)]
mac_data = 'menu=save_set_mac' + ''.join(['&mac%s=%s' % (index+1, value) for index, value in enumerate(mac)])
mac_data = mac_data.encode('utf-8')
response = session.post(set_mac_url, data=mac_data, headers=headers, verify=False)
soup = BeautifulSoup(response.text, "html5lib")
modify_info = soup.find('td', {'id': 'xy_info'}).find_all('li')[1].text
print(modify_info)

