# Security Policy

## Scope

This repository contains **Zabbix templates and external scripts** for monitoring various devices and services. It does not include:
- Network services that directly handle user input
- Web applications
- Authentication systems

However, **security considerations still apply** because:
- External scripts execute on the Zabbix server and can interact with monitored systems
- Scripts may handle sensitive data (SNMP credentials, API keys)
- Improperly configured templates could expose sensitive information
- SNMP queries could trigger unintended actions on monitored devices

## Security Best Practices

### When Using Templates

- ✅ **Always review templates before importing** — understand what items, triggers, and scripts they use
- ✅ **Test in a non-production environment first** — use the Docker demo environment in `examples/`
- ✅ **Use SNMPv3 with encryption** — avoid SNMPv1/v2c in production environments
- ✅ **Restrict SNMP access** — use ACLs to limit which IPs can query devices
- ✅ **Set appropriate permissions on hosts** — use Zabbix RBAC to limit who can see sensitive data
- ✅ **Review macro values** — don't hardcode passwords; use Zabbix secret storage when available

### When Using External Scripts

- ✅ **Review script code** — understand what the script does before deploying it
- ✅ **Set proper file permissions** — scripts should be owned by `zabbix` user with `chmod 750` or `755`
- ✅ **Validate input** — scripts that accept parameters should validate and sanitize inputs
- ✅ **Avoid hardcoded credentials** — pass credentials via Zabbix macros or secure storage
- ✅ **Use least privilege** — scripts should run with minimal permissions needed
- ✅ **Keep interpreters updated** — ensure Ruby, Python, PowerShell are patched

### General Security

- ✅ **Keep Zabbix updated** — apply security patches promptly
- ✅ **Enable TLS** — use encrypted connections for Zabbix frontend and agent communication
- ✅ **Strong authentication** — use strong passwords, consider LDAP/SAML, enable MFA if available
- ✅ **Regular audits** — review template configurations and script permissions periodically
- ✅ **Backup securely** — encrypt backups and restrict access to them

## Reporting Security Vulnerabilities

### For Template or Script Vulnerabilities

If you discover a security vulnerability in a **template or script in this repository**:

**DO NOT** open a public GitHub issue (it would expose the vulnerability).

Instead, report it privately:

1. **Email:** security@run-as-daemon.ru
2. **Subject:** `[SECURITY] Zabbix Templates — [Brief Description]`
3. **Include:**
   - Description of the vulnerability
   - Affected template/script file(s)
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if you have one)

**Expected response time:**
- Initial acknowledgment: Within 7 days
- Triage and fix: Best effort (no guaranteed SLA for community issues)
- Public disclosure: After fix is released or 90 days, whichever comes first

### For Zabbix Core Vulnerabilities

If the vulnerability is in **Zabbix itself** (not templates/scripts):
- Report to Zabbix SIA: [https://www.zabbix.com/security](https://www.zabbix.com/security)

### For Monitored Device Vulnerabilities

If you discover a vulnerability in **monitored devices** (Cisco, Fortinet, etc.):
- Report to the vendor's security team (not this repository)
- Follow responsible disclosure practices

## Supported Versions

| Version / Branch | Supported          |
| ---------------- | ------------------ |
| main (latest)    | ✅ Yes             |
| Older commits    | ❌ No (update to latest) |

We only provide security updates for the latest code on the `main` branch. Always pull the latest version before reporting issues.

## Known Limitations

- **Old templates:** Some templates were created years ago and may not follow modern security practices
- **Community contributions:** Templates are often community-contributed and may not have undergone security review
- **Vendor-specific risks:** Monitoring certain devices (network gear, storage) requires privileged SNMP/API access
- **Script execution:** External scripts run on the Zabbix server and inherit server privileges

**Mitigation:** Always review, test, and harden templates/scripts before production use.

## Security Updates

Security fixes will be:
- Applied to the `main` branch
- Documented in commit messages with `[SECURITY]` prefix
- Announced in GitHub Releases (if significant)
- Mentioned in SUPPORT.md or README.md if user action is required

## Third-Party Dependencies

This repository uses:
- **Zabbix** (GPL-2.0) — [https://www.zabbix.com/security](https://www.zabbix.com/security)
- **Docker images** (examples/) — official Zabbix and PostgreSQL images from Docker Hub
- **Python libraries** (tools/) — `requests` (check `pip-audit` for vulnerabilities)

We do not guarantee the security of third-party dependencies. Users should:
- Keep Zabbix and Docker images updated
- Run `pip-audit` or `safety` on Python dependencies
- Follow security advisories from vendors

## Disclaimer

**This software is provided "as-is" under GPL-2.0 license WITHOUT WARRANTY OF ANY KIND.**

- No guarantee of security or fitness for any purpose
- No liability for damages caused by vulnerabilities
- Use at your own risk in production environments

For professional security audits and hardening, contact: [run-as-daemon.ru](https://run-as-daemon.ru)

---

**Last updated:** 2024-11-17
