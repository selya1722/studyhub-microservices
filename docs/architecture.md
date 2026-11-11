# Architecture

## Scenario to service mapping (Lab 01, Part A)

| Business scenario | Owning microservice | Port |
|---|---|---|
| User registers / logs in / edits profile | user-service | 8001 |
| User creates and browses rooms and topics | room-service | 8002 |
| User posts messages in a room | message-service | 8003 |
| Room host is notified of new messages | notification-service | 8004 |
| Users see platform activity and stats | activity-service | 8005 |
| Clients reach everything through one door | api-gateway | 8000 |

## Diagram

```mermaid
flowchart TD
    Client[Browser / Swagger / Postman] --> GW[api-gateway :8000]
    GW --> US[user-service :8001]
    GW --> RS[room-service :8002]
    GW --> MS[message-service :8003]
    GW --> NS[notification-service :8004]
    GW --> AS[activity-service :8005]
    MS -- validate room (sync) --> RS
    MS -- notify host (async-ish) --> NS
    MS -- event --> AS
    RS -- event --> AS
    US --- UDB[(users.db)]
    RS --- RDB[(rooms.db)]
    MS --- MDB[(messages.db)]
    NS --- NDB[(notifications.db)]
    AS --- ADB[(activity.db)]
```

## Sequence: posting a message

```mermaid
sequenceDiagram
    participant C as Client
    participant G as Gateway
    participant M as message-service
    participant R as room-service
    participant N as notification-service
    participant A as activity-service
    C->>G: POST /api/messages (JWT)
    G->>M: forward
    M->>R: GET /rooms/{id}
    R-->>M: room (host_id, name)
    M->>M: save message
    M-)N: POST /notifications (host)
    M-)A: POST /events
    M-->>C: 201 Created
```

## Design decisions (for the viva)
- **Database per service**: no shared tables and no cross-service foreign keys. Services store `user_id` / `host_name` copies instead of joining; this is what the monolith's `ForeignKey(User)` had to be replaced with.
- **API gateway**: one public entry point; services are not exposed to the host in Docker Compose.
- **Stateless JWT auth**: no session sharing between services.
- **Graceful degradation**: only the room lookup is critical for posting; notifications and activity are best-effort.
- **Health endpoints**: every service has `/health`; gateway aggregates them.
- **Containerisation**: one Dockerfile per service, one `docker-compose.yml` for the system.

## Possible improvements (stretch goals)
- Replace the best-effort HTTP calls with a message broker (RabbitMQ / Redis streams).
- PostgreSQL per service instead of SQLite.
- Kubernetes manifests (the original project name hinted at K8S).
- Rate limiting and JWT validation in the gateway.
