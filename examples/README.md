# Zabbix Docker Demo Environment

This directory contains a Docker Compose configuration for quickly spinning up a complete Zabbix monitoring stack for testing and learning purposes.

## What's Included

- **Zabbix Server 7.x** (latest) with PostgreSQL backend
- **Zabbix Web UI** with Nginx
- **PostgreSQL 15** database
- **Zabbix Agent 2** for testing agent-based templates

All services use **official Zabbix Docker images** from Docker Hub.

## Prerequisites

- **Docker Engine** 20.10+ or Docker Desktop
- **Docker Compose** v2.0+ (or `docker-compose` v1.29+)
- At least 2GB of free RAM
- Ports 8080, 10050, and 10051 available on your host

## Quick Start

### 1. Start the Stack

```bash
# From the examples/ directory
cd examples

# Start all services in detached mode
docker compose up -d

# Check service status
docker compose ps

# View logs (optional)
docker compose logs -f
```

**Wait ~30–60 seconds** for all services to initialize. PostgreSQL and Zabbix Server need time to set up the database schema.

### 2. Access Zabbix Web UI

Open your browser and navigate to:

```
http://localhost:8080
```

**Default credentials:**
- **Username:** `Admin`
- **Password:** `zabbix`

⚠️ **Security Warning:** These are default demo credentials. **Never use this setup in production without changing passwords and hardening security.**

### 3. Verify Installation

After logging in:

1. Go to **Monitoring → Hosts**
2. You should see the "Zabbix server" host in the list
3. Check that the host is monitored and available (green ZBX icon)

### 4. Import and Test a Template

#### Option A: Via Web UI

1. Go to **Data collection → Templates** (or **Configuration → Templates** in older versions)
2. Click **Import**
3. Click **Choose File** and select a template XML from `../zbx-templates/`
   - For example: `../zbx-templates/zbx-linux/zbx-linux-generic/zbx-linux-generic.xml`
4. Review import options, then click **Import**
5. Go back to **Monitoring → Hosts**
6. Click on "Zabbix server" or "zabbix-agent2"
7. Go to the **Templates** tab
8. Click **Select**, choose the imported template, then **Add** → **Update**
9. Wait a few minutes for data collection
10. Go to **Monitoring → Latest data** and filter by the host to see collected metrics

#### Option B: Via API (Using tools/import_template.py)

```bash
# From the repository root
cd ..

# Install Python dependencies
pip install requests

# Import a template
python tools/import_template.py \
  --url http://localhost:8080 \
  --user Admin \
  --password zabbix \
  --template zbx-templates/zbx-cisco/zbx-cisco-interfaces/zbx-cisco-interfaces.xml
```

### 5. Testing SNMP Templates

The demo environment includes only Zabbix Server and Agent. To test **SNMP templates**:

**Option 1: Add SNMP simulator container**

Add this to `docker-compose.yml` under `services:`:

```yaml
  snmpsim:
    image: tandrup/snmpsim
    container_name: snmpsim
    restart: unless-stopped
    ports:
      - "161:161/udp"
    networks:
      - zabbix-net
```

Then:
```bash
docker compose up -d snmpsim
```

**Option 2: Monitor real network devices**

1. Ensure your network devices are reachable from the Docker host
2. Create a new host in Zabbix with the device IP
3. Set SNMP interface and community string macros
4. Link an appropriate template (e.g., Cisco, Fortinet)

### 6. Stop the Environment

```bash
# Stop all containers (data persists in volumes)
docker compose down

# Stop and remove volumes (DELETES ALL DATA)
docker compose down -v
```

## Accessing Templates from Inside Containers

The `docker-compose.yml` file mounts the repository's `zbx-templates/` and `zbx-scripts/` directories into the Zabbix Server container:

- **Templates:** `/opt/zabbix-templates` (read-only)
- **Scripts:** `/usr/lib/zabbix/externalscripts` (read-only)

You can access these from within the container:

```bash
# List templates
docker exec zabbix-server ls -la /opt/zabbix-templates

# Test a script
docker exec zabbix-server ls -la /usr/lib/zabbix/externalscripts
```

## Troubleshooting

### Services won't start

```bash
# Check logs
docker compose logs zabbix-server
docker compose logs postgres

# Verify ports are not already in use
sudo netstat -tulpn | grep -E '8080|10050|10051'

# Restart services
docker compose restart
```

### Can't connect to web UI

- Verify the container is running: `docker compose ps`
- Check if port 8080 is accessible: `curl http://localhost:8080`
- Check firewall rules on the host
- Try accessing via host IP: `http://192.168.x.x:8080`

### Database connection errors

- Wait longer (PostgreSQL needs time to initialize on first run)
- Check PostgreSQL health: `docker compose exec postgres pg_isready -U zabbix`
- View PostgreSQL logs: `docker compose logs postgres`

### Agent not connecting

- Check agent logs: `docker compose logs zabbix-agent2`
- Verify agent hostname matches Zabbix configuration
- Ensure firewall allows port 10050

### Templates don't discover items

- Check that macros are set correctly (e.g., `{$SNMP_COMMUNITY}`)
- Verify network connectivity to monitored devices
- Check Zabbix server logs: `docker compose logs zabbix-server | grep -i error`
- Review Discovery rules in the template

### External scripts not working

- Scripts are mounted read-only; copy them into the container if modifications are needed
- Verify script permissions and interpreter availability inside the container
- Test scripts manually: `docker exec -it zabbix-server /usr/lib/zabbix/externalscripts/script.sh`

## Customization

### Change Web UI Port

Edit `docker-compose.yml`:

```yaml
  zabbix-web:
    ports:
      - "8081:8080"  # Change 8080 to desired port
```

### Increase Poller Count (for more devices)

Edit `docker-compose.yml`:

```yaml
  zabbix-server:
    environment:
      ZBX_STARTPOLLERS: 10  # Increase from 5
```

### Change Database Password

Edit `docker-compose.yml` (update in both `postgres` and `zabbix-server` services):

```yaml
  postgres:
    environment:
      POSTGRES_PASSWORD: my_secure_password

  zabbix-server:
    environment:
      POSTGRES_PASSWORD: my_secure_password
```

Then recreate containers:
```bash
docker compose down -v
docker compose up -d
```

### Enable SNMP Trap Reception

Uncomment or add to `docker-compose.yml`:

```yaml
  zabbix-snmptraps:
    image: zabbix/zabbix-snmptraps:latest
    container_name: zabbix-snmptraps
    restart: unless-stopped
    ports:
      - "162:1162/udp"
    volumes:
      - snmptraps-data:/var/lib/zabbix/snmptraps
    networks:
      - zabbix-net
```

## Data Persistence

Data is stored in Docker volumes:

- `postgres-data` — PostgreSQL database (hosts, items, history, trends)
- `zabbix-server-data` — Zabbix Server internal data

To backup:

```bash
# Backup PostgreSQL database
docker compose exec -T postgres pg_dump -U zabbix zabbix > zabbix_backup_$(date +%Y%m%d).sql

# Restore from backup
cat zabbix_backup_20241117.sql | docker compose exec -T postgres psql -U zabbix zabbix
```

## Upgrading Zabbix Version

To upgrade to a newer Zabbix version:

1. Stop the stack: `docker compose down`
2. Edit `docker-compose.yml` and change image tags (e.g., `zabbix/zabbix-server-pgsql:6.4-alpine` → `zabbix/zabbix-server-pgsql:7.0-alpine`)
3. Pull new images: `docker compose pull`
4. Start the stack: `docker compose up -d`

⚠️ **Always backup your database before upgrading!**

## Security Considerations

This demo environment is **NOT production-ready**. Before deploying to production:

- ✅ Change all default passwords (database, Zabbix admin)
- ✅ Use strong, random passwords (32+ characters)
- ✅ Enable HTTPS with valid TLS certificates
- ✅ Restrict network access (firewall rules, Docker network isolation)
- ✅ Use SNMPv3 with encryption for device monitoring
- ✅ Enable Zabbix user authentication (LDAP, SAML, etc.)
- ✅ Regularly update Docker images and Zabbix versions
- ✅ Implement proper backup and disaster recovery
- ✅ Review and harden Zabbix configuration (disable guest access, etc.)

## Additional Resources

- **Zabbix Docker Documentation:** [https://www.zabbix.com/documentation/current/en/manual/installation/containers](https://www.zabbix.com/documentation/current/en/manual/installation/containers)
- **Zabbix Docker Hub:** [https://hub.docker.com/u/zabbix](https://hub.docker.com/u/zabbix)
- **PostgreSQL Docker Documentation:** [https://hub.docker.com/_/postgres](https://hub.docker.com/_/postgres)

## Getting Help

- **Repository Issues:** [https://github.com/ranas-mukminov/Zabbix-templates-and-scripts/issues](https://github.com/ranas-mukminov/Zabbix-templates-and-scripts/issues)
- **Zabbix Community Forums:** [https://www.zabbix.com/forum/](https://www.zabbix.com/forum/)
- **Professional Support:** [run-as-daemon.ru](https://run-as-daemon.ru)

---

**Happy monitoring! 🚀**
