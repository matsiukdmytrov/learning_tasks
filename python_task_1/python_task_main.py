import sys
from pathlib import Path

def sort_folders(inFolder=""):
    p = Path(inFolder)
    for x in p.iterdir():
        if x.is_dir():
            #print(x.name)
            locFolder = inFolder+"\\"+x.name
            print(locFolder)
            sort_folders(locFolder)
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
