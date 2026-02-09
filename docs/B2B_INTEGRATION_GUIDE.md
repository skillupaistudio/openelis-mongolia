# B2B System ↔ OpenELIS Integration Guide

## Товч хариулт

**✅ Тийм, бүрэн боломжтой!**

B2B захиалгын систем (Server 1) ба OpenELIS (Server 2) хоорондоо **REST API** эсвэл **FHIR API** ашиглан холбогдож болно.

```
┌─────────────────────┐          ┌─────────────────────┐
│  B2B Order System   │  ←────→  │   OpenELIS LIMS     │
│  (Server 1)         │   APIs   │   (Server 2)        │
│                     │          │                     │
│  - E-commerce       │          │  - Lab Tests        │
│  - Order Management │          │  - Patient Registry │
│  - Inventory        │          │  - Sample Tracking  │
│  - Billing          │          │  - Results          │
└─────────────────────┘          └─────────────────────┘

   MongoDB/MySQL               PostgreSQL (clinlims)
```

**Холбох хэрэгсэл:**
1. **FHIR API** (Standard, өргөн хэрэглэгддэг)
2. **REST API** (Custom endpoints)
3. **Message Queue** (RabbitMQ/Kafka - async)
4. **Webhooks** (Event-driven)

---

## 1. OpenELIS Integration Capabilities

### 1.1 FHIR API (HL7 FHIR R4)

OpenELIS аль хэдийн **FHIR server** суулгасан байна:

**Docker Compose-с:**
```yaml
fhir.openelis.org:
    container_name: external-fhir-api
    image: itechuw/openelis-global-2-fhir:develop
    ports:
        - "8081:8080"   # HTTP
        - "8444:8443"   # HTTPS
    environment:
      FHIR_SERVER_ADRESS: "http://fhir.openelis.org:8080/fhir/"
      FHIR_DATASOURCE_URL: "jdbc:postgresql://db.openelis.org:5432/clinlims"
```

**FHIR Resources (OpenELIS дэмжсэн):**
- ✅ `Patient` - Өвчтөний мэдээлэл
- ✅ `ServiceRequest` - Лабораторын захиалга
- ✅ `DiagnosticReport` - Шинжилгээний үр дүн
- ✅ `Observation` - Тест үр дүнгийн утга
- ✅ `Specimen` - Дээжийн мэдээлэл
- ✅ `Organization` - Эмнэлэг/Лабораторын мэдээлэл
- ✅ `Practitioner` - Эмч/Лаборанты мэдээлэл
- ✅ `Task` - Лабын даалгавар

**Base URL:**
```
http://openelis-server.mn:8081/fhir/
https://openelis-server.mn:8444/fhir/
```

---

### 1.2 REST API Endpoints

OpenELIS-д олон REST endpoints байна:

**Source code:**
```java
// File: FhirQueryRestController.java
@RestController
@RequestMapping("/rest/fhir")
public class FhirQueryRestController {
    
    @GetMapping(value = "/{resourceType}")
    public ResponseEntity<?> queryFhirResources(
        @PathVariable("resourceType") String resourceType,
        @RequestParam(required = false) Integer count
    ) {
        // FHIR ресурс хайх
    }
}
```

**Available REST endpoints:**
```
GET  /rest/fhir/Patient?identifier=12345
GET  /rest/fhir/ServiceRequest?patient=Patient/123
GET  /rest/fhir/DiagnosticReport?patient=Patient/123
POST /rest/fhir/ServiceRequest
PUT  /rest/fhir/ServiceRequest/123
GET  /rest/WorkPlanByTest
GET  /rest/WorkPlanByTestSection
POST /rest/PrintWorkplanReport
```

---

## 2. Integration Scenarios

### Scenario 1: B2B → OpenELIS (Test захиалга илгээх)

**Use Case:**  
Эмнэлгийн эмч B2B системээр лабораторын шинжилгээ захиална. Захиалга автоматаар OpenELIS-д илгээгдэх ёстой.

**Architecture:**

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│  B2B Web UI  │         │  B2B Backend │         │   OpenELIS   │
│   (Doctor)   │────────→│   (Node.js)  │────────→│   FHIR API   │
└──────────────┘         └──────────────┘         └──────────────┘
                              │                         │
                              ↓                         ↓
                         MongoDB                  PostgreSQL
```

**Implementation:**

**B2B Backend (Node.js):**

```javascript
// File: services/labOrderService.js
const axios = require('axios');

const OPENELIS_FHIR_URL = 'https://openelis-server.mn:8444/fhir';
const FHIR_AUTH_TOKEN = 'Bearer eyJhbGc...'; // OAuth token

class LabOrderService {
  
  /**
   * B2B системээс OpenELIS рүү лабын захиалга илгээх
   */
  async createLabOrder(orderData) {
    // 1. Patient бүртгэх/шалгах
    const patient = await this.ensurePatient(orderData.patient);
    
    // 2. ServiceRequest (лабын захиалга) үүсгэх
    const serviceRequest = {
      resourceType: "ServiceRequest",
      status: "active",
      intent: "order",
      subject: {
        reference: `Patient/${patient.id}`
      },
      code: {
        coding: [{
          system: "http://loinc.org",
          code: "24331-1",  // LOINC code (жнь: Lipid Panel)
          display: "Липидийн шинжилгээ"
        }]
      },
      requester: {
        reference: `Practitioner/${orderData.doctorId}`
      },
      specimen: [{
        reference: `Specimen/${orderData.specimenId}`
      }],
      authoredOn: new Date().toISOString(),
      priority: "routine",
      note: [{
        text: orderData.clinicalNotes
      }]
    };
    
    // 3. OpenELIS FHIR API-д илгээх
    const response = await axios.post(
      `${OPENELIS_FHIR_URL}/ServiceRequest`,
      serviceRequest,
      {
        headers: {
          'Authorization': FHIR_AUTH_TOKEN,
          'Content-Type': 'application/fhir+json'
        }
      }
    );
    
    console.log('✅ OpenELIS order created:', response.data.id);
    
    // 4. B2B database-д OpenELIS ID хадгалах
    await this.saveOrderMapping({
      b2bOrderId: orderData.orderId,
      openelisServiceRequestId: response.data.id,
      status: 'submitted'
    });
    
    return response.data;
  }
  
  /**
   * Patient бүртгэх (хэрэв OpenELIS-д байхгүй бол)
   */
  async ensurePatient(patientData) {
    // OpenELIS-д patient шалгах
    const searchResponse = await axios.get(
      `${OPENELIS_FHIR_URL}/Patient`,
      {
        params: {
          identifier: patientData.nationalId
        },
        headers: { 'Authorization': FHIR_AUTH_TOKEN }
      }
    );
    
    if (searchResponse.data.total > 0) {
      // Patient аль хэдийн байна
      return searchResponse.data.entry[0].resource;
    }
    
    // Шинээр patient бүртгэх
    const newPatient = {
      resourceType: "Patient",
      identifier: [{
        system: "http://health.mn/national-id",
        value: patientData.nationalId
      }],
      name: [{
        family: patientData.lastName,
        given: [patientData.firstName]
      }],
      gender: patientData.gender,
      birthDate: patientData.birthDate,
      telecom: [{
        system: "phone",
        value: patientData.phoneNumber
      }]
    };
    
    const createResponse = await axios.post(
      `${OPENELIS_FHIR_URL}/Patient`,
      newPatient,
      { headers: { 'Authorization': FHIR_AUTH_TOKEN, 'Content-Type': 'application/fhir+json' }}
    );
    
    return createResponse.data;
  }
}

module.exports = new LabOrderService();
```

**B2B API Endpoint:**

```javascript
// File: routes/labOrders.js
const express = require('express');
const router = express.Router();
const labOrderService = require('../services/labOrderService');

/**
 * POST /api/lab-orders
 * Лабын захиалга үүсгэх (OpenELIS-д илгээнэ)
 */
router.post('/lab-orders', async (req, res) => {
  try {
    const orderData = {
      orderId: req.body.orderId,
      patient: {
        nationalId: req.body.patient.nationalId,
        firstName: req.body.patient.firstName,
        lastName: req.body.patient.lastName,
        gender: req.body.patient.gender,
        birthDate: req.body.patient.birthDate,
        phoneNumber: req.body.patient.phone
      },
      doctorId: req.body.doctorId,
      testCode: req.body.testCode,  // LOINC code
      specimenType: req.body.specimenType,  // blood, urine, etc.
      clinicalNotes: req.body.notes
    };
    
    const result = await labOrderService.createLabOrder(orderData);
    
    res.json({
      success: true,
      message: 'Лабын захиалга OpenELIS-д амжилттай илгээгдлээ',
      openelisOrderId: result.id,
      b2bOrderId: orderData.orderId
    });
    
  } catch (error) {
    console.error('❌ Lab order creation failed:', error);
    res.status(500).json({
      success: false,
      message: 'Захиалга илгээхэд алдаа гарлаа',
      error: error.message
    });
  }
});

module.exports = router;
```

---

### Scenario 2: OpenELIS → B2B (Үр дүн буцаах)

**Use Case:**  
Лаборатори шинжилгээ дуусаад үр дүн бэлэн болсон. B2B систем автоматаар үр дүнг татаж авах, эмчид мэдэгдэх.

**Architecture:**

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   OpenELIS   │         │  B2B Backend │         │  B2B Web UI  │
│  (Lab Tech)  │────────→│  (Webhook)   │────────→│   (Doctor)   │
└──────────────┘         └──────────────┘         └──────────────┘
    Result                  Push notification       Email/SMS
    validated               Update order status     Dashboard alert
```

**Implementation:**

**OpenELIS Webhook Configuration:**

OpenELIS нь result validated үед webhook илгээх боломжтой.

**B2B Webhook Receiver:**

```javascript
// File: routes/webhooks.js
const express = require('express');
const router = express.Router();
const axios = require('axios');

const OPENELIS_FHIR_URL = 'https://openelis-server.mn:8444/fhir';

/**
 * POST /webhooks/openelis/result-ready
 * OpenELIS-с үр дүн бэлэн болсон webhook
 */
router.post('/openelis/result-ready', async (req, res) => {
  try {
    const webhookData = req.body;
    
    console.log('📥 Received OpenELIS webhook:', webhookData);
    
    // 1. ServiceRequest ID-гаар DiagnosticReport татах
    const serviceRequestId = webhookData.serviceRequestId;
    
    const diagnosticReport = await axios.get(
      `${OPENELIS_FHIR_URL}/DiagnosticReport`,
      {
        params: {
          basedOn: `ServiceRequest/${serviceRequestId}`
        },
        headers: { 'Authorization': process.env.FHIR_AUTH_TOKEN }
      }
    );
    
    if (diagnosticReport.data.total === 0) {
      return res.status(404).json({ error: 'DiagnosticReport not found' });
    }
    
    const report = diagnosticReport.data.entry[0].resource;
    
    // 2. Observation (үр дүнгийн утгууд) татах
    const observations = await Promise.all(
      report.result.map(ref => 
        axios.get(`${OPENELIS_FHIR_URL}/${ref.reference}`, {
          headers: { 'Authorization': process.env.FHIR_AUTH_TOKEN }
        })
      )
    );
    
    // 3. B2B database-д хадгалах
    const results = observations.map(obs => ({
      testName: obs.data.code.coding[0].display,
      value: obs.data.valueQuantity?.value,
      unit: obs.data.valueQuantity?.unit,
      normalRange: obs.data.referenceRange?.[0]?.text,
      status: obs.data.status,
      interpretation: obs.data.interpretation?.[0]?.text
    }));
    
    await saveLabResults({
      openelisReportId: report.id,
      serviceRequestId: serviceRequestId,
      patientId: report.subject.reference.split('/')[1],
      results: results,
      reportDate: report.issued,
      status: 'completed'
    });
    
    // 4. Эмчид мэдэгдэл илгээх
    await notifyDoctor({
      patientName: webhookData.patientName,
      testName: webhookData.testName,
      status: 'Үр дүн бэлэн боллоо'
    });
    
    // 5. SMS/Email илгээх
    await sendResultNotification({
      phone: webhookData.patientPhone,
      message: `Сайн байна уу! Таны ${webhookData.testName} шинжилгээний үр дүн бэлэн боллоо. Эмчээсээ дэлгэрэнгүй мэдээлэл авна уу.`
    });
    
    res.json({ success: true, message: 'Webhook processed' });
    
  } catch (error) {
    console.error('❌ Webhook processing failed:', error);
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
```

**Polling Alternative (Webhook байхгүй бол):**

```javascript
// File: jobs/pollOpenELISResults.js
const cron = require('node-cron');
const axios = require('axios');

/**
 * OpenELIS-с үр дүн татах (5 минут тутам)
 */
cron.schedule('*/5 * * * *', async () => {
  console.log('🔄 Polling OpenELIS for new results...');
  
  try {
    // Pending orders-г B2B database-с татах
    const pendingOrders = await getPendingLabOrders();
    
    for (const order of pendingOrders) {
      // OpenELIS-с DiagnosticReport шалгах
      const response = await axios.get(
        `${OPENELIS_FHIR_URL}/DiagnosticReport`,
        {
          params: {
            basedOn: `ServiceRequest/${order.openelisServiceRequestId}`,
            status: 'final'  // Баталгаажсан үр дүн
          },
          headers: { 'Authorization': process.env.FHIR_AUTH_TOKEN }
        }
      );
      
      if (response.data.total > 0) {
        console.log(`✅ Result ready for order ${order.b2bOrderId}`);
        
        // Process үр дүн
        await processLabResult(order, response.data.entry[0].resource);
      }
    }
    
  } catch (error) {
    console.error('❌ Polling failed:', error);
  }
});
```

---

## 3. Integration Patterns

### Pattern 1: Synchronous REST API

```
B2B System ──(HTTP POST)──→ OpenELIS
           ←──(Response)───
```

**Давуу тал:**
- ✅ Энгийн implementation
- ✅ Real-time response
- ✅ Error handling шууд

**Сул тал:**
- ❌ Coupling өндөр
- ❌ OpenELIS доогуур бол B2B доогуур
- ❌ Network latency

---

### Pattern 2: Asynchronous Message Queue

```
B2B System ──→ RabbitMQ ──→ OpenELIS
                  ↓
              Message Store
```

**Implementation:**

```javascript
// B2B Publisher
const amqp = require('amqplib');

async function publishLabOrder(orderData) {
  const connection = await amqp.connect('amqp://rabbitmq-server');
  const channel = await connection.createChannel();
  
  await channel.assertQueue('lab-orders', { durable: true });
  
  channel.sendToQueue(
    'lab-orders',
    Buffer.from(JSON.stringify(orderData)),
    { persistent: true }
  );
  
  console.log('✅ Lab order queued:', orderData.orderId);
}

// OpenELIS Consumer
async function consumeLabOrders() {
  const connection = await amqp.connect('amqp://rabbitmq-server');
  const channel = await connection.createChannel();
  
  await channel.assertQueue('lab-orders', { durable: true });
  
  channel.consume('lab-orders', async (msg) => {
    const orderData = JSON.parse(msg.content.toString());
    
    try {
      // OpenELIS-д order үүсгэх
      await createOpenELISOrder(orderData);
      
      // Success - ACK
      channel.ack(msg);
      
    } catch (error) {
      console.error('❌ Failed to process order:', error);
      
      // Retry бүү хий, dead letter queue рүү явуул
      channel.nack(msg, false, false);
    }
  });
}
```

**Давуу тал:**
- ✅ Decoupling (бие даасан системүүд)
- ✅ Fault tolerance (message алдагдахгүй)
- ✅ Load balancing

**Сул тал:**
- ❌ Complex infrastructure (RabbitMQ суулгах)
- ❌ Debugging хэцүү
- ❌ Message ordering асуудал

---

### Pattern 3: Event-Driven Architecture

```
OpenELIS ──(Event)──→ Event Bus ──→ B2B System
                         │
                         ├──→ Billing System
                         ├──→ Notification Service
                         └──→ Analytics Service
```

**Domain Events:**

```javascript
// OpenELIS Events
{
  eventType: "ResultValidated",
  eventId: "evt_12345",
  timestamp: "2026-01-31T10:30:00Z",
  data: {
    serviceRequestId: "ServiceRequest/789",
    patientId: "Patient/123",
    diagnosticReportId: "DiagnosticReport/456",
    testCode: "24331-1",
    testName: "Липидийн шинжилгээ",
    status: "final"
  }
}

{
  eventType: "SampleReceived",
  data: {
    sampleId: "SPM-2026-001234",
    patientId: "Patient/123",
    collectedDate: "2026-01-31T08:00:00Z",
    sampleType: "blood"
  }
}
```

---

## 4. Security & Authentication

### 4.1 OAuth 2.0 Authentication

**OpenELIS OAuth Configuration:**

```yaml
# application.yml (OpenELIS)
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://auth-server.mn/oauth2
```

**B2B получить token:**

```javascript
const axios = require('axios');

async function getOpenELISAccessToken() {
  const response = await axios.post(
    'https://auth-server.mn/oauth2/token',
    {
      grant_type: 'client_credentials',
      client_id: process.env.B2B_CLIENT_ID,
      client_secret: process.env.B2B_CLIENT_SECRET,
      scope: 'openelis.read openelis.write'
    }
  );
  
  return response.data.access_token;
}

// Ашиглалт
const token = await getOpenELISAccessToken();

axios.get(`${OPENELIS_FHIR_URL}/Patient/123`, {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

---

### 4.2 API Key Authentication

```javascript
// OpenELIS API Key check
@RestController
public class SecureApiController {
    
    @GetMapping("/api/secure-endpoint")
    public ResponseEntity<?> secureData(
        @RequestHeader("X-API-Key") String apiKey
    ) {
        if (!apiKeyService.validate(apiKey)) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                .body("Invalid API key");
        }
        
        // Process request
        return ResponseEntity.ok(data);
    }
}
```

```javascript
// B2B request with API key
axios.get('https://openelis-server.mn/api/secure-endpoint', {
  headers: {
    'X-API-Key': 'b2b_prod_key_abc123xyz789'
  }
});
```

---

## 5. Data Mapping

### B2B Order → FHIR ServiceRequest

| B2B Field | FHIR Field | Example |
|-----------|------------|---------|
| `orderId` | `identifier[0].value` | "B2B-2026-001234" |
| `patientNationalId` | `subject.identifier` | "УБ12345678" |
| `testCode` | `code.coding[0].code` | "24331-1" (LOINC) |
| `specimenType` | `specimen.type` | "blood" |
| `requestDate` | `authoredOn` | "2026-01-31T10:00:00Z" |
| `doctorId` | `requester.reference` | "Practitioner/456" |
| `priority` | `priority` | "routine" / "urgent" |
| `clinicalNotes` | `note[0].text` | "Suspicion of diabetes" |

### FHIR DiagnosticReport → B2B Result

| FHIR Field | B2B Field | Example |
|------------|-----------|---------|
| `id` | `openelisReportId` | "DiagnosticReport/789" |
| `status` | `resultStatus` | "final" |
| `issued` | `reportDate` | "2026-01-31T14:30:00Z" |
| `result[].valueQuantity.value` | `testValue` | 5.2 |
| `result[].valueQuantity.unit` | `unit` | "mmol/L" |
| `result[].interpretation` | `interpretation` | "High" |
| `conclusion` | `summary` | "Cholesterol elevated" |

---

## 6. Deployment Architecture

### Production Setup

```
┌─────────────────────────────────────────────────────────────┐
│                    Cloud Infrastructure                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │  B2B System      │         │  OpenELIS LIMS   │         │
│  │  VM 1            │         │  VM 2            │         │
│  │  (10.0.1.10)     │◄───────►│  (10.0.2.10)     │         │
│  │                  │  HTTPS  │                  │         │
│  │  - Node.js       │  :8444  │  - Java/Spring   │         │
│  │  - React         │         │  - React         │         │
│  │  - MongoDB       │         │  - PostgreSQL    │         │
│  └──────────────────┘         └──────────────────┘         │
│         ↑                              ↑                     │
│         │                              │                     │
│  ┌──────▼──────────────────────────────▼──────┐            │
│  │       Load Balancer / API Gateway          │            │
│  │       (Nginx / Kong / AWS ALB)             │            │
│  └────────────────────────────────────────────┘            │
│                        ↑                                     │
└────────────────────────┼─────────────────────────────────────┘
                         │
                         │ HTTPS
                         │
            ┌────────────▼────────────┐
            │     Internet Users      │
            │  (Doctors, Patients)    │
            └─────────────────────────┘
```

**Network Configuration:**

```yaml
# docker-compose.yml (B2B)
services:
  b2b-backend:
    networks:
      - b2b-network
    environment:
      - OPENELIS_API_URL=https://10.0.2.10:8444/fhir

networks:
  b2b-network:
    driver: bridge
    ipam:
      config:
        - subnet: 10.0.1.0/24
```

```yaml
# docker-compose.yml (OpenELIS)
services:
  fhir-api:
    networks:
      - openelis-network
    ports:
      - "8444:8443"
    environment:
      - ALLOWED_ORIGINS=https://10.0.1.10

networks:
  openelis-network:
    driver: bridge
    ipam:
      config:
        - subnet: 10.0.2.0/24
```

---

## 7. Testing Integration

### Integration Test (B2B → OpenELIS)

```javascript
// File: tests/integration/openelis.test.js
const axios = require('axios');
const { expect } = require('chai');

describe('OpenELIS Integration', () => {
  
  const OPENELIS_URL = process.env.OPENELIS_FHIR_URL;
  const AUTH_TOKEN = process.env.FHIR_AUTH_TOKEN;
  
  it('should create patient in OpenELIS', async () => {
    const patientData = {
      resourceType: "Patient",
      identifier: [{
        system: "http://health.mn/national-id",
        value: "TEST123456789"
      }],
      name: [{
        family: "Баatar",
        given: ["Dorj"]
      }],
      gender: "male",
      birthDate: "1990-01-15"
    };
    
    const response = await axios.post(
      `${OPENELIS_URL}/Patient`,
      patientData,
      {
        headers: {
          'Authorization': `Bearer ${AUTH_TOKEN}`,
          'Content-Type': 'application/fhir+json'
        }
      }
    );
    
    expect(response.status).to.equal(201);
    expect(response.data.id).to.exist;
    expect(response.data.resourceType).to.equal('Patient');
  });
  
  it('should create lab order (ServiceRequest)', async () => {
    // Test implementation...
  });
  
  it('should retrieve DiagnosticReport', async () => {
    // Test implementation...
  });
});
```

---

## 8. Monitoring & Logging

### Centralized Logging

```javascript
// File: middleware/apiLogger.js
const winston = require('winston');

const logger = winston.createLogger({
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'openelis-integration.log' })
  ]
});

function logAPICall(type, endpoint, data, response) {
  logger.info({
    timestamp: new Date().toISOString(),
    type: type,
    endpoint: endpoint,
    request: data,
    response: {
      status: response.status,
      data: response.data
    }
  });
}

module.exports = { logAPICall };
```

---

## 9. Cost Estimate

| Item | Monthly Cost |
|------|-------------|
| B2B Server (4GB RAM) | $24 |
| OpenELIS Server (8GB RAM) | $48 |
| Database backup (100GB) | $5 |
| Load balancer | $15 |
| SSL certificates | $0 (Let's Encrypt) |
| Monitoring (optional) | $10 |
| **Total** | **$102/сар** |

---

## 10. Санал

### Таны тохиолдолд:

**✅ ФАЗА 1 (3 сар): Тусдаа deployment**
```
B2B System: Server 1 (өөрөөр суулгах)
OpenELIS:   Server 2 (өөрөөр суулгах)
Integration: БАЙХГҮЙ (manual workflow)
```

**✅ ФАЗА 2 (6 сар): REST API integration**
```
B2B → OpenELIS: FHIR API ашиглан захиалга илгээх
OpenELIS → B2B: Webhook/Polling-оор үр дүн татах
```

**✅ ФАЗА 3 (12 сар): Full automation**
```
Event-driven architecture
Real-time notifications
Billing integration
Analytics dashboard
```

**Анхаас тусдаа байх шаардлагатай:** Тийм! Учир нь:
1. B2B нь өөрийн business logic-тай (inventory, billing, e-commerce)
2. OpenELIS нь лабораторын specific workflows-тай
3. Scale differently (B2B илүү traffic, OpenELIS stable)
4. Security requirements өөр (PCI DSS vs HIPAA)

---

Юу нэмж тайлбарлах вэ? API integration-ийн дэлгэрэнгүй code samples хэрэгтэй юу? 🚀
