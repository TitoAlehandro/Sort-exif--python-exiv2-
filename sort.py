import sys, os, datetime
from stat import *
import pyexiv2
def getsubs(dir):
    dirs = []
    files = []
    for dirname, dirnames, filenames in os.walk(dir):
        dirs.append(dirname)
        for subdirname in dirnames:
            dirs.append(os.path.join(dirname, subdirname))
        for filename in filenames:
            files.append(os.path.join(dirname, filename))
    return dirs, files

cur_dir = os.path.abspath(os.curdir)
main_dir = cur_dir

dirs_all, files_all = getsubs(cur_dir)
#files = os.listdir(cur_dir)
files = files_all
for f in files:
    FLAG_NOT_RENAME = 1
    
    sPathFile=os.path.join(cur_dir, f)
    nFileName = os.path.basename(sPathFile)
    if nFileName == 'sort.py':
        print "1", FLAG_NOT_RENAME, f
        FLAG_NOT_RENAME = 0
    metadata = pyexiv2.ImageMetadata(f)
    try:
        metadata.read()
        try:
            if len(metadata.exif_keys)==0:
                #print datetime.datetime.fromtimestamp(metadata._atime)  
                tag = datetime.datetime.fromtimestamp(metadata._mtime)  
                date = str(tag.day)
                month = str(tag.month)
                year = str(tag.year)
            else:
                if 'Exif.Image.DateTime' in metadata.exif_keys:
                    tag = metadata['Exif.Image.DateTime']
                    date = tag.raw_value[8:-9]
                    month = tag.raw_value[5:-12]
                    year = tag.raw_value[:4]
                elif 'Exif.Photo.DateTimeDigitized' in metadata.exif_keys:
                    tag = metadata['Exif.Photo.DateTimeDigitized']
                    date = tag.raw_value[8:-9]
                    month = tag.raw_value[5:-12]
                    year = tag.raw_value[:4]
                else:
                    tag = datetime.datetime.fromtimestamp(metadata._mtime)  
                    date = str(tag.day)
                    month = str(tag.month)
                    year = str(tag.year)
                if year == '0000':
                    tag = datetime.datetime.fromtimestamp(metadata._mtime)  
                    date = str(tag.day)
                    month = str(tag.month)
                    year = str(tag.year)
        except KeyError:            
            FLAG_NOT_RENAME = 0
            print "2", FLAG_NOT_RENAME, f, metadata
    except IOError:
        #tag = time.ctime(os.path.getmtime(f))
        tag = datetime.datetime.fromtimestamp(os.stat(f).st_mtime)
        date = str(tag.day)
        month = str(tag.month)
        year = str(tag.year)        
        print "3", FLAG_NOT_RENAME, f    
    if FLAG_NOT_RENAME == 1:
        #dtFile=datetime.date.fromtimestamp(os.stat(sPathFile)[ST_CTIME])
        #print "Path: ", sPathFile, dtFile.strftime("%d.%m.%Y")
        print "ok", FLAG_NOT_RENAME, f
        
        
        try:
            os.makedirs(main_dir+'/'+year)
        except OSError:
            pass
        try:
            os.makedirs(main_dir+'/'+year+'/'+month)
        except OSError:
            pass
        try:
            os.makedirs(main_dir+'/'+year+'/'+month + '/' + date)
        except OSError:
            pass
        oldDst = sPathFile
        newDst = (main_dir+'/'+year+'/'+month + '/' + date + '/' + nFileName)

        def recurs_name(file_name):
            try:
                newDst = (main_dir+'/'+year+'/'+month + '/' + date + '/' +'_'+ file_name)
                os.rename( oldDst, newDst)
            except OSError:
                recurs_name('_'+ file_name)

        try:
            os.rename( oldDst, newDst )
        except OSError:
            try:
                recurs_name(nFileName)
            except OSError:
                pass