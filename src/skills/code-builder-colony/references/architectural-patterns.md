---
name: architectural-patterns
description: >
  Read when structuring complete applications, setting up folder layouts, or defining service layers (Screaming/Hexagonal).
  Do not read for one-off scripts, configurations, or minor adjustments with no domain business logic.
---

# Architectural Patterns

Standards for layout, layering, and decoupling in our systems.

## Applicability

- **Apply When**: Developing complete services, domain modules, or applications that require explicit separation of concerns and clear logical layers.
- **Do Not Apply To**: One-off scripts, simple utility functions, configurations, or tasks with no domain business logic where introducing layers or suffix rules adds unnecessary boilerplate.


## 1. Screaming Architecture (Domain-Centric Structuring)

The directory structure and naming conventions must make the system's business domain and boundaries obvious.

### Layout Rules

- **Domain/Feature-Centric**: Group code by business domains (e.g. `user/`, `billing/`) rather than by technical layers (e.g. all controllers in one folder).

  ```text
  workspace/
  ├── user/
  │   ├── handler.py      (Entry Point / Presentation)
  │   ├── service.py      (Business Logic)
  │   └── repository.py   (Data Access / Persistence)
  ```

- **Avoid Deep Nesting**: Keep the domain directories flat (maximum 3-4 levels deep).
- **Avoid Tech-Polluted Names**: Name folders after pure business entities (e.g. `user/` instead of `user_db/`).

### Suffix Rules

Enforce class and file suffixes to indicate roles and data flow:

| Suffix | Purpose | Example |
| --- | --- | --- |
| `Handler` / `Controller` | First entry point accepting external requests (HTTP, CLI, events). | `UserHandler` |
| `Service` / `UseCase` | Handles core business rules and orchestration. | `BillingService` |
| `Repository` / `Dao` | Interface or implementation for accessing data stores. | `UserRepository` |
| `Dto` / `Request` / `Response` | Data containers for transferring info between layers. | `UserCreateDto` |
| `Client` / `Gateway` | Client for interacting with external APIs/systems. | `PaymentGateway` |

---

## 2. Layered Architecture

An architecture pattern that isolates responsibilities into horizontal layers.

### Standard 4-Layer Structure

1. **Presentation Layer**: Handles incoming requests, converts data types, returns responses (`Controller`, `Handler`, `DTO`).
2. **Business/Service Layer**: Orchestrates business workflows and maintains domain invariants (`Service`, `Domain Model`).
3. **Persistence Layer**: Abstract interface and implementation to query or save data (`Repository`, `DAO`).
4. **Database Layer**: The storage engine or external database systems.

*Rule: Dependency flow must point strictly downward (Presentation $\rightarrow$ Business $\rightarrow$ Persistence $\rightarrow$ Database).*

### Closed vs Open Layers

- **Closed Layer** (Recommended): A layer can only access its immediate next lower layer. Minimizes coupling.
- **Open Layer**: A layer can skip layers. Use sparingly, as it increases coupling.

---

## 3. Hexagonal Architecture (Ports and Adapters)

Decouples the core business logic from external infrastructures (databases, transport protocols, third-party libraries).

```text
               Outside (Infrastructure / Infrastructure Layer)
      ┌────────────────────────────────────────────────────────┐
      │   Primary Adapters (Driving: HTTP Controller, CLI)     │
      │                      │                                 │
      │                      ▼                                 │
      │               Inbound Ports (Driving Interfaces)       │
      │      ┌───────────────────────────────────────┐         │
      │      │            Inside (Core)              │         │
      │      │          Domain & Use Cases           │         │
      │      │            Outbound Ports             │         │
      │      └───────────────┬───────────────────────┘         │
      │                      │                                 │
      │                      ▼                                 │
      │   Secondary Adapters (Driven: DB Repositories, APIs)   │
      └────────────────────────────────────────────────────────┘
```

### Components

- **Core (Inside)**: Pure domain entities and Use Cases. Free of framework, database, and library dependencies.
- **Ports (Interface)**: Boundary definitions.
  - *Inbound Ports*: API/interfaces exposed by the Core for driving adapters.
  - *Outbound Ports*: SPI/interfaces defined by the Core for resources it needs to fetch (implemented by driven adapters).
- **Adapters (Outside)**: Concretions mapping to the outer world.
  - *Primary Adapters*: Call Inbound Ports (e.g. web controllers).
  - *Secondary Adapters*: Implement Outbound Ports (e.g. database repositories).

### Practical Guidelines

- **DIP**: All dependencies must point inward (Infrastructure $\rightarrow$ Ports/Core).
- **CRUD Warning**: Do not use Hexagonal Architecture for simple CRUD apps; it adds unnecessary boilerplate. Layered structure is preferred.
- **Separation**: Do not mix database entity decorators (e.g. JPA `@Entity`) with core domain objects. Keep database models and domain models separate, mapping between them at the adapter boundary.
