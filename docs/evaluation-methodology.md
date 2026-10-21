# Evaluation methodology

## Verification gates

1. **Identity:** match project name to its official maintainer and repository.
2. **License:** inspect actual LICENSE files, dependencies, and commercial-use restrictions; do not infer open-source status from public source code.
3. **Maintenance:** inspect releases, commits, issue responses, and security advisories. No arbitrary activity threshold guarantees safety.
4. **Operational suitability:** assess documentation, authentication, audit logging, secure configuration, upgrades, observability, and backup/restore where applicable.
5. **Integration:** validate API, log format, webhook, and interoperability claims with official documentation.
6. **Risk:** review supply-chain provenance, security posture, attack surface, and required privileges.

## Enterprise readiness

- `not-assessed`: no systematic review (default).
- `experimental`: research-stage or insufficient operational evidence.
- `lab-ready`: validated in a controlled lab for documented use cases.
- `enterprise-candidate`: evidence supports further enterprise pilot evaluation; **not a certification**.

Only change readiness after documenting evidence, reviewer, date, version, deployment context, and limitations in the pull request. **Verified identity is not enterprise readiness.**

## Important caveats

ATT&CK mappings must be evidence-backed and version-aware. An empty mapping means not yet assessed, not no coverage. A composite stack can have distinct component licenses. Do not auto-promote a tool based on stars, commit recency, or popularity.
