# OpenELIS Cloud Deployment Guide (Mongolia)

## Prerequisites
- Cloud server (Ubuntu 22.04 LTS recommended)
- Domain name (e.g., openelis.mn or demo.openelis.mn)
- SSH access to server
- 4GB RAM minimum, 8GB recommended
- 50GB disk space

## Step 1: Cloud Server Setup

### Option A: DigitalOcean (Recommended)
```bash
# Create Droplet:
# - Ubuntu 22.04 LTS
# - 4GB RAM / 2 CPU ($24/month)
# - San Francisco or Singapore datacenter (closest to Mongolia)
# - Add SSH key for secure access
```

### Option B: AWS Lightsail
```bash
# Create Instance:
# - OS: Linux/Unix → Ubuntu 22.04 LTS
# - Plan: $20/month (2GB RAM) or $40/month (4GB RAM)
# - Add firewall rules: 22 (SSH), 80 (HTTP), 443 (HTTPS)
```

## Step 2: Server Initial Configuration

SSH into your server:
```bash
ssh root@your-server-ip
```

Update system and install Docker:
```bash
# Update package list
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose-plugin -y

# Verify installation
docker --version
docker compose version
```

## Step 3: Deploy OpenELIS

Clone repository:
```bash
cd /opt
git clone https://github.com/I-TECH-UW/OpenELIS-Global-2.git openelis
cd openelis
git checkout develop
```

Create production configuration:
```bash
# Copy docker-compose and modify for production
cp docker-compose.yml docker-compose.prod.yml
```

Edit `docker-compose.prod.yml` for production:
```yaml
# Change these settings:
services:
  database:
    environment:
      # CHANGE DEFAULT PASSWORDS!
      POSTGRES_PASSWORD: "YOUR_STRONG_PASSWORD_HERE"  # Change from clinlims
  
  oe.openelis.org:
    environment:
      # CHANGE DEFAULT ADMIN PASSWORD
      DEFAULT_PW: "YOUR_ADMIN_PASSWORD_HERE"  # Change from adminADMIN!
    
    # Add resource limits
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
```

Start OpenELIS:
```bash
docker compose -f docker-compose.prod.yml up -d
```

## Step 4: Domain Configuration

### Buy Domain Name
- **Mongolia:** datacom.mn, univision.mn (₮15,000-30,000/year)
- **International:** namecheap.com, cloudflare.com ($10-15/year)

Suggested names:
- `demo.openelis.mn`
- `openelis-demo.mn`
- `lab.yourcompany.mn`

### Configure DNS Records
Add these records in your domain registrar:

```
Type    Name    Value               TTL
A       @       your-server-ip      300
A       www     your-server-ip      300
AAAA    @       your-ipv6 (optional) 300
```

Wait 5-30 minutes for DNS propagation.

## Step 5: SSL Certificate (HTTPS)

Install Certbot for free SSL:
```bash
# Install Certbot
apt install certbot python3-certbot-nginx -y

# Stop OpenELIS proxy temporarily
docker compose -f docker-compose.prod.yml stop proxy

# Install Nginx on host (for Certbot)
apt install nginx -y

# Get SSL certificate
certbot --nginx -d demo.openelis.mn -d www.demo.openelis.mn
```

Configure OpenELIS proxy for SSL:
```bash
# Copy SSL certs to OpenELIS
mkdir -p /opt/openelis/volumes/ssl
cp /etc/letsencrypt/live/demo.openelis.mn/fullchain.pem /opt/openelis/volumes/ssl/
cp /etc/letsencrypt/live/demo.openelis.mn/privkey.pem /opt/openelis/volumes/ssl/

# Update docker-compose.prod.yml proxy service
# Mount SSL certificates
```

Restart services:
```bash
docker compose -f docker-compose.prod.yml restart
```

## Step 6: Firewall Configuration

Set up UFW firewall:
```bash
# Enable firewall
ufw enable

# Allow SSH (IMPORTANT: do this first!)
ufw allow 22/tcp

# Allow HTTP and HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Check status
ufw status
```

## Step 7: Backup Configuration

Create daily backup script:
```bash
nano /opt/backup-openelis.sh
```

```bash
#!/bin/bash
# OpenELIS Database Backup Script

BACKUP_DIR="/opt/openelis-backups"
DATE=$(date +%Y%m%d_%H%M%S)
CONTAINER="openelisglobal-database"

mkdir -p $BACKUP_DIR

# Backup database
docker exec $CONTAINER pg_dump -U clinlims -d clinlims -F c -f /tmp/backup_$DATE.dump

# Copy from container to host
docker cp $CONTAINER:/tmp/backup_$DATE.dump $BACKUP_DIR/

# Remove old backups (keep last 7 days)
find $BACKUP_DIR -name "*.dump" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR/backup_$DATE.dump"
```

Make executable and schedule:
```bash
chmod +x /opt/backup-openelis.sh

# Add to cron (runs daily at 2 AM)
crontab -e
# Add this line:
0 2 * * * /opt/backup-openelis.sh >> /var/log/openelis-backup.log 2>&1
```

## Step 8: Security Hardening

### Change Default Passwords
```bash
# Access database
docker exec -it openelisglobal-database psql -U clinlims -d clinlims

-- Change admin password
UPDATE clinlims.system_user 
SET password = md5('YourNewSecurePassword123!') 
WHERE login_name = 'admin';

\q
```

### Disable Demo Data (for Production)
```sql
-- Delete demo test results
DELETE FROM clinlims.analysis;
DELETE FROM clinlims.sample;
DELETE FROM clinlims.patient;

-- Keep test catalog but remove Haiti-specific tests
UPDATE clinlims.test SET is_active='N' 
WHERE description LIKE '%Charge virale%';  -- Remove French tests
```

### Set up fail2ban (prevent brute force)
```bash
apt install fail2ban -y
systemctl enable fail2ban
```

## Step 9: Monitoring

### Check service health
```bash
# View running containers
docker compose -f docker-compose.prod.yml ps

# Check logs
docker compose -f docker-compose.prod.yml logs -f --tail=100

# Check resource usage
docker stats
```

### Install monitoring (optional)
```bash
# Install htop for system monitoring
apt install htop -y

# Install netdata for web-based monitoring
bash <(curl -Ss https://my-netdata.io/kickstart.sh)
# Access at http://your-server-ip:19999
```

## Step 10: User Access

Share with your team:
```
URL: https://demo.openelis.mn
Username: admin
Password: [Your new password]

Demo accounts (create these in UI):
- Lab Technician: labtech / Password123!
- Doctor: doctor / Password123!
- Data Entry: dataentry / Password123!
```

## Cost Summary (Monthly)

| Item | Cost (USD) | Cost (MNT) | Notes |
|------|-----------|------------|-------|
| DigitalOcean VPS | $24 | ₮82,000 | 4GB RAM, 2 CPU |
| Domain Name | $1 | ₮3,500 | Yearly ÷ 12 |
| SSL Certificate | $0 | ₮0 | Let's Encrypt (free) |
| Backup Storage | $5 | ₮17,000 | 100GB DigitalOcean Spaces |
| **Total** | **$30** | **₮102,500** | Per month |

## Maintenance Schedule

**Daily:**
- Automatic database backup (2 AM)
- SSL certificate auto-renewal check

**Weekly:**
- Check disk space: `df -h`
- Review error logs: `docker compose logs --tail=500`

**Monthly:**
- Update Docker images: `docker compose pull && docker compose up -d`
- Review user activity: Check patient/sample counts
- Database cleanup: Archive old completed tests

**Quarterly:**
- System updates: `apt update && apt upgrade`
- Security audit: Review user accounts, check failed login attempts
- Performance review: Analyze response times

## Troubleshooting

### Container won't start
```bash
# Check logs
docker compose -f docker-compose.prod.yml logs database webapp

# Restart all services
docker compose -f docker-compose.prod.yml restart

# Full reset (WARNING: loses data)
docker compose -f docker-compose.prod.yml down -v
docker compose -f docker-compose.prod.yml up -d
```

### Out of disk space
```bash
# Check usage
df -h

# Clean Docker cache
docker system prune -a --volumes

# Remove old backups
find /opt/openelis-backups -name "*.dump" -mtime +30 -delete
```

### Slow performance
```bash
# Check resource usage
docker stats

# Increase container memory limits in docker-compose.prod.yml
# Add under webapp service:
    deploy:
      resources:
        limits:
          memory: 3G
```

## Support Resources

- **OpenELIS Documentation:** https://docs.openelis-global.org/
- **GitHub Issues:** https://github.com/I-TECH-UW/OpenELIS-Global-2/issues
- **Community Chat:** OpenELIS Slack workspace
- **Email Support:** openelisglobal@uw.edu

## Next Steps After Deployment

1. **Create user accounts** for your team (Lab → User Management)
2. **Configure test catalog** for Mongolia (Admin → Test Management)
3. **Add facilities** (Admin → Organization Management)
4. **Import patient data** (if migrating from existing system)
5. **Train staff** on patient registration, sample collection, result entry
6. **Set up reports** (Reports → Configure Report Templates)
7. **Enable FHIR API** for integration with EMR systems (if needed)

---

**Deployment Time Estimate:** 2-4 hours for experienced admin, 4-8 hours for first-time deployment

**Recommended Team:** 
- 1 System Administrator (server setup)
- 1 Lab Director (test catalog configuration)
- 1 Trainer (user onboarding)
