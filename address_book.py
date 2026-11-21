from collections import UserDict
from datetime import datetime, timedelta


class Field:
    # Base class for all contact fields
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # Class for storing a contact's name
    pass


class Phone(Field):
    # Class for storing and validating a phone number

    def __init__(self, value):
        # Check if the phone number contains exactly 10 digits
        if not value.isdigit() or len(value) != 10:
            raise ValueError(
                "Phone number must contain exactly 10 digits."
            )

        super().__init__(value)


class Birthday(Field):
    # Class for storing and validating a birthday

    def __init__(self, value):
        try:
            # Convert the date string into a datetime object
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError(
                "Invalid date format. Use DD.MM.YYYY"
            )

    def __str__(self):
        # Return birthday in the required format
        return self.value.strftime("%d.%m.%Y")


class Record:
    # Class for storing contact information

    def __init__(self, name):
        # Store the contact name
        self.name = Name(name)

        # Create an empty list for phone numbers
        self.phones = []

        # Birthday is optional
        self.birthday = None

    def add_phone(self, phone):
        # Add a new phone number
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        # Find and remove a phone number
        found_phone = self.find_phone(phone)

        if found_phone:
            self.phones.remove(found_phone)
        else:
            raise ValueError("Phone number not found.")

    def edit_phone(self, old_phone, new_phone):
        # Find and replace an existing phone number
        found_phone = self.find_phone(old_phone)

        if found_phone:
            new_phone_obj = Phone(new_phone)
            index = self.phones.index(found_phone)
            self.phones[index] = new_phone_obj
        else:
            raise ValueError("Phone number not found.")

    def find_phone(self, phone):
        # Search for a phone number
        for p in self.phones:
            if p.value == phone:
                return p

        return None

    def add_birthday(self, birthday):
        # Add a birthday to the contact
        self.birthday = Birthday(birthday)

    def __str__(self):
        # Prepare phone numbers for display
        phones = "; ".join(p.value for p in self.phones)

        # Prepare birthday for display
        birthday = (
            str(self.birthday) if self.birthday else "Not specified"
        )

        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phones}, "
            f"birthday: {birthday}"
        )


class AddressBook(UserDict):
    # Class for storing and managing all contacts

    def add_record(self, record):
        # Add a new contact to the address book
        self.data[record.name.value] = record

    def find(self, name):
        # Find a contact by name
        return self.data.get(name)

    def delete(self, name):
        # Delete a contact by name
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        # Get birthdays happening in the next 7 days
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.value

            # Create this year's birthday date
            birthday_this_year = birthday.replace(year=today.year)

            # Move birthdays to Monday if they fall on weekends
            if birthday_this_year.weekday() >= 5:
                days_until_monday = (
                    7 - birthday_this_year.weekday()
                )
                birthday_this_year += timedelta(
                    days=days_until_monday
                )

            # Check if birthday is within the next 7 days
            days_difference = (birthday_this_year - today).days

            if 0 <= days_difference <= 7:
                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": birthday_this_year.strftime(
                        "%d.%m.%Y"
                    )
                })

        return upcoming_birthdays
