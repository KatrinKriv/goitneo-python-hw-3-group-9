from collections import defaultdict
from datetime import datetime, timedelta


class Birthday:
    def __init__(self, date=None):
        self.date = None
        if date:
            self.set_date(date)

    def set_date(self, date):
        try:
            self.date = datetime.strptime(date, "%d.%m.%Y").date()
        except ValueError:
            print("Invalid date format. Please use DD.MM.YYYY.")

    def __str__(self):
        return self.date.strftime("%d.%m.%Y") if self.date else "Not set"


class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = name
        self.phone = phone
        self.birthday = Birthday(birthday)

    def change_phone(self, phone):
        self.phone = phone

    def add_birthday(self, date):
        self.birthday.set_date(date)


class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, name, phone, birthday=None):
        self.contacts.append(Record(name, phone, birthday))

    def change_phone(self, name, phone):
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                contact.change_phone(phone)
                print(f"Phone number updated for {name}.")
                return
        print(f"Contact '{name}' not found.")

    def get_phone(self, name):
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                return contact.phone
        return None

    def show_all_contacts(self):
        if not self.contacts:
            print("Address book is empty.")
            return
        for contact in self.contacts:
            print(
                f"Name: {contact.name}, Phone: {contact.phone}, Birthday: {contact.birthday}"
            )

    def show_birthday(self, name):
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                print(f"Birthday for {name}: {contact.birthday}")
                return
        print(f"Contact '{name}' not found.")

    def get_birthdays_per_week(self):
        today = datetime.today().date()
        birthdays_by_weekday = defaultdict(list)
        for contact in self.contacts:
            if contact.birthday.date:
                birthday_this_year = contact.birthday.date.replace(year=today.year)
                delta_days = (birthday_this_year - today).days
                if delta_days < 0:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                    delta_days = (birthday_this_year - today).days
                weekday = birthday_this_year.strftime("%A")
                birthdays_by_weekday[weekday].append(contact.name)
        return birthdays_by_weekday

    def show_birthdays(self):
        birthdays_by_weekday = self.get_birthdays_per_week()
        for weekday, names in birthdays_by_weekday.items():
            print(f"{weekday}: {', '.join(names)}")


class Bot:
    def __init__(self):
        self.address_book = AddressBook()

    def handle_command(self, command):
        parts = command.split(" ")
        if parts[0] == "add":
            if len(parts) == 3:
                self.address_book.add_contact(parts[1], parts[2])
                print(f"Added {parts[1]} to contacts.")
            else:
                print("Invalid command format. Please use 'add [name] [phone]'")
        elif parts[0] == "change":
            if len(parts) == 3:
                self.address_book.change_phone(parts[1], parts[2])
            else:
                print("Invalid command format. Please use 'change [name] [new phone]'")
        elif parts[0] == "phone":
            if len(parts) == 2:
                phone = self.address_book.get_phone(parts[1])
                if phone:
                    print(f"Phone number for {parts[1]}: {phone}")
                else:
                    print(f"Contact '{parts[1]}' not found.")
            else:
                print("Invalid command format. Please use 'phone [name]'")
        elif parts[0] == "all":
            self.address_book.show_all_contacts()
        elif parts[0] == "add-birthday":
            if len(parts) == 3:
                self.address_book.add_contact(parts[1], parts[2])
                print(f"Added birthday for {parts[1]}.")
            else:
                print(
                    "Invalid command format. Please use 'add-birthday [name] [DD.MM.YYYY]'"
                )
        elif parts[0] == "show-birthday":
            if len(parts) == 2:
                self.address_book.show_birthday(parts[1])
            else:
                print("Invalid command format. Please use 'show-birthday [name]'")
        elif parts[0] == "birthdays":
            self.address_book.show_birthdays()
        elif parts[0] == "hello":
            print("Hello!")
        elif parts[0] == "close" or parts[0] == "exit":
            print("Closing the program.")
            exit()
        else:
            print("Invalid command.")


if __name__ == "__main__":
    bot = Bot()
    while True:
        command = input("Enter command: ")
        bot.handle_command(command)
