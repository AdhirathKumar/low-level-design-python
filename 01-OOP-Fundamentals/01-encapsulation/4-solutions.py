"""Step 4 of 4: solutions to 3-exercises.md.

Try the exercises first. Run with: python 4-solutions.py
"""

from dataclasses import FrozenInstanceError, dataclass
from decimal import Decimal


# ---------------------------------------------------------------------------
# Exercise 1 — Spot the bugs
#
# Problems in the original ShoppingCart:
#   1. `items=[]` default: the list is created once and shared by every cart
#      made without an argument, so adding to one cart adds to all of them.
#   2. `self.items = items` stores the caller's list, so the caller can still
#      change the cart's contents from outside.
#   3. `items` is public, so `cart.items.append(...)` skips add_item(): no
#      validation, and total is never updated.
#   4. `get_items()` returns the internal list itself, the same leak as 3.
#   5. The `total` setter lets anyone write any value, so total no longer
#      matches the items.
#   6. `price` is never validated, so a negative price lowers the total.
#   Also: `__total` uses name mangling where `_total` is enough, and money is
#   stored as float-friendly numbers rather than Decimal.
#
# Fixed version: copy the input, keep state internal, compute total instead
# of storing it, and return a tuple.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CartItem:
    name: str
    price: Decimal
    qty: int

    def __post_init__(self) -> None:
        if self.price < 0:
            raise ValueError("price cannot be negative")
        if self.qty <= 0:
            raise ValueError("qty must be positive")


class ShoppingCart:
    def __init__(self, owner: str, items: list[CartItem] | None = None) -> None:
        self.owner = owner
        self._items: list[CartItem] = list(items) if items else []  # fixes 1 and 2

    def add_item(self, name: str, price: Decimal, qty: int = 1) -> None:
        self._items.append(CartItem(name, price, qty))  # CartItem validates (fixes 6)

    @property
    def items(self) -> tuple[CartItem, ...]:
        return tuple(self._items)  # read-only copy (fixes 3 and 4)

    @property
    def total(self) -> Decimal:
        # Computed every time, so it can never drift from the items (fixes 5).
        return sum((item.price * item.qty for item in self._items), Decimal("0"))


# ---------------------------------------------------------------------------
# Exercise 2 — Refactor a leaky class
#
# Store only celsius. Fahrenheit is computed from it, and both setters go
# through the same validation. Callers still write t.celsius / t.fahrenheit,
# so no calling code changes.
# ---------------------------------------------------------------------------

class Temperature:
    ABSOLUTE_ZERO_C = -273.15

    def __init__(self, celsius: float) -> None:
        self.celsius = celsius  # goes through the setter, so it's validated

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < self.ABSOLUTE_ZERO_C:
            raise ValueError(f"{value} °C is below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self.celsius = (value - 32) * 5 / 9  # reuse the celsius validation


# ---------------------------------------------------------------------------
# Exercise 3 — Build from scratch
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SpotId:
    floor: int
    number: int

    def __post_init__(self) -> None:
        if self.floor <= 0 or self.number <= 0:
            raise ValueError("floor and number must be positive")


class ParkingSpot:
    SIZES = ("small", "medium", "large")

    def __init__(self, spot_id: SpotId, size: str) -> None:
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}")
        self._spot_id = spot_id
        self._size = size
        self._vehicle_number: str | None = None

    @property
    def spot_id(self) -> SpotId:
        return self._spot_id

    @property
    def size(self) -> str:
        return self._size

    @property
    def vehicle_number(self) -> str | None:
        return self._vehicle_number

    @property
    def is_free(self) -> bool:
        return self._vehicle_number is None

    def assign(self, vehicle_number: str) -> None:
        if not self.is_free:
            raise ValueError(f"spot {self._spot_id} is already taken")
        self._vehicle_number = vehicle_number

    def release(self) -> str:
        if self.is_free:
            raise ValueError(f"spot {self._spot_id} is already free")
        vehicle_number, self._vehicle_number = self._vehicle_number, None
        return vehicle_number


# ---------------------------------------------------------------------------
# Exercise 4 — Model answers (compare after answering aloud)
# ---------------------------------------------------------------------------

MODEL_ANSWERS = """
1. Python has no `private` keyword. How do you enforce encapsulation?
   By convention and by design. A leading underscore marks internal state,
   and changes go through methods or @property setters that check the rules.
   Python won't stop someone writing obj._x, but well-designed classes give
   no reason to. For values that must never change, a frozen dataclass makes
   assignment actually fail.

2. Why not make every attribute `__private` to be safe?
   Double underscore isn't real privacy: it only renames the attribute to
   _ClassName__x. It makes subclasses, tests and debugging awkward, and it
   signals more than you mean. Use it only to avoid name clashes between a
   base class and its subclasses. A single underscore is the normal choice.

3. A getter returns `self._items`, a list. What's wrong, and how do you fix it?
   The caller gets the same list object, so they can append to or clear it
   and bypass every rule the class enforces. Return a copy: a tuple (read-only)
   or list(self._items). If the items themselves are mutable, they may need
   to be immutable too, e.g. frozen dataclasses.

4. When would you use a frozen dataclass instead of a class with properties?
   For value objects: things defined entirely by their values that shouldn't
   change, like Money, Coordinate or DateRange. They're validated once, safe
   to share and use across threads, compare by value and work as dict keys.
   Use a regular class when the object has an identity and a lifecycle whose
   state changes, like a ParkingSpot or a BankAccount.

5. What's the difference between encapsulation and abstraction?
   Encapsulation hides an object's data: it controls who can change state and
   how. Abstraction hides complexity: callers use a simple interface without
   knowing the implementation. A PaymentGateway interface is abstraction; its
   Stripe implementation keeping its API key in _api_key is encapsulation.
"""


def try_it(label: str, action) -> None:
    try:
        action()
        print(f"  {label}: allowed")
    except (ValueError, AttributeError, FrozenInstanceError) as error:
        print(f"  {label}: blocked ({type(error).__name__}: {error})")


def main() -> None:
    print("Exercise 1 — fixed ShoppingCart")
    cart_a, cart_b = ShoppingCart("Asha"), ShoppingCart("Ravi")
    cart_a.add_item("Pen", Decimal("10"), 3)
    print(f"  cart_b unaffected by cart_a: {cart_b.items}")
    outside = [CartItem("Book", Decimal("200"), 1)]
    cart_c = ShoppingCart("Mira", outside)
    outside.clear()
    print(f"  caller clearing their list doesn't empty cart_c: {len(cart_c.items)} item(s)")
    try_it("append via cart_a.items", lambda: cart_a.items.append("fake"))
    try_it("set cart_a.total", lambda: setattr(cart_a, "total", Decimal("0")))
    try_it("add a negative price", lambda: cart_a.add_item("Refund", Decimal("-50")))
    print(f"  cart_a.total = {cart_a.total}")

    print("\nExercise 2 — Temperature (the original calling code)")
    t = Temperature(25)
    print(f"  {t.celsius} {t.fahrenheit}")
    t.celsius = 100
    print(f"  {t.fahrenheit}")
    t.fahrenheit = 32
    print(f"  {t.celsius}")
    try_it("Temperature(-300)", lambda: Temperature(-300))
    try_it("set fahrenheit to -500", lambda: setattr(t, "fahrenheit", -500))
    print(f"  stored attributes: {list(vars(t))}")

    print("\nExercise 3 — ParkingSpot and SpotId")
    spot = ParkingSpot(SpotId(1, 7), "medium")
    try_it("invalid size", lambda: ParkingSpot(SpotId(1, 8), "huge"))
    try_it("SpotId(0, 1)", lambda: SpotId(0, 1))
    try_it("change spot.size", lambda: setattr(spot, "size", "large"))
    try_it("set spot.is_free", lambda: setattr(spot, "is_free", False))
    try_it("set spot.vehicle_number", lambda: setattr(spot, "vehicle_number", "KA01"))
    try_it("release a free spot", spot.release)
    spot.assign("KA01AB1234")
    print(f"  after assign: is_free={spot.is_free}, vehicle={spot.vehicle_number}")
    try_it("assign a taken spot", lambda: spot.assign("MH02CD5678"))
    print(f"  release() returned {spot.release()}, is_free={spot.is_free}")
    try_it("change SpotId.floor", lambda: setattr(spot.spot_id, "floor", 2))
    spots = {SpotId(1, 7): spot}
    print(f"  equal SpotIds: {SpotId(1, 7) == SpotId(1, 7)}, dict lookup works: {SpotId(1, 7) in spots}")

    print("\nExercise 4 — model answers")
    print(MODEL_ANSWERS)


if __name__ == "__main__":
    main()
