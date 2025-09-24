import string
import datetime


def encode(text, shift):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet + alphabet.upper(), shifted_alphabet + shifted_alphabet.lower())
    encoded_text = text.translate(table)
    return (None, encoded_text) 


def decode(encoded_text, shift):
   
    lowercase_letters = list(string.ascii_lowercase)
    decoded_text = ''
    
    for char in encoded_text:
        if char.isalpha():
            old_index = lowercase_letters.index(char.lower())
            new_index = (old_index - shift) % len(lowercase_letters)
            if char.islower():
                decoded_text += lowercase_letters[new_index]
            else:
                decoded_text += lowercase_letters[new_index].upper()
        else:
            decoded_text += char
            
    return decoded_text





class BankAccount:
    def __init__(self, name="Rainy", ID="1234", creation_date=None, balance=0):
        if creation_date is None:
            creation_date = datetime.date.today()
        if creation_date > datetime.date.today():
            raise ValueError("date cannot be in the future.")
        self.name = name
        self.ID = ID
        self.creation_date = creation_date
        self.balance = balance


    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited ${amount}. New balance: ${self.balance}")
        else:
            print("Deposit amount must be positive. Transaction cancelled.")


    def withdraw(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            print(f"Withdrew ${amount}. New balance: ${self.balance}")
        else:
            print("Invalid withdrawal amount or insufficient funds. Transaction cancelled.")


    def view_balance(self):
        print(f"Current balance: ${self.balance}")




class SavingsAccount(BankAccount):
    def withdraw(self, amount):
        account_age_days = (datetime.date.today() - self.creation_date).days
        if account_age_days < 180:
            print("Account must be open for at least 180 days to withdraw.")
        elif amount > self.balance:
            print("Insufficient funds.")
        elif amount <= 0:
            print("Withdrawal amount must be positive.")
        else:
            self.balance -= amount
            print(f"Withdrew ${amount}. New balance: ${self.balance}")




class CheckingAccount(BankAccount):
    def withdraw(self, amount):
        overdraft_fee = 30
        if amount > self.balance:
            self.balance -= (amount + overdraft_fee)
        else:
            self.balance -= amount
