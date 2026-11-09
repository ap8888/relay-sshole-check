# Validation — 2026-11-09

## Performed

- 25 synthetic offline unittest cases passed with macOS `/bin/sh`.
- The same 25 cases passed with `/bin/dash` (50 successful case executions).
- Both shells passed syntax validation through the suite.
- Fixtures covered missing evidence, shadow opt-in, exact-star versus locked markers, both relevant hash prefixes, other hash prefixes, malformed/empty records, unknown linkage, package inventory without false fixed-version verdicts, effective-report filtering, configuration counts, argument errors and target paths with spaces.
- Synthetic secret strings and account names were absent from assessment output.
- An executable fixture at the target sshd path was not run; shell syntax in os-release was not sourced.
- Fixture file contents were unchanged across collection. This is not kernel-level syscall tracing and does not claim to check access-time changes.
- Packaged files and archive contents were verified using SHA-256 checksums.
- Article HTML was generated from its Markdown body and checked for local link targets and required document structure; no browser visual review was performed.

## Not performed

No live Linux or Alpine host assessment; no BusyBox ash validation; no authentication attempts; no exploit execution; no packet capture; no dynamic syscall audit; no actual daemon configuration evaluation; no package update, service restart or production change. ShellCheck was not installed. Permission-denial behavior is documented but not separately exercised with an unprivileged Linux account. Independent security review remains pending.

Synthetic fixtures demonstrate collector behavior, not vulnerability presence or remediation effectiveness. Before wider distribution, validate on supported Linux/Alpine lab systems with different builds, privileges and directory configurations. Do not label this release independently audited or production-certified.
