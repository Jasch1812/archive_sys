import platform #get type of the type of OS
import getpass #get the username
import os.path as path #handle the directory
import os
import time
import csv

def getpath(filename):
    '''return the path of the file in the disk'''
    ostype = platform.system()
    if ostype == 'Linux':
        pre_path = 'media'
    elif ostype == 'Darwin': #for Mac OS
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

    return abs_path.rstrip(filename)

def gettype(filename):
    '''return the type of file in lower case'''
    return path.splitext(filename)[1].lower()

type_category = {}
type_category['PIS'] = ['jpeg', 'jpg', 'png', 'bmp', 'svg']
type_category['MOV'] = ['rmvb', 'mov', 'mp4', 'mp3', 'mkv', 'wav',\
                        'wmv', 'flv', 'avi', 'flac', 'cue']
type_category['DOC'] = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt',\
                        'pptx', 'txt', 'tex', 'eps', 'ps']
type_category['PRO'] = ['c', 'cpp', 'h', 'hpp', 'py', 'pyc', 'pyx', 'rb', 'pl', 'tar', 'gz']
type_category['PAK'] = ['zip', 'rar', '7z']

def getsize(filename):
    return os.path.getsize(filename)

def file_classify(typename, class_dict=type_category):
    '''return the category of the file'''
    file_class = ''
    for class_item in class_dict.keys():
        print class_item
        print class_dict[class_item]
        if typename in class_dict[class_item]:
            file_class = class_item
        print "file class: ", file_class
    if not file_class: # if the file not in any category, it is 'other'
        file_class = 'other'

    return file_class

def getctime(filename):
    return time.ctime(path.getctime(filename))

def whatsin(dir_name):
    dir_list = []
    file_list = []
    for item in sorted(os.listdir(dir_name)):
        print item, os.path.isdir(path.join(dir_name,item))
        if item[0] == '.':
            # print 'pass'
            # continue
            pass

        elif os.path.isdir(path.join(dir_name,item)):
            # print "is dir"
            # dir_list.append(item.decode('utf-8'))
            dir_list.append(item)
        else:
            # file_list.append(item.decode('utf-8'))
            # print 'is file'
            file_list.append(item)
    return dir_list, file_list

class AS_Lite:
    def __init__(self):
        #self.csvfile = open('Dir_'+starting_dir, 'w')
        self.fieldnames = ['name', 'type', 'size', 'path', 'ctime']
        #self.info_write = csv.writer(self.csvfile, delimiter=',')
        #self.w = csv.DictWriter(self.csvfile, fieldnames = fieldnames)
        #self.w.writeheader()
        self.file_size_units = ['B', 'KB', 'MB', 'GB', 'TB']

    def file_size_reader(self, file_size_num):
        i = 0
        while file_size_num>=1024 and i < len(self.file_size_units)-1:
            file_size_num /= 1024.0
            i += 1
        file_size_tmp = ('%.3f' % file_size_num).rstrip('0').rstrip('.')
        return '%s %s' %(file_size_tmp, self.file_size_units[i])

    def file_class(self, filename):
        f_type = gettype(filename)
        print f_type
        f_cls = file_classify(f_type, class_dict=type_category)
        print f_cls
        return f_cls

    def dir_info(self, dir_name):
        dir_path = getpath(dir_name)
        dir_ctime = getctime(dir_name)
        dir_link = os.stat(dir_name).st_nlink
        info_dic={'name':dir_name.decode('utf-8'), 'type':'DIR', 'size':dir_link, 'path':dir_path, 'ctime':dir_ctime}
        self.w.writerow(info_dic)
        return self

    def file_info(self, file_name):
        file_nm = file_name.rsplit('/',1)[-1]
        file_path = file_name.rsplit('/',1)[0]
        file_ctime = getctime(file_name)
        file_size = self.file_size_reader(getsize(file_name))
        file_type = self.file_class(file_name)
        if file_type=='PIS':
            self.pist_num += 1
        info_file = {'name':file_nm, 'type':file_type, 'size':file_size,'path':file_path, 'ctime':file_ctime}
        self.w.writerow(info_file)
        return self

    def pist_num_reset(self):
        self.pist_num = 0
        return self

    def run(self, dir_name):
        dirs, files = whatsin(dir_name)

        #write infos about files
        print "dirs:", dirs
        print "files:", files
        self.pist_num_reset()
        for f in files:
            print f
            if self.pist_num > 10:
                break
            self.file_info(path.join(dir_name,f))
        self.pist_num_reset()

        #write infos about directories
        for d in dirs:
            self.dir_info(path.join(dir_name,d))

        #dig the infos in subdir
        for d in dirs:
            self.run(path.join(dir_name, d))

    def archive(self, dir_name, csv_name):
        with open('Dir_%s.csv' % csv_name, 'w') as csvfile:
            self.w = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            self.w.writeheader()
            self.run(dir_name)


if __name__ == '__main__':
    ar = AS_Lite()
    ar.archive('/home/johann/tmp', 'tmp')