import requests
import re
from selenium import webdriver

cookies = {
    'language': 'cHRfYnI.',
    'PHPSESSID': 'o269hcfppcijk0liagacu8ggc1',
}

headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'http://192.168.3.1/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

params = (
    ('token', 'MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LnBocA..'),
    ('where', '0;start_filter|yes;calldate_day_start|19/07/2019;calldate_day_end|19/07/2019;calldate_time_start|00:00:00;calldate_time_end|23:59:59;src|;dst|;dcontext|;disposition|;disposition_colorize|1;disposition_icons|1;disposition_general|0;disposition_monitor|0;trunk|;branchname|;route|;var1|MQ..;var2|YWxs;var3|;var4|YToyOntzOjk6IklOU0VTU0lPTiI7czoxMDoicDJiX3BhaW5lbCI7czoxMzoiVVNFUl9VU0VSTkFNRSI7czo4OiJiV0Z6ZEdWeSI7fQ..'),
    ('order', 'calldate'),
    ('by', 'desc'),
    ('page', '3'),
    ('limit','100'),
    ('_', '1563544521902'),
)

response = requests.get('http://192.168.3.1/pbxip/framework/container.ajax.php',
                        headers=headers, params=params, cookies=cookies, verify=False)

dx = re.findall(r'"[a-z]+[:.].*wav"', response.text)

#print(dx)
links_array = []
for link in dx:
    links_array.append(link.split('>')[0].replace('"', ''))
#    print(links_array)
#print('---- ate aqui ----')

#print(l)
driver = webdriver.Chrome('chromedriver.exe')
#driver.get("http://192.168.3.1/pbxip/framework/")

for link in links_array:
    driver.get(link)


