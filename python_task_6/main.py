from collections import UserDict
from datetime import datetime, date
import re
from typing import Any, Generator
import json
import os
from pathlib import Path


class Field:
    value: str

    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if value == "":
            raise ValueError("Ім'я повинно бути заповнене")
        super().__init__(value)


class Phone(Field):
    __value: str

    def __init__(self, value):
        super().__init__(value)
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if not self.is_valid(value):
            raise ValueError("Телефон може містити тільки цифри і повинен мати довжину 10 символів")
        self.__value = value

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return len(value) == 10 and value.isdigit()

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    # datetime(1955, 10, 28)
    __value: str

    def __init__(self, in_value: str):
        super().__init__(in_value)
        self.value = in_value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if not self.is_valid(value):
            raise ValueError("День народження повинен бути вказаний в форматі 2022-02-24")
        self.__value: date = datetime.strptime(value, "%Y-%m-%d").date()

    def __str__(self):
        return str(self.value.strftime("%Y-%m-%d"))

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return re.match(r"^\d{4}-\d{2}-\d{2}$", value) is not None


class Record:
    name: Name
    phones: list[Phone]
    birthday: Birthday | None

    def __init__(self, args):
        self.name = Name(args[0])
        self.phones = []
        self.birthday = None
        if len(args) > 1:
            loc_add_info_list = args[1:]
            loc_add_info: str
            for loc_add_info in loc_add_info_list:
                if Phone.is_valid(loc_add_info):
                    self.add_phone(loc_add_info)
                elif Birthday.is_valid(loc_add_info):
                    self.birthday = Birthday(loc_add_info)
                elif str(loc_add_info) == "None":
                    continue
                else:
                    raise ValueError(
                        f"Вказане значення '{loc_add_info}' є в невідомому форматі ( формат телефона: '0123456789'; формат дня народження: '2022-02-24' )"
                    )

    def add_phone(self, in_phone: str):
        self.phones.append(Phone(in_phone))

    def find_phone(self, in_phone: str) -> Phone | None:
        return next((p for p in self.phones if p.value == in_phone), None)

    def remove_phone(self, in_phone: str):
        loc_found_phone = self.find_phone(in_phone)
        if loc_found_phone:
            self.phones.remove(loc_found_phone)

    def edit_phone(self, old_phone: str, new_phone: str):
        loc_found_phone = self.find_phone(old_phone)
        if loc_found_phone:
            loc_found_phone.value = new_phone

    def has_phone(self, in_phone: str) -> bool:
        return self.find_phone(in_phone) is not None

    def days_to_birthday(self) -> int:
        if self.birthday is None:
            return 0

        today = date.today()
        # Встановлюємо день народження на поточний рік
        next_birthday = self.birthday.value.replace(year=today.year)

        # Якщо день народження цього року вже пройшов (або сьогодні),
        # рахуємо дні до дня народження у наступному році
        if next_birthday <= today:
            next_birthday = next_birthday.replace(year=today.year + 1)

        # Рахуємо різницю в днях
        delta = next_birthday - today
        return delta.days

    def __eq__(self, other) -> bool:
        if isinstance(other, Record):
            return self.name == other.name
        if isinstance(other, str):
            return self.name.value == other
        return False

    def __str__(self):
        lp = ""
        if len(self.phones) > 0:
            lp = f"; телефони: {', '.join(str(p) for p in self.phones)}"
        lb = ""
        if self.birthday:
            lb = f"; День народження: {self.birthday}"

        return f"Контакт: {self.name}{lp}{lb}"

    def to_json(self):
        return {
            "name": str(self.name),
            "phones": [str(p) for p in self.phones],
            "birthday": str(self.birthday),
        }

    def has_part_name(self, in_part_str: str) -> bool:
        return in_part_str in str(self.name)

    def has_part_phone(self, in_part_str: str) -> bool:
        return next((p for p in self.phones if in_part_str in str(p.value)), None) is not None


class AddressBook(UserDict):
    data: dict[str, Record]

    def add_record(self, in_record: Record):
        self.data[in_record.name.value] = in_record

    def find(self, in_name: str) -> Record | None:
        return next((p for p in self.data.values() if p == in_name), None)

    def delete(self, args):
        self.data.pop(args[0])

    def delete_all(self):
        self.data.clear()

    def find_by_phone(self, in_phone: str) -> Record | None:
        return next((p for p in self.data.values() if p.has_phone(in_phone)), None)

    def find_by_str(self, in_str: str) -> list[Record]:
        return [p for p in self.data.values() if p.has_part_name(in_str)] + [
            p for p in self.data.values() if p.has_part_phone(in_str)
        ]

    def add_contact(self, args) -> str:
        loc_name = args[0]
        found_rec = self.find(loc_name)
        if found_rec:
            return f"Контакт {loc_name} вже існує."
        self.add_record(Record(args))
        return f"Контакт {loc_name} додано."

    def show_all(self) -> str:
        if self.data:
            return f"{'\n'.join(str(p) for p in self.data.values())}"
        return "Ше нічого не зробив, а вже дивишся (Книга контактів порожня)."

    def change_contact(self, args) -> str:
        loc_name, phone_before, phone_after = args

        loc_rec = self.find(loc_name)
        if not loc_rec:
            return f"Контакт {loc_name} не знайдено."

        loc_rec.edit_phone(phone_before, phone_after)
        return f"Контакт {loc_name} змінено."

    def show_phone(self, args) -> str:
        loc_phone = args[0]

        found_phone_rec = self.find_by_phone(loc_phone)
        if found_phone_rec:
            return f"{found_phone_rec}"
        return f"Контакт по телефону {loc_phone} не знайдено."

    def get_iterator_page(self, iter_len=2, page_num=0) -> Generator[list[Record], Any, None]:
        records = list(self.data.values())

        for i in range((page_num * iter_len), (page_num * iter_len + iter_len), 1):
            yield records[i : i + 1]
        # return records[(page_num * iter_len) : (page_num * iter_len + iter_len)]

    def paginator(self, iter_len=2) -> Generator[list[Record], Any, None]:
        # Перетворюємо всі записи книги (значення словника) на список
        records = list(self.data.values())

        # Рухаємося по списку з кроком N
        for i in range(0, len(records), iter_len):
            # Повертаємо зріз від поточного індексу до i + n
            yield records[i : i + iter_len]

    def show_iterate(self) -> str:
        if self.data:
            return_str = ""
            paginator = self.paginator()
            for part in paginator:
                return_str = return_str + f"\n--- Нова сторінка (ітерація) ---\n"
                return_str = return_str + f"{'\n'.join(str(p) for p in part)}"

            return return_str
        return "Ше нічого не зробив, а вже дивишся (Книга контактів порожня)."

    def show_iterator_page(self, args) -> str:
        # iteratepage
        if self.data:
            return_str = ""
            if len(args) == 1:
                return_str = return_str + f"\n--- Нова сторінка (ітерація) ---"
                paginator = self.get_iterator_page(2, int(args[0]))
                for part in paginator:
                    return_str = return_str + f"\n{''.join(str(p) for p in part)}"
                return return_str
            return "Недостатньо аргументів ( вкажи сторінку ітерації )."

        return "Ше нічого не зробив, а вже дивишся (Книга контактів порожня)."

    def search(self, args) -> str:
        if len(args) == 0:
            return "Недостатньо аргументів ( рядок пошуку )."

        if len(args) > 1:
            return "Забагато аргументів ( потрібен ОДИН рядок пошуку )."

        rec_list = self.find_by_str(args[0])

        if len(rec_list) == 0:
            return "Нічого не знайдено"

        return_str = ""
        # for rec in rec_list:
        return_str = return_str + f"{'\n'.join(str(p) for p in rec_list)}"
        return return_str


# Декоратор для обробки помилок введення
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"ValueError: {e}"
        except KeyError:
            return "Контакт не знайдено."
        except IndexError:
            return "Enter user name please."
        except TypeError as t:
            return f"TypeError: {t}"

    return inner


@input_error
def add_contact(args) -> str:
    return main_book.add_contact(args)


@input_error
def change_contact(args) -> str:
    return main_book.change_contact(args)


@input_error
def show_phone(args) -> str:
    return main_book.show_phone(args)


@input_error
def show_all(args) -> str:
    return main_book.show_all()


@input_error
def show_iterate(args) -> str:
    return main_book.show_iterate()


@input_error
def show_iterator_page(args) -> str:
    return main_book.show_iterator_page(args)


@input_error
def del_contact(args) -> str:
    main_book.delete(args)
    return "Запис видалено"


@input_error
def search(args) -> str:
    return main_book.search(args)


def close_command(args) -> str:
    dbase_file_path = Path(dbase_file)
    if dbase_file_path.exists():
        user_input = input("Found database file.: " + dbase_file + "\n Save Address book in it (y) ?:")
        if user_input.strip() == "y":
            save_to_file("")
    return "break"


def hello_command(args) -> str:
    return "How can I help you?"


# Парсер команд: розбиває рядок на команду та аргументи
def parse_input(user_input: str) -> tuple | str:
    command, *args = user_input.split()
    command = command.strip().lower()

    if command == "good":
        if not (len(args) > 0 and args[0].strip().lower() == "bye"):
            return "Unknown command."
    elif command == "show":
        if not (len(args) > 0 and args[0].strip().lower() == "all"):
            return "Unknown command."

    return command, *args


class AddressBookEncoder(json.JSONEncoder):
    def default(self, obj):
        # Check if the object is our custom User class
        if isinstance(obj, AddressBook):
            if obj.data:
                return [p.to_json() for p in obj.data.values()]

        # Let the base class JSONEncoder handle anything else or raise a TypeError
        return super().default(obj)


class AddressBookDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        # We pass our custom object_hook to the base class constructor
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct) -> Record | None:
        if "name" in dct and "birthday" in dct and "phones" in dct:
            return Record([dct["name"], dct["birthday"]] + dct["phones"])
        # If it doesn't match, return None
        return None


def save_to_file(args):
    json_string = json.dumps(main_book, cls=AddressBookEncoder)
    print(json_string)

    if len(args) == 0:
        save_file = dbase_file
    else:
        save_file = args[0]

    with open(save_file, "w", encoding="utf-8") as file:
        file.write(json_string)

    return "Адресна книга збережена в файл: " + save_file


def load_from_file(args):
    clean_db_before = False
    if len(args) == 0:
        load_file = dbase_file
    elif args[0] == "True":
        load_file = dbase_file
        clean_db_before = True
    else:
        load_file = args[0]

    if len(args) > 1 and args[1] == "True":
        clean_db_before = True

    json_string = ""
    with open(load_file, "r", encoding="utf-8") as file:
        json_string = file.read()

    if len(json_string) == 0:
        return "Файл пустий: " + load_file

    if clean_db_before:
        main_book.delete_all()

    list_rec = json.loads(json_string, cls=AddressBookDecoder)
    for rec in list_rec:
        if rec:
            main_book.add_record(rec)
    return "Адресна книга завантажена з файлу: " + load_file


command_dict = {
    "close": close_command,
    "exit": close_command,
    "good": close_command,
    "hello": hello_command,
    "add": add_contact,
    "del": del_contact,
    "change": change_contact,
    "phone": show_phone,
    "show": show_all,
    "iterate": show_iterate,
    "iteratepage": show_iterator_page,
    "save": save_to_file,
    "load": load_from_file,
    "search": search,
}

main_book = AddressBook()

# current_dir = os.getcwd()
dbase_file = os.getcwd() + "\\db.json"


# Головна функція, що керує циклом запит-відповідь
def main():
    print("Welcome to the assistant bot!")

    # main_book.add_record(Record(["John", "1234567890", "2021-01-30"]))
    # main_book.add_record(Record(["Jane", "0000000000", "5555555555"]))
    # main_book.add_record(Record(["Kris", "1111111111"]))

    dbase_file_path = Path(dbase_file)
    if dbase_file_path.exists():
        user_input = input("Found database file.: " + dbase_file + "\n Load Address book from it (y) ?:")
        if user_input.strip() == "y":
            load_from_file("")

    while True:
        user_input = input("Enter a command: ")
        if not user_input.strip():
            continue

        command, *args = parse_input(user_input)
        loc_func = command_dict.get(command)
        if loc_func:
            res_parse_input = loc_func(args)
            if res_parse_input == "break":
                print("Good bye!")
                break
            else:
                print(res_parse_input)
                continue
        else:
            print("Unknown command.")
            continue


if __name__ == "__main__":
    main()
