# pe3.py
from __future__ import annotations
import datetime
import string
from typing import List, Tuple

ALPHABET: List[str] = list(string.ascii_lowercase)
ALPHABET_LEN = len(ALPHABET)
INDEX = {ch: i for i, ch in enumerate(ALPHABET)}

def _shift_char(ch: str, shift: int) -> str:
    """Shift a single character in the lowercase English alphabet.
    Non-letters are returned unchanged. Output is always lowercase."""
    lo = ch.lower()
    if lo in INDEX:
        pos = (INDEX[lo] + shift) % ALPHABET_LEN
        return ALPHABET[pos]
    return ch

def encode(input_text: str, shift: int) -> Tuple[List[str], str]:
    """Return (alphabet_list, encoded_text) using Caesar shift."""
    encoded = "".join(_shift_char(c, shift) for c in input_text)
    return (ALPHABET.copy(), encoded)

def decode(input_text: str, shift: int) -> str:
    """Return decoded text (inverse Caesar shift)."""
    return "".join(_shift_char(c, -shift) for c in input_text)


class BankAccount:
    """Basic bank account."""
    def __init__(
        self,
        name: str = "Rainy",
        ID: str | int = "1234",
        creation_date: datetime.date | None = None,
        balance: float = 0,
    ) -> None:
        if creation_date is None:
            creation_date = datetime.date.today()
        if creation_date > datetime.date.today():
            # Spec: must raise Exception (not a subclass)
            raise Exception("creation_date cannot be in the future.")
        self.name = name
        self.ID = str(ID)
        self.creation_date = creation_date
        self.balance = float(balance)

    def deposit(self, amount: float) -> None:
        if amount < 0:
            raise Exception("Negative deposit not allowed.")
        self.balance += float(amount)
        print(f"Balance after deposit: {self.balance}")

    def withdraw(self, amount: float) -> None:
        if amount < 0:
            raise Exception("Negative withdrawal not allowed.")
        self.balance -= float(amount)
        print(f"Balance after withdrawal: {self.balance}")

    def view_balance(self) -> float:
        print(f"Current balance: {self.balance}")
        return self.balance


class SavingsAccount(BankAccount):
    """Savings: no overdrafts; withdrawals only after 180 days."""
    def withdraw(self, amount: float) -> None:
        if amount < 0:
            raise Exception("Negative withdrawal not allowed.")
        days_open = (datetime.date.today() - self.creation_date).days
        if days_open < 180:
            raise Exception("Withdrawals allowed only after 180 days.")
        if self.balance - float(amount) < 0:
            raise Exception("Overdrafts are not permitted for SavingsAccount.")
        self.balance -= float(amount)
        print(f"Balance after withdrawal: {self.balance}")


class CheckingAccount(BankAccount):
    """Checking: overdrafts allowed, but each overdraft incurs a $30 fee."""
    OVERDRAFT_FEE = 30.0

    def withdraw(self, amount: float) -> None:
        if amount < 0:
            raise Exception("Negative withdrawal not allowed.")
        self.balance -= float(amount)
        if self.balance < 0:
            self.balance -= self.OVERDRAFT_FEE
        print(f"Balance after withdrawal: {self.balance}")
