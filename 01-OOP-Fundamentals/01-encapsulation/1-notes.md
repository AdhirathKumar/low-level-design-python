# Encapsulation

**Phase 1 · Week 1 — Core OOPs Concepts** · Step 1 of 4 · Next: [2-example.py](2-example.py) → [3-exercises.md](3-exercises.md) → [4-solutions.py](4-solutions.py)

## The short version

**Encapsulation means an object protects its own data.** Outside code can't put the object into a bad state. Any change goes through the object's own methods, and those methods check the rules.

If you've used Pydantic, you've already done half of this.

## Start from what you know: Pydantic

```python
from pydantic import BaseModel, field_validator

class Account(BaseModel):
    owner: str
    balance: int

    @field_validator("balance")
    @classmethod
    def not_negative(cls, value):
        if value < 0:
            raise ValueError("balance cannot be negative")
        return value

Account(owner="Asha", balance=-5)     # ❌ ValidationError: the rule is checked on creation

account = Account(owner="Asha", balance=100)
account.balance = -500                # ✅ allowed! The rule isn't checked on changes
```

Pydantic checks the data **when the object is created**. After that, by default, anyone can change any field to anything. For API input that's fine: you validate the request, then pass the data along.

But in LLD problems, objects **live and change**: a parking spot gets taken and freed, an account gets deposits and withdrawals. The rules have to hold **after every change**, not just at creation. That's what encapsulation gives you.

## Step 1 — The same rule in a plain class

```python
class BankAccount:
    def __init__(self, owner, balance):
        if balance < 0:
            raise ValueError("balance cannot be negative")
        self.owner = owner
        self.balance = balance

account = BankAccount("Asha", 100)
account.balance = -500                # ✅ still allowed
```

Same gap as Pydantic: checked at creation, unprotected after.

## Step 2 — Make changes go through methods

```python
class BankAccount:
    def __init__(self, owner):
        self.owner = owner
        self._balance = 0             # leading underscore = "internal, don't touch"

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self._balance += amount

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("insufficient funds")
        self._balance -= amount
```

Two changes:

- **`_balance` has a leading underscore.** In Python this is a **naming convention** meaning "internal, not for outside code". Python doesn't actually block access, but every Python developer reads it as "hands off".
- **The balance only changes through `deposit()` and `withdraw()`.** Each one checks the rules, so the rules live in one place.

**New problem:** how does outside code *read* the balance? Writing `account._balance` breaks the convention.

## Step 3 — `@property`: let callers read, but not write

```python
class BankAccount:
    # ... same as above, plus:

    @property
    def balance(self):
        return self._balance

account = BankAccount("Asha")
account.deposit(100)
account.balance                       # 100: reads like a normal attribute
account.balance = 5                   # ❌ AttributeError: property has no setter
```

`@property` turns a method into something that **looks like an attribute** when you use it. You write `account.balance`, not `account.balance()`, but Python runs the method behind the scenes. With no setter defined, assignment fails.

## Step 4 — `@property` setter: allow changes, but checked

Sometimes outside code *should* be able to set a value directly, as long as it's valid. Add a setter:

```python
class BankAccount:
    def __init__(self, owner):
        self.owner = owner            # this line runs the setter below
        self._balance = 0

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        if not value.strip():
            raise ValueError("owner cannot be empty")
        self._owner = value

account = BankAccount("Asha")
account.owner = "Asha Rao"            # ✅ valid, allowed
account.owner = "   "                 # ❌ ValueError
BankAccount("")                       # ❌ ValueError: __init__ goes through the setter too
```

This is the plain-Python version of Pydantic's `validate_assignment=True`: the rule is checked **every time** the value changes, including in `__init__`.

## Which tool when

| You want… | Use |
|-----------|-----|
| A field with no rules | A plain attribute: `self.name = name` |
| State that changes only through specific operations | `self._x` plus methods like `deposit()` |
| Callers can read it but never set it | `@property` with no setter |
| Callers can set it, but only to valid values | `@property` plus a setter |

**Check the core:** close this file and try to (1) explain encapsulation in two sentences, and (2) write a class with a read-only property and a validated setter. If you can, you have the core. Everything below is depth.

---

## Going deeper

*Optional on a first read. The exercises use these, so come back before doing them.*

### Don't hand out your internal lists

```python
class Order:
    def __init__(self):
        self._items = []

    @property
    def items(self):
        return self._items            # ❌ caller gets the real list

order = Order()
order.items.append("free TV")         # bypasses every rule in the class
```

Return a copy instead: `return tuple(self._items)`. A tuple can't be changed. The same goes the other way: if `__init__` receives a list, store a copy (`list(items)`), not the caller's list. And never use a mutable default like `def __init__(self, items=[])`: that one list is shared by every object created without the argument.

### Immutable objects: frozen dataclasses

Some objects should never change after creation, like `Money(250, "INR")` or a `Coordinate(3, 4)`. Make them frozen:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: int
    currency: str

    def __post_init__(self):          # runs right after __init__: validate here
        if self.amount < 0:
            raise ValueError("amount cannot be negative")

price = Money(250, "INR")
price.amount = 0                      # ❌ FrozenInstanceError
```

Validated once, then can never break. Frozen objects compare by value (`Money(250, "INR") == Money(250, "INR")`) and can be `dict` keys. To "change" one, make a new one: `dataclasses.replace(price, amount=200)`.

**When to use which:** frozen for *values* (money, coordinates, date ranges); a regular class with properties for *things that change over time* (a parking spot, a bank account).

### Double underscore: `__name`

```python
class Base:
    def __init__(self):
        self.__token = "x"            # Python stores this as _Base__token
```

Python renames `__name` to `_ClassName__name`. This isn't real privacy. It exists so that a subclass defining its own `__token` doesn't accidentally overwrite the parent's. Use a single underscore by default. Reach for double only when you're designing a class to be subclassed and need to avoid that clash.

### Encapsulation vs abstraction

Interviewers often ask for the difference. Abstraction is the next topic.

- **Encapsulation hides an object's *data*:** it controls who can change state, and how.
- **Abstraction hides *complexity*:** callers use a simple interface without knowing what's behind it.

Example: a `PaymentGateway` interface with `pay()` is abstraction, since callers don't know if Stripe or Razorpay is behind it. The Stripe implementation keeping its API key in `self._api_key` is encapsulation.

### Common mistakes

- **Writing a getter and setter for every field.** If the setter has no rule, just use a plain attribute. You can switch to a property later without changing any calling code, because both are used as `obj.x`.
- **Using `__double` everywhere** because it "looks private". Single underscore is the norm.
- **Checking a rule in `__init__` but not in the setter,** or the other way round. Route `__init__` through the setter so the rule lives in one place.

### In interviews

- Show **internal state + public methods**: e.g. `ParkingSpot` has `assign()` and a read-only `is_free`, not a writable `vehicle` field.
- **Say why:** "I keep `_balance` internal so the no-negative-balance rule can't be bypassed."

### FastAPI connection

- Pydantic validates data at the API boundary. Encapsulated classes protect it after that.
- Pydantic has the same tools under different names: `validate_assignment=True` (like a property setter), `PrivateAttr` (like `_internal` state), and `@computed_field` (like a read-only property in the response).

---

## Exercises

Four exercises, from easier to harder: [3-exercises.md](3-exercises.md)

1. Spot the bugs in a leaky `ShoppingCart`
2. Refactor a `Temperature` class without breaking its callers
3. Build a `ParkingSpot` and a `SpotId` value object from scratch
4. Answer five interview questions out loud

Solutions: [4-solutions.py](4-solutions.py). Check them only after trying.

## Self-check

- [ ] Can I explain encapsulation in two sentences, and how it goes further than Pydantic validation?
- [ ] Can I write a read-only property and a validated setter from memory?
- [ ] Can I explain why returning an internal list breaks encapsulation?
- [ ] Can I explain when to use a frozen dataclass instead of a class with properties?
- [ ] Can I explain `_x` vs `__x`?
- [ ] Can I explain the difference between encapsulation and abstraction in one sentence?
