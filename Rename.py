import os

init = "GVXPISPLFT-"
ein = "-in"
eout = "-out"
name_array = ['1404',
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

path = input("Enter the directory path where you need to  rename: ")
for filename in os.listdir(path):
    filename_without_ext = os.path.splitext(filename)[0]
    n = filename.split('-')
    extension = os.path.splitext(filename)[1]
    print(n)
    for ramal in name_array:
        new_file_name = init+n[0]+n[1]+"-"+n[2]+"-"+n[3]+ein
        print(new_file_name)
    for ramal in name_array:
        new_file_name = init+n[0]+n[1]+"-"+n[2]+"-"+n[3]+eout
        print(new_file_name)
       
    
    #os.rename(os.path.join(path, filename),
    #          os.path.join(path, new_file_name_with_ext))
