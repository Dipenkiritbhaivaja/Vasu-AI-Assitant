# ADR-001: Core Project Architecture

**Status:** Accepted

**Date:** 2026-07-30

---

# Context

VASU AI ASSISTANT is intended to become a long-term software project.

The application will eventually include:

* Application Management
* File Management
* Browser Integration
* Voice Recognition
* AI Providers
* Memory System
* Automation Engine
* Plugins
* Windows Integration

Without a structured architecture, the project would become difficult to maintain as features increase.

---

# Decision

The project will follow a layered architecture.

```text
User
    │
    ▼
Console Interface
    │
    ▼
Command Manager
    │
    ▼
Command Parser
    │
    ▼
Command Handler
    │
    ▼
Manager
    │
    ▼
Service
    │
    ▼
Operating System
```

Every layer has a single responsibility.

---

# Responsibilities

## Interface

Responsible only for communication with the user.

No business logic.

---

## Command Layer

Responsible for:

* parsing commands
* routing commands
* validation

No operating system access.

---

## Managers

Responsible for business rules.

Managers coordinate services.

Managers never interact directly with the operating system.

---

## Services

Responsible for interacting with external systems.

Examples:

* Windows
* Browser
* File System
* Database

Services contain no business rules.

---

# Dependency Direction

Dependencies always move downward.

```text
Interface
    ↓
Command
    ↓
Manager
    ↓
Service
```

Reverse dependencies are prohibited.

Example:

ApplicationService must never call ApplicationManager.

---

# Design Principles

The architecture follows:

* Single Responsibility Principle
* Dependency Injection
* Low Coupling
* High Cohesion
* Separation of Concerns
* Clean Architecture concepts

---

# Alternatives Considered

## Option 1

Place all logic inside handlers.

Rejected because handlers would become very large and difficult to maintain.

---

## Option 2

Place operating system code inside managers.

Rejected because business logic would become tightly coupled to Windows-specific code.

---

## Option 3

Use a layered Manager → Service architecture.

Accepted.

This approach keeps business logic independent from operating system implementation.

---

# Consequences

## Positive

* Easy to extend.
* Easier to test.
* Easier to replace implementations.
* Better separation of responsibilities.
* Lower maintenance cost.

## Negative

* More classes.
* More files.
* Slightly more boilerplate.

These trade-offs are acceptable because long-term maintainability is prioritized over short-term simplicity.

---

# Future Impact

All future modules should follow this architecture.

Examples:

* Browser
* Files
* Memory
* Notifications
* Automation
* AI Providers
* Plugins

No future module should bypass the layered architecture without a documented architectural decision.

---

# Related Documents

* docs/ARCHITECTURE.md
* docs/CODE_GUIDELINES.md
* docs/PROJECT_PROGRESS.md
* docs/ROADMAP.md
