# OpenELIS Rebranding & Mongolian Localization Guide

## Overview
This guide shows how to rebrand OpenELIS to your own name (e.g., "MongoLIS", "LabSys.mn") and fully localize to Mongolian language while maintaining compliance with Apache 2.0 License.

## Legal Compliance (Apache 2.0 License)

### ✅ What you CAN do:
- Change the product name displayed to users
- Modify all user-facing text and branding
- Add your own logo and colors
- Sell as commercial product
- Host on your own servers
- Make any code modifications
- **No need to inform original vendor**

### ⚠️ What you MUST do:
- Keep the LICENSE file in the source code
- Keep copyright notices in source code files
- Include a NOTICE file if you modify the code
- Make it clear this is "based on OpenELIS" in documentation (not in UI)

### ❌ What you CANNOT do:
- Remove the Apache 2.0 LICENSE file from repository
- Claim you wrote the original code
- Use "OpenELIS" trademark as your own product name

## Phase 1: Rebranding (Visual Identity)

### Step 1.1: Choose Your Brand Name

Examples:
- **MongoLIS** (Mongolia Laboratory Information System)
- **LabSys.mn** (Lab System Mongolia)
- **SmartLab** (Smart Laboratory)
- **EліS** (Electronic Laboratory Information System)

### Step 1.2: Update Application Title

**Frontend (React):**

File: `frontend/public/index.html`
```html
<!-- Change from: -->
<title>OpenELIS</title>

<!-- To: -->
<title>MongoLIS - Лабораторын мэдээллийн систем</title>
```

File: `frontend/src/components/layout/Header.js`
```javascript
// Change logo and title
const appTitle = "MongoLIS";
const appSubtitle = "Монгол Улс";
```

### Step 1.3: Replace Logo

**Create your logo files:**
```bash
# Your logo should be in these sizes:
frontend/public/logo192.png     # 192x192 px
frontend/public/logo512.png     # 512x512 px
frontend/public/favicon.ico     # 32x32 px
frontend/src/images/logo.svg    # Vector format
```

**Replace in React components:**
File: `frontend/src/components/layout/Header.js`
```javascript
import logo from '../../images/mongolab-logo.svg';  // Your logo

const Header = () => (
  <div className="header">
    <img src={logo} alt="MongoLIS" />
    <h1>МонгоЛИС</h1>
  </div>
);
```

### Step 1.4: Update Color Theme

File: `frontend/src/styles/variables.scss`
```scss
// Change from OpenELIS blue to your brand colors
$primary-color: #0066CC;      // Your primary color
$secondary-color: #FF9900;    // Your secondary color
$accent-color: #00AA66;       // Your accent color

// Mongolia flag colors example:
// $primary-color: #C4272F;    // Red
// $secondary-color: #015197;   // Blue
// $accent-color: #FFD900;      // Yellow
```

## Phase 2: Mongolian Localization

### Step 2.1: Set Up Translation Files

OpenELIS uses i18n (internationalization). Add Mongolian language:

File: `frontend/src/i18n/locales/mn.json` (CREATE NEW)
```json
{
  "header": {
    "title": "МонгоЛИС",
    "subtitle": "Лабораторын мэдээллийн систем"
  },
  "menu": {
    "home": "Нүүр",
    "patient": "Өвчтөн",
    "order": "Захиалга",
    "results": "Үр дүн",
    "reports": "Тайлан",
    "admin": "Удирдлага"
  },
  "patient": {
    "registration": "Өвчтөн бүртгэх",
    "search": "Өвчтөн хайх",
    "firstName": "Нэр",
    "lastName": "Овог",
    "nationalId": "Регистрийн дугаар",
    "birthDate": "Төрсөн огноо",
    "gender": "Хүйс",
    "male": "Эрэгтэй",
    "female": "Эмэгтэй",
    "phoneNumber": "Утасны дугаар",
    "address": "Хаяг"
  },
  "sample": {
    "collection": "Дээж авах",
    "barcode": "Баркод",
    "collectionDate": "Дээж авсан огноо",
    "collectionTime": "Дээж авсан цаг",
    "sampleType": "Дээжийн төрөл",
    "blood": "Цус",
    "urine": "Шээс",
    "stool": "Баас",
    "sputum": "Цэрэгцлэх"
  },
  "test": {
    "name": "Шинжилгээний нэр",
    "section": "Хэсэг",
    "method": "Арга",
    "result": "Үр дүн",
    "unit": "Нэгж",
    "normalRange": "Хэвийн хэмжээ",
    "status": "Төлөв",
    "pending": "Хүлээгдэж буй",
    "inProgress": "Гүйцэтгэж буй",
    "completed": "Дууссан",
    "validated": "Баталгаажсан"
  },
  "buttons": {
    "save": "Хадгалах",
    "cancel": "Цуцлах",
    "search": "Хайх",
    "print": "Хэвлэх",
    "submit": "Илгээх",
    "edit": "Засах",
    "delete": "Устгах",
    "add": "Нэмэх"
  }
}
```

### Step 2.2: Configure Default Language

File: `frontend/src/i18n/config.js`
```javascript
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import mn from './locales/mn.json';
import en from './locales/en.json';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      mn: { translation: mn },  // Mongolian
      en: { translation: en }   // English (fallback)
    },
    lng: 'mn',                  // Default language: Mongolian
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
```

### Step 2.3: Update Database Test Catalog

Create Mongolia-specific test catalog:

File: `db/mongo_test_catalog.sql` (CREATE NEW)
```sql
-- Delete Haiti demo tests
DELETE FROM clinlims.test WHERE description LIKE '%Charge virale%';
DELETE FROM clinlims.test WHERE description LIKE '%Hémoglobine%';

-- Add Mongolian test catalog
-- General Chemistry
INSERT INTO clinlims.test (id, description, test_section_id, is_active, sort_order) VALUES
(gen_random_uuid(), 'Цусны сахар (Глюкоз)', (SELECT id FROM clinlims.test_section WHERE name='Biochemistry'), 'Y', 10),
(gen_random_uuid(), 'Холестерол', (SELECT id FROM clinlims.test_section WHERE name='Biochemistry'), 'Y', 20),
(gen_random_uuid(), 'Триглицерид', (SELECT id FROM clinlims.test_section WHERE name='Biochemistry'), 'Y', 30),
(gen_random_uuid(), 'Креатинин', (SELECT id FROM clinlims.test_section WHERE name='Biochemistry'), 'Y', 40),
(gen_random_uuid(), 'Мочевин (BUN)', (SELECT id FROM clinlims.test_section WHERE name='Biochemistry'), 'Y', 50),
(gen_random_uuid(), 'АЛТ (SGPT)', (SELECT id FROM clinlims.test_section WHERE name='Biochemistry'), 'Y', 60),
(gen_random_uuid(), 'АСТ (SGOT)', (SELECT id FROM clinlims.test_section WHERE name='Biochemistry'), 'Y', 70);

-- Hematology
INSERT INTO clinlims.test (id, description, test_section_id, is_active, sort_order) VALUES
(gen_random_uuid(), 'Цусны ерөнхий шинжилгээ (ЦЕШ)', (SELECT id FROM clinlims.test_section WHERE name='Hematology'), 'Y', 10),
(gen_random_uuid(), 'Гемоглобин', (SELECT id FROM clinlims.test_section WHERE name='Hematology'), 'Y', 20),
(gen_random_uuid(), 'Цагаан эс (WBC)', (SELECT id FROM clinlims.test_section WHERE name='Hematology'), 'Y', 30),
(gen_random_uuid(), 'Улаан эс (RBC)', (SELECT id FROM clinlims.test_section WHERE name='Hematology'), 'Y', 40),
(gen_random_uuid(), 'Тромбоцит', (SELECT id FROM clinlims.test_section WHERE name='Hematology'), 'Y', 50),
(gen_random_uuid(), 'ESR (ХЖХ)', (SELECT id FROM clinlims.test_section WHERE name='Hematology'), 'Y', 60);

-- Microbiology
INSERT INTO clinlims.test (id, description, test_section_id, is_active, sort_order) VALUES
(gen_random_uuid(), 'Шээсний ерөнхий шинжилгээ', (SELECT id FROM clinlims.test_section WHERE name='ECBU'), 'Y', 10),
(gen_random_uuid(), 'Шээсний бактерийн өсгөвөр', (SELECT id FROM clinlims.test_section WHERE name='Bacteria'), 'Y', 20),
(gen_random_uuid(), 'Баасны шинжилгээ', (SELECT id FROM clinlims.test_section WHERE name='Parasitology'), 'Y', 30),
(gen_random_uuid(), 'Цэрэгцлэхний ARB шинжилгээ', (SELECT id FROM clinlims.test_section WHERE name='Mycobacteriology'), 'Y', 40);

-- Serology/Immunology
INSERT INTO clinlims.test (id, description, test_section_id, is_active, sort_order) VALUES
(gen_random_uuid(), 'ХИВ-ийн эсрэг бие (HIV)', (SELECT id FROM clinlims.test_section WHERE name='Serology-Immunology'), 'Y', 10),
(gen_random_uuid(), 'Элэгний В вирус (HBsAg)', (SELECT id FROM clinlims.test_section WHERE name='Serology-Immunology'), 'Y', 20),
(gen_random_uuid(), 'Элэгний С вирус (HCV)', (SELECT id FROM clinlims.test_section WHERE name='Serology-Immunology'), 'Y', 30),
(gen_random_uuid(), 'Сифилис (VDRL)', (SELECT id FROM clinlims.test_section WHERE name='Serology-Immunology'), 'Y', 40);
```

Apply changes:
```bash
docker exec -i openelisglobal-database psql -U clinlims -d clinlims < db/mongo_test_catalog.sql
```

### Step 2.4: Translate Report Templates

File: `src/main/resources/reports/patient_report_mn.jrxml` (CREATE NEW)

Example JRXML for Mongolian report:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<jasperReport>
  <title>
    <band height="50">
      <staticText>
        <text>ЛАБОРАТОРЫН ҮР ДҮНГИЙН ХУУДАС</text>
      </staticText>
    </band>
  </title>
  <pageHeader>
    <staticText>
      <text>Өвчтөний нэр:</text>
    </staticText>
    <textField>
      <textFieldExpression>$F{patient_name}</textFieldExpression>
    </textField>
  </pageHeader>
  <!-- Add more Mongolian report sections -->
</jasperReport>
```

## Phase 3: Domain & Branding Deployment

### Step 3.1: Domain Registration

**Mongolia Domain Registrars:**
1. **Datacom** (datacom.mn)
   - Price: ₮15,000-30,000/year
   - Process: 1-2 days

2. **Univision** (univision.mn)
   - Price: ₮12,000-25,000/year
   - Process: Same day

**Suggested domains:**
- `lis.mn` (if available)
- `mongolab.mn`
- `mongollis.mn`
- `labsys.mn`

### Step 3.2: Update Docker Compose for Your Brand

File: `docker-compose.yml`
```yaml
services:
  # Change service names to your brand
  database:
    container_name: mongolab-database  # Changed from openelisglobal-database
    
  webapp:
    container_name: mongolab-backend   # Changed from openelisglobal-webapp
    environment:
      - APP_NAME=MongoLIS              # Your brand name
      - APP_LOCALE=mn_MN               # Mongolian locale
    
  frontend:
    container_name: mongolab-frontend  # Changed from openelisglobal-frontend
```

### Step 3.3: Build Custom Docker Images

Create build script:

File: `build_mongolab.sh`
```bash
#!/bin/bash
# Build MongoLIS branded Docker images

BRAND_NAME="mongolab"
VERSION="1.0.0"

echo "Building ${BRAND_NAME} Docker images..."

# Build frontend with Mongolian translations
cd frontend
docker build -t ${BRAND_NAME}/frontend:${VERSION} \
  --build-arg DEFAULT_LANG=mn \
  --build-arg APP_NAME="MongoLIS" .

# Build backend
cd ../
docker build -t ${BRAND_NAME}/backend:${VERSION} \
  --build-arg APP_LOCALE=mn_MN .

echo "Build complete!"
echo "Images created:"
echo "  - ${BRAND_NAME}/frontend:${VERSION}"
echo "  - ${BRAND_NAME}/backend:${VERSION}"
```

Make executable and run:
```bash
chmod +x build_mongolab.sh
./build_mongolab.sh
```

## Phase 4: Legal Compliance Documentation

### Step 4.1: Create NOTICE File

File: `NOTICE` (CREATE in root directory)
```
MongoLIS (Mongolia Laboratory Information System)
Copyright 2026 [Your Organization Name]

This product includes software developed by the OpenELIS-Global project
(https://github.com/I-TECH-UW/OpenELIS-Global-2)

OpenELIS-Global is licensed under the Apache License, Version 2.0
See LICENSE file for full license text.

Modifications made by [Your Organization]:
- Mongolian language localization
- Custom branding and user interface
- Mongolia-specific test catalog
- [List other major modifications]
```

### Step 4.2: Update README

File: `README.md`
```markdown
# MongoLIS - Лабораторын мэдээллийн систем

Mongolia Laboratory Information System - Монгол Улсын эрүүл мэнд, 
лабораторийн үйлчилгээний цахим систем.

## Based On
This system is based on [OpenELIS-Global](https://github.com/I-TECH-UW/OpenELIS-Global-2), 
an open-source laboratory information system, and is licensed under 
Apache License 2.0.

## Mongolian Customizations
- Full Mongolian language interface
- Mongolia-specific test catalog
- Local healthcare regulations compliance
- Custom reporting for Mongolian labs

## License
Apache License 2.0 - See LICENSE file
```

## Phase 5: Deployment to Your Server

### Step 5.1: Your Server Requirements

**Minimum specs:**
- Ubuntu 22.04 LTS or similar
- 8GB RAM (16GB recommended for production)
- 4 CPU cores
- 100GB SSD storage
- Static IP address
- Ports 80, 443, 22 open

### Step 5.2: Deploy to Your Internal Server

```bash
# SSH to your server
ssh admin@your-server.internal.mn

# Clone your customized version
cd /opt
git clone https://github.com/YourOrg/MongoLIS.git
cd MongoLIS

# Deploy with your custom images
docker compose up -d
```

### Step 5.3: Configure Nginx for Your Domain

```bash
# Install Nginx
sudo apt install nginx -y

# Create configuration
sudo nano /etc/nginx/sites-available/mongolab.mn
```

```nginx
server {
    listen 80;
    server_name lis.mn www.lis.mn;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/mongolab.mn /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Phase 6: Quality Assurance

### Testing Checklist

**Visual Branding:**
- [ ] Logo displays correctly on all pages
- [ ] App title shows your brand name (not "OpenELIS")
- [ ] Colors match your brand guidelines
- [ ] Favicon updated in browser tab

**Mongolian Localization:**
- [ ] All menu items in Mongolian
- [ ] Patient registration form in Mongolian
- [ ] Test names in Mongolian
- [ ] Reports print in Mongolian
- [ ] Date/time format: YYYY-MM-DD (ISO 8601)
- [ ] Number format: Mongolian style

**Functionality:**
- [ ] Patient registration works
- [ ] Sample collection generates barcodes
- [ ] Test results entry works
- [ ] Reports generate correctly
- [ ] Database backup runs daily
- [ ] User accounts can login

**Legal Compliance:**
- [ ] LICENSE file present in code
- [ ] NOTICE file created with attribution
- [ ] README mentions OpenELIS origin
- [ ] No "OpenELIS" branding visible to end users

## Support & Maintenance

### Your Team Needs:
1. **System Administrator** (1 person)
   - Server maintenance
   - Backup management
   - Security updates

2. **Lab Director** (1 person)
   - Test catalog management
   - Quality control
   - User training

3. **Developer** (1 person, part-time)
   - Custom features
   - Mongolian translations
   - Bug fixes

### Update Schedule:
- **Monthly:** Check OpenELIS-Global updates
- **Quarterly:** Merge important security patches
- **Annually:** Major version updates (plan 2-3 week project)

---

## Quick Start Commands

```bash
# 1. Check domain availability
whois lis.mn

# 2. Build custom images
./build_mongolab.sh

# 3. Deploy locally (test)
docker compose up -d

# 4. Deploy to your server
ssh admin@your-server
cd /opt/MongoLIS
docker compose -f docker-compose.prod.yml up -d

# 5. Check logs
docker compose logs -f

# 6. Backup database
./backup_mongolab.sh
```

## Cost Estimate

| Item | One-Time | Annual | Notes |
|------|----------|--------|-------|
| Domain (lis.mn) | - | ₮20,000 | Datacom/Univision |
| Rebranding work | ₮500,000 | - | 1 week developer time |
| Mongolian translation | ₮800,000 | - | 2 weeks translator + dev |
| Your server | ₮0 | ₮0 | Already have |
| SSL certificate | ₮0 | ₮0 | Let's Encrypt free |
| Maintenance | - | ₮1,200,000 | Part-time developer |
| **Total Year 1** | **₮1,300,000** | **₮1,220,000** | - |
| **Total Year 2+** | - | **₮1,220,000** | Annual only |

**Timeline:**
- Domain registration: 1-2 days
- Rebranding: 1 week
- Mongolian translation: 2-3 weeks
- Testing: 1 week
- **Total: 4-5 weeks to launch**

---

**Questions? Contact:**
- Email: [your-email]
- Phone: [your-phone]
- Slack: [your-workspace]
```

