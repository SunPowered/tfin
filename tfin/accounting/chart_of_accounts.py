from .types import N
from .enums import AccountType
from .core import Account, Asset, Liability, Income, Expense, Equity, accounts_by_type

class ChartOfAccounts:
    """A chart of accounts that can manage and filter accounts"""

    def __init__(self):

        self._accounts: dict[str, dict[str, Account]] = dict(
            ((act_type.name, {}) for act_type in AccountType)
        )

    def __len__(self):
        """Return the total number of accounts under management"""
        return sum([len(self._accounts[acc_type]) for acc_type in self._accounts])

    def _convert_account_type(
        self, account_type: AccountType | str
    ) -> AccountType | None:
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

    def _create_account(self, acc_cls: Account, name: str, balance: float = 0.0):
        account = acc_cls(name, balance)
        self.add_account(account)
        return account

    def create_asset_account(self, name: str, balance: float = 0.0) -> Account:
        """Helper method to create and add an Asset account by parameters"""
        return self._create_account(Asset, name, balance)

    def create_liability_account(self, name: str, balance: float = 0.0) -> Account:
        """Helper method to create and add a Liability account by parameters"""
        return self._create_account(Liability, name, balance)

    def create_income_account(self, name: str, balance: float = 0.0) -> Account:
        """Helper method to create and add an Income account by parameters"""
        return self._create_account(Income, name, balance)

    def create_expense_account(self, name: str, balance: float = 0.0) -> Account:
        """Helper method to create and add an Expense account by parameters"""
        return self._create_account(Expense, name, balance)

    def create_equity_account(self, name: str, balance: float = 0.0) -> Account:
        """Helper method to create and add an Equity account by parameters"""
        return self._create_account(Equity, name, balance)

    def create_and_add_account(
        self,
        account_type: AccountType | str,
        account_name: str,
        starting_balance: N = 0.0,
    ) -> Account | None:
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
        self, account_type: AccountType | str
    ) -> dict[str, Account] | None:
        """Returns a dict of accounts with a given account type.

        You can pass an AccountType directly, or a string of the account type"""

        cast_account_type = self._convert_account_type(account_type)
        return self._accounts[cast_account_type.name] if cast_account_type else None

    def by_name_and_type(
        self,
        account_name: str,
        account_type: AccountType | str,
    ) -> Account | None:
        """Look for an account by its name and type, return it if found, None otherwise"""
        accounts = self.by_type(account_type)
        return accounts.get(account_name, None) if accounts else None

