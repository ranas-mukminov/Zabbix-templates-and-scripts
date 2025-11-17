# Zabbix Templates and Scripts Collection (run-as-daemon fork)

[![Zabbix](https://img.shields.io/badge/Zabbix-2.0%2B-red)](https://www.zabbix.com/)
[![SNMP](https://img.shields.io/badge/SNMP-v1%2Fv2c%2Fv3-blue)](https://en.wikipedia.org/wiki/Simple_Network_Management_Protocol)
[![License](https://img.shields.io/badge/license-GPL2-green.svg)](LICENSE)

**A curated fork of jjmartres/Zabbix with additional documentation, examples, and Docker demo environment**

[English] | [Русский](README.ru.md)

---

## About This Project

This repository is a fork of the well-known community collection [jjmartres/Zabbix](https://github.com/jjmartres/Zabbix) — "A great collection of Zabbix scripts and templates" for monitoring network equipment, storage systems, and servers from various vendors (Cisco, Brocade, Fortinet, Dell, Windows, Linux, and more).

**Purpose:** This fork provides:
- The original community-contributed templates and scripts
- Enhanced documentation and usage examples
- A ready-to-run Docker Compose demo environment for testing templates
- Professional SRE/DevOps services and consulting

**Maintainer:** [run-as-daemon](https://run-as-daemon.ru) — SRE/DevOps engineer specializing in Zabbix monitoring solutions.

---

## Repository Structure

This repository is organized into three main directories:

### 📂 zbx-templates/

XML template files for importing into Zabbix, organized by vendor/technology:

#### Network Equipment
- **zbx-cisco/** — Comprehensive Cisco monitoring suite (BGP, CDP, HSRP, MPLS, interfaces, optical monitoring, environmental sensors, hardware inventory, VPDN)
- **zbx-brocade/** — Brocade Fiber Channel switches (FC port monitoring, environmental sensors)
- **zbx-dell-powerconnect/** — Dell PowerConnect switches (interfaces, environmental monitoring, stacking)
- **zbx-fortinet/** — Fortinet FortiGate firewalls (CPU, memory, sessions, VPN, IDS, HA, VDOM, hardware sensors)
- **zbx-netopia/** — Netopia network devices (interfaces, xDSL, environmental monitoring)
- **zbx-audiocodes/** — AudioCodes VoIP equipment (interface monitoring)

#### Storage Systems
- **zbx-infortrend/** — Infortrend storage arrays (RAID status, disk health, controller metrics, volume performance)
- **zbx-datacore/** — DataCore SANsymphony-V (virtual disk status, replication health)
- **zbx-dell-compellent/** — Dell Compellent storage systems

#### UPS & Power
- **zbx-apc/** — APC UPS systems (battery status, load, voltage, runtime, temperature)
- **zbx-eaton/** — Eaton UPS systems with vendor-specific metrics

#### Servers & Operating Systems
- **zbx-windows/** — Windows server monitoring (IIS, MSSQL, Exchange 2007/2010, environmental sensors)
- **zbx-linux/** — Linux server templates
- **zbx-vmware/** — VMware infrastructure monitoring
- **zbx-veeam/** — Veeam backup monitoring

#### Services & Applications
- **zbx-drbd/** — DRBD replication monitoring
- **zbx-icewarp/** — IceWarp mail server
- **zbx-rblcheck/** — RBL (Real-time Blackhole List) checking
- **zbx-smstools/** — SMS gateway monitoring
- **zbx-gandi/** — Gandi hosting services monitoring

**Key use cases:** Monitoring network interfaces, BGP/OSPF routing protocols, MPLS VPNs, Fiber Channel SANs, CPU/memory/temperature sensors, UPS battery status, database performance, web server metrics, backup jobs, and more.

### 📂 zbx-scripts/

External scripts (Ruby, Shell, Python, PowerShell) for advanced monitoring and automation:

- **as.name/** — AS (Autonomous System) name lookup by IP address (Ruby, uses whois.cymru.com)
- **if.speed/** — Real interface speed detection (ifSpeed/ifHighSpeed SNMP OIDs)
- **if.count/** — Interface counting and statistics
- **if.vdom/** — Fortinet VDOM interface association
- **ift.ldmode/**, **ift.ldsize/**, **ift.ldstatus/** — Infortrend logical drive monitoring
- **powerconnect.optical/** — Dell PowerConnect optical transceiver monitoring
- **rbl.check/** — RBL blacklist checking
- **gandi.check/** — Gandi service availability checks
- **vcloud.check/** — VMware vCloud monitoring
- **vpn.vdom/** — Fortinet VPN and VDOM association
- **echo.something/** — Simple echo test utility
- **discovery_update/**, **hosts_update/**, **nmsupdate/** — Zabbix automation scripts

**Typical usage:** Place these scripts in Zabbix's ExternalScripts directory (e.g., `/usr/lib/zabbix/externalscripts`) and call them from template items.

### 📂 zbx-agent/

Zabbix agent installation files and configuration examples:
- Windows Zabbix agent installers (versions 2.0.6, 2.0.7, 2.0.9)
- Agent configuration fragments and examples

---

## Requirements & Compatibility

**Zabbix Versions:**
- Templates were originally created for Zabbix 2.0–4.x
- Many templates work with Zabbix 5.x–7.x but may require adjustments
- Always test templates in a non-production environment first
- Check individual template README files for specific version compatibility

**Dependencies:**
- **SNMP support** — Most templates require SNMP v1, v2c, or v3 access to monitored devices
- **Zabbix Agent** (classic or agent2) — Required for some templates (Windows, Linux servers)
- **External scripts** — Some templates require Ruby, Python, or PowerShell runtime
- **Network access** — Proper firewall rules for SNMP (UDP/161), Zabbix agent (TCP/10050), etc.

**Important Notes:**
- This is a **community-driven collection**, not an official product of Zabbix SIA
- Templates are provided "as-is" without warranty or guaranteed support
- Always review and test templates before deploying to production
- Some templates may need macro adjustments or OID updates for newer device firmware

---

## How to Use These Templates

### Step 1: Prepare External Scripts (if needed)

If your chosen template uses external scripts:

**For Linux/Unix Zabbix Server:**
```bash
# Find your ExternalScripts directory
grep ExternalScripts /etc/zabbix/zabbix_server.conf
# Typically: ExternalScripts=/usr/lib/zabbix/externalscripts

# Copy scripts from zbx-scripts/
sudo cp zbx-scripts/script_name/script_name.rb /usr/lib/zabbix/externalscripts/
sudo chmod +x /usr/lib/zabbix/externalscripts/*
sudo chown zabbix:zabbix /usr/lib/zabbix/externalscripts/*

# Test the script manually
sudo -u zabbix /usr/lib/zabbix/externalscripts/script_name.rb test_params
```

**For Windows Zabbix Server:**
- Place PowerShell scripts in the configured ExternalScripts path (e.g., `C:\Program Files\Zabbix Agent\scripts\`)
- Ensure execution policy allows running scripts: `Set-ExecutionPolicy RemoteSigned`

### Step 2: Configure Zabbix Agent (if needed)

Use configuration examples from `zbx-agent/` directory:
```bash
# Linux agent configuration
sudo nano /etc/zabbix/zabbix_agentd.conf
# Add custom UserParameters or include configs

# Restart agent
sudo systemctl restart zabbix-agent
```

### Step 3: Import XML Template

**Via Web UI:**
1. Download the desired `.xml` file from `zbx-templates/`
2. Log in to Zabbix web interface
3. Navigate to **Data collection → Templates** (Zabbix 6.x+) or **Configuration → Templates** (older versions)
4. Click **Import**
5. Choose the XML file
6. Review import options (create new, update existing, delete missing)
7. Click **Import**

**Via API (automated):**
See [tools/import_template.py](#automated-import-with-zabbix-api) for an example script.

### Step 4: Link Template to Host

1. **Configuration → Hosts** (or **Data collection → Hosts**)
2. Select an existing host or create a new one
3. Go to the **Templates** tab
4. Click **Select** and choose the imported template(s)
5. Click **Add** → **Update**

### Step 5: Configure Macros

Most templates use macros for easy customization:

```
Host or Template Macros:
{$SNMP_COMMUNITY} = "public"           (SNMPv2c community string)
{$SNMP_USER} = "zabbix"                (SNMPv3 username)
{$SNMP_AUTH_PASS} = "AuthPass123"      (SNMPv3 auth password)
{$SNMP_PRIV_PASS} = "PrivPass123"      (SNMPv3 privacy password)
{$INTF_REGEX} = "^(Gi|Te|Ethernet).*"  (Interface name filter regex)
{$CPU_THRESHOLD} = "80"                (CPU usage warning threshold, %)
{$TEMP_THRESHOLD} = "75"               (Temperature warning threshold, °C)
{$BANDWIDTH_THRESHOLD} = "80"          (Bandwidth utilization threshold, %)
```

**Set macros:**
- **Global level:** Administration → General → Macros
- **Template level:** Data collection → Templates → [Template name] → Macros
- **Host level:** Data collection → Hosts → [Host name] → Macros

### Common Pitfalls & Troubleshooting

**Permission Issues:**
- External scripts must be executable and owned by the `zabbix` user
- Check SELinux/AppArmor policies if scripts fail to run
- Verify script interpreters (Ruby, Python) are installed

**SNMP Issues:**
- Test SNMP access: `snmpwalk -v2c -c public device_ip system`
- Check firewall rules (UDP port 161 for SNMP queries, UDP 162 for traps)
- Verify SNMP is enabled on the target device
- Ensure correct SNMP community string or SNMPv3 credentials

**Template Compatibility:**
- Older templates may use deprecated features (Simple checks, legacy macros)
- Discovery filters may need adjustment for newer Zabbix versions
- Some OIDs may differ between device firmware versions
- Check Zabbix server logs: `/var/log/zabbix/zabbix_server.log`

**Version Mismatches:**
- Templates created for Zabbix 2.x–4.x may not import directly into 6.x–7.x
- Use Zabbix's built-in template converter if available
- Manually update XML structure or create new templates based on old ones

---

## Demo Environment with Docker Compose

This repository includes a **Docker Compose demo environment** in the `examples/` directory. It provides:

- **Zabbix Server** with PostgreSQL database backend
- **Zabbix Web UI** with Nginx
- **PostgreSQL** database
- **Zabbix Agent 2** for testing agent-based templates

**Purpose:** 
- Quick testing and learning environment
- Import templates and see them in action
- Safe experimentation without affecting production systems

**NOT intended for production use** — this is a demo setup with default credentials and minimal security hardening.

See [examples/README.md](examples/README.md) for detailed instructions.

---

## Quick Start (with Docker)

Want to try templates quickly? Use the Docker demo environment:

```bash
# Clone the repository
git clone https://github.com/ranas-mukminov/Zabbix-templates-and-scripts.git
cd Zabbix-templates-and-scripts/examples

# Start the Zabbix stack (uses official Docker images)
docker compose up -d

# Wait ~30 seconds for services to initialize
docker compose ps

# Open web UI in browser
# URL: http://localhost:8080
# Default credentials: Admin / zabbix

# After login:
# 1. Go to Data collection → Templates
# 2. Click Import
# 3. Choose a template from ../zbx-templates/
# 4. Link the template to the "Zabbix server" host or the "zabbix-agent2" host
# 5. Check Latest data and Problems

# When done, stop the environment
docker compose down

# To completely remove (including database volumes)
docker compose down -v
```

---

## Automated Import with Zabbix API

For bulk import or automation, use the included Python script:

```bash
# Install requirements
pip install requests

# Import a template via API
python tools/import_template.py \
  --url http://localhost:8080 \
  --user Admin \
  --password zabbix \
  --template zbx-templates/zbx-cisco/zbx-cisco-bgp4/zbx-cisco-bgp4.xml

# Bulk import all templates (example)
for template in zbx-templates/*/*.xml; do
  python tools/import_template.py --url http://zabbix.local --user Admin --password secret --template "$template"
done
```

See [tools/import_template.py](tools/import_template.py) for usage details.

---

## Professional SRE/DevOps/Zabbix Services

This repository, templates, documentation, and Docker demo environment are maintained by **[run-as-daemon](https://run-as-daemon.ru)** — an SRE/DevOps engineer specializing in enterprise monitoring solutions.

**Services offered:**

- **🚀 Zabbix Deployment & Architecture Design**
  - Production-grade Zabbix installation (on-premises, Docker, Kubernetes)
  - High Availability (HA) and clustering setup
  - PostgreSQL/MySQL optimization for large-scale monitoring
  - Proxy deployment for distributed monitoring

- **🔄 Migration & Upgrades**
  - Migrate from Nagios, Cacti, PRTG, or other monitoring systems
  - Upgrade older Zabbix installations (2.x/3.x → 6.x/7.x)
  - Template conversion and modernization
  - Data migration and historical data preservation

- **🔌 Integration & Automation**
  - Integrate Zabbix with Grafana, Prometheus, InfluxDB, Elasticsearch
  - Connect to ITSM systems (Jira, ServiceNow, PagerDuty)
  - Custom alerting channels (Telegram bots, Slack, MS Teams, webhooks)
  - Monitoring as Code (Terraform, Ansible, GitOps workflows)

- **⚡ Performance Tuning & Optimization**
  - Database query optimization
  - Housekeeper and history cleanup strategies
  - Template efficiency audits (reduce database load)
  - Server sizing and capacity planning

- **📝 Custom Templates & Scripting**
  - Develop custom templates for specific vendors/devices/applications
  - MIB parsing and SNMP trap handling
  - External check scripts in Python, Ruby, Go, PowerShell
  - Low-Level Discovery (LLD) rules for dynamic environments

- **🔍 Auditing & Cleanup**
  - Review existing Zabbix configurations
  - Identify misconfigured items, inefficient triggers, unused hosts
  - Security hardening (SNMPv3, encrypted connections, RBAC)
  - Documentation and runbooks for operations teams

**Contact:** [run-as-daemon.ru](https://run-as-daemon.ru)

---

## Support / Contributing

### Community Support

- **GitHub Issues:** [Open an issue](https://github.com/ranas-mukminov/Zabbix-templates-and-scripts/issues) for bug reports, questions, or feature requests
- **Pull Requests:** Contributions are welcome! See [CONTRIBUTING guidelines](.github/PULL_REQUEST_TEMPLATE.md)
- **No SLA:** This is a community-driven project without guaranteed response times or support

### Show Your Appreciation

If you find this collection useful:
- ⭐ **Star this repository** on GitHub
- 🔗 **Share it** with colleagues and on social media
- 💬 **Open issues/PRs** to improve templates and documentation
- 💰 **Sponsor:** Support continued maintenance via [GitHub Sponsors](https://github.com/sponsors/ranas-mukminov) or [custom support link](https://run-as-daemon.ru/support)

### Paid Support & Consulting

For priority support, custom development, or consulting services, contact:
- 🌐 **Website:** [run-as-daemon.ru](https://run-as-daemon.ru)
- 📧 **Email:** contact@run-as-daemon.ru
- 💬 **Telegram:** @run_as_daemon

---

## License

This project is licensed under the **GNU General Public License v2.0 (GPL-2.0)**.

**What this means:**
- ✅ You can freely use, modify, and distribute this software
- ✅ You can use it for commercial purposes
- ⚠️ Any derivative works must also be licensed under GPL-2.0
- ⚠️ No warranty is provided; use at your own risk

See the [LICENSE](LICENSE) file for full legal text.

### Attribution

- **Original Work:** Jean-Jacques Martrès — [jjmartres/Zabbix](https://github.com/jjmartres/Zabbix)
- **Fork Maintainer:** Ranas Mukminov — [run-as-daemon.ru](https://run-as-daemon.ru)
- **Contributors:** See [GitHub contributors](https://github.com/ranas-mukminov/Zabbix-templates-and-scripts/graphs/contributors)

**Contributions must be GPL-2.0 compatible.** By submitting a pull request, you agree to license your contribution under GPL-2.0.

---

## Additional Resources

- **Zabbix Official Documentation:** [www.zabbix.com/documentation](https://www.zabbix.com/documentation)
- **Zabbix Community Forums:** [www.zabbix.com/forum](https://www.zabbix.com/forum/)
- **SNMP OID Repository:** [www.oid-info.com](http://www.oid-info.com/)
- **MIB Browser Tools:** [iReasoning MIB Browser](http://www.ireasoning.com/mibbrowser.shtml), Net-SNMP tools

---

<div align="center">

**Enterprise monitoring solutions by [run-as-daemon.ru](https://run-as-daemon.ru)**

*Zabbix • SNMP • Network Monitoring • Infrastructure Monitoring • SRE/DevOps*

</div>
