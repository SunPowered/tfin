"""Allows for an accounting style journal of accounts and transactions"""
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Dict, Optional, Protocol, Type, Union

__all__ = [
    "Account",
    "Asset",
    "Liability",
    "Equity",
    "Income",
    "Expense",
    "AccountType",
    "accounts_by_type",
    "ChartOfAccounts",
]


class AccountType(Enum):
    ASSET = auto()
    LIABILITY = auto()
    EQUITY = auto()
    INCOME = auto()
    EXPENSE = auto()


N = Union[float, int]  # Numeric type
C = Callable[[float, float], float]  # Numeric callable operator type


class AccountLike(Protocol):
    """The Account Protocol interface"""

    account_type: AccountType

    @property
    @abstractmethod
    def balance(self):
        """The balance of the account"""

    @abstractmethod
    def credit(self, amount: N):
        """Credit the account"""

    @abstractmethod
    def debit(self, amount: N):
        """Debit the account"""


@dataclass
class AccountBase:
    """Account dataclass."""

    name: str
    starting_balance: float = 0.0

    def __post_init__(self):
        self._balance = self.starting_balance

    @property
    def balance(self):
        return self._balance

    def set_balance(self, amount: N):
        self._balance = float(amount)

    def __str__(self):
        return f"{self.name}[{self.account_type.name} - ${self.balance:.2f}]"


class Account(AccountBase):
    """Account abstract dataclass.

    Do not instantiate directly.  It is useful, however, as a typing reference and
    for isinstance() checks"""

    debit_op: C
    credit_op: C
    account_type: AccountType

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


accounts_by_type: Dict[AccountType, Type[Account]] = {
    AccountType.ASSET: Asset,
    AccountType.LIABILITY: Liability,
    AccountType.EQUITY: Equity,
    AccountType.INCOME: Income,
    AccountType.EXPENSE: Expense,
}


class ChartOfAccounts:
    """A chart of accounts that can manage and filter accounts"""

    def __init__(self):

        self._accounts: Dict[str, Dict[str, Account]] = dict(
            ((act_type.name, {}) for act_type in AccountType)
        )

    def __len__(self):
        """Return the total number of accounts under management"""
        return sum([len(self._accounts[acc_type]) for acc_type in self._accounts])

    def _convert_account_type(
        self, account_type: Union[AccountType, str]
    ) -> Optional[AccountType]:
        """Convert a string account type to a proper AccountType Object"""

        if isinstance(account_type, AccountType):
            return account_type

        if isinstance(account_type, str):
            try:
                return AccountType[account_type.upper()]
            except KeyError:
                ...
        return None

    @property
    def accounts(self):
        return self._accounts

    def add_account(self, account: Account):
        """Add an instantiated account to the chart"""
        if isinstance(account, Account):
            self._accounts[account.account_type.name][account.name] = account

    def remove_account(self, account: Account):
        """Remove an account from the chart"""
        if not isinstance(account, Account):
            return
        accounts = self.by_type(account.account_type)
        if accounts and account.name in accounts:
            del self._accounts[account.account_type.name][account.name]

    def create_account(
        self,
        account_type: Union[AccountType, str],
        account_name: str,
        starting_balance: N = 0.0,
    ) -> Optional[Account]:
        """Create and add a new account from its constructor parameters and add return it"""

        cast_account_type = self._convert_account_type(account_type)
        if not cast_account_type:
            return None

        account = accounts_by_type[cast_account_type](
            name=account_name, starting_balance=float(starting_balance)
        )
        self.add_account(account)
        return account

    def has_account(self, account: Account) -> bool:
        """Method to see whether an instantiated account is present in the coa"""
        return account.name in self._accounts[account.account_type.name]

    def by_type(
        self, account_type: Union[AccountType, str]
    ) -> Optional[Dict[str, Account]]:
        """Returns a dict of accounts with a given account type.

        You can pass an AccountType directly, or a string of the account type"""

        cast_account_type = self._convert_account_type(account_type)
        return self._accounts[cast_account_type.name] if cast_account_type else None

    def by_name_and_type(
        self,
        account_name: str,
        account_type: Union[AccountType, str],
    ) -> Optional[Account]:
        """Look for an account by its name and type, return it if found, None otherwise"""
        accounts = self.by_type(account_type)
        return accounts.get(account_name, None) if accounts else None
