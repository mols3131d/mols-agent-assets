---
name: python-style-guide
description: >
  Read when writing/testing Python code, utilizing pytest fixtures/markers, mock time travel, or resolving common Python gotchas.
  Do not read for non-Python code, raw SQL files, static config files, or shell scripts.
---

# Python Style & Testing Guide

A consolidated guide to writing Pythonic, clean, and well-tested Python code.

## Applicability

- **Apply When**: Developing, modifying, or testing Python codebase files (modules, classes, methods, and pytest suites) where execution correctness, testability, and standard Pythonic structure are required.
- **Do Not Apply To**: Shell/bash scripts, SQL query scripts, configurations, or other languages where Python-specific idioms (like EAFP, wraps, or freezegun) are irrelevant.


## 1. Pythonic Code (Idioms & Features)

- **No Wildcard Imports**: Avoid `from module import *`. Explicitly import required names.
- **Limit List Comprehension Complexity**: Use regular `for` loops if a comprehension spans multiple lines or becomes hard to read.
- **EAFP (Easier to Ask for Forgiveness than Permission)**: Prefer `try/except` over checking existence beforehand (LBYL), unless performance dictates otherwise.

  ```python
  # EAFP Style
  try:
      with open(filepath) as f:
          content = f.read()
  except FileNotFoundError:
      content = None
  ```

- **Context Managers**: Always use `with` for resource cleanup (files, sockets, database transactions). Use `@contextlib.contextmanager` to create custom managers.
- **Generator vs List**: Use generator expressions `(x for x in data)` to process large/infinite datasets without loading the entire collection into memory.
- **Modern Type Hints (Python 3.10+)**: Use Union types via `|` instead of `typing.Union`.

  ```python
  def fetch_user(user_id: int) -> dict[str, str] | None:
      ...
  ```

- **typing.Protocol**: Use protocols to declare interfaces for duck-typing while maintaining static type validation.
- **Bare Exceptions Prohibited**: Do not write `except:` or `except Exception:` unless logging and re-raising, as it catches system-level exceptions (`KeyboardInterrupt`). Catch specific exceptions.
- **Exception Chaining**: Always use `raise ... from e` when wrapping low-level exceptions in domain exceptions to preserve the stack trace.
- **Decorators**: Always decorate wrapper functions inside custom decorators with `@functools.wraps(func)` to preserve original function metadata.
- **Asyncio Event Loop Blocking**: Never run blocking synchronous operations (e.g. `time.sleep()`, synchronous DB or HTTP calls) in an `async` function. Use `await asyncio.sleep()` or run synchronous functions in an executor via `run_in_executor`.

---

## 2. Common Python Gotchas

- **Mutable Default Arguments**: Never use mutable containers (e.g., `list`, `dict`) as default argument values in functions. Use `None` instead.

  ```python
  # Bad: def add_item(item, items=[]):
  # Good:
  def add_item(item, items=None):
      if items is None:
          items = []
      items.append(item)
      return items
  ```

- **Late Binding in Closures**: Variables captured inside lambdas/closures in a loop bind their values at invocation time, not definition time. Solve with default arguments.

  ```python
  # Good:
  multipliers = [lambda x, i=i: x * i for i in range(3)]
  ```

- **Class vs Instance Variables**: Variables declared inside the class body are shared across all instances. Initialize instance variables inside `__init__` using `self`.

---

## 3. Design Patterns in Python

- **Dict Maps over Factory/Registry**: Avoid bloated Factory patterns if a simple dictionary mapping suffices.

  ```python
  FORMATTERS = {"json": JsonFormatter, "csv": CsvFormatter}
  def get_formatter(name: str) -> Formatter:
      return FORMATTERS[name]()
  ```

- **Composition over Inheritance**: Combine object behavior rather than extending deep hierarchies. Any class inheritance depth > 2 is an architectural bug.
- **Constructor Injection**: Inject dependencies via the constructor rather than instantiating them internally. If constructor arguments exceed 5-7, split the class into smaller units.
- **Rule of Three**: Only abstract a pattern once you have at least three instances of duplication.

---

## 4. Testing Patterns (pytest)

### Test Directory Structure

```text
tests/
├── conftest.py           # Shared fixtures
├── test_unit/            # Unit tests (Isolated mocks)
│   ├── test_models.py
│   └── test_services.py
└── test_integration/     # Integration tests (DB, APIs)
    └── test_api.py
```

### Test Naming

Use `test_<unit>_<scenario>_<expected_outcome>`. Ensure names describe the target behavior:

```python
def test_create_user_with_duplicate_email_raises_conflict():
    ...
```

### Testing retry behavior

Use side-effects in mocks to test retry and error escalation limits.

```python
def test_gives_up_after_max_retries():
    client = Mock()
    client.request.side_effect = ConnectionError("Failed")
    service = ServiceWithRetry(client, max_retries=3)

    with pytest.raises(ConnectionError):
        service.fetch()
    assert client.request.call_count == 3
```

### Mocking Time (freezegun)

Control time using `@freeze_time` for predictable assertions.

```python
@freeze_time("2026-01-15 10:00:00")
def test_token_expiry():
    token = create_token(expires_in_seconds=3600)
    assert token.expires_at == datetime(2026, 1, 15, 11, 0, 0)
```

### Test Markers

Categorize tests using custom markers in `pytest.ini`:

```python
@pytest.mark.slow
def test_heavy_computation():
    ...
```

Run with `pytest -m "not slow"` or `pytest -m slow`.
