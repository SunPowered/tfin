"""Allows for an accounting style journal of accounts and transactions"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Protocol, Union

__all__ = ["Account", "Asset", "Liability", "Equity", "Income", "Expense"]


class AccountType(Enum):
    ASSET = auto()
    LIABILITY = auto()
    EQUITY = auto()
    INCOME = auto()
    EXPENSE = auto()


#
# The following few bits of Interface / Dataclass Mixin hell is due to mypy not being able to respond
#   correctly to a Dataclass that inherits from an ABC (ie typing.Protocol)
#
# I found a workaround from which I based this design:
#       https://github.com/python/mypy/issues/5374#issuecomment-582093112
#  FIXME: Make this pretty when mypy can take the heat
#
# Also, see: https://bugs.python.org/issue45081

N = Union[float, int]
C = Callable[[float, float], float]


class AccountInterface(Protocol):
    """The Account Protocol interface"""

    account_type: AccountType
    debit_op: C
    credit_op: C

    @property
    def balance(self) -> float:
        ...

    def credit(self, amount: N):
        ...

    def debit(self, amount: N):
        ...


@dataclass
class AccountMixin:
    """Account dataclass."""

    name: str
    starting_balance: float = 0.0

    def __post_init__(self):
        self._balance = self.starting_balance


class Account(AccountMixin, AccountInterface):
    """Account abstract dataclass.

    Do not instantiate directly.  It is useful, however, as a typing reference and
    for isinstance() checks"""

    @property
    def balance(self):
        return self._balance

    def set_balance(self, amount: N):
        self._balance = float(amount)

    def debit(self, amount: N):
        """Debit the account by an amount."""
        self.set_balance(self.__class__.debit_op(self.balance, float(amount)))

    def credit(self, amount: N):
        """Credit the account by an amount"""
        self.set_balance(self.__class__.credit_op(self.balance, float(amount)))


class AssetLike:
    """Mixin to manage the asset like accounts wrt to the operation of debit and credit"""

    debit_op = float.__add__
    credit_op = float.__sub__


class LiabilityLike:
    """Mixin to manage the liability like accounts wrt to the operation of debit and credit"""

    debit_op = float.__sub__
    credit_op = float.__add__


class Asset(Account, AssetLike):
    """Asset Account"""

    account_type = AccountType.ASSET


class Liability(Account, LiabilityLike):
    """Liability Account"""

    account_type = AccountType.LIABILITY


class Equity(Account, LiabilityLike):
    """Equity Account"""

    account_type = AccountType.EQUITY


class Income(Account, LiabilityLike):
    """Income Account"""

    account_type = AccountType.INCOME


class Expense(Account, AssetLike):
    """Expense Account"""

    account_type = AccountType.EXPENSE
