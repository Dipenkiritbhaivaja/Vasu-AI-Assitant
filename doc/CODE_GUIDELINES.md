# VASU AI ASSISTANT - Code Guidelines

## Purpose

This document defines the coding standards for the VASU AI ASSISTANT project.

Every new module, class, method, and feature should follow these guidelines to keep the codebase consistent, maintainable, and scalable.

---

# General Principles

* Write readable code before clever code.
* Keep classes focused on one responsibility.
* Keep methods short and easy to understand.
* Prefer composition over inheritance.
* Avoid duplicate code.
* Follow SOLID principles.
* Design for maintainability first.

---

# Project Structure

Every module should follow the existing architecture.

```text
Interface
    ↓
Command
    ↓
Manager
    ↓
Service
    ↓
Operating System
```

Higher layers may call lower layers.

Lower layers must never call higher layers.

---

# Naming Conventions

## Classes

Use PascalCase.

Examples:

* ApplicationManager
* BrowserService
* FileManager
* CommandParser

---

## Methods

Use snake_case.

Examples:

```python
find_application()

open_browser()

is_running()
```

---

## Variables

Use descriptive snake_case names.

Good:

```python
application_name

command_target

search_results
```

Avoid:

```python
x

tmp

obj
```

---

# Class Responsibilities

## Managers

Managers contain business logic.

Managers may:

* Validate input
* Resolve aliases
* Coordinate services
* Apply business rules

Managers must NOT:

* Print to console
* Access user interface
* Perform OS operations directly

---

## Services

Services communicate with external systems.

Services may:

* Launch applications
* Search files
* Open browsers
* Interact with Windows

Services should not contain business rules.

---

## Handlers

Handlers should remain lightweight.

Responsibilities:

* Validate commands
* Call managers
* Handle command flow

Handlers should not contain complex logic.

---

## Models

Models represent data only.

Models should not contain business logic.

---

# Logging

Always use LoggerManager.

Never configure logging directly inside modules.

Log important events.

Avoid excessive logging inside loops unless debugging.

---

# Exceptions

Never expose Python tracebacks to users.

Use project-specific exceptions.

ConsoleInterface is responsible for displaying user-friendly error messages.

Unexpected exceptions should be logged.

---

# Dependency Injection

Never create dependencies inside business logic if they can be injected.

Preferred:

```python
class ApplicationManager:

    def __init__(
        self,
        application_service,
    ):
        self._application_service = application_service
```

Avoid unnecessary object creation inside methods.

---

# Type Hints

Every public method should include type hints.

Example:

```python
def find(
    self,
    name: str,
) -> Application:
```

---

# Documentation

Every module should include:

* Module docstring
* Class docstring
* Public method docstrings

Complex algorithms should include explanatory comments.

Avoid commenting obvious code.

---

# Formatting

* Follow PEP 8.
* Keep line length consistent.
* Group imports logically.
* Use blank lines to improve readability.

---

# Testing

Every completed feature should be manually tested before committing.

Bug fixes should include regression testing to ensure existing functionality still works.

---

# Git Commits

Each commit should represent one logical change.

Good examples:

* feat(files): add recursive file search
* fix(applications): resolve calculator process detection
* refactor(commands): simplify command validation
* docs: add architecture documentation

Avoid combining unrelated changes in a single commit.

---

# Future Rule

When unsure between a quick solution and a maintainable solution, always choose the maintainable solution, even if it requires more work.
