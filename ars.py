import platform #get type of the type of OS
import getpass #get the username
import os.path as path #handle the directory

def getpath(filename):
    '''return the path of the file in the disk'''
    ostype = platform.system()
    if ostype == 'Linux':
        pre_path = 'media'
    elif OStype == 'Darwin': #for Mac OS
        pre_path = 'Volumes'
    else:
        pre_path = ''

    username = getpass.getuser() # get the user name

    abs_path = path.abspath(filename).split('/', 1)[-1]

    #remove pre_path from the abs_path
    pre_tmp, post_tmp = abs_path.split('/', 1)
    if pre_tmp == pre_path:
        abs_path = post_tmp
    pre_tmp, post_tmp = abs_path.split('/', 1)
    if pre_tmp == username:
        abs_path = post_tmp

    return abs_path

def gettype(filename):
    '''return the type of file in lower case'''
    return path.splitext(filename)[1].lower()

type_category = {}
type_category['PIS'] = ['jpeg', 'jpg', 'png', 'bmp', 'svg']
type_category['MOV'] = ['rmvb', 'mov', 'mp4', 'mp3', 'mkv', 'wav',\
                        'wmv', 'flv', 'avi', 'flac', 'cue']
type_category['DOC'] = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt',\
                        'pptx', 'txt', 'tex', 'eps', 'ps']
type_category['PRO'] = ['c', 'cpp', 'h', 'hpp', 'py', 'pyx', 'rb', 'pl', 'tar', 'gz']
type_category['PAK'] = ['zip', 'rar', '7z']

def file_classify(typename, class_dict=type_category):
    '''return the category of the file'''
    file_class = ''
    for class_item in class_dict.keys():
        if typename in class_dict[class_item]:
            file_class = class_item
    if not file_class: # if the file not in any category, it is 'other'
        file_class = 'other'

    return file_class

