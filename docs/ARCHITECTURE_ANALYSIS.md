# OpenELIS-Global Архитектурын Дүн шинжилгээ

## Товч хариулт

OpenELIS нь **Layered (Давхаргат) Architecture** + **Transaction Script** загвартай систем.

**Domain-Driven Design (DDD):**
- ❌ Bounded Context БАЙХГҮЙ
- ❌ Aggregate Root БАЙХГҮЙ  
- ❌ Domain Events БАЙХГҮЙ
- ❌ Domain Services (DDD утгаар) БАЙХГҮЙ
- ⚠️ Anemic Domain Model (зөвхөн getter/setter бүхий entities)

**Учир шалтгаан:** 2000-ээд оны эхээр Minnesota Health Department-аас эхэлсэн legacy систем. Тэр үед DDD төдийлөн түгээмэл байгаагүй.

---

## 1. Одоогийн Архитектур

### 1.1 Layered Architecture (Классик MVC)

```
┌─────────────────────────────────────────────────────┐
│  Presentation Layer (Controller)                    │
│  - @Controller classes                              │
│  - REST endpoints                                   │
│  - JSON/JSP views                                   │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│  Service Layer (Business Logic)                     │
│  - @Service classes                                 │
│  - Transaction boundaries (@Transactional)          │
│  - Procedural business rules                        │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│  Data Access Layer (DAO/Repository)                 │
│  - @Repository/@Transactional                       │
│  - Hibernate ORM                                    │
│  - SQL queries                                      │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│  Database (PostgreSQL)                              │
│  - clinlims schema                                  │
│  - 308 tables                                       │
└─────────────────────────────────────────────────────┘
```

### 1.2 Package бүтэц (Feature-based, DDD биш)

```
org.openelisglobal/
├── patient/                    # Patient module
│   ├── valueholder/            # Domain objects (Entities)
│   │   └── Patient.java        # Anemic entity (getter/setter only)
│   ├── dao/                    # Data Access Objects
│   │   └── PatientDAO.java
│   ├── daoimpl/                # DAO Implementation
│   ├── service/                # Business logic
│   │   └── PatientService.java
│   ├── controller/             # Web controllers
│   ├── validator/              # Input validation
│   └── action/                 # Legacy Struts actions
│
├── sample/                     # Sample module
│   ├── valueholder/
│   ├── dao/
│   ├── service/
│   └── controller/
│
├── test/                       # Laboratory Test module
│   ├── valueholder/
│   ├── dao/
│   ├── service/
│   └── controller/
│
├── analysis/                   # Test Analysis module
├── result/                     # Test Results
├── provider/                   # Healthcare Providers
├── organization/               # Organizations
└── common/                     # Shared utilities
    ├── service/
    │   └── BaseObjectService.java  # Generic CRUD
    └── dao/
        └── BaseDAO.java
```

**Онцлог:**
- ✅ Модуль бүр feature-аар (patient, sample, test) ялгагдсан
- ❌ Харин domain context-аар БИШИ (жишээ нь: "Lab Operations", "Patient Management")
- ❌ Cross-module dependency хязгаарлалт алга
- ❌ Module boundary тодорхойгүй

---

## 2. Domain Model Analysis

### 2.1 Anemic Domain Model (Anti-pattern)

**Patient.java жишээ:**

```java
@Entity
public class Patient extends BaseObject<String> {
    private String id;
    private String gender;
    private String nationalId;
    private Timestamp birthDate;
    private ValueHolderInterface person;
    
    // Зөвхөн getter/setter
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getGender() { return gender; }
    public void setGender(String gender) { this.gender = gender; }
    
    // ❌ Business logic БАЙХГҮЙ!
    // ❌ Domain behavior БАЙХГҮЙ!
    // ❌ Invariants защита БАЙХГҮЙ!
}
```

**DDD-д байх байсан утга:**

```java
// DDD Rich Domain Model (OpenELIS дээр БАЙХГҮЙ)
@Entity
public class Patient extends AggregateRoot<PatientId> {
    private PatientId id;
    private Gender gender;
    private NationalId nationalId;
    private BirthDate birthDate;
    
    // Constructor with invariants
    public Patient(NationalId nationalId, Gender gender, BirthDate birthDate) {
        if (nationalId == null) throw new DomainException("National ID required");
        if (birthDate.isInFuture()) throw new DomainException("Birth date cannot be future");
        
        this.id = PatientId.generate();
        this.nationalId = nationalId;
        this.gender = gender;
        this.birthDate = birthDate;
        
        // Domain event
        registerEvent(new PatientRegisteredEvent(this.id, nationalId));
    }
    
    // Domain behavior
    public void changeGender(Gender newGender) {
        if (this.gender.equals(newGender)) return;
        this.gender = newGender;
        registerEvent(new PatientGenderChangedEvent(this.id, newGender));
    }
    
    // Business rule encapsulation
    public boolean isEligibleForTest(TestType testType) {
        return testType.isApplicableForGender(this.gender) 
            && this.age() >= testType.getMinimumAge();
    }
}
```

### 2.2 Transaction Script Pattern

Business logic Service давхаргад байна (Domain объектод биш):

**PatientService.java:**

```java
@Service
@Transactional
public class PatientServiceImpl implements PatientService {
    
    @Autowired
    private PatientDAO patientDAO;
    
    // Business logic SERVICE давхаргад (Domain биш!)
    public void persistPatientData(PatientManagementInfo info, 
                                   Patient patient, 
                                   String sysUserId) {
        // Validation
        if (patient.getNationalId() == null) {
            throw new RuntimeException("National ID required");
        }
        
        // Orchestration
        Person person = createOrUpdatePerson(info);
        patient.setPerson(new ValueHolder(person));
        
        // Save
        patientDAO.save(patient);
        
        // Create identity records
        createPatientIdentities(patient, info);
        
        // Audit
        auditService.log("Patient created", patient.getId(), sysUserId);
    }
}
```

**Үр дагавар:**
- ❌ Domain logic давхаргад тархсан (Service, Controller)
- ❌ Entity зөвхөн өгөгдлийн "bag" (бүх logic Service-д)
- ❌ Reusability доогуур (logic-ийг Service бүр дахин бичих)
- ❌ Testing хэцүү (Service dependencies олон)

---

## 3. Bounded Context байхгүй шалтгаан

### 3.1 Monolithic Database Schema

**308 tables нэг schema-д:**

```sql
-- clinlims schema
- patient
- person
- patient_identity
- sample
- sample_item
- analysis
- test
- test_result
- test_section
- provider
- organization
- role
- system_user
... 300+ tables
```

**DDD-д байх байсан:**

```
PatientContext:
  - patient
  - person
  - patient_identity

LabOperationsContext:
  - sample
  - analysis
  - test_result

TestCatalogContext:
  - test
  - test_section
  - method

UserManagementContext:
  - system_user
  - role
  - permission
```

### 3.2 Cross-Module Dependencies

Patient → Sample → Analysis → Result **бүгд шууд холбоотой:**

```java
// Cross-context dependency (DDD зөрчсөн)
public class Patient {
    // Patient нь Sample-тай шууд холбогдоно
    private Set<Sample> samples;  // ❌ Bounded context boundary давсан!
}

public class Sample {
    // Sample нь Patient, Analysis-тай холбогдоно
    private Patient patient;      // ❌ Cross-context
    private Set<Analysis> analyses; // ❌ Cross-context
}
```

**DDD-д байх байсан:**

```java
// Patient Context (бие даасан)
public class Patient extends AggregateRoot {
    private PatientId id;
    private NationalId nationalId;
    // ❌ Sample-тай ШУУД холбоогүй
}

// Lab Operations Context (өөр bounded context)
public class Sample extends AggregateRoot {
    private SampleId id;
    private PatientId patientId;  // ✅ Reference by ID only
    // Integration through domain events
}
```

---

## 4. Архитектурын давуу ба сул талууд

### ✅ Давуу талууд:

1. **Ойлгомжтой, энгийн бүтэц**
   - Junior developer ойлгоход хялбар
   - Spring MVC standard загвар
   - Clear separation of concerns (Controller/Service/DAO)

2. **CRUD operation-д тохиромжтой**
   - Patient бүртгэх, засах, устгах → хялбар
   - Simple business logic-д өндөр performance

3. **Өргөтгөх боломжтой**
   - Шинэ module (жнь: `billing/`) нэмэхэд хялбар
   - Dependency injection (Spring) ашиглаж байгаа

4. **Legacy migration бага өртөгтэй**
   - 2000-ээд оноос өөрчлөгдөөгүй бүтэц
   - Struts → Spring migration хийсэн
   - Database schema тогтвортой

### ❌ Сул талууд:

1. **Complex business logic зохион байгуулахад хэцүү**
   - Logic Service давхаргад "гадаа" байна
   - Олон Service зэрэг дуудвал logic давхцана
   - Example: Sample validation logic 5-6 газар давтагдсан

2. **Testing хүндрэлтэй**
   - Service нь олон dependency-тай (DAO, validators, calculators)
   - Unit test бичихэд mock объект олон хэрэгтэй
   - Integration test хурдан биш

3. **Domain expertise capture хийхгүй байна**
   - Lab technician-ийн domain мэдлэг code-д ороогүй
   - Business rules documentation-д л байна (code биш)
   - "Why?" асуултанд code хариулахгүй

4. **Refactoring риск өндөр**
   - Patient.java өөрчилвөл 50+ Service, Controller өөрчлөгдөх
   - Database schema refactoring маш хэцүү
   - Breaking change авахад 6-12 сарын regression testing

5. **Scalability хязгаарлагдмал**
   - Monolithic database → horizontal scaling хийхгүй
   - Cross-module join query performance issue
   - Sample + Patient + Test → 5-10 table JOIN query

---

## 5. DDD-рүү шилжүүлэх боломж

### Сценари: Patient Domain → Bounded Context

**Одоогийн байдал:**

```java
org.openelisglobal.patient/
  valueholder/Patient.java        // Anemic
  service/PatientService.java     // God class (1000+ lines)
  dao/PatientDAO.java
```

**DDD рүү шилжүүлсэн:**

```java
org.openelisglobal.patientmanagement/  // Bounded Context
  domain/
    model/
      Patient.java                 // Aggregate Root (rich model)
      PatientId.java              // Value Object
      NationalId.java             // Value Object
      PersonalInfo.java           // Value Object
    service/
      PatientRegistrationService.java  // Domain Service
    event/
      PatientRegisteredEvent.java      // Domain Event
    repository/
      PatientRepository.java            // Repository (not DAO)
  application/
    PatientApplicationService.java      // Use case orchestration
  infrastructure/
    persistence/
      PatientJpaRepository.java         // JPA implementation
```

**Хувиргалтын зардал:**
- Хугацаа: 3-6 сар (Patient domain л бол)
- Нөөц: 2-3 senior developer
- Риск: High (existing functionality regression)
- ROI: Medium-Low (CRUD системд DDD overengineering байж магадгүй)

---

## 6. Санал зөвлөмж

### Монгол deployment-д:

**Scenario 1: Хурдан ашиглалтад гаргах (3-6 сар)**
```
✅ Одоогийн архитектур хэвээр үлдээ
✅ Зөвхөн Mongolian localization + rebrand
✅ Minor bug fix
❌ Architecture refactoring битгий хий
```

**Учир шалтгаан:**
- OpenELIS 20+ жилийн battle-tested код
- CRUD operation-д тохиромжтой
- Mongolia use case (patient registry, lab test results) энгийн
- DDD overhead шаардлагагүй

---

**Scenario 2: Урт хугацаат стратеги (2-3 жил)**
```
Phase 1 (Year 1): Deploy одоогийн архитектур, production data цуглуул
Phase 2 (Year 2): Pain points тодорхойл (жнь: Sample workflow, QC process)
Phase 3 (Year 3): Specific domain-уудыг DDD руу refactor (зөвхөн шаардлагатай хэсгийг)
```

**Жишээ нь:**
```
✅ Keep as-is: Patient management (CRUD-д хангалттай)
✅ Keep as-is: User authentication
🔄 Refactor to DDD: Sample lifecycle (complex workflow)
🔄 Refactor to DDD: Quality Control (domain rules олон)
🔄 Refactor to DDD: Result validation (business logic төвөгтэй)
```

---

## 7. Дүгнэлт

| Асуулт | Хариулт |
|--------|---------|
| **OpenELIS архитектур юу вэ?** | Layered Architecture + Transaction Script |
| **DDD ашигласан уу?** | ❌ Үгүй |
| **Bounded Context байна уу?** | ❌ Үгүй, monolithic module бүтэц |
| **Aggregate Root байна уу?** | ❌ Үгүй, anemic entities |
| **Domain Events байна уу?** | ❌ Үгүй, synchronous service calls |
| **Repository pattern байна уу?** | ⚠️ DAO pattern (Repository биш) |
| **Монгол дээр ашиглаж болох уу?** | ✅ Тийм! Архитектур сайн, production-ready |
| **DDD руу шилжүүлэх үү?** | ❌ Одоохондоо шаардлагагүй (CRUD хангалттай) |

---

## Нэмэлт судалгаа

Та нэмэлт мэдээлэл хэрэгтэй бол:

1. **Spring Service Layer architecture** → `/src/main/java/org/openelisglobal/*/service/`
2. **Hibernate Entities** → `/src/main/java/org/openelisglobal/*/valueholder/`
3. **REST API Controllers** → `/src/main/java/org/openelisglobal/*/controller/`
4. **Database Schema** → `docker exec openelisglobal-database psql -U clinlims -d clinlims -c '\dt'`

Юу нэмж тодруулах вэ? 🤔
