# Encapsulation — Exercises

Step 3 of 4 · Notes: [1-notes.md](1-notes.md) · Example: [2-example.py](2-example.py) · Solutions: [4-solutions.py](4-solutions.py)

**Rules:**
- Do these **without looking at** the notes, the example or the solutions.
- Write your code in this topic's `practice/` folder, e.g. `practice/exercise_3.py`. Git ignores `practice/`, so your attempts never get committed.
- Check the solutions only after you've finished, or after you've been properly stuck for a while.
- **Tick Encapsulation in the roadmap once you've done all four.**

---

## Exercise 1 — Spot the bugs

*Tests: recognizing broken encapsulation, the way you would in a code review.*

The rule this class should protect: **`total` always equals the sum of `price × qty` over the cart's items, every price is ≥ 0, and every quantity is > 0.**

Find **at least 5** ways the rule can be broken, or ways one cart's state can leak into something else. For each, write one line on what goes wrong and how you'd fix it.

```python
class ShoppingCart:
    def __init__(self, owner, items=[]):
        self.owner = owner
        self.items = items
        self.__total = 0

    def add_item(self, name, price, qty=1):
        if qty <= 0:
            raise ValueError("qty must be positive")
        self.items.append((name, price, qty))
        self.__total += price * qty

    def get_items(self):
        return self.items

    @property
    def total(self):
        return self.__total

    @total.setter
    def total(self, value):
        self.__total = value
```

> Hint: think about what happens when you create two carts, when the caller passes in their own list, and what callers can reach without calling `add_item()`.

---

## Exercise 2 — Refactor a leaky class

*Tests: fixing existing code without breaking the code that uses it.*

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius
        self.fahrenheit = celsius * 9 / 5 + 32
```

This class has two problems:
- After `t.celsius = 100`, `t.fahrenheit` still shows the old value.
- Nothing stops a temperature below absolute zero (−273.15 °C).

**Refactor it so that:**
1. `t.celsius` can be read and set, and `t.fahrenheit` always matches it.
2. `t.fahrenheit` can also be set, e.g. `t.fahrenheit = 212` makes `t.celsius` 100.
3. Any temperature below −273.15 °C raises `ValueError`: in the constructor and in both setters.
4. Only one value is actually stored.
5. **This existing code still works without any changes:**

```python
t = Temperature(25)
print(t.celsius, t.fahrenheit)   # 25 77.0
t.celsius = 100
print(t.fahrenheit)              # 212.0
t.fahrenheit = 32
print(t.celsius)                 # 0.0
```

---

## Exercise 3 — Build from scratch

*Tests: designing a class from requirements, as LLD rounds do.*

**Build a `ParkingSpot` class:**

1. It has a `spot_id` and a `size` (`"small"`, `"medium"` or `"large"`). Neither can change after creation, and an invalid size raises `ValueError`.
2. `is_free` is a read-only property.
3. `assign(vehicle_number: str)` parks a vehicle. It raises an error if the spot is already taken.
4. `release()` frees the spot and returns the vehicle number that was parked. It raises an error if the spot is already free.
5. The parked vehicle number can be read, but there's no way to set it except through `assign()`.

**Then add a value object:**

6. Make `spot_id` a frozen dataclass `SpotId(floor: int, number: int)`. Both must be positive. Show that two `SpotId`s with the same values are equal and can be used as `dict` keys.

**Check yourself:** in a `main()` function, try to break every rule above and print what happens. If every rule holds, you're done.

---

## Exercise 4 — Explain it aloud

*Tests: justifying your design, which interviewers weigh as much as the code.*

Answer each question **out loud, in under a minute**, as if an interviewer asked it. Then compare with the model answers at the bottom of the solutions file.

1. Python has no `private` keyword. How do you enforce encapsulation?
2. Why not make every attribute `__private` to be safe?
3. A getter returns `self._items`, which is a list. What's wrong with that, and how do you fix it?
4. When would you use a frozen dataclass instead of a regular class with properties?
5. What's the difference between encapsulation and abstraction?
