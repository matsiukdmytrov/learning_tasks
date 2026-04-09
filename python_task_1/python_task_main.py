import string
import sys
#import os
#import stat
from pathlib import Path
import shutil
import cyrtranslit

other_folder = ""

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

def sort_files(in_folder,file_extension_dict={}):
    for fn in file_extension_dict:
        t = file_extension_dict[fn]
        for locExt in t:
            for tf in list(in_folder.glob("*."+locExt)):
                if "archives" in fn:
                    shutil.unpack_archive(tf,fn+"\\"+tf.name)
                    tf.unlink()
                else:
                    lp = Path(fn)
                    if not lp.exists():
                        lp.mkdir(exist_ok=True)
                    tf.move_into(fn)
    for tf in list(in_folder.glob("*.*")):
        lp = Path(other_folder)
        if not lp.exists():
            lp.mkdir(exist_ok=True)
        tf.move_into(other_folder)
    return 0

def sort_folders(in_folder,file_extension_dict={}):
    for internal_object in in_folder.iterdir():
        if internal_object.is_dir():
            sort_folders(internal_object,file_extension_dict)
            internal_object.rmdir()
    sort_files(in_folder, file_extension_dict)
    return 0

def main():
    #if len(sys.argv) < 2:
    #    print("Error: Please provide a folder path.")
    #    print("Usage: python sort.py /path/to/folder")
    #    sys.exit(1)

    #litter_folder = sys.argv[1]
    #folder_path = Path(litter_folder)

    #if not folder_path.exists():
    #    print(f"Error: The path '{folder_path}' does not exist.")
    #    sys.exit(1)

    #if not folder_path.is_dir():
    #    print(f"Error: '{folder_path}' is not a directory.")
    #    sys.exit(1)

    #print(f"Starting to sort: {folder_path.absolute()}")

    global other_folder
    litter_folder = input("Input litter folder:")

    l_image = ['JPEG', 'PNG', 'JPG', 'SVG']
    l_document = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
    l_video = ['AVI', 'MP4', 'MOV', 'MKV']
    l_audio = ['MP3', 'OGG', 'WAV', 'AMR']
    l_archive = ['ZIP', 'GZ', 'TAR']

    images_folder = litter_folder + "\\images"
    documents_folder = litter_folder + "\\documents"
    videos_folder = litter_folder + "\\videos"
    audio_folder = litter_folder + "\\audio"
    archives_folder = litter_folder + "\\archives"

    file_extension_dict = {images_folder:l_image,documents_folder:l_document,videos_folder:l_video,audio_folder:l_audio,archives_folder:l_archive}

    other_folder  = litter_folder + "\\other"
    litter_folder_path = Path(litter_folder)
    sort_folders(litter_folder_path,file_extension_dict)
    return 0

if __name__ == "__main__":
    sys.exit(main())
