import requests
import re
from selenium import webdriver

Sd = str(input('Start Day: '))
Ed = str(input('End Day: '))

Sda = Sd+"/2019"
Eda = Ed+"/2019"

phpsessid = '7cn6eunr6c28j6v4h795o8cap7'

cookies = {
    'language': 'cHRfYnI.',
    'PHPSESSID': phpsessid,
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': '*/*',
    'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Referer': 'http://192.168.3.1/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk',
}

for page in range(1,3):
    params = (
        ('token', 'MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LnBocA..'),
        ('where', '0;start_filter|yes;calldate_day_start|'+Sda+';calldate_day_end|'+Eda+';calldate_time_start|00:00:00;calldate_time_end|23:59:59;src|;dst|;dcontext|;disposition|;disposition_colorize|1;disposition_icons|1;disposition_general|0;disposition_monitor|0;trunk|;branchname|;route|;var1|MQ..;var2|YWxs;var3|;var4|YToyOntzOjk6IklOU0VTU0lPTiI7czoxMDoicDJiX3BhaW5lbCI7czoxMzoiVVNFUl9VU0VSTkFNRSI7czo4OiJiV0Z6ZEdWeSI7fQ..'),
        ('order', 'calldate'),
        ('by', 'desc'),
        ('page', page),
        ('limit', '100'),
        ('_', '1566239217101'),
    )

    response = requests.get('http://192.168.3.1/pbxip/framework/container.ajax.php', headers=headers, params=params, cookies=cookies)

    #NB. Original query string below. It seems impossible to parse and
    #reproduce query strings 100% accurately so the one below is given
    #in case the reproduced version is not "correct".
    # response = requests.get('http://192.168.3.1/pbxip/framework/container.ajax.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LnBocA..&where=0;start_filter|yes;calldate_day_start|19/08/2019;calldate_day_end|19/08/2019;calldate_time_start|00:00:00;calldate_time_end|23:59:59;src|;dst|;dcontext|;disposition|;disposition_colorize|1;disposition_icons|1;disposition_general|0;disposition_monitor|0;trunk|;branchname|;route|;var1|MQ..;var2|YWxs;var3|;var4|YToyOntzOjk6IklOU0VTU0lPTiI7czoxMDoicDJiX3BhaW5lbCI7czoxMzoiVVNFUl9VU0VSTkFNRSI7czo4OiJiV0Z6ZEdWeSI7fQ..&order=calldate&by=desc&page=1&limit=100&_=1566239217101', headers=headers, cookies=cookies)


    dx = re.findall(r'"[a-z]+[:.].*wav"', response.text)
 
    #print(dx)
    links_array = []
    for link in dx:
        links_array.append(link.split('>')[0].replace('"', ''))
        print(links_array)
    print('---- ate aqui ----')

    #print(l)
    # open it, go to a website, and get results
    # driver = webdriver.Chrome('./chromedriver')
    # #driver.get("http://192.168.3.1/pbxip/framework/")

    # for link in links_array:
    #     driver.get(link)


