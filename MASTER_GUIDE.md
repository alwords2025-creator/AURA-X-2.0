# AURA-X 2.0 Core — Master Integration Guide

## What this delivery contains
Ten separate runnable Python/FastAPI starter services. They demonstrate service boundaries and basic request/response flows. They are **not yet one connected, production-ready AI platform**. No real multi-LLM orchestration, API-key pool, production authentication, hosted database, external web search, image/video rendering, or cloud synchronization is preconfigured.

## Packages
1. Admin Control Center
2. Agent Orchestrator
3. Knowledge Store & RAG starter
4. Research & Source Agent
5. Data Pipeline & Analytics
6. Engineering Build & Test
7. Video/Image/Audio workflow planner
8. Offline/Online Sync Queue
9. Monitoring & Admin Alerts
10. Academic & STEM Solver Gateway

## Recommended setup order
1. Start each service locally and verify `/health` and `/docs`.
2. Keep all services bound to `127.0.0.1` during initial testing.
3. Add shared authentication and role-based access control.
4. Define service contracts, task IDs, idempotency keys, timeouts, retry limits and audit events.
5. Add one authorized model provider connector; validate usage and limits.
6. Add additional providers only through their official API/terms, one at a time.
7. Add tests, secret management, backups, retention controls and alert routing.
8. Deploy to cloud only after security review. Use separate environment variables for each deployment.

## Hybrid operation
- Offline PC: local database, local files, locally installed tools/models; internet-dependent services are unavailable.
- Online portal: authenticated remote access and cloud services.
- Sync: use authenticated, encrypted transfers, conflict detection and explicit rules for sensitive data.
- Do not sync secrets, passwords, raw API keys or private files by default.

## Free-first rule
Free tiers have limits and can change. They do not guarantee unlimited RAM, storage, execution time, API calls or 24/7 availability. Never create duplicate accounts to evade provider limits. Do not enable paid plans without explicit approval.

## Admin authority
Admin control should be implemented with strong authentication, recovery procedures, role-based access, audit logs and secure key rotation. Avoid a hidden master password or hard-coded credentials.

## Safe media and research
Use content you own, public-domain works, or appropriately licensed material. Do not bypass DRM or access restrictions. Respect source terms, robots policies where applicable, privacy, and provider rules.

## Before production
This starter set is not production-ready. Required work includes automated tests, security review, authentication, rate limiting, request validation, structured logs, encrypted transport, database migration/backup, dependency pinning, monitoring, incident response and deployment-specific checks.


## Added: Mobile Voice Workspace
See `11-mobile-voice-workspace/README.md`. This responsive browser UI adds voice typing, TTS playback, file selection/local downloads, camera/photo/video capture, experimental QR scanning, and a chat/messenger placeholder. It is a UI starter and must be connected to a compatible API and cloud storage before real tasks or cloud uploads work.
