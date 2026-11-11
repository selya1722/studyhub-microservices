# Amaya's Guide - StudyHub Microservices

**Your role:** Documentation, API testing and the look of the web page, plus one small code change.
**Deadline:** 20 November (then presentation + viva). **Your issues:** #6, #7, #8, #9, #10, #11.
You do **not** need to be an expert. Every task below has steps; ask Tharindu whenever you are unsure.

---

## 1. What is the project? (read this first)

**StudyHub** is a chat website where people join **rooms** about a **topic** (for example "python"), write **messages**, and get **notifications**. There is also an **activity feed** showing what is happening.

The special part: instead of one big program (a "monolith"), the system is split into **small independent programs called microservices**. Each one does one job and has its own database:

| Service | Job | Port |
|---|---|---|
| api-gateway | the front door; all requests come here; also shows the web page | 8000 |
| user-service | sign up, log in, profile | 8001 |
| room-service | create and list rooms/topics | 8002 |
| message-service | write and read messages | 8003 |
| notification-service | tells the room owner when someone writes | 8004 |
| activity-service | the activity feed and statistics | 8005 |

Example: when Bob writes a message, message-service asks room-service "does this room exist?", saves the message, tells notification-service to alert the owner, and tells activity-service to record it.

Why microservices? If one service is broken (e.g. notifications), the others keep working. The marks are given for the idea **and** for showing this architecture clearly - that is where your tasks help most.

---

## 2. One-time setup

1. Accept the GitHub invitation (check your email or https://github.com/tharinduk001/studyhub-microservices/invitations).
2. Install: **Git**, **Python 3.10+**, **VS Code**, and **Postman**.
3. Open a terminal (PowerShell) and run:
```bash
git clone https://github.com/tharinduk001/studyhub-microservices.git
cd studyhub-microservices
git checkout develop
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn httpx pyjwt
python scripts/run_local.py
```
4. Open http://localhost:8000 in your browser. You should see the StudyHub page. Register, create a room, post a message - that is the app working.
5. Stop everything with `Ctrl+C`.

## 3. How to save your work (do this for each task)

```bash
git checkout develop
git pull
git checkout -b feature/<branch-name-given-in-the-task>
# ... do your work ...
git add .
git commit -m "docs: short description of what you did"
git push -u origin feature/<branch-name-given-in-the-task>
```
Then go to the repository on GitHub, click **Compare & pull request**, make sure the base branch is **`develop`**, and write one or two lines about what you did. Tharindu will review it. This is how your contribution is recorded - please always use your own branch and your own commits.

---

## 4. Your tasks (in this order)

### Task 1 - Architecture diagram (issue #6, branch `feature/diagram`) - easy
1. Open `docs/architecture.md`; it contains a diagram written in Mermaid.
2. Go to https://mermaid.live and paste the code from the ```mermaid block. You will see the diagram.
3. Or draw your own in https://app.diagrams.net (draw.io): boxes for the 6 services, 5 database cylinders, arrows as in the document. Use a different colour for the gateway.
4. Export as **PNG** and save it as `docs/architecture.png`.
5. In `README.md` add under the Architecture heading: `![Architecture](docs/architecture.png)`.
6. Commit and open a pull request.

### Task 2 - Postman collection (issue #7, branch `feature/postman`) - easy/medium
Goal: a file that lets anyone test every endpoint with clicks. The app must be running (`python scripts/run_local.py`).
1. In Postman create a **Collection** "StudyHub" and an **Environment** with variables `baseUrl = http://localhost:8000` and `token` (empty).
2. Add one request for each row below (use `{{baseUrl}}` in the URL). For requests marked "needs token", open the **Authorization** tab, choose *Bearer Token* and enter `{{token}}`. For POST/PUT, use *Body -> raw -> JSON*.

| Request | Method and URL | Body (example) | Token? |
|---|---|---|---|
| Register | POST `/api/auth/register` | `{"username":"amaya","email":"a@x.com","password":"secret123"}` | no |
| Login | POST `/api/auth/login` | `{"username":"amaya","password":"secret123"}` | no |
| My profile | GET `/api/users/me` | - | yes |
| Update profile | PUT `/api/users/me` | `{"bio":"Hello"}` | yes |
| List rooms | GET `/api/rooms` | - | no |
| Create room | POST `/api/rooms` | `{"name":"Python Help","topic":"python","description":"Ask here"}` | yes |
| Get room | GET `/api/rooms/1` | - | no |
| Topics | GET `/api/topics` | - | no |
| Post message | POST `/api/messages` | `{"room_id":1,"body":"Hello!"}` | yes |
| List messages | GET `/api/messages?room_id=1` | - | no |
| Notifications | GET `/api/notifications` | - | yes |
| Activity feed | GET `/api/activity` | - | no |
| Activity stats | GET `/api/activity/stats` | - | no |

3. To save the token automatically: in the **Register** and **Login** requests open the **Scripts** tab (Post-response) and paste:
```javascript
pm.environment.set("token", pm.response.json().token);
```
4. Run Register (or Login) first, then try the other requests. Take **screenshots** of a few successful responses (e.g. Create room 201, Post message 201) for the report.
5. Export the collection (`...` -> Export) to `docs/postman_collection.json`, commit, open a pull request.

### Task 3 - Make the web page look good (issue #8, branch `feature/frontend-polish`) - easy
File: `services/gateway/static/index.html`
1. Run the app and open http://localhost:8000.
2. In VS Code open the file. Everything between `<style>` and `</style>` at the top is the design (CSS). **Only change the CSS and the text/HTML** - do not touch the part under `<script>`.
3. Ideas: change colours (the header is `#3f51b5`), fonts, spacing, button hover colour, add a heading/logo text, nicer boxes. Save the file and press F5 in the browser to see the change.
4. Take a before/after screenshot for the report. Commit and open a pull request.

### Task 4 - Small code change: filter the activity feed (issue #9, branch `feature/activity-filter`) - guided
File: `services/activity-service/app.py`. Find the function `feed` near the bottom:
```python
@app.get("/activity")
def feed(limit: int = 20):
    with db() as c:
        return [dict(r) for r in c.execute("SELECT * FROM events ORDER BY id DESC LIMIT ?", (limit,))]
```
Replace it with:
```python
@app.get("/activity")
def feed(limit: int = 20, type: str | None = None):
    query, args = "SELECT * FROM events", []
    if type:
        query += " WHERE type=?"
        args.append(type)
    query += " ORDER BY id DESC LIMIT ?"
    args.append(limit)
    with db() as c:
        return [dict(r) for r in c.execute(query, args)]
```
Test: run the app, open http://localhost:8005/docs, click `GET /activity`, *Try it out*, enter `type = message_posted`, Execute. You should only see message events. Commit, open a pull request. (Ask Tharindu if the code looks scary - this is exactly what he is there for.)

### Task 5 - Report and slides (issue #10) - important for marks
Write in a shared document (Google Doc / Word). Suggested sections:
1. **Project idea** - what StudyHub is, who uses it, why it is useful.
2. **Business scenarios** - the table of 6 services from section 1 (which capability each service owns).
3. **Architecture** - your diagram and a short explanation of how services communicate.
4. **Technologies** - Python/FastAPI, SQLite (one DB per service), JWT, Docker, GitHub.
5. **Team contribution** - a table: member, services/tasks, what they built. Add GitHub evidence: screenshot of *Insights -> Contributors*, the list of pull requests and issues.
6. **Testing** - Postman screenshots and the smoke test output.
7. **Challenges and future work** - e.g. message queue, Kubernetes.
Slides (about 10): title, idea, scenarios, architecture diagram, demo, each member's contribution, testing, lessons learned.

### Task 6 - Demo rehearsal (issue #11)
Practise explaining the project idea and clicking through the UI: register, create room, post message. Know the name and job of each of the 6 services.

---

## 5. Suggested schedule
| Date | Goal |
|---|---|
| 12 Nov | Accept invite, app runs on your computer |
| 13 Nov | Task 1 (diagram) pull request |
| 14-15 Nov | Task 2 (Postman) pull request |
| 16 Nov | Tasks 3 and 4 pull requests |
| 17-19 Nov | Report and slides, rehearsal |
| 20 Nov | Submission |

**Stuck?** Copy the error message and send it to Tharindu - nobody expects you to solve everything alone.
