
contacts = {}

# Декоратор для обробки помилок введення
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter user name please."
    return inner

# Хендлери (Функції обробники команд)

@input_error
def add_contact(args):
    name, phone = args
    if name in contacts:
        return f"Contact {name} already exists. Use 'change' command to update."
    contacts[name] = phone
    return f"Contact {name} added."


@input_error
def change_contact(args):
    name, phone = args
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return f"Contact {name} updated."


@input_error
def show_phone(args, ):
    if len(args)==0:
        raise IndexError
    name = args[0]
    if name not in contacts:
        raise KeyError
    return f"{name}: {contacts[name]}"

def show_all(args):
    if not contacts:
        return "Your contact book is empty."
    # Форматуємо словник у зручний для читання вигляд
    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])

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

if __name__ == "__main__":
    main()