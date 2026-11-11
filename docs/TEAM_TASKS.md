# Team Task Plan

Deadline: **20 November** (presentation + viva afterwards). Everyone works on their own `feature/*` branch and opens a pull request into `develop`. Commit often so GitHub shows each person's contribution. Tasks are tracked as GitHub issues (labels: `tharindu`, `duvindu`, `amaya`).

| Member | GitHub | Role |
|---|---|---|
| Tharindu Kalhara | tharinduk001 | Team lead: architecture, repo, integration, review |
| Duvindu Embuldeniya | duvindu-embuldeniya | Senior developer: backend features, security, DevOps |
| Amaya Jayasekara | selya1722 | Documentation, API testing, UI and a small backend change |

## Tharindu (lead)
- [x] Architecture, repo, gateway, user-service, room-service, docker-compose (branch `feature/core-services`)
- [ ] #1 Unit tests for user-service and room-service (`feature/tests-core`)
- [ ] #2 Review all pull requests, keep `develop` green, merge to `main` and tag `v1.0`
- [ ] #11 Rehearse demo; present architecture, gateway and service communication

## Duvindu (experienced, most technical work)
- [ ] #3 Message-service: edit message, pagination, internal room cleanup (`feature/message-service`)
- [ ] #4 Notification-service: mark all read + unread count (`feature/notification-service`)
- [ ] #12 Gateway: JWT validation and rate limiting (`feature/gateway-hardening`)
- [ ] #13 CI: GitHub Actions running the smoke test (`feature/ci`)
- [ ] #5 Kubernetes manifests, stretch goal (`feature/kubernetes`)
- [ ] #11 Rehearse demo; present message flow, resilience demo (stop a service), CI/Kubernetes

## Amaya (guided, well-scoped tasks)
- [ ] #6 Final architecture diagram (`feature/diagram`)
- [ ] #7 Postman collection for all endpoints (`feature/postman`)
- [ ] #8 Polish the web UI, HTML/CSS only (`feature/frontend-polish`)
- [ ] #9 Activity-service: filter feed by event type, one small change (`feature/activity-filter`)
- [ ] #10 Report and slides: project idea, scenarios, team contributions
- [ ] #11 Rehearse demo; present the project idea and the UI walk-through

## Shared before submission
- [ ] Everyone can run `docker compose up --build` on their own machine
- [ ] `python scripts/smoke_test.py` passes
- [ ] Rehearse the demo twice; each person explains the parts they built
- [ ] Tag the final commit on `main` (`v1.0`)

## Evidence of contribution
GitHub Insights -> Contributors, the pull request list, issues assigned per person, and `git shortlog -sn` output in the report.
