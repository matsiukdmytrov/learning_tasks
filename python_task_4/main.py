from collections import UserDict
from operator import truediv


class Field:
    value: str
    def __init__(self, value:str):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        Field.__init__(self, value)

class Phone(Field):
    def __init__(self, value):
        if not Phone.__isValid__(value):
            raise ValueError("Телефон може містити тільки цифри і повинен мати довжину 10 символів")
        else:
            Field.__init__(self, value)

    @staticmethod
    def __isValid__(value:str):
        if len(value) == 10:
            if value.isdigit():
                return True
            else:
                return False
        else:
            return False


class Record:
    name:Name
    phones:list[Phone]
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, in_phone:str):
        self.phones.append(Phone(in_phone))

    def remove_phone(self, in_phone:str):
        loc_found_phone = next((p for p in self.phones if p.value == in_phone),None)
        if loc_found_phone is not None:
            self.phones.remove(loc_found_phone)

    def edit_phone(self, old_phone:str,new_phone:str):
        loc_found_phone = next((p for p in self.phones if p.value == old_phone),None)
        loc_found_phone.value = new_phone

    def find_phone(self, in_phone:str):
        match = next((p for p in self.phones if p.value == in_phone),None)
        if match is None:
            return ""
        else:
            return match.value

    def has_phone(self, in_phone: str):
        match = next((p for p in self.phones if p.value == in_phone), None)
        if match is None:
           return False
        else:
           return True


    def __str__(self):
        return f"Контакт: {self.name.value}, телефони: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    data:dict[str, Record]
    #def __init__(self):
    #    UserDict.__init__(self, dict)
    #    self.data = {}

    def add_record(self, in_record:Record):
        self.data[in_record.name.value] = in_record

    def find(self, in_name:str):
        loc_record = next((p for p in self.data.values() if p.name.value == in_name),None)
        return loc_record

    def find_by_phone(self, in_phone:str):
        loc_record = next((p for p in self.data.values() if p.has_phone(in_phone)),None)
        return loc_record

    def delete(self, in_name:str):
        #loc_record = next((p for p in self.data.values() if p.name.value == in_name),None)
        self.data.__delitem__(in_name)


# Декоратор для обробки помилок введення
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"{e}"
        except KeyError:
            return "Контакт не знайдено."
        except IndexError:
            return "Enter user name please."

    return inner

# # Парсер команд: розбиває рядок на команду та аргументи
# def parse_input(user_input):
#     cmd, *args = user_input.split()
#     cmd = cmd.strip().lower()
#     return cmd, *args

@input_error
def add_contact(args):
    loc_name = args[0]
    loc_phone_list = []
    if len(args) > 1:
        loc_phone_list = args[1:]

    found_rec = main_book.find(loc_name)
    if found_rec is None:
        loc_rec = Record(loc_name)
        if len(loc_phone_list) > 0:
            for loc_phone in loc_phone_list:
                loc_rec.add_phone(loc_phone)
        main_book.add_record(loc_rec)
        return f"Контакт {loc_name} додано."
    else:
        return f"Контакт {loc_name} вже існує."

@input_error
def change_contact(args):
    loc_name, phone_before, phone_after = args

    loc_rec = main_book.find(loc_name)
    if loc_rec is None:
        return f"Контакт {loc_name} не знайдено."
    else:
        loc_rec.edit_phone(phone_before, phone_after)
        return f"Контакт {loc_name} змінено."


@input_error
def show_phone(args):
    loc_phone = args[0]

    found_phone_rec = main_book.find_by_phone(loc_phone)
    if found_phone_rec is None:
        return f"Контакт по телефону {loc_phone} не знайдено."
    else:
        print(found_phone_rec)

def show_all(args):
    if not len(main_book):
        print("Ше нічого не зробив, а вже дивишся (Книга контактів порожня).")
        return

    for loc_name, loc_record in main_book.data.items():
        print(loc_record)


def close_command(args):
    return "break"

def hello_command(args):
    return "How can I help you?"

# Парсер команд: розбиває рядок на команду та аргументи
def parse_input(user_input:str):
    command, *args = user_input.split()
    command = command.strip().lower()

    if command == "good":
        if not(len(args) > 0 and args[0].strip().lower() == "bye"):
            return "Unknown command."
    elif command == "show":
        if not(len(args) > 0 and args[0].strip().lower() == "all"):
            return "Unknown command."

    return command, *args


command_dict = {"close": close_command, "exit": close_command, "good": close_command, "hello": hello_command,
                "add": add_contact, "change": change_contact, "phone": show_phone, "show": show_all,}


main_book = AddressBook()
# Головна функція, що керує циклом запит-відповідь
def main():

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        if not user_input.strip():
            continue

        command, *args = parse_input(user_input)
        if command in command_dict:
            res_parse_input = command_dict[command](args)
            if res_parse_input == "break":
                print("Good bye!")
                break
            else:
                print(res_parse_input)
                continue
        else:
            print("Unknown command.")
            continue

# # Головна функція, що керує циклом запит-відповідь
# def main():
#
#     print("Вас вітає бот-асистент!")
#
#     while True:
#         user_input = input("Введіть команду: ")
#         if not user_input.strip():
#             continue
#
#         command, *args = parse_input(user_input)
#
#         if command in ["close", "exit", "good"]:
#             # Додаткова перевірка для "good bye"
#             if command == "good" and (not args or args[0].lower() != "bye"):
#                 print("Мене до такого розробник не готував (невідома команда).")
#                 continue
#             print("Уходиш - ну й п*здуй (Бувай)!")
#             break
#
#         elif command == "hello":
#             print("Шо ти з мене хочеш (Чим я можу допомогти)?")
#
#         elif command == "add":
#             print(add_contact(args, main_book))
#
#         elif command == "change":
#             print(change_contact(args, main_book))
#
#         elif command == "phone":
#             print(show_phone(args, main_book))
#
#         elif command == "show":
#             if args and args[0].lower() == "all":
#                 show_all(main_book)
#             else:
#                 print("Шось не по нашому (невідома команда). Можливо ти мав на увазі 'show all'?")
#
#         else:
#             print("Мене до такого розробник не готував (невідома команда).")


if __name__ == "__main__":
    main()


# ##```
# ## Після реалізації ваш код має виконуватися наступним чином:
# ##```python
# # Створення нової адресної книги
# book = AddressBook()
#
# # Створення запису для John
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")
#
# # Додавання запису John до адресної книги
# book.add_record(john_record)
#
# # Створення та додавання нового запису для Jane
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# book.add_record(jane_record)
#
# # Виведення всіх записів у книзі
# print("Виведення всіх записів у книзі:")
# for name, record in book.data.items():
#     print(record)
#
# # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")
# print("Знаходження та редагування телефону для John:")
# print(john)
# # Виведення: Contact name: John, phones: 1112223333; 5555555555
#
# # Пошук конкретного телефону у записі John
# print("Пошук конкретного телефону у записі John:")
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")
# # Виведення: 5555555555
#
# # Видалення запису Jane
# book.delete("Jane")
#
# print("Видалення запису Jane:")
# for name, record in book.data.items():
#     print(record)