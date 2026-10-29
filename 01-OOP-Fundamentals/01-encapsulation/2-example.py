"""Encapsulation in Python.

Step 2 of 4. Run with: python 2-example.py
Notes: 1-notes.md · Next: 3-exercises.md

Each demo matches a step in the notes. Try changing things to see what breaks.
"""

from dataclasses import FrozenInstanceError, dataclass


# Demo 1 (notes, Step 1): the rule is checked at creation, then never again.
class LeakyAccount:
    def __init__(self, owner: str, balance: int) -> None:
        if balance < 0:
            raise ValueError("balance cannot be negative")
        self.owner = owner
        self.balance = balance


# Demos 2 and 3 (notes, Steps 2 to 4): the rules hold after every change.
class BankAccount:
    def __init__(self, owner: str) -> None:
        self.owner = owner                  # runs the owner setter below
        self._balance = 0                   # internal: changed only by methods
        self._history: list[str] = []       # internal list

    # Read-only property (Step 3): no setter, so assignment fails.
    @property
    def balance(self) -> int:
        return self._balance

    # Validated property (Step 4): assignment allowed, but checked.
    @property
    def owner(self) -> str:
        return self._owner

    @owner.setter
    def owner(self, value: str) -> None:
        if not value.strip():
            raise ValueError("owner cannot be empty")
        self._owner = value

    # Return a copy so callers can't change the internal list (Going deeper).
    @property
    def history(self) -> tuple[str, ...]:
        return tuple(self._history)

    # Changes go through methods that check the rules (Step 2).
    def deposit(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self._balance += amount
        self._history.append(f"deposit {amount}")

    def withdraw(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if amount > self._balance:
            raise ValueError("insufficient funds")
        self._balance -= amount
        self._history.append(f"withdraw {amount}")


# Demo 4 (notes, Going deeper): an immutable value object.
@dataclass(frozen=True)
class Money:
    amount: int
    currency: str

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("amount cannot be negative")


def try_it(label: str, action) -> None:
    """Run action and print whether Python allowed it or blocked it."""
    try:
        action()
        print(f"  {label}: allowed")
    except (ValueError, AttributeError, FrozenInstanceError) as error:
        print(f"  {label}: blocked ({type(error).__name__}: {error})")


def main() -> None:
    print("Demo 1: checked at creation, unprotected after")
    leaky = LeakyAccount("Asha", 100)
    try_it("create with balance -5", lambda: LeakyAccount("Asha", -5))
    try_it("set balance to -500 later", lambda: setattr(leaky, "balance", -500))
    print(f"  leaky.balance is now {leaky.balance}  <- the rule is broken")

    print("\nDemo 2: changes go through methods, balance is read-only")
    account = BankAccount("Asha")
    account.deposit(100)
    account.withdraw(30)
    print(f"  balance = {account.balance}")
    try_it("withdraw 500", lambda: account.withdraw(500))
    try_it("deposit -5", lambda: account.deposit(-5))
    try_it("set balance to -500", lambda: setattr(account, "balance", -500))
    print(f"  balance is still {account.balance}")

    print("\nDemo 3: owner can be changed, but only to a valid value")
    try_it("set owner to 'Asha Rao'", lambda: setattr(account, "owner", "Asha Rao"))
    try_it("set owner to '   '", lambda: setattr(account, "owner", "   "))
    try_it("create BankAccount('')", lambda: BankAccount(""))
    try_it("append to account.history", lambda: account.history.append("fake"))
    print(f"  history is still {account.history}")

    print("\nDemo 4 (Going deeper): a frozen value object")
    price = Money(250, "INR")
    try_it("create Money(-1, 'INR')", lambda: Money(-1, "INR"))
    try_it("set price.amount to 0", lambda: setattr(price, "amount", 0))
    print(f"  equal by value: {price == Money(250, 'INR')}")


if __name__ == "__main__":
    main()
