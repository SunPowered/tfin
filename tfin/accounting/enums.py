from enum import Enum, auto

class AccountType(Enum):
    ASSET = auto()
    LIABILITY = auto()
    EQUITY = auto()
    INCOME = auto()
    EXPENSE = auto()

