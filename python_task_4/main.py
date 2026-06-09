from collections import UserDict
from operator import truediv


class Field:
    def __init__(self, value:str):
        self.value = value
        self.isMandatory = False

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        Field.__init__(self, value)
        self.isMandatory = True

class Phone(Field):
    def __init__(self, value):
        Field.__init__(self, value)

    @staticmethod
    def __isValid__(value:str):
        if value.__len__() == 10:
            if value.isdigit():
                return True
            else:
                return False
        else:
            return False


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone:Phone):
        self.phones.append(phone)

    def remove_phone(self, phone:Phone):
        self.phones.remove(phone)

    def edit_phone(self, rem_phone:Phone,add_phone:Phone):
        self.phones.remove(rem_phone)
        self.phones.append(add_phone)

    def find_phone(self, phone:Phone):
        if phone in self.phones:
            return True
        else:
            return False


    def set_name(self, owner, in_name:Name):
        self.name = in_name

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    # реалізація класу
##```
## Після реалізації ваш код має виконуватися наступним чином:
##```python
# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)
# Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")
# Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")