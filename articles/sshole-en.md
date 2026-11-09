---
title: "SSHole: assess the authentication path, not just the OpenSSH version"
description: "CVE-2026-123158, vendor backports, and a passive local assessment tool from RELAY / n0hup.nl."
author: "RELAY / n0hup.nl"
date: "2026-11-09"
lang: "en"
slug: "sshole-cve-2026-123158"
---

# SSHole: assess the authentication path, not just the OpenSSH version

**RELAY / n0hup.nl · 9 November 2026 · Technical advisory and tool release**

SSHole deserves prompt attention, but an old SSH banner is not an assessment. The practical task is to establish which daemon is running, how it authenticates users, and whether its vendor has already supplied a fix.

CVE-2026-123158 concerns a password-authentication bypass in certain Linux deployments combining OpenSSH, musl libc and a non-PAM authentication path. NVD identifies upstream versions before 10.6p2 and displays a CNA score of 8.1 (High); its own assessment was not yet available when checked. These conditions matter more than the headline version range. [NVD record](https://nvd.nist.gov/vuln/detail/CVE-2026-123158)

## What fails

At the boundary between the password-checking code and the C library, a failure representation can be mistaken for a successful password comparison. OpenSSH's corrective commit adds a minimum stored-hash-length condition before accepting the comparison and adjusts password-buffer handling. The maintainers describe the change as avoiding the bypass, while locating the root cause outside OpenSSH. This distinction is useful for understanding the fix; it does not reduce an operator's need to remediate affected systems. [Upstream corrective commit](https://github.com/openssh/openssh-portable/commit/4353fdc43ef646c43a8dda7025cc1a898caf1482)

Portable OpenSSH 10.6p2 was released on 5 November 2026. Distribution backports mean an earlier upstream version can nevertheless contain the correction. Use the vendor's package revision and branch-specific advisory, not a comparison against `10.6p2` alone. [OpenSSH release notes](https://www.openssh.org/releasenotes.html#10.6p2)

## Where to focus

Alpine's advisory describes the relevant account combination as an exact `*` password field together with another local account using a SHA-256 or SHA-512 crypt hash. Password authentication must be enabled; PAM-enabled builds with `UsePAM yes` are outside that described path. Root's login policy is a separate constraint. A container without a running SSH server is not exposed through that container's SSH service. [Alpine advisory](https://alpinelinux.org/posts/2026-11-05-openssh-password-authentication-bypass/)

Do not turn a distribution name into a verdict. Red Hat states that its product builds are unaffected because they use glibc and PAM. That statement applies to those builds; a separately deployed container or custom binary needs its own inventory. [Red Hat assessment](https://access.redhat.com/security/cve/cve-2026-123158)

For an estate review, start with services reachable from untrusted networks, then inspect images and appliances that embed an SSH server. Record the actual executable, package origin, configuration path and service launch arguments. Distinguish the filesystem being inspected from the host, container or namespace serving the connection. A package in an image inventory does not prove that its daemon is active.

## Why a passive assessment is useful

RELAY SSHole Check v0.1.0 collects a small set of local facts without attempting authentication. It reads distribution identifiers, Alpine package metadata, the presence of a conventional musl loader and SSH binary, and counts selected directives in the main SSH configuration. Optional shadow inspection reports only aggregate counts. No username, password field or hash is printed.

The result is deliberately conservative:

- `REVIEW_REQUIRED`: evidence remains incomplete.
- `PRIORITY_REVIEW`: a musl loader and the local account pattern coexist; investigate promptly.

Neither result asserts exploitability. Neither is a safety certificate. A loader on disk does not establish the daemon's linkage; local files do not cover directory-service accounts; a patched package does not prove that the running process has been replaced.

The tool does not run `sshd`, query NSS, call a package manager, create temporary files or contact a host. It can read an existing `sshd -T` report, but labels that evidence as supplied and unverified. Its main configuration scan counts directives rather than pretending to implement OpenSSH's parser.

## Configuration needs context

OpenSSH provides `sshd -T` to validate and display configuration. Supplying `-C` applies rules for a selected connection context. Inspect relevant combinations of user, source and destination, including the service's actual configuration and overrides; one default-context report cannot establish every user's policy. [sshd manual](https://man.openbsd.org/sshd.8)

For a review record, retain the source of each observation and its time. Keep “installed package”, “running executable”, “effective connection policy” and “account eligibility” as separate fields. This makes disagreements actionable: a fixed package and an old process require different work from a disabled password path and an unpatched image template.

## Remediate, then verify the deployment

Use the [remediation guide](../docs/REMEDIATION.md) for the verified Alpine revision table and an operator-controlled workflow. Schedule changes with working console access and a tested alternate login. Update deployment sources as well as current instances, then verify a new connection before closing the maintenance session.

If exposure is suspected, preserve authentication logs and investigate unexpected successful logins and privilege use. A missing log entry is not evidence that access never occurred. This article does not claim that attacks were observed in your environment, nor does it establish a global exploitation timeline.

## Release scope

The release includes source, documentation and synthetic offline tests. Local validation covers `/bin/sh` and `dash` on macOS; it does not constitute Alpine, BusyBox or production integration testing. The repository records these limits explicitly. AI-assisted preparation is disclosed; independent security review remains pending.

The useful outcome is an evidence-backed remediation decision. Start with passive inventory, establish vendor patch provenance, and close the operational loop on the daemon that actually serves users.
