import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

cookies = {
    'language': 'cHRfYnI.',
    'PHPSESSID': '9ot1fqrkggfbod8k86d9fhos60',
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
    ('where', '0;start_filter|yes;calldate_day_start|16/07/2019;calldate_day_end|16/07/2019;calldate_time_start|00:00:00;calldate_time_end|23:59:59;src|;dst|;dcontext|;disposition|;disposition_colorize|1;disposition_icons|1;disposition_general|0;disposition_monitor|0;trunk|;branchname|;route|;var1|MQ..;var2|YWxs;var3|;var4|YToyOntzOjk6IklOU0VTU0lPTiI7czoxMDoicDJiX3BhaW5lbCI7czoxMzoiVVNFUl9VU0VSTkFNRSI7czo4OiJiV0Z6ZEdWeSI7fQ..'),
    ('order', 'calldate'),
    ('by', 'desc'),
    ('page', '1'),
    ('limit', '100'),
    ('_', '1563456005910'),
)

response = requests.get('http://192.168.3.1/pbxip/framework/container.ajax.php',
                        headers=headers, params=params, cookies=cookies, verify=False)

soup = bs(response.text, 'html.parser')
table = soup.findAll('table')
df = pd.read_html(str(table))[0]

print(df)  