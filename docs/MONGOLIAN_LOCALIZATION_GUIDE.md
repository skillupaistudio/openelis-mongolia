# OpenELIS Mongolian Localization Guide

## Товч хариулт

**OpenELIS-д localization documentation БАЙХГҮЙ боловч систем нь аль хэдийн олон хэлний дэмжлэгтэй!**

**Орчуулгын механизм:**
- ❌ **PO файл БАЙХГҮЙ** (gettext format биш)
- ✅ **JSON файл** (React Intl ашигладаг)
- ✅ **19 хэл аль хэдийн дэмжигдсэн**
- ✅ **2,385 translation keys** (frontend)

**Монгол хэл нэмэх:**
1. `frontend/src/languages/mn.json` үүсгэх
2. `frontend/src/languages/index.js` засах
3. Backend хэлний сонголт нэмэх (опционал)

**React 19 migration-аас өмнө хийх үү?**  
✅ **ТИЙМ!** Энэ нь хялбар, бие даасан ажил (React version-д хамааралгүй)

---

## 1. Одоогийн i18n Architecture

### 1.1 Frontend (React Intl)

**Library:** `react-intl` (FormatJS)

**Structure:**

```
frontend/src/
├── App.js                      # IntlProvider wrapper
├── languages/
│   ├── index.js                # Language registry
│   ├── en.json                 # English (2,385 keys)
│   ├── fr.json                 # French
│   ├── es.json                 # Spanish
│   ├── sw.json                 # Swahili
│   ├── am_ET.json              # Amharic
│   ├── si.json                 # Sinhala
│   ├── ta.json                 # Tamil
│   ├── id.json                 # Indonesian
│   ├── ro.json                 # Romanian
│   ├── mg.json                 # Malagasy
│   └── (19 languages total)
└── components/                 # Using intl
```

**App.js (Language loader):**

```javascript
import { IntlProvider } from "react-intl";
import { languages } from "./languages";

export default function App() {
  const defaultLocale =
    localStorage.getItem("locale") || navigator.language.split(/[-_]/)[0];

  const initialLocale = languages[defaultLocale] ? defaultLocale : "en";

  const [locale, setLocale] = useState(initialLocale);
  const [messages, setMessages] = useState(languages[initialLocale].messages);

  return (
    <IntlProvider locale={locale} messages={messages}>
      {/* App components */}
    </IntlProvider>
  );
}
```

**Component usage:**

```javascript
import { FormattedMessage, useIntl } from "react-intl";

function PatientForm() {
  const intl = useIntl();
  
  return (
    <div>
      {/* Method 1: FormattedMessage component */}
      <h1>
        <FormattedMessage id="patient.registration.title" />
      </h1>
      
      {/* Method 2: useIntl hook */}
      <input 
        placeholder={intl.formatMessage({ id: "patient.firstName.placeholder" })}
      />
    </div>
  );
}
```

---

### 1.2 Backend (Java MessageBundle)

**Backend-д properties файл байна:**

```
src/main/resources/
├── MessageResources.properties         # English
├── MessageResources_fr.properties      # French
└── (Other language properties)
```

**Гэхдээ backend орчуулга одоогоор limited** (зөвхөн email templates, reports)

Frontend нь primary UI - энд орчуулна!

---

## 2. PO файл vs JSON файл

### PO файл (OpenELIS ашиглаагүй)

**PO = Portable Object (GNU gettext format)**

```po
# patient.po
msgid "patient.registration.title"
msgstr "Өвчтөн бүртгэх"

msgid "patient.firstName"
msgstr "Нэр"

msgid "patient.lastName"
msgstr "Овог"
```

**Давуу тал:**
- ✅ Translation tool support (Poedit, Weblate)
- ✅ Context, comments, pluralization

**Сул тал:**
- ❌ OpenELIS ашиглаагүй (React Intl нь JSON ашигладаг)
- ❌ Хувиргалт хэрэгтэй (PO → JSON)

---

### JSON файл (OpenELIS ашигладаг) ⭐

**en.json жишээ:**

```json
{
  "patient.registration.title": "Patient Registration",
  "patient.firstName": "First Name",
  "patient.lastName": "Last Name",
  "patient.gender": "Gender",
  "patient.gender.male": "Male",
  "patient.gender.female": "Female",
  "sample.type.blood": "Blood",
  "sample.type.urine": "Urine",
  "test.result.status.pending": "Pending",
  "test.result.status.completed": "Completed"
}
```

**Давуу тал:**
- ✅ React Intl шууд ашиглана
- ✅ Build tool шаардлагагүй
- ✅ Hot reload (development-д)

**Сул тал:**
- ❌ Translation tool дэмжлэг бага
- ❌ Context, pluralization хэцүү

---

## 3. Монгол хэл нэмэх (Step-by-Step)

### Step 1: mn.json үүсгэх

**Option A: Manual орчуулга (demo/testing)**

```json
// frontend/src/languages/mn.json
{
  "patient.registration.title": "Өвчтөн бүртгэх",
  "patient.firstName": "Нэр",
  "patient.lastName": "Овог",
  "patient.gender": "Хүйс",
  "patient.gender.male": "Эрэгтэй",
  "patient.gender.female": "Эмэгтэй",
  "patient.birthDate": "Төрсөн огноо",
  "patient.nationalId": "Регистрийн дугаар",
  "patient.phoneNumber": "Утасны дугаар",
  "patient.address": "Хаяг",
  
  "sample.collection": "Дээж авах",
  "sample.type.blood": "Цус",
  "sample.type.urine": "Шээс",
  "sample.type.stool": "Баас",
  "sample.barcode": "Баркод",
  
  "test.name": "Шинжилгээний нэр",
  "test.result": "Үр дүн",
  "test.status.pending": "Хүлээгдэж буй",
  "test.status.completed": "Дууссан",
  
  "button.save": "Хадгалах",
  "button.cancel": "Цуцлах",
  "button.submit": "Илгээх",
  "button.print": "Хэвлэх",
  "button.search": "Хайх",
  
  "menu.home": "Нүүр",
  "menu.patient": "Өвчтөн",
  "menu.sample": "Дээж",
  "menu.results": "Үр дүн",
  "menu.reports": "Тайлан"
}
```

**Option B: Copy en.json болон AI орчуулга**

```bash
# PowerShell
cd frontend\src\languages
Copy-Item en.json mn.json

# Дараа нь mn.json-г AI ашиглан орчуулна (өмнө бичсэн Python script)
```

---

### Step 2: index.js засах

**Файл:** `frontend/src/languages/index.js`

```javascript
import en from "./en.json";
import enGB from "./en_GB.json";
import enLK from "./en_LK.json";
import enUS from "./en_US.json";
import es from "./es.json";
import fr from "./fr.json";
import id from "./id.json";
import idID from "./id_ID.json";
import mg from "./mg.json";
import ro from "./ro.json";
import si from "./si.json";
import siLK from "./si_LK.json";
import ta from "./ta.json";
import taLK from "./ta_LK.json";
import amET from "./am_ET.json";
import sw from "./sw.json";
// ✅ НЭМЭХ: Монгол хэл import
import mn from "./mn.json";

export const languages = {
  en: { label: "English", messages: en },
  "en-GB": { label: "English (UK)", messages: enGB },
  "en-LK": { label: "English (Sri Lanka)", messages: enLK },
  "en-US": { label: "English (US)", messages: enUS },
  es: { label: "Español", messages: es },
  fr: { label: "Français", messages: fr },
  id: { label: "Indonesia", messages: id },
  "id-ID": { label: "Indonesia (ID)", messages: idID },
  mg: { label: "Malagasy", messages: mg },
  ro: { label: "Română", messages: ro },
  si: { label: "සිංහල", messages: si }, // Sinhala
  "si-LK": { label: "සිංහල (Sri Lanka)", messages: siLK },
  ta: { label: "தமிழ்", messages: ta }, // Tamil
  "ta-LK": { label: "தமிழ் (Sri Lanka)", messages: taLK },
  sw: { label: "Swahili", messages: sw },
  "am-ET": { label: "Amharic", messages: amET },
  
  // ✅ НЭМЭХ: Монгол хэл registry
  mn: { label: "Монгол", messages: mn },
};
```

---

### Step 3: Testing

**Browser дээр туршиж үзэх:**

```javascript
// Browser console дээр
localStorage.setItem('locale', 'mn');
location.reload();

// Check current locale
console.log(localStorage.getItem('locale'));
```

**UI дээр:**
1. OpenELIS нэвтэрнэ
2. User Profile → Language → "Монгол" сонгох
3. Page refresh хийнэ
4. Бүх текст монгол хэл дээр харагдах ёстой

---

### Step 4: Language Selector Component

**OpenELIS дээр аль хэдийн байгаа:**

```javascript
// Component structure (already exists)
function LanguageSelector() {
  const [locale, setLocale] = useState(localStorage.getItem('locale') || 'en');
  
  const handleLanguageChange = (newLocale) => {
    localStorage.setItem('locale', newLocale);
    setLocale(newLocale);
    window.location.reload(); // Reload app with new language
  };
  
  return (
    <Select
      id="language-selector"
      value={locale}
      onChange={(e) => handleLanguageChange(e.target.value)}
    >
      {Object.keys(languages).map(key => (
        <SelectItem key={key} value={key}>
          {languages[key].label}
        </SelectItem>
      ))}
    </Select>
  );
}
```

---

## 4. Translation Keys бүтэц

### 4.1 Naming Convention

OpenELIS нь **module.feature.field** format ашигладаг:

```json
{
  // Patient module
  "patient.registration.title": "...",
  "patient.firstName": "...",
  "patient.search.placeholder": "...",
  
  // Sample module
  "sample.collection.date": "...",
  "sample.type.blood": "...",
  "sample.barcode.generate": "...",
  
  // Test module
  "test.result.entry": "...",
  "test.status.pending": "...",
  
  // Common buttons
  "button.save": "...",
  "button.cancel": "...",
  
  // Common labels
  "label.date": "...",
  "label.time": "...",
  
  // Validation messages
  "validation.required": "...",
  "validation.invalid.email": "..."
}
```

---

### 4.2 Top Priority Keys (хамгийн түрүүнд орчуулах)

**1. Navigation (Menu):**
```json
{
  "banner.menu.home": "Нүүр",
  "banner.menu.patient": "Өвчтөн",
  "banner.menu.patient.addOrEdit": "Өвчтөн нэмэх/засах",
  "banner.menu.order": "Захиалга",
  "banner.menu.results": "Үр дүн",
  "banner.menu.reports": "Тайлан",
  "banner.menu.admin": "Удирдлага"
}
```

**2. Common Actions:**
```json
{
  "button.save": "Хадгалах",
  "button.cancel": "Цуцлах",
  "button.submit": "Илгээх",
  "button.search": "Хайх",
  "button.print": "Хэвлэх",
  "button.edit": "Засах",
  "button.delete": "Устгах",
  "button.add": "Нэмэх"
}
```

**3. Patient Registration:**
```json
{
  "patient.registration": "Өвчтөн бүртгэх",
  "patient.firstName": "Нэр",
  "patient.lastName": "Овог",
  "patient.gender": "Хүйс",
  "patient.birthDate": "Төрсөн огноо",
  "patient.nationalId": "Регистрийн дугаар",
  "patient.phoneNumber": "Утасны дугаар"
}
```

**4. Test Names (Medical terminology):**
```json
{
  "test.hematology.cbc": "Цусны ерөнхий шинжилгээ (ЦЕШ)",
  "test.biochemistry.glucose": "Цусны сахар (Глюкоз)",
  "test.biochemistry.cholesterol": "Холестерол",
  "test.immunology.hiv": "ХИВ-ийн эсрэг бие",
  "test.microbiology.urine": "Шээсний шинжилгээ"
}
```

---

## 5. Translation Process (Automated)

### 5.1 Using AI (ChatGPT/Claude)

**Script дээр бүтээсэн (өмнө):**

```bash
# Python script ашиглах
cd D:\B2B-GYALS\OpenELIS-Global-2-develop

python scripts\translate_to_mongolian.py \
  --api-key YOUR_OPENAI_API_KEY \
  --provider openai \
  --input frontend\src\languages\en.json \
  --output frontend\src\languages\mn.json
```

**Хугацаа:** 15 минут (2,385 keys)  
**Зардал:** ~$2.50 (GPT-4)

---

### 5.2 Using Translation Tools

**Poedit (PO файлд ашиглагддаг, OpenELIS-д биш)**

**Жишээ workflow (хэрэв PO хэрэг болвол):**

```bash
# 1. JSON → PO convert
json-to-po en.json en.po

# 2. Poedit ашиглан орчуулна
poedit en.po

# 3. PO → JSON convert
po-to-json mn.po mn.json
```

**Гэхдээ OpenELIS-д шаардлагагүй!** JSON шууд засна.

---

## 6. Testing Checklist

### Phase 1: Smoke Testing

```
✅ Login page Монгол хэл дээр
✅ Main menu Монгол хэл дээр
✅ Patient registration form Монгол хэл дээр
✅ Sample collection Монгол хэл дээр
✅ Button labels Монгол хэл дээр
```

### Phase 2: Full Testing

```
✅ Бүх navigation menu items
✅ Form labels (Patient, Sample, Test)
✅ Validation messages
✅ Success/Error messages
✅ Table headers
✅ Modal dialogs
✅ Dropdown options
✅ Date/time formatting (Монгол формат)
✅ Number formatting (Монгол формат)
```

### Phase 3: Medical Terminology Review

```
✅ Test names accuracy
✅ Medical units (mmol/L, g/dL)
✅ Sample types (цус, шээс, баас)
✅ Result interpretations (Өндөр, Доогуур, Хэвийн)
```

---

## 7. React 19 Migration-тай харьцуулалт

### Монгол хэл нэмэх vs React 19 Migration

| Критери | Монгол хэл нэмэх | React 19 Migration |
|---------|------------------|-------------------|
| **Хугацаа** | 3-5 хоног | 3 долоо хоног |
| **Complexity** | Доод | Өндөр |
| **Risk** | Бага | Дунд |
| **Dependencies** | Байхгүй | React, Carbon Design System |
| **Testing effort** | Бага | Их |
| **User impact** | Шууд харагдах | Backend, performance only |
| **ROI** | Өндөр (visual) | Дунд (technical debt) |

---

### Яагаад React 19-с ӨМНӨ хийх нь зөв вэ?

**✅ Давуу талууд:**

1. **Бие даасан ажил**
   - React version-д хамааралгүй
   - JSON файл л нэмнэ
   - Код өөрчлөлт бага

2. **Хурдан үр дүн**
   - 3-5 хоногт бэлэн
   - Шууд харагдах (UI)
   - Stakeholder-үүд үнэлж чадна

3. **Risk бага**
   - Breaking change байхгүй
   - Rollback хялбар (JSON файл л устгана)
   - Production-д шууд deploy болно

4. **Team-д үзүүлэх**
   - Багт системийг Монгол хэл дээр харуулна
   - Feedback авна (terminology засна)
   - User acceptance testing эхэлнэ

5. **React 19 migration-д саад болохгүй**
   - JSON файл React 19-д ч ажиллана
   - react-intl library үргэлжлэх
   - Орчуулга алдагдахгүй

**❌ React 19-ийг эхлээд хийвэл:**

1. Баг 3 долоо хоног technical ажил үзнэ (UI өөрчлөгдөхгүй)
2. Stakeholder-үүд үр дүн харахгүй
3. Монгол хэл бүү хэл одоо хүлээх хэрэгтэй
4. Team motivation доогуур болно

---

## 8. Implementation Plan

### Week 1: Preparation

**Day 1-2: Translation keys analysis**
```bash
# Check current translations completeness
node scripts/check-translations.js

# Identify missing keys
node scripts/find-missing-keys.js
```

**Day 3: Sample translation (100 keys)**
```json
// mn.json (sample)
{
  "banner.menu.home": "Нүүр",
  "patient.registration.title": "Өвчтөн бүртгэх",
  "button.save": "Хадгалах",
  // ... 97 more keys
}
```

**Day 4: Testing sample**
- Deploy to dev environment
- Team reviews first 100 keys
- Adjust medical terminology

**Day 5: Feedback & corrections**
- Fix terminology issues
- Finalize translation style guide

---

### Week 2: Full Translation

**Day 1-3: AI-powered translation**
```bash
# Run translation script
python scripts/translate_to_mongolian.py --api-key xxx

# Output: frontend/src/languages/mn.json (2,385 keys)
```

**Day 4-5: Quality review**
- Medical terminology review
- Grammar check
- Context validation

---

### Week 3: Integration & Testing

**Day 1: Code integration**
```bash
# Add mn.json to index.js
# Test language switching
# Deploy to staging
```

**Day 2-3: Full UI testing**
- Patient registration workflow
- Sample collection workflow
- Result entry workflow
- Reports printing

**Day 4: Bug fixing**
- Fix layout issues (Mongolian text longer/shorter)
- Adjust date/number formatting
- Fix validation messages

**Day 5: User Acceptance Testing**
- Lab staff testing
- Doctor testing
- Admin testing

---

### Week 4: Deployment & Training

**Day 1-2: Production deployment**
```bash
# Build frontend with mn.json
npm run build

# Deploy to production
docker-compose up -d --build frontend
```

**Day 3-4: User training**
- Create Mongolian user manual (screenshots)
- Video tutorials (Mongolian voiceover)
- FAQ document

**Day 5: Go-live support**
- Monitor user feedback
- Fix urgent issues
- Collect improvement suggestions

---

## 9. Medical Terminology Dictionary

### Лабораторын нэр томъёо

```json
{
  // Sample types
  "sample.type.blood": "Цус",
  "sample.type.serum": "Сийвэн",
  "sample.type.plasma": "Плазма",
  "sample.type.urine": "Шээс",
  "sample.type.stool": "Баас",
  "sample.type.sputum": "Цэрэгцлэх",
  "sample.type.csf": "Нугасны шингэн",
  
  // Test sections
  "test.section.hematology": "Цусны эмнэлэг",
  "test.section.biochemistry": "Биохими",
  "test.section.microbiology": "Нянгийн судлал",
  "test.section.serology": "Серологи",
  "test.section.immunology": "Дархлалын судлал",
  "test.section.pathology": "Эмгэг судлал",
  
  // Common tests
  "test.cbc": "Цусны ерөнхий шинжилгээ (ЦЕШ)",
  "test.hemoglobin": "Гемоглобин",
  "test.wbc": "Цагаан эс",
  "test.rbc": "Улаан эс",
  "test.platelet": "Тромбоцит",
  "test.glucose": "Глюкоз (цусны сахар)",
  "test.cholesterol": "Холестерол",
  "test.creatinine": "Креатинин",
  "test.alt": "АЛТ (SGPT)",
  "test.ast": "АСТ (SGOT)",
  
  // Test results
  "result.normal": "Хэвийн",
  "result.high": "Өндөр",
  "result.low": "Доогуур",
  "result.positive": "Эерэг",
  "result.negative": "Сөрөг",
  "result.pending": "Хүлээгдэж буй",
  "result.completed": "Дууссан",
  "result.validated": "Баталгаажсан"
}
```

---

## 10. Code Examples

### Example 1: Patient Form with Mongolian

**Before (English only):**

```javascript
function PatientForm() {
  return (
    <Form>
      <FormGroup>
        <TextInput
          id="firstName"
          labelText="First Name"
          placeholder="Enter first name"
        />
      </FormGroup>
      <Button type="submit">Save</Button>
    </Form>
  );
}
```

**After (i18n ready):**

```javascript
import { FormattedMessage, useIntl } from "react-intl";

function PatientForm() {
  const intl = useIntl();
  
  return (
    <Form>
      <FormGroup>
        <TextInput
          id="firstName"
          labelText={intl.formatMessage({ id: "patient.firstName" })}
          placeholder={intl.formatMessage({ id: "patient.firstName.placeholder" })}
        />
      </FormGroup>
      <Button type="submit">
        <FormattedMessage id="button.save" />
      </Button>
    </Form>
  );
}
```

**mn.json:**
```json
{
  "patient.firstName": "Нэр",
  "patient.firstName.placeholder": "Нэрээ оруулна уу",
  "button.save": "Хадгалах"
}
```

**Result:** "Нэр" label, "Нэрээ оруулна уу" placeholder, "Хадгалах" button

---

### Example 2: Date Formatting

```javascript
import { FormattedDate } from "react-intl";

function TestResult({ result }) {
  return (
    <div>
      <p>
        <FormattedMessage id="test.result.date" />:{" "}
        <FormattedDate 
          value={result.date} 
          year="numeric"
          month="long"
          day="2-digit"
        />
      </p>
    </div>
  );
}
```

**Output:**
- English: "January 31, 2026"
- Mongolian: "2026 оны 1-р сарын 31"

---

## 11. FAQ

**Q: PO файл ашиглах боломжтой юу?**  
A: Боломжтой боловч OpenELIS JSON ашигладаг. PO → JSON convert хэрэгтэй.

**Q: Backend орчуулга хэрэгтэй юу?**  
A: Одоохондоо үгүй. Frontend нь primary UI. Backend зөвхөн email/reports-д.

**Q: React 19 migration орчуулга алдуулах уу?**  
A: Үгүй! react-intl library үргэлжилнэ. JSON файл хадгалагдана.

**Q: Монгол хэлний сонголт хэрхэн ажиллах вэ?**  
A: User Profile → Language → "Монгол" → Page reload → Бүх текст монгол болно.

**Q: Орчуулга incomplete байвал юу болох вэ?**  
A: Fallback to English. "patient.firstName" key mn.json-д байхгүй бол en.json-оос авна.

**Q: Database content (test names) орчуулагдах уу?**  
A: Үгүй. Database content нь UI translation биш. Тэр нь өгөгдөл - өөрөөр оруулах хэрэгтэй.

---

## 12. Next Steps

### Immediate Actions (Одоо шууд)

1. **mn.json үүсгэх** (empty файл)
```bash
cd frontend\src\languages
echo {} > mn.json
```

2. **index.js засах** (Монгол хэл бүртгэх)

3. **Test switching** (Browser дээр туршиж үзэх)

4. **Sample translation** (100 keys орчуулах)

5. **Team review** (Terminology зөв эсэхийг шалгах)

---

### Short-term (1-2 долоо хоног)

1. **Full translation** (AI ашиглах)
2. **Quality review** (Medical terms шалгах)
3. **Integration testing** (UI бүхэлдээ шалгах)
4. **Bug fixes** (Layout issues)

---

### Long-term (3-4 долоо хоног)

1. **UAT** (Lab staff testing)
2. **Production deployment**
3. **User training** (Mongolian manual)
4. **Ongoing maintenance** (Translation updates)

---

## Дүгнэлт

**Монгол хэл нэмэх:**
- ✅ 3-5 хоног
- ✅ Risk бага
- ✅ React 19-д саад болохгүй
- ✅ Шууд үр дүн (UI Монгол хэл дээр)
- ✅ Баг + stakeholders-д үзүүлж болно

**React 19 migration:**
- ⏳ 3 долоо хоног
- ⚠️ Risk дунд
- 🔧 Technical ажил (UI өөрчлөгдөхгүй)
- 📊 Backend үр дүн (users харахгүй)

**Санал:** Монгол хэл → React 19 migration дараалал зөв! 🚀
