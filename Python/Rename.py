import os
import shutil

init = "GVXPISPLFT-"
ein = "-in"
eout = "-out"
name_array = ['1403',
    '1404',
    '1408',
    '1416',
    '1414',
    '1415',
    '1417',
    '1410',
    '1406',
    '1418',
    '1404',
    '1401',
    '1407',
    '1405',
    '1409',
    '7000',
    '7001',
    '7002',
    '7003',
    '7004',
    '7005',
    '7006',
    '1406',
    '1405',
    '1417',
    '1415',
    '1601',
    '1603',
    '1605',
    '1606',
    '1609',
    'e1406',
    'e1404',
    'e1408',
    'e1416',
    'e1414',
    'e1415',
    'e1410',
    'e1418',
    'e1404',
    'e1401',
    'e1407',
    'e1405',
    'e1409']

path = "C:\\Users\\wallace.nascimento.LFTM\\Downloads"
for filename in os.listdir(path):
    filename_without_ext = os.path.splitext(filename)[0]
    n = filename.split('-')
    extension = os.path.splitext(filename)[1]
    for ramal in name_array:
        inList = False
    #for ramal in name_array:
        tl = len(n)
        if tl >= 4:
            if n[2] == ramal:
                inList = True
                new_file_name = init+n[0]+n[1]+"-"+n[2]+"-"+n[3]+ein+".wav"
                os.rename(os.path.join(path, filename),
                        os.path.join(path, new_file_name))
                os.remove(os.path.isfile(new_file_name))
                print(new_file_name)
                break
            elif n[3] == ramal:
                inList = True
                new_file_name = init+n[0]+n[1]+"-"+n[2]+"-"+n[3]+eout+".wav"
                os.rename(os.path.join(path, filename),
                        os.path.join(path, new_file_name))
                os.remove(os.path.isfile(new_file_name))
                print(new_file_name)
                break

            if inList == False:
                print(filename)
                try:
                    os.remove(os.path.join(path, filename))
                except:
                    print("Nao sei oq aconteceu: ")

        else:
            try:
                os.remove(os.path.join(path, filename))
            except:
                print("Nao sei oq aconteceu: ")



    
        # elif n[2] & n[3] == ramal:
                #    new_file_name2 = init+n[0]+n[1]+"-"+n[2]+"-"+n[3]+ein+".wav"
                #     new_file_name = init+n[0]+n[1]+"-"+n[2]+"-"+n[3]+eout+".wav"
                #     shutil.copyfile(path, os.path.join(path, new_file_name2))
                #     break
                #     inList = True
            
                


    # os.rename(os.path.join(path, filename),
    #     os.path.join(path, new_file_name))

    
    # if os.path.exists(filename):
    #     new_file_name = "DELET"
    #     os.rename(os.path.join(path, filename),
    #               os.path.join(path, new_file_name))
        
    # else:
    #     os.rename(os.path.join(path, filename),
    #             os.path.join(path, new_file_name))
                    
       
# Pendencias: 
#   1 - Apagar arquivos que não fazem parte do pacote que será enviado para XP
#   2 - Resolver problemas de arquivos In e Out
#   3 - Resolver problema do nome que atrapalham a função do if n[3] == ramal: 
#   4 - Problemas com nomes iguais  
