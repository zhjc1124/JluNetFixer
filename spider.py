import requests
from bs4 import BeautifulSoup
from random import randint
session = requests.Session()
# 获取验证码和phpsession
safecode_url = r'https://ip.jlu.edu.cn/pay/img_safecode.php'
response = session.get(safecode_url)
phpsession = list(response.cookies)[0].value
with open('code.gif', 'wb') as f:
    f.write(response.content)

card = '20150108849'
pwd = '109308'
safecode = input()

login_url = r'https://ip.jlu.edu.cn/pay/?'
login_data = 'menu=chklogin&card=' + card + '&pwd=' + pwd + '&imgcode=' + safecode + '&x=' + str(
    randint(1, 43)) + '&y=' + str(randint(1, 23))
login_data = login_data.encode()
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://ip.jlu.edu.cn/pay/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
session.post(login_url, data=login_data, headers=headers, verify=False)


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
content = soup.find('div', {'id': 'xy_info'}).find_all('li')[1].text
ip_address = content.split('-')[0][1:]
mac = content.split('：')[-1]

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
print(soup.find('td', {'id': 'xy_info'}).find_all('li')[1].text)