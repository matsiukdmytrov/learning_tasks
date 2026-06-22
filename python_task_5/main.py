from collections import UserDict
from datetime import datetime, date, timedelta

class Field:
    value: str
    def __init__(self, value:str):
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
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError("Телефон може містити тільки цифри і повинен мати довжину 10 символів")
        super().__init__(value)

    @classmethod
    def is_valid(cls, value:str)->bool:
        return len(value) == 10 and value.isdigit()

class Birthday(Field):
    # datetime(1955, 10, 28)
    def __init__(self, in_value:str):
        if not self.is_valid(in_value):
            raise ValueError("День народження повинен бути вказаний в форматі 2022-02-24")
        super().__init__(in_value)
        self.value: datetime = datetime.strptime(in_value, "%Y-%m-%d")

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return True


    # @classmethod
    # def str_to_datetime(cls, value: str) -> datetime:
    #     return datetime.strptime(value, "%Y-%m-%d")
    # def __str__(self):


class Record:
    name:Name
    phones:list[Phone]
    def __init__(self, args):
        self.name = Name(args[0])
        self.phones = []
        if len(args) > 1:
           loc_phone_list = args[1:]
           for loc_phone in loc_phone_list:
               self.add_phone(loc_phone)

    def add_phone(self, in_phone:str):
        self.phones.append(Phone(in_phone))

    def find_phone(self, in_phone:str)->Phone|None:
        return next((p for p in self.phones if p.value == in_phone),None)

    def remove_phone(self, in_phone:str):
        loc_found_phone = self.find_phone(in_phone)
        if loc_found_phone:
            self.phones.remove(loc_found_phone)

    def edit_phone(self, old_phone:str,new_phone:str):
        loc_found_phone = self.find_phone(old_phone)
        if loc_found_phone:
            loc_found_phone.value = new_phone

    def has_phone(self, in_phone: str)->bool:
        return self.find_phone(in_phone) is not None

    def __eq__(self, other)->bool:
        if isinstance(other, Record):
            return self.name == other.name
        if isinstance(other, str):
            return self.name.value == other
        return False

    def __str__(self):
        return f"Контакт: {self.name.value}, телефони: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    data:dict[str, Record]

    def add_record(self, in_record:Record):
        self.data[in_record.name.value] = in_record

    def find(self, in_name:str)->Record|None:
        return next((p for p in self.data.values() if p == in_name),None)

    def delete(self, args):
        self.data.pop(args[0])

    def find_by_phone(self, in_phone:str)->Record|None:
        return next((p for p in self.data.values() if p.has_phone(in_phone)),None)

    def add_contact(self, args)->str:
        loc_name = args[0]
        found_rec = self.find(loc_name)
        if found_rec:
            return f"Контакт {loc_name} вже існує."
        self.add_record(Record(args))
        return f"Контакт {loc_name} додано."

    def show_all(self)->str:
        if self.data:
            return f"{'\n'.join(str(p) for p in self.data.values())}"
        return "Ше нічого не зробив, а вже дивишся (Книга контактів порожня)."

    def change_contact(self, args)->str:
        loc_name, phone_before, phone_after = args

        loc_rec = self.find(loc_name)
        if not loc_rec:
            return f"Контакт {loc_name} не знайдено."

        loc_rec.edit_phone(phone_before, phone_after)
        return f"Контакт {loc_name} змінено."

    def show_phone(self,args) -> str:
        loc_phone = args[0]

        found_phone_rec = self.find_by_phone(loc_phone)
        if found_phone_rec:
            return f"{found_phone_rec}"
        return f"Контакт по телефону {loc_phone} не знайдено."




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
        except TypeError as t:
            return f"{t}"

    return inner

@input_error
def add_contact(args)->str:
    return main_book.add_contact(args)

@input_error
def change_contact(args)->str:
    return main_book.change_contact(args)

@input_error
def show_phone(args)->str:
    return main_book.show_phone(args)

@input_error
def show_all(args)->str:
    return main_book.show_all()

@input_error
def del_contact(args)->str:
    main_book.delete(args)
    return "Запис видалено"

def close_command(args)->str:
    return "break"

def hello_command(args)->str:
    return "How can I help you?"

# Парсер команд: розбиває рядок на команду та аргументи
def parse_input(user_input:str)->tuple|str:
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
                "add": add_contact,"del": del_contact, "change": change_contact, "phone": show_phone, "show": show_all,}


main_book = AddressBook()
# Головна функція, що керує циклом запит-відповідь
def main():

    print("Welcome to the assistant bot!")

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