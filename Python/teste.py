import re
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup as bd
from selenium import webdriver as wb

# #container que estão as ligações
link = "http://192.168.3.1/pbxip/framework/container.ajax.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk%7CINCLUDE/aW5kZXgucmVwb3J0LnBocA..&where=0;start_filter%7Cyes;calldate_day_start%7C20/08/2019;calldate_day_end%7C20/08/2019;calldate_time_start%7C00:00:00;calldate_time_end%7C23:59:59;src%7C;dst%7C;dcontext%7C;disposition%7C;disposition_colorize%7C1;disposition_icons%7C1;disposition_general%7C0;disposition_monitor%7C0;trunk%7C;branchname%7C;route%7C;var1%7CMQ..;var2%7CYWxs;var3%7C;var4%7CYToyOntzOjk6IklOU0VTU0lPTiI7czoxMDoicDJiX3BhaW5lbCI7czoxMzoiVVNFUl9VU0VSTkFNRSI7czo4OiJiV0Z6ZEdWeSI7fQ..&order=calldate&by=desc&page=1&limit=100&_=1566334277875"
link2 = "http://192.168.3.1/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk"
link3 = "http://192.168.3.1/pbxip/framework/container.ajax.php"

driver = wb.Chrome('./chromedriver')
driver.get("http://192.168.3.1/pbxip/framework/")

#comandos para logar no site com comandos JavaScript
driver.execute_script("document.getElementById('authusername').value = 'master'")
driver.execute_script("document.getElementById('authpassword').value = 'Agil@agg9809GG'")
driver.execute_script("document.nonautenticated2.submit();")

# #Comandos para fazer a pesquisa das ligações
# driver.get("http://192.168.3.1/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk")
# driver.execute_script("page_filter()")
cookies = {
    'language': 'cHRfYnI.',
    'PHPSESSID': 'kpfkek4pjg81ng146uk2udlun7',
}   

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': '*/*',
    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Referer': 'http://192.168.3.1/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk',
}

params = (
    ('token', 'MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LnBocA..'),
    ('where', '0;start_filter|yes;calldate_day_start|19/08/2019;calldate_day_end|19/08/2019;calldate_time_start|00:00:00;calldate_time_end|23:59:59;src|;dst|;dcontext|;disposition|;disposition_colorize|1;disposition_icons|1;disposition_general|0;disposition_monitor|0;trunk|;branchname|;route|;var1|MQ..;var2|YWxs;var3|;var4|YToyOntzOjk6IklOU0VTU0lPTiI7czoxMDoicDJiX3BhaW5lbCI7czoxMzoiVVNFUl9VU0VSTkFNRSI7czo4OiJiV0Z6ZEdWeSI7fQ..'),
    ('order', 'calldate'),
    ('by', 'desc'),
    ('page', '1'),
    ('limit', '100'),
    ('_', '1566239217101'),
)

# driver.get(link)
response = requests.get(link3, headers=headers, params=params, cookies=cookies)

dx = re.findall(r'"[a-z]+[:.].*wav"', response.text)

print(dx)
# links_array = []
# for link in dx:
#     links_array.append(link.split('>')[0].replace('"', ''))
#     print(links_array)
    
# print('---- ate aqui ----')