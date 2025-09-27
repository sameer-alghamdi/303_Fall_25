"""
Pair Exercise #3: Functions and Classes
Caesar's Cipher and Banking System Implementation
"""

import string
import datetime


def encode(input_text, shift):
    """
    Encode text using Caesar's cipher.
    
    Args:
        input_text (str): The text to be encrypted
        shift (int): Number of places to shift along the alphabet
        
    Returns:
        tuple: (list of lowercase alphabet, encoded text)
    """
    alphabet = list(string.ascii_lowercase)
    encoded_text = ""
    
    for char in input_text:
        if char.isalpha():
            # Convert to lowercase for processing
            lower_char = char.lower()
            # Find position in alphabet
            old_index = alphabet.index(lower_char)
            # Calculate new position with wrapping
            new_index = (old_index + shift) % 26
            # Get new character
            new_char = alphabet[new_index]
            encoded_text += new_char
        else:
            # Keep non-alphabetic characters unchanged
            encoded_text += char
    
    return (alphabet, encoded_text)


def decode(input_text, shift):
    """
    Decode text using Caesar's cipher.
    
    Args:
        input_text (str): The text to be decrypted
        shift (int): Number of places to shift along the alphabet
        
    Returns:
        str: The decoded text
    """
    alphabet = list(string.ascii_lowercase)
    decoded_text = ""
    
    for char in input_text:
        if char.isalpha():
            # Convert to lowercase for processing
            lower_char = char.lower()
            # Find position in alphabet
            old_index = alphabet.index(lower_char)
            # Calculate original position with wrapping
            new_index = (old_index - shift) % 26
            # Get original character
            new_char = alphabet[new_index]
            decoded_text += new_char
        else:
            # Keep non-alphabetic characters unchanged
            decoded_text += char
    
    return decoded_text


class BankAccount:
    """
    A basic bank account class with deposit, withdrawal, and balance viewing functionality.
    """
    
    def __init__(self, name="Rainy", ID="1234", creation_date=None, balance=0):
        """
        Initialize a BankAccount instance.
        
        Args:
            name (str): Owner's name, default "Rainy"
            ID (str): Alphanumeric ID, default "1234"
            creation_date (datetime.date): Date of account creation, default today
            balance (float): Account balance, default 0
        """
        self.name = name
        self.ID = ID
        
        # Set creation_date to today if not provided
        if creation_date is None:
            self.creation_date = datetime.date.today()
        else:
            # Check if creation_date is in the future
            if creation_date > datetime.date.today():
                raise Exception("Creation date cannot be in the future")
            self.creation_date = creation_date
        
        self.balance = balance
    
    def deposit(self, amount):
        """
        Deposit money into the account.
        
        Args:
            amount (float): Amount to deposit (must be positive)
        """
        if amount >= 0:
            self.balance += amount
        print(f"Account balance: ${self.balance}")
    
    def withdraw(self, amount):
        """
        Withdraw money from the account.
        
        Args:
            amount (float): Amount to withdraw
        """
        self.balance -= amount
        print(f"Account balance: ${self.balance}")
    
    def view_balance(self):
        """
        View the current account balance.
        
        Returns:
            float: Current account balance
        """
        return self.balance


class SavingsAccount(BankAccount):
    """
    A savings account that extends BankAccount with additional restrictions.
    """
    
    def withdraw(self, amount):
        """
        Withdraw money from the savings account.
        Withdrawals are only permitted after 180 days and overdrafts are not allowed.
        
        Args:
            amount (float): Amount to withdraw
        """
        # Check if account has been open for at least 180 days
        days_since_creation = (datetime.date.today() - self.creation_date).days
        
        if days_since_creation < 180:
            # Don't allow withdrawal, don't change balance
            print(f"Account balance: ${self.balance}")
            return
        
        # Check if withdrawal would cause overdraft
        if self.balance - amount < 0:
            # Don't allow overdraft, don't change balance
            print(f"Account balance: ${self.balance}")
            return
        
        # Perform withdrawal
        self.balance -= amount
        print(f"Account balance: ${self.balance}")


class CheckingAccount(BankAccount):
    """
    A checking account that extends BankAccount with overdraft fees.
    """
    
    def withdraw(self, amount):
        """
        Withdraw money from the checking account.
        Overdrafts are permitted but incur a $30 fee.
        
        Args:
            amount (float): Amount to withdraw
        """
        # Check if withdrawal will cause overdraft
        if self.balance - amount < 0:
            # Apply overdraft fee
            self.balance = self.balance - amount - 30
        else:
            # Normal withdrawal
            self.balance -= amount
        
        print(f"Account balance: ${self.balance}")
