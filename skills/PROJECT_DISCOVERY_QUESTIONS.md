# Project Discovery Questions (Please Answer)

These answers will let us turn generic skills into project-specific standards.

## 1) Stack and Runtime

1. What primary implementation language(s) will be used (e.g., C++, Go, Rust, Python)?
2. Is GUI framework already chosen? If yes, which one?
3. Is TUI framework already chosen? If yes, which one?
4. Will this run as a local desktop app only, or also as a local/remote service?

## 2) Protocol and Networking Scope

5. For MVP TCP/UDP support, what exact use cases matter first (client mode, server mode, or both)?
6. Do you need TLS in MVP, or plain TCP/UDP only for now?
7. Do you need packet-level control (framing/chunking), or message-level simulation is enough?

## 3) Contracts and Task Model

8. How are `.h` files provided (single repo, imported folder, generated artifacts)?
9. Should task definitions be JSON, YAML, both, or another format?
10. Do tasks require versioning and backward-compatibility guarantees in MVP?

## 4) Capture/Replay and Verification

11. Should capture/replay be file-based only, or include live session management UI?
12. What verification depth is required first: count/order only, or full field-level assertions?
13. Do you need deterministic replay across different machines, or only same-machine repeatability?

## 5) Quality and Delivery Rules

14. What is your minimum target for automated testing in MVP (unit/integration/e2e expectations)?
15. What coding standard do you want enforced (style guide/linter set)?
16. Any strict constraints on third-party licenses (e.g., Apache/MIT only)?
17. What OS matrix is mandatory for MVP portability (Windows/macOS/Linux versions)?

## 6) Team and Workflow

18. How many developers are expected to contribute in parallel?
19. Do you prefer trunk-based development or feature-branch workflow?
20. Should we define a mandatory PR checklist with blockers (yes/no)?
