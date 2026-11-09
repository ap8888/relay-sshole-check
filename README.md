# RELAY SSHole Check v0.1.0

Passive local evidence collection for CVE-2026-123158, prepared for **RELAY / n0hup.nl**. A POSIX shell assessment aid, not an exploit, remote scanner or vulnerability certification engine.

## Run

```sh
sh bin/relay-sshole-check
sh bin/relay-sshole-check --shadow
sh bin/relay-sshole-check --root /absolute/trusted/snapshot --shadow
sh bin/relay-sshole-check --effective /absolute/private/sshd-T.txt
```

No installation or dependencies beyond a POSIX shell, `awk` and `cat`. Shadow inspection is opt-in and requires existing read permission. Start without elevated privileges; the tool never invokes sudo. Use only trusted system files or a trusted snapshot. `--root` is a path prefix, not a chroot or hostile-image sandbox; symlinks can lead outside it. It never executes programs from the snapshot. Alternate daemon/config paths are not automatically discovered.

Reports go to standard output. The CLI creates no files and performs no requested writes to the target. Ordinary reads may update filesystem access times, and the environment may audit execution; “read-only” does not promise zero OS bookkeeping. Shell tracing is unsuitable for sensitive assessment runs. No telemetry, credential requests, authentication attempts, NSS queries, service operations, package operations or network calls are implemented.

## Results and automation

| Exit | Meaning |
|---|---|
| 0 | Help/version only |
| 1 | REVIEW_REQUIRED — incomplete evidence |
| 2 | PRIORITY_REVIEW — musl loader plus local exact-star and SHA-256/512 fields coexist |
| 64 | Invalid arguments/input path |
| 70 | Evidence processing failed |

There is deliberately no “safe” exit code. Exit 2 does not prove exposure: the binary may be fixed, unrelated, inactive, use another libc/PAM path, or deny relevant logins. Exit 1 does not reduce urgency by itself. A supplied password-disabled report does not suppress the conservative priority flag.

Example automation that preserves the result:

```sh
rc=0
sh bin/relay-sshole-check --shadow || rc=$?
printf 'Assessment exit: %s\n' "$rc"
```

Output is line-oriented `key=value` text. Repeated `apk_package` keys are expected. Missing/unreadable evidence stays unknown. Package revisions are inventory only: v0.1.0 does **not** perform a fixed-version comparison. Static configuration counts are not effective settings. A supplied report is not authenticated, freshness-checked or associated automatically with the inspected filesystem.

## Files

```text
bin/relay-sshole-check         passive POSIX CLI
tests/test_cli.py              synthetic offline tests (Python 3)
articles/sshole-en.md          finished English article, metadata and source links
articles/sshole-en.html        standalone English publication page
articles/sshole-ru.md          complete Russian translation
articles/sshole-ru.html        standalone Russian publication page
docs/QUICKSTART.md             English operator introduction
docs/REMEDIATION.md            manual patch/mitigation workflow
docs/SOURCES.md               verified claims and source caveats
docs/VALIDATION.md             performed checks and outstanding validation
SECURITY.md                   safety boundaries and reporting
CHANGELOG.md                  release history
LICENSE                       MIT
SHA256SUMS                     release file checksums
```

## Limits that matter

- A musl loader's presence does not prove sshd linkage. No binary execution or `ldd` is used.
- Only conventional `/usr/sbin/sshd`, `/etc/ssh/sshd_config`, `/etc/os-release`, `/lib/ld-musl-*.so.1`, `/lib/apk/db/installed` and optional `/etc/shadow` are examined beneath the selected root.
- Includes and Match blocks are counted, not expanded/evaluated. Use the manual workflow for effective configuration.
- Shadow parsing produces counts only, with minimal structural validation. It neither proves valid hashes nor determines account login eligibility. Directory accounts are outside coverage. No candidate usernames are emitted.
- No daemon/process, network reachability, exploitability or compromise determination is made.
- A live filesystem may change during collection. A consistent trusted snapshot is preferable for reproducible offline work, but does not establish current runtime state.
- Use a trusted shell and base utilities in the fixed system PATH. The tool is not designed to operate safely on a compromised operating system or malicious filesystem.

## Test and publish

```sh
python3 tests/test_cli.py
TEST_SHELL=/bin/dash python3 tests/test_cli.py
```

Tests create synthetic files only in a temporary test directory and clean it afterward. Test-file creation is separate from CLI behavior. See [validation](docs/VALIDATION.md) for actual tested environments.

The Markdown article is ready for a CMS; the HTML is a self-contained page with no external assets or scripts. Its relative documentation links need to remain alongside it or be adapted by the site's publisher. No repository, website or release has been uploaded by this package. There is no implied vendor endorsement or independent audit. AI-assisted implementation and writing; human production acceptance remains pending.

[Article](articles/sshole-en.md) · [Remediation](docs/REMEDIATION.md) · [Quick start](docs/QUICKSTART.md) · [Russian article](articles/sshole-ru.md)
