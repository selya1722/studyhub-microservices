# Duvindu's Guide - StudyHub Microservices

**Your role:** Senior developer. You own the backend features, security and DevOps tasks.
**Deadline:** 20 November (then presentation + viva). **Your issues:** #3, #4, #12, #13, #5 (stretch), #11.

---

## 1. The application in 2 minutes

**StudyHub** is a topic-based chat platform (rooms, messages, notifications, activity feed). You built the original Django version; we have now split it into **6 independent microservices**, each with its own database, behind one gateway. That is what the lecturer wants to see.

| Service | Port | What it does | File |
|---|---|---|---|
| api-gateway | 8000 | single entry point, routes `/api/...`, serves the web UI | `services/gateway/app.py` |
| user-service | 8001 | register, login (JWT), profiles | `services/user-service/app.py` |
| room-service | 8002 | rooms and topics | `services/room-service/app.py` |
| message-service | 8003 | messages in rooms | `services/message-service/app.py` |
| notification-service | 8004 | tells a room host when someone posts | `services/notification-service/app.py` |
| activity-service | 8005 | activity feed and stats | `services/activity-service/app.py` |

Key ideas (you will be asked about these in the viva):
- **Database per service** - no shared tables.
- **JWT auth** - user-service signs tokens, other services verify with the shared `JWT_SECRET`.
- **Service-to-service calls** - message-service calls room-service (must succeed) and notification/activity (best effort; if they are down the post still works).
- **Internal endpoints** use the `X-Internal-Key` header and are blocked at the gateway.

Full diagrams: `docs/architecture.md`.

---

## 2. One-time setup

1. Accept the GitHub invitation (email or https://github.com/tharinduk001/studyhub-microservices/invitations).
2. Install Git, Python 3.10+ and (optional) Docker Desktop.
3. In a terminal:
```bash
git clone https://github.com/tharinduk001/studyhub-microservices.git
cd studyhub-microservices
git checkout develop
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install fastapi uvicorn httpx pyjwt
python scripts/run_local.py     # starts all 6 services
```
4. Open http://localhost:8000 (UI). Swagger for each service: `http://localhost:8001/docs` ... `8005/docs`.
5. In a second terminal run `python scripts/smoke_test.py`. It should print `ALL TESTS PASSED`.

## 3. Workflow for every task

```bash
git checkout develop
git pull
git checkout -b feature/<branch-name-from-the-task>
# ... make changes, restart run_local.py, test ...
git add .
git commit -m "feat: short description"
git push -u origin feature/<branch-name-from-the-task>
```
Then on GitHub click **Compare & pull request**, set the base branch to **`develop`** (not main), write 2-3 lines of description, and mention the issue (`Closes #3`). Tharindu reviews and merges.
Rules: one branch per task, small commits, never push directly to `main` or `develop`.

---

## 4. Your tasks

### Task A - Message-service features (issue #3, branch `feature/message-service`)
File: `services/message-service/app.py`

1. **Edit a message** - add `PUT /messages/{message_id}`. Body: `{"body": "new text"}` (reuse the `Field(min_length=1)` style). Copy the logic of `delete_message`: 404 if missing, 403 if `row["user_id"]` is not the caller, otherwise `UPDATE messages SET body=? WHERE id=?` and return the updated row.
2. **Pagination** - in `list_messages` add `offset: int = 0` and change the query end to `ORDER BY id DESC LIMIT ? OFFSET ?`.
3. **Internal cleanup** - add `DELETE /messages?room_id=<id>` that removes all messages of a room and returns `{"deleted": n}`. Protect it with an `internal_only` dependency (copy it from `services/notification-service/app.py`, and add `INTERNAL_KEY` handling).
4. **Make it a real service interaction** - in `services/room-service/app.py` `delete_room`, after deleting the room call this endpoint with `httpx.delete(f"{MESSAGE_URL}/messages", params={"room_id": room_id}, headers={"X-Internal-Key": INTERNAL_KEY}, timeout=2)` inside a `try/except httpx.HTTPError`. Add `MESSAGE_URL` env var (default `http://127.0.0.1:8003`) and in `docker-compose.yml` (`MESSAGE_URL: http://message-service:8000` for room-service).
5. Extend `scripts/smoke_test.py` with checks for edit (200, and 403 for another user) and for pagination.

Done when: smoke test passes, and deleting a room leaves no messages for it.

### Task B - Notification-service features (issue #4, branch `feature/notification-service`)
File: `services/notification-service/app.py`
1. `POST /notifications/read-all` - marks all of the caller's notifications read (`UPDATE ... WHERE user_id=?`), returns `{"updated": n}`.
2. `GET /notifications/count` - returns `{"unread": n}` for the caller.
3. Add a smoke-test check.
4. Optional: show the unread count next to "Notifications" in `services/gateway/static/index.html`.

### Task C - Gateway hardening (issue #12, branch `feature/gateway-hardening`)
File: `services/gateway/app.py`
1. Add `pyjwt==2.10.1` to `services/gateway/requirements.txt`, read `JWT_SECRET` from env (same default as other services) and add `JWT_SECRET` to the gateway in `docker-compose.yml`.
2. Define which requests need a token: everything except `POST /api/auth/*`, and `GET` on rooms, topics, messages and activity. In `proxy()`, for protected requests decode the `Authorization` header and return `401` immediately if invalid (before forwarding).
3. **Rate limiting**: keep an in-memory dict `{ip: [timestamps]}`; allow 60 requests/minute per IP (`request.client.host`), otherwise return `429`.
4. Add smoke-test checks (bad token -> 401, 61 quick requests -> 429 -  run the rate-limit check last).

### Task D - CI pipeline (issue #13, branch `feature/ci`)
Create `.github/workflows/ci.yml`:
```yaml
name: CI
on: [pull_request]
jobs:
  smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install fastapi uvicorn httpx pyjwt
      - run: python scripts/run_local.py &
      - run: sleep 8 && python scripts/smoke_test.py
```
Push, open a PR, check the green tick. Add the badge to `README.md`.

### Task E (stretch) - Kubernetes (issue #5, branch `feature/kubernetes`)
Folder `k8s/`: one Deployment + Service per service (image built from `services/<name>`), env vars from `docker-compose.yml`, a NodePort/Ingress for the gateway, and a short "how to apply" section in the README.

### Task F - Demo (issue #11)
Rehearse and be ready to demo: stop one service (`docker compose stop notification-service`), post a message (still works), show `/health`. Explain the message flow diagram.

---

## 5. Suggested schedule
| Date | Goal |
|---|---|
| 12 Nov | Accept invite, setup works, smoke test passes |
| 14 Nov | PRs for Task A and B open |
| 16 Nov | Task C and D merged |
| 17-18 Nov | Kubernetes (if time), fix review comments |
| 19 Nov | Rehearsal |
| 20 Nov | Submission |

**Stuck?** Ask Tharindu in the group chat with the error text; don't wait more than an hour.
