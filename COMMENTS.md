# COMMENTS

## Implementation Notes

- The project follows hexagonal architecture to separate concerns between domain logic, infrastructure (adapters), and application (API).
- The domain models are isolated from FastAPI and Pydantic; request/response schemas are only used at the edges (API layer).
- Transitions between package statuses are validated strictly in the domain service layer.
- Concurrency is handled using `asyncio.Lock` inside the in-memory repository to avoid race conditions.
- All exceptions (validation, not found, business rules) are handled and logged with structured logging using Python’s logging module.
- The FastAPI app uses a lifespan context for preload logic instead of deprecated `@on_event("startup")`.

## Notifying External Systems

To replace the `NotificationStub`, the system can integrate with real external services by implementing a new adapter responsible for sending status change notifications.

The most common approach would be to create an **HTTP-based adapter** that sends POST requests to an external system's webhook when a package changes status. This adapter could use libraries like `httpx` or `aiohttp` to make non-blocking calls.

Other alternatives depending on the context:

- **Message Queue Integration**: Publish events (e.g., `PACKAGE_DELIVERED`) to a Kafka topic, RabbitMQ queue, or Amazon SNS topic for other systems to consume asynchronously.
- **Email/SMS Notification**: Trigger customer notifications through an external email API (like SendGrid or Mailgun) or SMS service (like Twilio).
- **Audit or Monitoring Hooks**: Send updates to a logging/observability system like Datadog, Sentry, or an internal metrics pipeline.

The adapter would be injected into the router and called asynchronously (e.g., via FastAPI `BackgroundTasks`) to avoid blocking the main request lifecycle. This ensures resilience and allows the core domain logic to remain unaffected by the notification mechanism.

Each of these strategies would respect the hexagonal architecture by keeping the notification logic outside the domain layer and behind a stable interface.


## Replacing In-Memory Storage

To replace the in-memory storage with a real database (e.g., PostgreSQL), I would:

- **Create a new adapter**, e.g. `SQLPackageRepository`, that implements the existing `PackageRepository` interface.
- **Use an async-compatible ORM**, such as **SQLAlchemy (with async support)**, or a direct driver like `asyncpg`.
- **Implement the required async methods**:
  - `get_by_id(package_id: str)` → fetch a row by primary key.
  - `save(package: Package)` → insert or update package.
  - `list_all()` → return all rows as `Package` instances.
- **Inject `SQLPackageRepository` into the application** in place of the current in-memory one. Since use cases depend on the interface (not the implementation), no change is needed in domain or API layers.

This approach preserves the architecture and ensures that infrastructure changes remain isolated.

Example scenarios:

- Using **SQLAlchemy ORM** with an `async_session`, define a `PackageModel` table and map it to the domain entity via `.from_orm()` or manual conversion.
- Alternatively, use **raw SQL with asyncpg** for more control/performance (e.g., in high-load systems).

This swap would allow the application to persist data across restarts and integrate with production-grade storage.
