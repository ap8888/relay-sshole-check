# Verification record

Checked 2026-11-09 (Asia/Baku publication date). Sources were read during preparation, not copied from the prior chat. No exploitation resources were executed. These are live links, not archived attestations.

| Source | Used for |
|---|---|
| [OpenSSH 10.6p2 release notes](https://www.openssh.org/releasenotes.html#10.6p2) | Release date, scope, upstream fix and attribution |
| [Corrective commit 4353fdc43ef646c43a8dda7025cc1a898caf1482](https://github.com/openssh/openssh-portable/commit/4353fdc43ef646c43a8dda7025cc1a898caf1482) | Actual password-comparison code change |
| [Alpine advisory](https://alpinelinux.org/posts/2026-11-05-openssh-password-authentication-bypass/) | Distribution-specific prerequisites, package revisions and operator actions |
| [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-123158) | CVE description and attribution of displayed severity |
| [Red Hat](https://access.redhat.com/security/cve/cve-2026-123158) | Vendor-specific product scope |
| [sshd manual](https://man.openbsd.org/sshd.8) | Test/configuration modes and connection contexts |
| [sshd_config manual](https://man.openbsd.org/sshd_config.5) | Ordering, Match and authentication policy semantics |
| [Research landing page](https://sshhole.com/) | Naming and background; not the sole authority for package or exposure decisions |

## Editorial decisions

- Publish no universal banner-based vulnerability verdict. The CLI does not maintain a vulnerable/fixed version database.
- Do not repeat the prior chat's claim of attacks beginning on a specific day as an independently verified fact. Reports of exploit availability and confirmed attacks are distinct claims.
- Omit payloads, reproducers, remote login tests and password-length recipes.
- Do not equate a key being configured with password authentication being disabled.
- Do not describe every musl distribution, appliance or container as affected. Obtain its own vendor/build evidence.
- NVD and vendor severity labels can differ; preserve source attribution rather than presenting an unattributed universal score.
- Publish the check date. Recheck source revisions before subsequent releases.

The original research report is credited in the [upstream release notes](https://www.openssh.org/releasenotes.html#10.6p2) to Özgün Kültekin of Wakefield. RELAY is providing an independent assessment aid, not claiming discovery.
