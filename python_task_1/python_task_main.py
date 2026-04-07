import string
import sys
#import os
from pathlib import Path
import shutil
import cyrtranslit

def normalize(in_str):
    return_sr_start = cyrtranslit.to_latin(in_str,"ua")
    return_str = ""
    for locSymb in return_sr_start:
        if locSymb in string.ascii_letters:
            return_str = return_str + locSymb
        elif locSymb in string.digits:
            return_str = return_str + locSymb
        else:
            return_str = return_str + "_"

    return return_str

def sort_files(in_folder):
    l_image = ['JPEG', 'PNG', 'JPG', 'SVG']
    l_document = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
    l_video = ['AVI', 'MP4', 'MOV', 'MKV']
    l_audio = ['MP3', 'OGG', 'WAV', 'AMR']
    l_archive = ['ZIP', 'GZ', 'TAR']
    file_extension_dict = {("images",l_image),("documents",l_document),("videos",l_video),("audio",l_audio),("archives",l_archive)}
    #new_Folder = ""
    p = Path(in_folder)
    for fn,t in file_extension_dict:
        for locExt in t:
            for tf in list(p.glob("*."+locExt)):
                if fn=="archives":
                    shutil.unpack_archive(str(tf),in_folder+"\\"+fn)
                else:
                    shutil.move(str(tf), in_folder+"\\"+fn)
    for tf in list(p.glob("*.*")):
        shutil.move(str(tf), in_folder + "\\other")
    return 0

def sort_folders(in_folder=""):
    p = Path(in_folder)
    for x in p.iterdir():
        if x.is_dir():
            #print(x.name)
            loc_folder = in_folder+"\\"+x.name
            print(loc_folder)
            sort_folders(loc_folder)
        sort_files(in_folder)
        #for tf in list(p.glob("*.*")):
        #    sort_file(tf,in_folder)


    #print([x  if x.is_dir()])
    #print(list(p.glob('*.*')))
    return 0

def main():
    litter_folder = input("Input litter folder:")
    print(litter_folder)
    sort_folders(litter_folder)
    return 0

if __name__ == "__main__":
    sys.exit(main())
