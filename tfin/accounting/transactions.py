from dataclasses import dataclass

from .core import Account
from ..engine import Event

@dataclass
class TransactionItem:
    """Object to store relevant transaction item data"""

    account: Account
    amount: float


class Transaction(Event):
    """A transaction event to manage accounting transactions between accounts

    A transaction consists of both debits and credits.  Each debit/credit item
    belongs to an account and an amount"""

    def __init__(self, timestep: int, name: str):
        super().__init__(timestep, name)
        self.clear()

    def clear(self):
        """Clears the current transaction of all debits and credits"""
        self._debits: list[TransactionItem] = []
        self._credits: list[TransactionItem] = []

    @property
    def debits(self):
        """The debits stored in this transaction"""
        return self._debits

    @property
    def credits(self):
        """The credits stored in this transaction"""
        return self._credits

    @property
    def is_balanced(self) -> bool:
        """A boolean property indicating whether the current transaction is balanced"""
        return self.total_credits == self.total_debits

    @property
    def n_entries(self) -> int:
        """An integer property of the total number of elements in the transaction"""
        return len(self._credits) + len(self._debits)

    @property
    def total_debits(self) -> float:
        """A float property of the total amount of debits in the transaction"""
        return sum([i.amount for i in self._debits])

    @property
    def total_credits(self) -> float:
        """A float property of the total amount of credits in the transaction"""
        return sum([i.amount for i in self._credits])

    def add_debit(self, item: Account | TransactionItem, amount: float = None):
        """Adds a TransactionItem to the debits"""
        if isinstance(item, Account):
            if amount is None:
                return
            trans_item = TransactionItem(item, amount)
        elif isinstance(item, TransactionItem):
            trans_item = item
        else:
            return

        self._debits.append(trans_item)

    def add_credit(self, item: Account | TransactionItem, amount: float = None):
        """Adds a TransactionItem to the credits"""
        if isinstance(item, Account):
            if amount is None:
                return
            trans_item = TransactionItem(item, amount)
        elif isinstance(item, TransactionItem):
            trans_item = item
        else:
            return

        self._credits.append(trans_item)

    def call(self, *args):
        """Executes the transaction, applying credits and debits to accounts"""
        if not self.is_balanced:
            return

        for item in self._credits:
            item.account.credit(item.amount)

        for item in self._debits:
            item.account.debit(item.amount)

        yield None
