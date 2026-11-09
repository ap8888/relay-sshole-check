# RELAY SSHole Check v0.1.0 — Quick start

This tool collects passive local evidence for a CVE-2026-123158 review. It does not attempt an SSH login, start a server or change configuration. It never issues a “system safe” verdict.

From the extracted release directory:

```sh
sh bin/relay-sshole-check
```

To opt into aggregate local password-field inspection:

```sh
sh bin/relay-sshole-check --shadow
```

`--shadow` permits reading `/etc/shadow` when the current user already has access. Only counts are printed, never usernames or hashes. Privileges are not elevated automatically. Do not use shell tracing for an assessment. Start without additional privileges.

To inspect a trusted filesystem snapshot:

```sh
sh bin/relay-sshole-check --root /absolute/trusted/snapshot --shadow
```

This is a path prefix, not an isolation boundary: symlinks can point outside the selected directory. Do not use this mode on untrusted images.

| Result | Meaning |
|---|---|
| REVIEW_REQUIRED, exit 1 | Evidence is incomplete; administrator review is required |
| PRIORITY_REVIEW, exit 2 | Coexisting indicators warrant priority review |
| Exit 64 | Invalid arguments or input path |
| Exit 70 | Evidence processing failure |
| Exit 0 | Help or version only |

Exit 2 does not prove vulnerability; exit 1 does not prove its absence. Package versions are printed for source-based review, without automatic patch classification. Finding musl on disk does not establish that the SSH daemon uses it.

Only conventional paths are examined by default. The tool counts directives in the main configuration file but does not evaluate Include or Match rules. An existing `sshd -T` report can be supplied with `--effective /absolute/report.txt`; its contents are labelled supplied, unverified evidence. Preparing that report is a separate operator action.

The publication article is available in [English](../articles/sshole-en.md) and [Russian](../articles/sshole-ru.md), each with an HTML edition. See [REMEDIATION.md](REMEDIATION.md) for the manual remediation workflow and package revisions, and [VALIDATION.md](VALIDATION.md) for test coverage and limitations.

Ordinary reads may update file access times, and the operating system may audit execution. The tool does not promise the absence of OS bookkeeping.
