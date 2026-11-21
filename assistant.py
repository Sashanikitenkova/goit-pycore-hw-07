from address_book import AddressBook, Record


def input_error(func):
    # Decorator for handling input errors
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Please provide all required arguments."

    return inner


def parse_input(user_input):
    # Split user input into command and arguments
    parts = user_input.strip().split()

    if not parts:
        return "", []

    command = parts[0].lower()
    args = parts[1:]

    return command, args


@input_error
def add_contact(args, book: AddressBook):
    # Add a new contact or update an existing contact
    if len(args) < 2:
        raise ValueError("Usage: add [name] [phone]")

    name, phone = args[0], args[1]

    record = book.find(name)

    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    record.add_phone(phone)

    return message


@input_error
def change_contact(args, book: AddressBook):
    # Change an existing phone number
    if len(args) != 3:
        raise ValueError(
            "Usage: change [name] [old phone] [new phone]"
        )

    name, old_phone, new_phone = args

    record = book.find(name)

    if record is None:
        raise KeyError

    record.edit_phone(old_phone, new_phone)

    return "Phone number updated successfully."


@input_error
def show_phone(args, book: AddressBook):
    # Show all phone numbers for a contact
    if len(args) != 1:
        raise ValueError("Usage: phone [name]")

    name = args[0]

    record = book.find(name)

    if record is None:
        raise KeyError

    if not record.phones:
        return f"{name} has no phone numbers."

    phones = "; ".join(phone.value for phone in record.phones)

    return f"{name}: {phones}"


def show_all(book: AddressBook):
    # Display all contacts
    if not book.data:
        return "Address book is empty."

    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    # Add a birthday to an existing contact
    if len(args) != 2:
        raise ValueError(
            "Usage: add-birthday [name] [DD.MM.YYYY]"
        )

    name, birthday = args

    record = book.find(name)

    if record is None:
        raise KeyError

    record.add_birthday(birthday)

    return f"Birthday for {name} added successfully."


@input_error
def show_birthday(args, book: AddressBook):
    # Show the birthday of a contact
    if len(args) != 1:
        raise ValueError("Usage: show-birthday [name]")

    name = args[0]

    record = book.find(name)

    if record is None:
        raise KeyError

    if record.birthday is None:
        return f"Birthday for {name} is not specified."

    return f"{name}'s birthday: {record.birthday}"


@input_error
def birthdays(args, book: AddressBook):
    # Display upcoming birthdays
    if args:
        raise ValueError("Usage: birthdays")

    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No upcoming birthdays in the next 7 days."

    result = ["Upcoming birthdays:"]

    for person in upcoming:
        result.append(
            f"{person['name']}: {person['congratulation_date']}"
        )

    return "\n".join(result)


def main():
    # Create an address book
    book = AddressBook()

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")

        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
