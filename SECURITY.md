# Security boundaries

The CLI uses passive local file reads only. It implements no network protocol, authentication attempt, remediation, package update, service control, subprocess execution from an inspected filesystem, or secret export.

Use a trusted operating system, shell, base utilities and input tree. This is not a forensic acquisition tool, hostile-image parser or substitute for incident response. Reads can cause filesystem access-time updates or OS audit entries. Snapshot symlinks are followed; `--root` is not containment. Files may change between reads.

Do not attach real shadow files, password hashes, private keys, full configuration reports or personal account data to public issues. Report a tool defect through the repository's private reporting mechanism if one is enabled; otherwise contact the publisher through an already verified private channel. This unpublished package does not invent a support address or promise response times.

Independent review and native Linux integration acceptance remain pending. Review the source before privileged use. Follow vendor advisories for the underlying vulnerability; do not send this tool's bugs to upstream OpenSSH as though they were upstream defects.
