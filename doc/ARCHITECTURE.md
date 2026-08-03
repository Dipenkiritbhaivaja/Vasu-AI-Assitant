# VASU AI ASSISTANT - Architecture

## Overview

VASU AI ASSISTANT is a modular, extensible desktop AI assistant written in Python.

The project follows Clean Architecture principles, SOLID principles, Dependency Injection, and Separation of Concerns.

The goal is to build an assistant that can grow from a lightweight offline assistant into a powerful AI-powered automation platform without requiring major architectural changes.

---

# High Level Architecture

```
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
Command Object
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

Each layer has exactly one responsibility.

---

# Layer Responsibilities

## Console Interface

Responsible for:

* Reading user input
* Displaying output
* Displaying errors
* Never contains business logic

---

## Command Manager

Responsible for:

* Parsing commands
* Selecting the correct handler
* Executing handlers

It should never directly interact with the operating system.

---

## Command Parser

Responsible for converting raw user input into a Command object.

Example:

```
open notepad
```

becomes

```
Command(
    action="open",
    target="notepad",
    arguments=[],
)
```

---

## Command Handlers

Responsible for implementing a single user action.

Examples:

* OpenApplicationHandler
* CloseApplicationHandler
* RestartApplicationHandler
* StatusApplicationHandler
* FindFileHandler

Handlers coordinate Managers and Services but should remain lightweight.

---

## Managers

Managers contain business logic.

Examples:

* ApplicationManager
* FileManager

Responsibilities include:

* Validation
* Alias resolution
* Searching registered objects
* Business rules

Managers never directly communicate with the operating system.

---

## Services

Services communicate with external systems.

Examples:

* ApplicationService
* BrowserService
* FileService

Responsibilities include:

* Launching applications
* Closing applications
* Opening browsers
* Searching the file system

Services should contain no business rules.

---

## Models

Models represent data structures used throughout the application.

Examples:

* Command
* Application
* FileInfo

Models should remain lightweight.

---

## Logging

Logging is centralized through LoggerManager.

Every module should use LoggerManager.

Direct logging configuration outside LoggerManager is not allowed.

---

# Dependency Flow

Allowed dependency direction:

```
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

Reverse dependencies are not allowed.

Example:

ApplicationService must never call ApplicationManager.

---

# Current Modules

* Core
* Commands
* Applications
* Browser
* Files
* Interfaces

---

# Design Principles

* Single Responsibility Principle
* Dependency Injection
* Clean Architecture
* Small reusable classes
* High cohesion
* Low coupling
* Modular design
* Easy testing
* Extensible architecture

---

This document should always describe the current architecture of the project.

Whenever a major architectural change is introduced, this document must be updated.
