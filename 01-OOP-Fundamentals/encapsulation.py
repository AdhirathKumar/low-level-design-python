"""Encapsulation in Python.

Run with: python encapsulation.py
Notes: 01-encapsulation.md
"""

from decimal import Decimal


class BankAccount:
    """A bank account whose balance can never go negative.

    That rule (the invariant) holds because the balance is only changed
    through deposit() and withdraw(), which both validate their input.
    """

    def __init__(self, owner: str, overdraft_fee: Decimal = Decimal("0")) -> None:
        self.owner = owner                  # public: no rules attached
        self._balance = Decimal("0")        # internal: change via methods only
        self._transactions: list[str] = []  # internal mutable state
        self.overdraft_fee = overdraft_fee  # goes through the setter below

    # Read-only property: callers can read the balance but not assign to it.
    @property
    def balance(self) -> Decimal:
        return self._balance

    # Validated property: assignment is allowed, but only to valid values.
    @property
    def overdraft_fee(self) -> Decimal:
        return self._overdraft_fee

    @overdraft_fee.setter
    def overdraft_fee(self, value: Decimal) -> None:
        if value < 0:
            raise ValueError("overdraft_fee cannot be negative")
        self._overdraft_fee = value

    # Return a copy so callers can't modify the internal list.
    @property
    def transactions(self) -> tuple[str, ...]:
        return tuple(self._transactions)

    def deposit(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("deposit amount must be positive")
        self._balance += amount
        self._transactions.append(f"deposit {amount}")

    def withdraw(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("insufficient funds")
        self._balance -= amount
        self._transactions.append(f"withdraw {amount}")


class Base:
    def __init__(self) -> None:
        self.__token = "base-secret"  # stored as _Base__token

    def base_token(self) -> str:
        return self.__token


class Child(Base):
    def __init__(self) -> None:
        super().__init__()
        self.__token = "child-value"  # stored as _Child__token, no clash


def try_it(label: str, action) -> None:
    try:
        action()
        print(f"  {label}: allowed")
    except (ValueError, AttributeError) as error:
        print(f"  {label}: blocked ({type(error).__name__}: {error})")


def main() -> None:
    print("1. Normal use goes through methods")
    account = BankAccount("Asha")
    account.deposit(Decimal("100"))
    account.withdraw(Decimal("30"))
    print(f"  balance = {account.balance}")
    print(f"  transactions = {account.transactions}")

    print("\n2. The invariant can't be broken through the public interface")
    try_it("withdraw more than the balance", lambda: account.withdraw(Decimal("500")))
    try_it("deposit a negative amount", lambda: account.deposit(Decimal("-5")))
    try_it("assign balance directly", lambda: setattr(account, "balance", Decimal("1000000")))
    try_it("set a negative overdraft_fee", lambda: setattr(account, "overdraft_fee", Decimal("-1")))
    try_it("set a valid overdraft_fee", lambda: setattr(account, "overdraft_fee", Decimal("25")))

    print("\n3. Returning a copy protects internal state")
    try_it("append to account.transactions", lambda: account.transactions.append("fake"))
    print(f"  transactions still = {account.transactions}")

    print("\n4. '_' is only a convention: Python doesn't stop you")
    account._balance = Decimal("-999")
    print(f"  balance after writing account._balance = {account.balance}  <- don't do this")

    print("\n5. '__' name mangling avoids clashes between base class and subclass")
    child = Child()
    print(f"  base class still sees its own value: {child.base_token()}")
    print(f"  stored attributes: {sorted(k for k in vars(child) if 'token' in k)}")


if __name__ == "__main__":
    main()
