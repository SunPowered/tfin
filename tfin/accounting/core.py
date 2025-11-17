from dataclasses import dataclass
from collections.abc import Callable
from .types import N
from .enums import AccountType

@dataclass
class AccountBase:
    """Account dataclass."""

    name: str
    starting_balance: float = 0.0

    def __post_init__(self):
        self._balance = float(self.starting_balance)

    @property
    def balance(self):
        return self._balance

    def set_balance(self, amount: N):
        self._balance = float(amount)

   
type NumericOp = Callable[[float], float]

class Account(AccountBase):
    """Account abstract dataclass.

    Do not instantiate directly.  It is useful, however, as a typing reference and
    for isinstance() checks"""

    debit_op: NumericOp
    credit_op: NumericOp
    
    account_type: AccountType

    def debit(self, amount: N):
        """Debit the account by an amount."""
        # TODO: Fix the typing issue on refactor
        self.set_balance(self.__class__.debit_op(self.balance, float(amount)))  # type: ignore

    def credit(self, amount: N):
        """Credit the account by an amount"""
        # TODO: Fix the typing issue on refactor
        self.set_balance(self.__class__.credit_op(self.balance, float(amount))) # type: ignore

    def __str__(self):
        return f"{self.name}[{self.account_type.name} - ${self.balance:.2f}]"

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

AccountTypes = Asset | Liability | Equity | Income | Expense

accounts_by_type: dict[AccountType, type[Account]] = {
    AccountType.ASSET: Asset,
    AccountType.LIABILITY: Liability,
    AccountType.EQUITY: Equity,
    AccountType.INCOME: Income,
    AccountType.EXPENSE: Expense,
}
