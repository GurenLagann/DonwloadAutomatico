import os
import re
import time
import shutil
import requests
from selenium import webdriver

links_array = []
driver = webdriver.Chrome('./Webdriver/chromedriver')
phpsessid = 'uf192b7ep3u39j7eu64jturpo2'


class Requisicao:    

    def GetLinks(self, phpsessid):
        Sda = "23/08/2019"
        Eda = "23/08/2019"
        
        
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

            
            global links_array
            #print(dx)
            for link in dx:
                links_array.append(link.split('>')[0].replace('"', ''))
                print(links_array)
            print('---- ate aqui ----')

            for link in links_array:
                 driver.get(link)

teste = Requisicao()
teste.GetLinks(phpsessid)

class Rename:
    init = "GVXPISPLFT-"
    ein = "-in"
    eout = "-out"

    #Array de numeros que serão mantidos 
    name_array = ['1401', '1403', '1404', '1405', '1406', '1407', '1408', '1409', '1410', '1414', '1415', '1416', '1417', '1418', '1601', '1603', '1605', '1606', '1609', '7000', '7001', '7002', '7003', '7004', '7005', '7006', 'e1401', 'e1404', 'e1405', 'e1406', 'e1407', 'e1408', 'e1409', 'e1410', 'e1414', 'e1415', 'e1416', 'e1418']

    path = '/home/wallace/Downloads'
    path2 = '/home/wallace/Data/in'
    path3 = '/home/wallace/Data/out'

    # For dos arquivos que serão renomeados
    for filename in os.listdir(path):
        filename_without_ext = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]
        #Separa o nome do arquivo em uma lista para o nome ser desmembrado e reorganizado em um novo nome
       
        n = filename.split('-')
        #For para verificar os arquivos que estão no nome_array para modificar o nome, os que não estão serão apagados    
       
        for ramal in name_array:
            inList = False
            #Verifica se a separação da lista n tem mais de 4 itens dentro dela
            
            tl = len(n)
            if tl >= 4: 

                if n[2] == ramal:
                    inList = True
                    new_file_name = init+n[0]+n[1]+"-"+n[2]+"-"+n[3]+eout+".wav"             
                    try:
                        os.rename(os.path.join(path, filename),
                            os.path.join(path3, new_file_name))
                        #todo: shutil.move(path, path2)                
                    except:
                        print("Socorro 01!" + filename)                    
                    print(filename)
                    break
                
                elif n[3] == ramal:
                    inList = True
                    new_file_name = init+n[0]+n[1]+"-"+n[2]+"-"+n[3]+ein+".wav"               
                    try:
                        os.rename(os.path.join(path, filename),
                            os.path.join(path2, new_file_name))
                        # shutil(path, path3)                   
                    except:
                        print("Socorro 02!" + filename)
                    print(filename)
                    break
                
                # if inList == False:
                #     try:
                #         print(os.remove(os.path.join(path, filename)))
                #     except:
                #         print("Porque Senhor, PQ!!!!!!!")
            
            # else:
            #     try:
            #         print(os.remove(os.path.join(path, filename)))
            #     except:   
            #         print("Porque Senhor, PQ!!!!!!!")

time.sleep(10)
teste2 = Rename()

teste2
