# 📡 Zabbix Templates & Scripts - Enterprise Collection

[![Zabbix](https://img.shields.io/badge/Zabbix-2.0%2B-red)](https://www.zabbix.com/)
[![SNMP](https://img.shields.io/badge/SNMP-v1%2Fv2c%2Fv3-blue)](https://en.wikipedia.org/wiki/Simple_Network_Management_Protocol)
[![License](https://img.shields.io/badge/license-GPL2-green.svg)](LICENSE)

**Production-ready Zabbix templates and scripts for monitoring enterprise infrastructure**

[English] | [Русский](README.ru.md)

> Comprehensive collection of Zabbix templates for network equipment, storage systems, and servers. Based on jjmartres/Zabbix with enhancements and professional support.

---

## 🎯 What's Included

### Network Equipment

#### 🔵 Cisco - Complete monitoring suite
- **BGP4**: BGP neighbors (IPv4/VPNv4), state monitoring, prefix statistics
- **CDP**: Auto-discovery of CDP neighbors, topology mapping
- **Environmental**: Temperature, voltage, fans, power supplies monitoring
- **Hardware**: Inventory via ENTITY-MIB, serial numbers, firmware versions
- **HSRP**: HSRP group discovery, active/standby status
- **Interfaces**: Interface discovery (IF-MIB), traffic stats, optical levels, UDLD
- **MPLS**: LDP neighbor discovery, LSP statistics, MPLS VPN monitoring
- **Optical**: DOM (Digital Optical Monitoring), TX/RX power, temperature
- **VPDN**: Virtual Private Dialup Network session statistics

#### 🟢 Dell PowerConnect
- Switch monitoring with interface stats
- Environmental sensors
- Stack status monitoring

#### 🟠 Fortinet
- Firewall policy monitoring
- VPN tunnel statistics
- IPS/IDS metrics
- High Availability status

#### 🟣 Brocade Fiber Channel
- FC port discovery and statistics
- Environmental monitoring (temperature, fans, PSU)
- Optical levels monitoring

#### 🔴 Netopia
- Network device monitoring
- Interface statistics

### Infrastructure

#### ⚡ UPS Systems
- **APC**: Battery status, load percentage, input/output voltage, runtime, temperature
- **Eaton**: Complete power system monitoring with Eaton-specific metrics

#### 💾 Storage Systems
- **Infortrend**: RAID status, disk health, controller metrics, volume performance
- **DataCore**: SANsymphony-V monitoring, virtual disk status, replication health

### Servers

#### 🖥️ Windows
- **Environmental**: CPU temperature, system fans, voltage sensors
- **MSSQL**: Database status, query performance, locks/deadlocks, backup status
- **IIS**: Website status, request statistics, application pool monitoring

### Scripts

- **as.name**: AS Name lookup by IP (Ruby)
- **if.speed**: Real interface speed detection (Shell/Python)
- **echo.something**: Simple echo test utility
- And more discovery and monitoring scripts...

---

## ✨ Features

- 📊 **Low-Level Discovery (LLD)**: Automatically discover devices and components
- 🔔 **Pre-configured Triggers**: Ready-to-use alerts with sensible thresholds
- 📈 **Performance Metrics**: Detailed monitoring with historical data
- 🎨 **Grafana Integration**: Export capabilities for enhanced visualization
- 🔧 **Customizable**: Easy to modify with macros and custom OIDs
- 📚 **Well Documented**: Individual READMEs for each template
- 🏢 **Enterprise-Ready**: Tested on production environments with thousands of devices
- 🌍 **SNMP Support**: Works with v1, v2c, and v3

---

## 🚀 Quick Start

### Prerequisites

- Zabbix Server >= 2.0 (recommended: 6.x or 7.x)
- SNMP access to monitored devices
- Properly configured SNMP community strings or v3 credentials
- External scripts support enabled (for script-based monitoring)

### Installation

#### 1. Import Templates

**Via Web UI:**
```
1. Download the desired template XML file from zbx-templates/
2. Log in to Zabbix Web Interface
3. Navigate to Configuration → Templates
4. Click "Import"
5. Select the XML file
6. Configure import rules as needed
7. Click "Import"
```

**Via API (for automation):**
```python
# See examples in the repository for API-based import scripts
```

#### 2. Install Scripts

```bash
# Find your ExternalScripts directory
grep ExternalScripts /etc/zabbix/zabbix_server.conf

# Copy scripts (usually to /usr/lib/zabbix/externalscripts)
sudo cp zbx-scripts/*/script_name /usr/lib/zabbix/externalscripts/

# Set permissions
sudo chmod +x /usr/lib/zabbix/externalscripts/*
sudo chown zabbix:zabbix /usr/lib/zabbix/externalscripts/*

# Test the script
sudo -u zabbix /usr/lib/zabbix/externalscripts/script_name test_params
```

#### 3. Configure SNMP

**Cisco IOS example:**
```cisco
! SNMPv2c (basic)
snmp-server community public RO

! SNMPv3 (recommended for production)
snmp-server group ZABBIX v3 priv
snmp-server user zabbix ZABBIX v3 auth sha AuthPass123 priv aes 128 PrivPass123
```

#### 4. Link Templates to Hosts

```
1. Configuration → Hosts
2. Select or create a host
3. Go to Templates tab
4. Click "Select" and choose the template
5. Add → Update
```

#### 5. Configure Macros

```
Host level macros (Configuration → Hosts → Macros):
{$SNMP_COMMUNITY} = "public"
{$INTF_REGEX} = "^(Gi|Te|Ethernet).*"
{$CPU_THRESHOLD} = "80"
{$TEMP_THRESHOLD} = "75"
```

---

## 📖 Documentation

Each template and script includes its own README with:
- Detailed description
- Requirements and dependencies
- Installation instructions
- Configuration examples
- Available items and triggers
- Troubleshooting tips

Browse the `zbx-templates/` and `zbx-scripts/` directories for specific documentation.

---

## 🔧 Customization

### Modify Thresholds

Templates use macros for easy customization:
- `{$SNMP_COMMUNITY}` - SNMP community string
- `{$INTF_REGEX}` - Interface name filter regex
- `{$CPU_THRESHOLD}` - CPU usage threshold
- `{$TEMP_THRESHOLD}` - Temperature threshold
- `{$BANDWIDTH_THRESHOLD}` - Bandwidth utilization threshold

Override these at the host or template level as needed.

### Add Custom OIDs

You can extend templates with additional SNMP OIDs specific to your environment. See individual template documentation for examples.

---

## 🤝 Professional Services

Need help implementing Zabbix monitoring for your enterprise infrastructure?

### Available Services:

- ✅ **Deployment**: Full Zabbix setup and configuration
- ✅ **Custom Templates**: Develop templates for your specific equipment
- ✅ **Integration**: Connect with existing monitoring and ITSM systems
- ✅ **Migration**: Migrate from other monitoring platforms
- ✅ **Training**: Zabbix administration and template development
- ✅ **Support**: Enterprise-grade 24/7 support

**Contact**: [run-as-daemon.ru](https://run-as-daemon.ru)

---

## 🏆 Use Cases

This collection is actively used in:
- **Telecommunications**: ISP network infrastructure monitoring (500+ routers/switches)
- **Banking**: Multi-site enterprise monitoring (2000+ devices)
- **Industrial**: SCADA integration and manufacturing monitoring
- **Data Centers**: Complete infrastructure visibility
- **Enterprise IT**: Comprehensive server and network monitoring

---

## 🐛 Troubleshooting

### SNMP Issues
- Verify SNMP connectivity: `snmpwalk -v2c -c public device_ip system`
- Check firewall rules (UDP port 161)
- Verify community strings or v3 credentials
- Ensure device has SNMP enabled

### Script Issues
- Check script permissions and ownership
- Verify script path in Zabbix configuration
- Test scripts manually as zabbix user
- Check Zabbix server logs: `/var/log/zabbix/zabbix_server.log`

### Template Issues
- Verify template compatibility with your Zabbix version
- Check that required macros are defined
- Review item prototype filters in Low-Level Discovery rules
- Monitor discovery logs in Zabbix UI

---

## 🤝 Contributing

Contributions are welcome! If you have:
- Bug fixes
- New templates
- Improvements to existing templates
- Documentation updates

Please feel free to submit pull requests or open issues.

---

## 📄 License

This project is licensed under the **GNU General Public License v2.0** - see the [LICENSE](LICENSE) file for details.

### Attribution

**Original Work**: Jean-Jacques Martrès ([jjmartres/Zabbix](https://github.com/jjmartres/Zabbix))  
**Fork Maintainer**: Ranas Mukminov ([run-as-daemon.ru](https://run-as-daemon.ru))

---

## 🔗 Links

- **Zabbix Official**: [www.zabbix.com](https://www.zabbix.com/)
- **Documentation**: [Zabbix Documentation](https://www.zabbix.com/documentation)
- **Community**: [Zabbix Forums](https://www.zabbix.com/forum/)
- **Professional Services**: [run-as-daemon.ru](https://run-as-daemon.ru)

---

<div align="center">

**Enterprise monitoring solutions by [run-as-daemon.ru](https://run-as-daemon.ru)**

*Zabbix • SNMP • Network Monitoring • Infrastructure Monitoring*

</div>
