import datetime
import string

def encode(input_text, shift):
    alphabet = list(string.ascii_lowercase)
    encoded_text = ""
    for char in input_text:
        if 'a' <= char.lower() <= 'z':
            start = ord('a')
            encoded_char = chr((ord(char.lower()) - start + shift) % 26 + start)
            encoded_text += encoded_char
        else:
            encoded_text += char
    return alphabet, encoded_text

def decode(input_text, shift):
    decoded_text = ""
    for char in input_text:
        if 'a' <= char.lower() <= 'z':
            start = ord('a')
            decoded_char = chr((ord(char.lower()) - start - shift) % 26 + start)
            decoded_text += decoded_char
        else:
            decoded_text += char
    return decoded_text

class BankAccount:
    def __init__(self, name="Rainy", ID="1234", creation_date=None, balance=0):
        self.name = name
        self.ID = ID
        if creation_date is None:
            self.creation_date = datetime.date.today()
        else:
            if isinstance(creation_date, tuple):
                creation_date = datetime.date(*creation_date)
            if not isinstance(creation_date, datetime.date):
                raise TypeError("creation_date must be a datetime.date object")
            if creation_date > datetime.date.today():
                raise Exception("Creation date cannot be in the future.")
            self.creation_date = creation_date
        self.balance = balance

    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def view_balance(self):
        return self.balance

class SavingsAccount(BankAccount):
    def withdraw(self, amount):
        creation_date = self.creation_date
        if isinstance(creation_date, tuple):
            creation_date = datetime.date(*creation_date)

        if (datetime.date.today() - creation_date).days < 180:
            return
        if self.balance - amount < 0:
            return
        super().withdraw(amount)

class CheckingAccount(BankAccount):
    def withdraw(self, amount):
        if self.balance >= 0 and self.balance - amount < 0:
            self.balance -= 30
        super().withdraw(amount)

