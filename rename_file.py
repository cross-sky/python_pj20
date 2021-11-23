'''
Author: your name
Date: 2021-11-23 23:53:12
LastEditTime: 2021-11-24 01:14:20
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \video\rename_file.py
'''

import os
import os.path
import chardet

file_dir = r'D:\doc\su_720\Slink仕様書2_00-FFコマンド詳細'

def decode_name(name:str):
    result = name.encode('gbk').decode('shift_jis')

def rename(file_dir):
    '''
    parent 表示当前正在访问的文件夹路径
    dirnames 表示该文件夹下的子目录名list
    filenames 表示该文件夹下的文件list
    '''
    
    
    # first rename filenames 
    for parent, dirnames, filenames in os.walk(file_dir):
        # second rename dirname
        for dir_name in dirnames:
            try:
                dirname_new = dir_name.encode('gbk').decode('shift_jis')
                os.rename(file_dir + '/' + dir_name, file_dir + '/' + dirname_new)
            except UnicodeDecodeError as e1:
                print(e1)
                
        for filename in filenames:
            try:
                filename_new = filename.encode('gbk').decode('shift_jis')
                print(parent)
                print(filename)
                os.rename(parent + '/' + filename, parent + '/' + filename_new)
            except UnicodeDecodeError as e:
                print(e)

        
        
    print('done')

    

    '''

    for parent, dirnames, filenames in os.walk(file_dir):
        print('P: ' + parent + ',dir: ' + str(dirnames) +  'file: ' + str(filenames) +'\r\n')

    for filename in filenames:
        filename_new = ''
        os.rename(file_dir + '/' + filename, file_dir, filename_new)
    
    '''
def display_file(dir):
    for path, dir_list, file_list in os.walk(dir):
        for file_name in file_list:
            print(os.path.join(path, file_name))

def display_dir(dir):
    for path, dir_list, file_list in os.walk(dir):
        for dir_name in dir_list:
            print(os.path.join(path, dir_name))


def findAll(file_dir):
    for root, ds, fs in os.walk(file_dir):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname
if __name__ == "__main__":
    #for i in findAll(file_dir):
    #    print(i)
    rename(file_dir)