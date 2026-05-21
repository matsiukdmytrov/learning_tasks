import sys


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


# Парсер команд: розбиває рядок на команду та аргументи
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# Хендлери (Функції обробники команд)

@input_error
def add_contact(args, contacts):
    name, phone = args
    if name in contacts:
        return f"Contact {name} already exists. Use 'change' command to update."
    contacts[name] = phone
    return f"Contact {name} added."


@input_error
def change_contact(args, contacts):
    name, phone = args
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return f"Contact {name} updated."


@input_error
def show_phone(args, contacts):
    name = args[0]
    if name not in contacts:
        raise KeyError
    return f"{name}: {contacts[name]}"


def show_all(contacts):
    if not contacts:
        return "Your contact book is empty."

    # Форматуємо словник у зручний для читання вигляд
    result = []
    for name, phone in contacts.items():
        result.append(f"{name}: {phone}")
    return "\n".join(result)


# Головна функція, що керує циклом запит-відповідь
def main():
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        if not user_input.strip():
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit", "good"]:
            # Додаткова перевірка для "good bye"
            if command == "good" and (not args or args[0].lower() != "bye"):
                print("Unknown command.")
                continue
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, contacts))

        elif command == "change":
            print(change_contact(args, contacts))

        elif command == "phone":
            print(show_phone(args, contacts))

        elif command == "show":
            if args and args[0].lower() == "all":
                print(show_all(contacts))
            else:
                print("Unknown command. Did you mean 'show all'?")

        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()