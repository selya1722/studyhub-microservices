# Tharindu's Guide - Team Lead

**Your role:** Team lead and integrator: architecture, repo, reviews, testing, release and presentation.
**Deadline:** 20 November (then presentation + viva). **Your issues:** #1, #2, #11, plus the extra tasks below.
Repo: https://github.com/tharinduk001/studyhub-microservices

---

## 1. Project snapshot

**StudyHub** = topic-based chat platform split into 6 microservices (gateway, user, room, message, notification, activity), each with its own SQLite database, JWT auth, REST calls between services, Docker Compose to start everything. Details: `README.md`, `docs/architecture.md`.

Already done by you (v0.1 on `main`): architecture, all 6 services, web UI, Docker files, `scripts/run_local.py`, `scripts/smoke_test.py` (21 checks passing), git branches, 13 issues.

Not yet verified: **`docker compose up --build`** (Docker Desktop was not running during development).

## 2. Team split (who owns what)

| Member | GitHub | Main responsibility |
|---|---|---|
| Tharindu | tharinduk001 | integration, tests for user/room services, reviews, release, architecture presentation |
| Duvindu | duvindu-embuldeniya | message + notification features, gateway security, CI, Kubernetes |
| Amaya | selya1722 | diagram, Postman, UI polish, activity filter, report and slides |

Their detailed guides: `docs/guides/DUVINDU_GUIDE.md` and `docs/guides/AMAYA_GUIDE.md`.

## 3. Workflow (same for everyone)

```bash
git checkout develop && git pull
git checkout -b feature/<name>
# work, test, commit often
git push -u origin feature/<name>
# open a pull request into develop
```
`main` = stable only. `develop` = integration. One feature branch per task.

---

## 4. Your tasks

### Task 1 - Unit tests for user-service and room-service (issue #1, branch `feature/tests-core`)
Every service has the module name `app`, so run pytest **inside each service folder**.

1. `pip install pytest` (httpx is already installed; FastAPI's TestClient needs it).
2. Create `services/user-service/tests/test_users.py`:
```python
import os, tempfile
os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "users.db")  # set BEFORE importing app

from fastapi.testclient import TestClient
import app as user_app

client = TestClient(user_app.app)

def register(name="alice"):
    return client.post("/auth/register", json={"username": name, "email": "a@x.com", "password": "secret123"})

def test_register_and_duplicate():
    assert register("alice").status_code == 201
    assert register("alice").status_code == 409

def test_login():
    register("bob")
    assert client.post("/auth/login", json={"username": "bob", "password": "secret123"}).status_code == 200
    assert client.post("/auth/login", json={"username": "bob", "password": "wrong"}).status_code == 401

def test_me_requires_token():
    assert client.get("/users/me").status_code == 401
    token = register("carol").json()["token"]
    r = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert r.json()["username"] == "carol"
```
3. Run from the service folder: `cd services/user-service && python -m pytest tests -v`.
4. Do the same for `services/room-service/tests/test_rooms.py` (set `DB_PATH` to `rooms.db`). Create a JWT in the test with `jwt.encode({"sub": "1", "username": "alice"}, "dev-secret-change-me", algorithm="HS256")`. Test: create room (201), no token (401), list/search, update/delete by the host (ok) and by another user (403). To avoid the 2 s wait for activity-service, add `monkeypatch.setattr(room_app, "publish_event", lambda *a, **k: None)`.
5. Commit, push, open PR. Optional: Duvindu's CI (#13) can run these too.

### Task 2 - Review and integration (issue #2) - ongoing
For every pull request:
- [ ] Branch targets `develop`, small focused diff, clear title, mentions the issue (`Closes #N`).
- [ ] Pull the branch, run `python scripts/run_local.py` and `python scripts/smoke_test.py` - must say `ALL TESTS PASSED`.
- [ ] No secrets, `.env`, `venv/` or `*.db` files committed.
- [ ] Each service still only touches its own database.
- Leave at least one helpful comment, then merge (use "Create a merge commit" to keep history visible).
After Duvindu's issues are merged, make sure `docker-compose.yml` env vars match any new settings (`MESSAGE_URL`, `JWT_SECRET` for the gateway).

### Task 3 - Verify Docker (you, branch `feature/docker-verify`)
1. Start Docker Desktop, run `docker compose up --build`.
2. Open http://localhost:8000 and run `python scripts/smoke_test.py`.
3. Check `docker compose ps` shows 6 containers; `docker compose stop notification-service` -> posting still works; `docker compose start notification-service`.
4. Fix any problems (the likely ones: ports, env vars, Python wheel versions). Add a `.gitattributes` with `* text=auto eol=lf` so Dockerfiles keep LF line endings on Windows.

### Task 4 - Contribution tasks beyond the lead role
Pick at least two so your Git history shows more than setup:
- **Profile pictures or bio on the UI** - the profile endpoint exists (`PUT /api/users/me`); add a small "My profile" box in `services/gateway/static/index.html`.
- **Room edit/delete buttons in the UI** for the room host (`PUT/DELETE /api/rooms/{id}`).
- **Room member count**: message-service endpoint `GET /messages/stats?room_id=` returning distinct posters; show it in the room header.
- **`/api/activity/stats` panel** in the UI.
- **Structured logging**: add a request-ID header at the gateway and log it in each service (matches the log format in the original project).

### Task 5 - Release (end of project)
```bash
git checkout main && git pull
git merge --no-ff develop
git tag v1.0
git push origin main --tags
```
Do this on **18-19 Nov**, after all PRs are merged and the smoke test passes. Final check: fresh clone -> `docker compose up --build` works.

### Task 6 - Presentation and viva (issue #11)
You explain: architecture (database per service, gateway, JWT, sync vs best-effort calls), the Docker setup and the testing. Prepare answers to:
- Why microservices instead of the monolith? (independent deploy, fault isolation, team ownership)
- What happens if notification-service is down? (post still succeeds; only room-service is critical)
- How do services authenticate each other? (JWT for users, `X-Internal-Key` for internal calls)
- What would you improve? (message broker, PostgreSQL per service, Kubernetes, service discovery)

### Team coordination
- Once invites are accepted, assign issues: #3, #4, #5, #12, #13 to Duvindu; #6-#10 to Amaya; add them to #11.
- Check the Issues/PR list every day; ask each person for a status on 14 Nov and 17 Nov.
- Make sure each person's commits are under their own GitHub account (needed as contribution evidence).
- Evidence for the report: Insights -> Contributors screenshot, PR list, `git shortlog -sn --all`.

## 5. Schedule

| Date | Goal |
|---|---|
| 11-12 Nov | Teammates accepted and set up; issues assigned; Task 3 (Docker) done |
| 13-15 Nov | Task 1 tests; first PRs from Duvindu and Amaya reviewed |
| 16-17 Nov | All feature PRs merged; Task 4 contributions |
| 18 Nov | Release candidate, report draft ready |
| 19 Nov | Release `v1.0`, full rehearsal (everyone) |
| 20 Nov | Submission |
