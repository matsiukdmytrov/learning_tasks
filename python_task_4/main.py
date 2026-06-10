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

    def add_phone(self, in_phone:str):
        self.phones.append(Phone(in_phone))

    def remove_phone(self, in_phone:str):
        self.phones.remove(next((p for p in self.phones if p.value == in_phone),None))

    def edit_phone(self, old_phone:str,new_phone:str):
        self.phones.remove(next((p for p in self.phones if p.value == old_phone),None))
        self.phones.append(Phone(new_phone))

    def find_phone(self, in_phone:str):
        match = next((p for p in self.phones if p.value == in_phone),None)
        if match is None:
            return ""
        else:
            return match.value
        #if phone in self.phones:
        #    return True
        #else:
        #    return False

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    #def __init__(self):
    #    UserDict.__init__(self, dict)
    #    self.data = {}

    def add_record(self, in_record:Record):
        self.data[in_record.name.value] = in_record

    def find(self, in_name:str):
        loc_record = next((p for p in self.data.values() if p.name.value == in_name),None)
        return loc_record

    def delete(self, in_name:str):
        #loc_record = next((p for p in self.data.values() if p.name.value == in_name),None)
        self.data.__delitem__(in_name)





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
print("Виведення всіх записів у книзі:")
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")
print("Знаходження та редагування телефону для John:")
print(john)
# Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
print("Пошук конкретного телефону у записі John:")
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")
# Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")

print("Видалення запису Jane:")
for name, record in book.data.items():
    print(record)