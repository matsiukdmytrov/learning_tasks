import string
import sys
from pathlib import Path
import shutil

other_folder = Path()
trans_table = {}
file_extension_dict = {}
extensions_dict = {
    "images": ("JPEG", "PNG", "JPG", "SVG"),
    "documents": ("DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX"),
    "audio": ("MP3", "OGG", "WAV", "AMR"),
    "videos": ("MP4", "AVI", "MOV", "MKV"),
    "archives": ("ZIP", "GZ", "TAR"),
}


def normalize(in_str: str) -> str:
    global trans_table
    return_sr_start = in_str.translate(trans_table)
    return_str = ""
    for locSymb in return_sr_start:
        if locSymb in string.ascii_letters:
            return_str += locSymb
        elif locSymb in string.digits:
            return_str += locSymb
        else:
            return_str += "_"

    return return_str


def file_rename_with_controle(
    in_file: Path, in_new_short_file_name: str, iter_suffix: int = 0
):
    if iter_suffix:
        new_file = (
            in_file.parent / f"{in_new_short_file_name}_{iter_suffix}{in_file.suffix}"
        )
    else:
        new_file = in_file.parent / f"{in_new_short_file_name}{in_file.suffix}"

    if not new_file.exists():
        in_file.rename(new_file)
    else:
        iter_suffix += 1
        file_rename_with_controle(in_file, in_new_short_file_name, iter_suffix)

    return 0


def normalize_names_in_folders(in_folder: Path):

    for internal_object in in_folder.iterdir():
        if internal_object.is_dir():
            normalize_names_in_folders(internal_object)
            short_file_name = normalize(internal_object.name)

            new_file = internal_object.with_name(short_file_name)
            internal_object.rename(new_file)
        else:
            short_file_name = normalize(internal_object.stem)

            file_rename_with_controle(internal_object, short_file_name)
    return 0


def file_move_into_with_control(
    in_file: Path, in_move_folder: Path, iter_suffix: int = 0
):
    if iter_suffix == 0:
        new_file = in_move_folder / in_file.name
    else:
        new_file = in_move_folder / f"{in_file.stem}_{iter_suffix}{in_file.suffix}"

    if not new_file.exists():
        in_file.rename(new_file)
    else:
        iter_suffix += 1
        file_move_into_with_control(in_file, in_move_folder, iter_suffix)

    return 0


def sort_files(in_folder: Path):
    global file_extension_dict
    for file_extension_folder in file_extension_dict:
        file_extension_list = file_extension_dict[file_extension_folder]
        for loc_ext in file_extension_list:
            for tf in list(in_folder.glob("*." + loc_ext)):
                if "archives" in str(file_extension_folder):
                    shutil.unpack_archive(
                        tf, str(file_extension_folder) + "\\" + tf.name
                    )
                    tf.unlink()
                else:
                    if not file_extension_folder.exists():
                        file_extension_folder.mkdir(exist_ok=True)
                    if file_extension_folder.absolute() != tf.parent:
                        file_move_into_with_control(tf, file_extension_folder)
    for tf in list(in_folder.glob("*.*")):
        if not other_folder.exists():
            other_folder.mkdir(exist_ok=True)
        if other_folder != tf.parent:
            file_move_into_with_control(tf, other_folder)
    return 0


def sort_folders(in_folder: Path):
    global file_extension_dict
    for internal_object in in_folder.iterdir():
        if (
            internal_object.absolute() in file_extension_dict
            or internal_object.absolute() == other_folder
        ):
            continue
        if internal_object.is_dir():
            sort_folders(internal_object)
            internal_object.rmdir()
    sort_files(in_folder)
    return 0


def init_global_variables(in_litter_folder: str):
    global other_folder
    global trans_table
    global file_extension_dict

    other_folder = Path(in_litter_folder + "\\other")

    for ext_folder, ext_list in extensions_dict.items():
        file_extension_dict[Path(in_litter_folder + "\\" + ext_folder)] = ext_list

    trans_dict = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "h",
        "ґ": "g",
        "д": "d",
        "е": "e",
        "є": "ye",
        "ж": "zh",
        "з": "z",
        "и": "y",
        "і": "i",
        "ї": "yi",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "kh",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ь": "",
        "ю": "yu",
        "я": "ya",
    }

    trans_table = str.maketrans(
        trans_dict | {k.upper(): v.upper() for k, v in trans_dict.items()}
    )
    return 0


def main():
    if len(sys.argv) < 2:
        print("Error: Please provide a folder path.")
        print("Usage: python sort.py /path/to/folder")
        sys.exit(1)

    litter_folder = sys.argv[1]
    litter_folder_path = Path(litter_folder)

    if not litter_folder_path.exists():
        print(f"Error: The path '{litter_folder_path}' does not exist.")
        sys.exit(1)

    if not litter_folder_path.is_dir():
        print(f"Error: '{litter_folder_path}' is not a directory.")
        sys.exit(1)

    print(f"Starting to sort: {litter_folder_path.absolute()}")

    # litter_folder = input("Input litter folder:")
    init_global_variables(str(litter_folder_path.absolute()))
    # litter_folder_path = Path(litter_folder)

    sort_folders(litter_folder_path)
    normalize_names_in_folders(litter_folder_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
