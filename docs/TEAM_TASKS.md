# Team Task Plan

Deadline: **20 November** (presentation + viva afterwards). Everyone works on their own `feature/*` branch and opens a pull request into `develop`. Commit often so GitHub shows each person's contribution.

Names are placeholders: replace `Member 1/2/3` with real names.

## Member 1 (lead, technical)
- [x] Architecture, repo, gateway, user-service, room-service, docker-compose (initial version, branch `feature/core-services`)
- [ ] Add unit tests for user-service and room-service (`feature/tests-core`)
- [ ] Review all pull requests, keep `develop` green, merge to `main` before submission
- [ ] Present: architecture, gateway, service communication, Docker

## Member 2 (technical)
- [ ] `feature/message-service`: understand `services/message-service/app.py`, then add: edit message (`PUT /messages/{id}`), pagination (`offset`), delete all messages of a room (`DELETE /messages?room_id=`, internal)
- [ ] `feature/notification-service`: add "mark all as read", unread count endpoint (`GET /notifications/count`)
- [ ] `feature/kubernetes` (stretch): write Deployment + Service YAML for each service
- [ ] Present: message flow, notifications, resilience demo (stop a service)

## Member 3 (less technical, well-scoped tasks)
- [ ] `docs/diagram`: draw the final architecture diagram (draw.io / Mermaid) for the report and slides
- [ ] `feature/postman`: build a Postman collection with one request per endpoint, export to `docs/postman_collection.json`; screenshots for the report
- [ ] `feature/frontend-polish`: improve `services/gateway/static/index.html` (colours, layout, empty states, logo), HTML/CSS only
- [ ] `feature/activity-service`: small change: add `GET /activity?type=message_posted` filter (guided by Member 1)
- [ ] Write the report sections: project idea, business scenarios, team contributions; and the slides
- [ ] Present: project idea, live demo walk-through of the UI

## Shared before submission
- [ ] Everyone can run `docker compose up --build` on their own machine
- [ ] `python scripts/smoke_test.py` passes
- [ ] Rehearse the demo twice; each person explains the parts they built
- [ ] Tag the final commit on `main` (`v1.0`)

## Evidence of contribution
GitHub Insights -> Contributors, the pull request list, issues assigned per person, and `git shortlog -sn` output in the report.
