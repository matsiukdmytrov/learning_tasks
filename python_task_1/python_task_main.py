import sys
import os
from pathlib import Path
import shutil
import cyrtranslit

def normalize(inStr):
    returnStr = cyrtranslit.to_latin(inStr,"ua")
    return returnStr

def sort_file(inFileName,inFolder):
    l_image = ['JPEG', 'PNG', 'JPG', 'SVG']
    l_document = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
    l_video = ['AVI', 'MP4', 'MOV', 'MKV']
    l_audio = ['MP3', 'OGG', 'WAV', 'AMR']
    l_archive = ['ZIP', 'GZ', 'TAR']
    File_Extension_dict = {("images",l_image),("documents",l_document),("videos",l_video),("audio",l_audio),("archives",l_archive)}
    new_Folder = ""
    for fn,t in File_Extension_dict:
        for tf in list(p.glob("*."+t)):
            shutil.move(str(tf), inFolder+"\\"+fn)

    for tf in list(p.glob("*.*")):
        shutil.move(str(tf), inFolder + "\\other")
    return 0

def sort_folders(inFolder=""):


    p = Path(inFolder)
    for x in p.iterdir():
        if x.is_dir():
            #print(x.name)
            locFolder = inFolder+"\\"+x.name
            print(locFolder)
            sort_folders(locFolder)
        for tf in list(p.glob("*.*")):

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
