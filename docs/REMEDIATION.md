# Remediation and verification

Verified 2026-11-09. This is a manual change guide. The assessment CLI never runs these steps. Review the live vendor advisory before maintenance; this release's facts will age.

## Vendor package evidence

Alpine lists these fixed revisions in its [security advisory](https://alpinelinux.org/posts/2026-11-05-openssh-password-authentication-bypass/):

| Branch | Fixed openssh revision |
|---|---|
| edge | 10.6_p2-r0 |
| 3.24 | 10.3_p1-r2 |
| 3.23 | 10.2_p1-r1 |
| 3.22 | 10.0_p1-r11 |
| 3.21 | 9.9_p2-r1 |
| 3.20 | 9.7_p1-r6 |
| 3.19 | 9.6_p1-r3 |
| 3.18 | 9.3_p2-r4 |
| 3.17 | 9.1_p1-r7 |
| 3.16 | 9.0_p1-r6 |

Old branches receiving this correction are not thereby restored to general support. Do not use lexical version sorting or compare revisions across branches. For custom builds, obtain build provenance showing the corrective commit or an equivalent vendor patch; the CLI does not do that verification.

## Controlled operator workflow

1. Identify the real service, executable, package owner, configuration and launch arguments. Include containers, image templates and separately installed binaries. Record the observation time.
2. Arrange console/recovery access, configuration backups and a working key-based login. Keep the current administrative session open. Agree the maintenance scope and rollback procedure before changes.
3. Refresh package metadata from the approved repositories for the existing branch. Review the proposed transaction. Alpine's advisory recommends `apk upgrade -U -a`, which can upgrade more than SSH; apply that broad transaction only within the agreed maintenance scope. Do not switch repository branches casually.
4. Validate the intended configuration with the installed daemon's `-t` mode. Replace the running daemon through the deployment's service manager or recreate the container. Alpine documents `rc-service sshd restart`; an installed update alone is insufficient. These are manual changes, not CLI actions. [Alpine instructions](https://alpinelinux.org/posts/2026-11-05-openssh-password-authentication-bypass/)
5. Verify the installed package revision, the new process/executable and relevant connection policies. Establish a fresh authorized connection. Update the source image or automation so a redeploy does not restore the old build.
6. Retain a short evidence record: service identity, vendor advisory, package revision, change time, process replacement, configuration checks and successful access test. Do not retain password hashes in that record.

## If updating must wait

Disable the password path under a reviewed change, then validate all applicable contexts. Alpine identifies `PasswordAuthentication no` as a workaround. Do not blindly append a drop-in: effective policy depends on Includes, ordering and Match rules. [Alpine workaround](https://alpinelinux.org/posts/2026-11-05-openssh-password-authentication-bypass/)

Review the intended key/MFA workflow separately before altering keyboard-interactive or PAM settings. Changing those settings can break access and is not an automatic part of this tool. Restricting network reachability may reduce exposure while maintenance is prepared; it does not patch the daemon.

## Optional effective-configuration evidence

The following is an **operator example**, not a command executed by the CLI. Use a trusted installed daemon and an actual local account and connection context. Replace the example values, configuration path and any service-specific overrides. Output redirection writes a report file chosen by the operator.

```sh
/usr/sbin/sshd -T -f /etc/ssh/sshd_config \
  -C user=reviewuser,addr=192.0.2.10,host=client.example,laddr=192.0.2.20,lport=22 \
  > /absolute/private/path/sshd-effective.txt
sh bin/relay-sshole-check --effective /absolute/private/path/sshd-effective.txt
```

`-T` reads configuration and checks keys; elevated access may be needed. `-C` selects a context rather than enumerating every possible context. Consult your installed portable OpenSSH manual for PAM-specific behavior. Runtime validation can involve environment-dependent lookups; it is deliberately outside the passive CLI. [sshd manual](https://man.openbsd.org/sshd.8)

A complete policy review also considers root restrictions, Allow/Deny rules, AuthenticationMethods, account state and directory sources. Review the full report privately; the CLI prints only an allowlisted subset. Do not interpret a supplied report as attested runtime state.

## Suspected compromise

Preserve available evidence before rebuilding. Review unexplained successful authentication, privilege escalation, keys, accounts and persistence. If unauthorized access cannot be excluded, follow your incident-response process, including credential rotation from a trusted system and restoration from known-good sources. An update prevents the corrected failure path; it does not remove an intruder.

Rollback must retain a protective control or network isolation; returning to an exposed unpatched service is not an acceptable completion state.
