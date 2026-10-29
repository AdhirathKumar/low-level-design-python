# LLD Roadmap 2026 — Python Edition

> A Python version of the [general roadmap](00-Roadmap.md), which stays the source of truth. Topics, order and durations are the same. Each item adds the Python features and idioms to focus on. Where a topic shows up in everyday FastAPI work, a **FastAPI** note connects it to code you already write.

Total duration: **10 weeks** (fast track: **5 weeks**) · Total topics: **58**

| Phase | Focus | Duration | Fast track | Topics |
|-------|-------|----------|------------|--------|
| 1 | OOP Fundamentals | 1 week | 0.5 week | 6 |
| 2 | Design Patterns | 3 weeks | 1.5 weeks | 23 |
| 3 | Supporting Data Structures | 1 week | 0 weeks | 6 |
| 4 | LLD Problems | 5 weeks | 3 weeks | 23 |

> The fast-track numbers were handwritten by the speaker at the end of the video. They likely mean a compressed plan, with Phase 3 skipped if you already know DSA.

## Python toolkit for LLD

These come up in almost every topic below, so get comfortable with them first:

- **Type hints**: `typing` (`Optional`, `Protocol`, `Generic`, `TypeVar`). Interviewers read them as your interface contracts.
- **`dataclasses`**: `@dataclass`, `field(default_factory=...)`, `frozen=True` for value objects.
- **`enum.Enum`**: statuses, vehicle types, directions, and so on.
- **`abc`**: `ABC` and `@abstractmethod` for interfaces.
- **Concurrency**: `threading.Lock` / `RLock`, `queue.Queue`, `concurrent.futures`. Know what the GIL does and doesn't protect you from.
- **Project layout**: one module per concern, a `main.py` driver, `pytest` for quick checks. Machine coding rounds expect runnable code.

> **FastAPI in interviews:** use FastAPI to *recognize* patterns, not to *answer* LLD rounds. Those rounds expect in-memory, plain Python (classes, a `main.py` driver, tests), not routes and a database.

## Phase 1: OOP Fundamentals (1 Week)

6 topics.

### Week 1 — Core OOPs Concepts

- [ ] Encapsulation: `_protected` / `__private` naming conventions (name mangling), `@property` getters and setters · *FastAPI:* Pydantic `PrivateAttr` and `@computed_field`
- [ ] Abstraction: `abc.ABC` with `@abstractmethod`, or `typing.Protocol` for structural interfaces · *FastAPI:* a repository interface that routes depend on instead of the database directly
- [ ] Inheritance: `super()`, multiple inheritance and the MRO (`Class.__mro__`), mixins · *FastAPI:* Pydantic schema inheritance (`UserBase` → `UserCreate` / `UserRead`)
- [ ] Classes & Objects: instance vs class attributes, `@classmethod` / `@staticmethod`, dunder methods (`__repr__`, `__eq__`, `__hash__`), `@dataclass` · *FastAPI:* when to use a Pydantic `BaseModel` (validation at the edges) vs a `@dataclass` (domain objects)
- [ ] Constructors & Access Modifiers: `__init__` vs `__new__`, alternative constructors with `@classmethod`. Python has no real access modifiers, only naming conventions.
- [ ] SOLID Principles: apply them with ABCs/Protocols and duck typing. Dependency injection goes through `__init__` arguments. · *FastAPI:* `Depends()` is dependency injection (the D in SOLID), and thin routes that call service classes follow single responsibility (the S).

## Phase 2: Design Patterns (3 Weeks)

23 topics.

> Python's first-class functions, modules and dynamic typing make some classic GoF patterns much smaller. Learn the textbook class-based version for interviews, and also the Pythonic shortcut.

### Week 2 — Creational Patterns

- [ ] Singleton (Logger, DB Pool, Config) ⭐⭐: a module-level instance is the Pythonic singleton. Also know the `__new__` override, the metaclass approach, and thread-safe lazy init with a `Lock`. · *FastAPI:* `@lru_cache` on `get_settings()` with pydantic-settings, and a DB engine created once at startup
- [ ] Factory Method (Frameworks, APIs) ⭐⭐: a registry `dict` mapping names to classes or callables, or `@classmethod` factories · *FastAPI:* a dependency function that returns a different implementation based on config
- [ ] Abstract Factory (UI Toolkits) ⭐: ABC factory interfaces with concrete factory classes
- [ ] Builder ⭐⭐: fluent methods that `return self`. Keyword arguments and `@dataclass` defaults often replace it, so be ready to say when a builder is still worth it. · *FastAPI:* SQLAlchemy's `select(...).where(...).order_by(...)` is a fluent builder
- [ ] Prototype (Object cloning): `copy.copy` vs `copy.deepcopy`, custom `__copy__` / `__deepcopy__`

### Week 3 — Structural Patterns

- [ ] Adapter (Payment gateway wrappers) ⭐: wrap a third-party client behind your own ABC · *FastAPI:* wrapping an external API's `httpx` client so routes never see its quirks
- [ ] Facade (AWS SDK, service layers) ⭐⭐: a single service class or module that hides subsystems (think `boto3` behind a small API) · *FastAPI:* the service layer your routes call
- [ ] Decorator (Java I/O, middleware) ⭐⭐: the GoF object wrapper vs Python's `@decorator` syntax. Know both, and know how they differ. Use `functools.wraps`. · *FastAPI:* `@app.get(...)` uses Python's decorator syntax but registers a route rather than wrapping it. Middleware is the closer match to the GoF pattern.
- [ ] Proxy (Caching, lazy loading) ⭐⭐: delegate with `__getattr__`, cache with `functools.lru_cache` / `cached_property`
- [ ] Composite (File systems, UI trees) ⭐: a shared ABC for leaf and container, plus recursive `__iter__` · *FastAPI:* `APIRouter`s nested with `include_router`
- [ ] Bridge (Device + remote abstraction): pass the implementation into the abstraction through composition
- [ ] Flyweight (Game sprites, glyph rendering): `__slots__` to cut per-object memory, shared instances via a factory `dict`, `sys.intern`

### Week 4 — Behavioral Patterns

- [ ] Observer (Kafka consumers, pub/sub) ⭐⭐: subscriber lists of callables, `weakref` to avoid leaks · *FastAPI:* `BackgroundTasks`, and startup/shutdown hooks in `lifespan`
- [ ] Strategy (Payment modes) ⭐⭐: pass functions or Protocol-typed objects, and swap them at runtime · *FastAPI:* `app.dependency_overrides` in tests swaps one implementation for another
- [ ] Command (Undo/redo, queued tasks) ⭐: command objects with `execute()` / `undo()`, `functools.partial` for simple cases, undo/redo stacks as lists
- [ ] State (Vending machine, order FSM) ⭐⭐: state classes plus an `Enum` for states, or a transition-table `dict` · *FastAPI:* rejecting invalid status changes (e.g. `PATCH /orders/{id}`) with a `409`
- [ ] Iterator (Custom collections) ⭐: `__iter__` / `__next__`, generators and `yield`, `itertools` · *FastAPI:* `StreamingResponse` from a generator, and `yield` dependencies for setup/teardown
- [ ] Template Method (Frameworks, hooks): a base class with an ABC skeleton method and overridable hook methods
- [ ] Chain of Responsibility (Middleware, auth): linked handlers, or a list of callables processed in order · *FastAPI:* the middleware stack, and chained `Depends()` for auth (token → user → permission check)
- [ ] Mediator (Chat rooms, air traffic): a central object that components hold a reference to
- [ ] Visitor (AST traversal, compilers): `functools.singledispatch` / `singledispatchmethod` instead of double dispatch, and `ast.NodeVisitor`
- [ ] Memento (Snapshots, save states): `copy.deepcopy`, or a frozen `@dataclass` snapshot
- [ ] Interpreter (SQL parsers, regex): small expression-tree classes, the `ast` module, the `re` module

## Phase 3: Supporting Data Structures (1 Week)

6 topics.

### Week 5 — Data Structures for LLD

- [ ] HashMap / HashSet: `dict`, `set`, `collections.defaultdict`, `Counter`. Implement `__hash__` and `__eq__` together on custom keys.
- [ ] Doubly LinkedList: build a node class with `__slots__`. Know that `collections.OrderedDict` is backed by one, which is why `move_to_end` is O(1).
- [ ] Priority Queue / Heap: `heapq` (min-heap only, so negate values for a max-heap, and use tuples or `@dataclass(order=True)` for ordering). Use `queue.PriorityQueue` when you need thread safety.
- [ ] Stack & Queue: `list` for stacks, `collections.deque` for queues (not `list.pop(0)`), `queue.Queue` across threads · *FastAPI:* `asyncio.Queue` inside `async` code
- [ ] Trie: nested `dict`s, or a node class with `children: dict[str, Node]`
- [ ] Mutex / Locks: `threading.Lock`, `RLock`, `Condition`, `Semaphore`, using `with lock:`. The GIL does **not** make compound operations atomic. · *FastAPI:* plain `def` endpoints run in a thread pool, so they need `threading.Lock`. `async def` endpoints share the event loop and need `asyncio.Lock` around any `await` in a critical section.

## Phase 4: LLD Problems (5 Weeks)

23 topics.

> For each problem, aim for: `Enum`s for types and states, `@dataclass` entities, ABC/Protocol interfaces, a service/manager class, a `main.py` demo, and a few `pytest` cases.

### Week 6 — Easy Problems

- [ ] Parking Lot ⭐⭐: `Enum` for spot and vehicle types, Strategy for spot allocation and pricing, a `Lock` around spot assignment
- [ ] Vending Machine ⭐⭐: the State pattern with an `Enum` plus state classes
- [ ] Library Management ⭐: `@dataclass` for Book, Member and Loan, `datetime` for due dates and fines
- [ ] Elevator System ⭐⭐: Strategy for scheduling, `heapq` for request queues, optionally `threading` per elevator
- [ ] ATM: State pattern, Chain of Responsibility for dispensing notes
- [ ] Hotel Booking: date-range overlap checks with `datetime.date`, a `Lock` to prevent double booking

### Weeks 7–8 — Intermediate Problems

- [ ] Chess / Snake & Ladder ⭐⭐: a piece class hierarchy with move-validation polymorphism, `random` for dice (seeded for tests)
- [ ] Splitwise / Expense Sharing ⭐⭐: Strategy for split types, `decimal.Decimal` for money (never `float`), balance simplification with heaps
- [ ] Ride Sharing (Uber) ⭐⭐: Strategy for matching and pricing, Observer for trip updates — *Note: can be asked in both LLD and HLD rounds*
- [ ] Movie Ticket Booking ⭐⭐: seat locking with `threading.Lock` and timeouts, `Enum` for seat status
- [ ] PhoneBook ⭐⭐: a Trie for prefix search, `dict` indexes for lookup
- [ ] Food Delivery (Swiggy) ⭐: an order State machine, Observer for notifications
- [ ] E-commerce Cart: `decimal.Decimal` pricing, Strategy for discounts and coupons
- [ ] Notification System: Observer plus Strategy per channel (email, SMS, push), `queue.Queue` for async dispatch · *FastAPI:* sending via `BackgroundTasks` after the response
- [ ] Cache System (LRU) ⭐: `OrderedDict` with `move_to_end` / `popitem(last=False)`. Also be able to hand-build it with a `dict` plus a doubly linked list. Know `functools.lru_cache`.

### Weeks 9–10 — Advanced Problems

- [ ] Logging Framework ⭐⭐: Singleton logger, Chain of Responsibility for levels, Strategy for sinks. Compare your design with the stdlib `logging` module (handlers, formatters, filters). · *FastAPI:* request-logging middleware with a request ID in each log line
- [ ] Rate Limiter ⭐⭐: token bucket and sliding window using `time.monotonic()`, `collections.deque` of timestamps, a `Lock` for thread safety · *FastAPI:* applied as middleware or a dependency that returns `429 Too Many Requests`
- [ ] Payment Gateway ⭐⭐: Adapter per provider, a State machine for transactions, idempotency keys, `decimal.Decimal` · *FastAPI:* reading an `Idempotency-Key` header so a retried request doesn't charge twice
- [ ] Search Autocomplete ⭐: a Trie with top-k results per node via `heapq`
- [ ] File System: the Composite pattern for files and directories, path parsing with `str.split("/")`
- [ ] Job Scheduler: `heapq` keyed by run time, worker threads via `concurrent.futures.ThreadPoolExecutor`, `threading.Event` for shutdown · *FastAPI:* starting and stopping the worker in `lifespan`
- [ ] Event Sourcing Model: an append-only event list of frozen `@dataclass`es, state rebuilt by replay, Memento for snapshots
- [ ] Pub-Sub Engine: Observer with topic → subscribers `dict`, `queue.Queue` per subscriber, or `asyncio.Queue` for an async version · *FastAPI:* pushing published messages to clients over WebSockets
