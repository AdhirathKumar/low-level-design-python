# Encapsulation

**Phase 1 · Week 1 — Core OOPs Concepts** · Example code: [encapsulation.py](encapsulation.py)

## What it is

Encapsulation means **bundling data with the methods that operate on it, and controlling how that data can be changed**.

The goal isn't just hiding things. It's protecting **invariants**: rules that must always be true about an object. For example, "a bank account balance never goes negative". If any code anywhere can write `account.balance = -500`, nothing can guarantee that rule. If changes have to go through `withdraw()`, one place enforces it.

## Encapsulation in Python

Python has no `private` / `protected` keywords like Java. It relies on conventions instead:

| Syntax | Meaning | Enforced? |
|--------|---------|-----------|
| `name` | Public: part of the class's interface | — |
| `_name` | Internal: "don't touch this from outside" | No, convention only |
| `__name` | Name-mangled to `_ClassName__name` | Partly: avoids accidental access and subclass name clashes |

> Python's philosophy is "we're all consenting adults here". Privacy is a signal to other developers, not a lock.

### `@property`: controlled access

`@property` lets you expose an attribute that reads like a field but runs code behind the scenes:

- **Read-only attributes:** define a getter with no setter.
- **Validation on write:** a `@x.setter` checks the value before storing it.
- **Computed values:** derive a value on access instead of storing it.

Because callers use `obj.x` either way, you can start with a plain attribute and switch to a property later **without changing any calling code**. That's why Python doesn't need Java-style `get_x()` / `set_x()` methods up front.

## When to use which

- **Plain public attribute:** no rules attached (e.g. `name` on a `User`).
- **`_internal` attribute + public methods:** state that must change through specific operations (e.g. `_balance` changed only via `deposit()` / `withdraw()`).
- **`@property` getter only:** callers need to read it but never set it directly.
- **`@property` + setter with validation:** callers may set it, but only to valid values.
- **`__mangled`:** rarely. Mainly to stop a subclass from accidentally overwriting a base-class attribute.

## Common mistakes

- **Using `__double_underscore` everywhere** because it "looks private". It makes debugging and testing harder and isn't real privacy. Prefer `_single`.
- **Writing a getter and setter for every field.** If the setter has no rule, it's a public attribute with extra steps.
- **Returning internal mutable state directly.** Returning `self._transactions` lets callers `.append()` to it. Return a copy or a `tuple`.
- **Validating in `__init__` but not in setters**, or the other way round. Route both through the same setter so the rule lives in one place.

## Interview angle

- Interviewers look for **private state + public behavior**: e.g. `ParkingSpot` exposes `assign_vehicle()` and `is_free`, not a writable `vehicle` field.
- Be ready to explain that Python privacy is by convention, and that name mangling exists mainly to avoid name clashes in subclasses.
- Say *why*: "I keep `_balance` internal so the no-negative-balance rule can't be bypassed."

## FastAPI connection

- Pydantic models validate data on the way in, which is encapsulation at the API boundary: invalid data never reaches your objects.
- `PrivateAttr` holds internal state that isn't part of the schema, and `@computed_field` exposes derived values in the response like a read-only `@property`.

## Self-check

- [ ] Can I explain the difference between `_x` and `__x`, and what `_ClassName__x` is?
- [ ] Can I write a read-only property and a validated property from memory?
- [ ] Can I explain why returning a mutable internal list breaks encapsulation?
- [ ] Can I name the invariant a class is protecting?
