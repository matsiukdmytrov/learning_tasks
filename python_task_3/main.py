import sys


contacts = {}

# Декоратор для обробки помилок введення
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            print("Give me name and phone please.")
            return "continue"
        except KeyError:
            print("Contact not found.")
            return "continue"
        except IndexError:
            print("Enter user name please.")
            return "continue"

    return inner

# Хендлери (Функції обробники команд)

@input_error
def add_contact(args ):
    name, phone = args
    if name in contacts:
        print(f"Contact {name} already exists. Use 'change' command to update.")
        return "continue"
    contacts[name] = phone
    print(f"Contact {name} added.")
    return "continue"


@input_error
def change_contact(args):
    name, phone = args
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    print(f"Contact {name} updated.")
    return "continue"


@input_error
def show_phone(args, ):
    name = args[0]
    if name not in contacts:
        raise KeyError
    print(f"{name}: {contacts[name]}")
    return "continue"

def show_all():
    if not contacts:
        return "Your contact book is empty."
    # Форматуємо словник у зручний для читання вигляд
    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])

def close_command(args):
    print("Good bye!")
    return "break"

def close_command_long(args):
    if not args or args[0].lower() != "bye":
        print("Unknown command.")
        return "continue"
    print("Good bye!")
    return "break"

def hello_command(args):
    print("How can I help you?")
    return "continue"

def show_command(args):
    if args and args[0].lower() == "all":
        print(show_all())
        return "continue"
    else:
        print("Unknown command. Did you mean 'show all'?")
        return "continue"

# Парсер команд: розбиває рядок на команду та аргументи
def parse_input(user_input:str):
    command, *args = user_input.split()
    command = command.strip().lower()

    #command, *args = parse_input(user_input)

    if command in command_dict:
        return command_dict[command](args)
    else:
        print("Unknown command.")
        return "continue"



command_dict = {"close": close_command, "exit": close_command, "good": close_command_long, "hello": hello_command,
                "add": add_contact, "change": change_contact, "phone": show_phone, "show": show_command,}


# Головна функція, що керує циклом запит-відповідь
def main():


    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        if not user_input.strip():
            continue
        res_perse_input = parse_input(user_input)
        if res_perse_input == "break":
            break
        else:
            continue


if __name__ == "__main__":
    main()