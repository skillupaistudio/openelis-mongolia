# AI API Key - Бүрэн заавар

## API Key гэж юу вэ?

**API Key** = Таны дугаарласан нэвтрэх түлхүүр

Жишээ нь:
```
sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
```

Энэ нь:
- 🔐 Таныг таних ID (таны дансыг олно)
- 💰 Төлбөр тооцох (ашигласан үгийн тоогоор)
- 📊 Хэрэглээ хянах (хэдэн request илгээсэн)

---

## 1. OpenAI API Key авах (ChatGPT)

### Алхам 1: Бүртгүүлэх
```
1. https://platform.openai.com руу орно
2. "Sign Up" товч дарна
3. Email + Google account-аар нэвтэрнэ
4. Гар утасны дугаар баталгаажуулна (SMS)
```

### Алхам 2: Төлбөрийн мэдээлэл оруулах
```
1. Settings → Billing → Payment methods руу орно
2. Кредит карт нэмнэ (Visa/Mastercard)
3. $5-10 deposit хийнэ (эхлээд бага дүн туршаад үз)
```

### Алхам 3: API Key үүсгэх
```
1. API Keys хэсэг рүү орно
2. "+ Create new secret key" товч дарна
3. Нэр өгнө: "OpenELIS Translation"
4. Key-г хуулж аваад АЮУЛГҮЙ газар хадгална!
```

**⚠️ АНХААР:**
- Key нэг удаа харагдана! Алдвал шинээр үүсгэх хэрэгтэй
- Хэн ч мэдэхгүй газар хадгална (жнь: LastPass, 1Password)
- GitHub/public дээр ХЭЗЭЭ Ч upload хийхгүй!

---

## 2. API Key яаж ажилладаг вэ?

### Техникийн урсгал:

```
[Таны компьютер]                    [OpenAI Server]
      │                                      │
      │  1. Request илгээнэ                 │
      │  ──────────────────────────────────>│
      │     Header: "Authorization:          │
      │              Bearer sk-xxx"          │
      │     Body: "Translate to Mongolian"   │
      │                                      │
      │  2. OpenAI Key-г шалгана            │
      │                    <─────────────────│
      │                    "Valid! $5 үлдсэн"│
      │                                      │
      │  3. AI орчуулга хийнэ               │
      │                    ................. │
      │                    GPT-4 thinking... │
      │                                      │
      │  4. Үр дүн буцаана                  │
      │  <──────────────────────────────────│
      │     Result: "Монгол хэл дээр текст" │
      │     Cost: $0.0025 (500 tokens)      │
      │                                      │
      │  5. Таны балансаас $0.0025 хасна    │
      │                                      │
```

---

## 3. Python код дээр API Key ашиглах

### 3.1 Environment Variable (Аюулгүй арга)

**Windows PowerShell:**
```powershell
# Түр зуурын (Terminal хаахад устана)
$env:OPENAI_API_KEY = "sk-proj-YOUR_KEY_HERE"

# Байнгын (System environment variable)
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'sk-proj-YOUR_KEY_HERE', 'User')
```

**Python код:**
```python
import os
from openai import OpenAI

# Environment variable-аас уншина
api_key = os.getenv('OPENAI_API_KEY')

# OpenAI client үүсгэнэ
client = OpenAI(api_key=api_key)

# AI-руу хүсэлт илгээнэ
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Translate to Mongolian: Hello"}
    ]
)

print(response.choices[0].message.content)
# Output: Сайн уу
```

### 3.2 .env файл ашиглах (Local development)

**1. .env файл үүсгэх:**
```bash
# D:\B2B-GYALS\OpenELIS-Global-2-develop\.env
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
```

**2. .gitignore-д нэмэх (ЗААВАЛ!):**
```bash
# Git-д оруулахгүй!
.env
*.env
.env.local
```

**3. Python-оос ашиглах:**
```python
from dotenv import load_dotenv
import os

# .env файл уншина
load_dotenv()

# Одоо os.getenv() ажиллана
api_key = os.getenv('OPENAI_API_KEY')
```

---

## 4. Орчуулга хийх бодит жишээ

### Хувилбар 1: ChatGPT Web Interface (Code-гүйгээр)

Хэрэв Python мэдэхгүй бол:

```
1. https://chat.openai.com руу орно
2. ChatGPT Plus-д элсэнэ ($20/сар)
3. Энэ мессеж илгээнэ:

"I will give you a JSON file with 2,385 English UI strings. 
Translate each value to Mongolian (Cyrillic script) while:
- Keeping all keys unchanged
- Preserving {{variables}}, HTML tags, and placeholders
- Using proper medical terminology

Here is the first batch (50 strings):
[paste JSON here]"

4. Үр дүнг хуулж, mn.json файл үүсгэнэ
5. 50 мөр бүрээр давтана (2,385 ÷ 50 = 48 batch)
```

**Хугацаа:** 2-3 цаг (manual copy-paste)  
**Зардал:** $20 (нэг сарын ChatGPT Plus)

---

### Хувилбар 2: Python Script (Автомат)

**Суулгалт:**
```powershell
# Python packages суулгах
pip install openai python-dotenv
```

**translate_simple.py файл үүсгэх:**
```python
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# .env файл уншина
load_dotenv()

# OpenAI client үүсгэнэ
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def translate_to_mongolian(english_text):
    """Нэг текст Монгол хэл дээр орчуулах"""
    
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system", 
                "content": "You are a medical translator. Translate UI strings to Mongolian (Cyrillic). Keep variables {{like_this}} unchanged."
            },
            {
                "role": "user", 
                "content": f"Translate to Mongolian: {english_text}"
            }
        ],
        temperature=0.3,  # Consistent translation
        max_tokens=200
    )
    
    return response.choices[0].message.content

# en.json уншина
with open('frontend/src/languages/en.json', 'r', encoding='utf-8') as f:
    en_data = json.load(f)

# Орчуулна
mn_data = {}
count = 0

for key, value in en_data.items():
    count += 1
    print(f"[{count}/{len(en_data)}] Translating: {key}")
    
    mn_data[key] = translate_to_mongolian(value)
    
    # Progress харуулах
    if count % 10 == 0:
        print(f"  ✓ {count} keys translated")

# mn.json хадгална
with open('frontend/src/languages/mn.json', 'w', encoding='utf-8') as f:
    json.dump(mn_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Done! {count} keys translated to Mongolian")
```

**Ажиллуулах:**
```powershell
python translate_simple.py
```

**Хугацаа:** 15-20 минут (2,385 keys)  
**Зардал:** ~$2.50

---

## 5. Зардал тооцоолол

### OpenAI Pricing (2026):

| Model | Input | Output | 2,385 keys зардал |
|-------|-------|--------|-------------------|
| GPT-4 Turbo | $10/1M tokens | $30/1M tokens | **$2.50** |
| GPT-3.5 Turbo | $0.50/1M tokens | $1.50/1M tokens | **$0.25** |

**Token тооцоолол:**
- 2,385 keys × 3 үг дундаж = 7,155 үг
- 1 үг ≈ 1.3 token
- Input: 7,155 × 1.3 = **9,300 tokens**
- Output (Mongolian): ~12,000 tokens (Cyrillic илүү урт)
- **Нийт:** ~21,000 tokens

**GPT-4 зардал:**
```
Input:  9,300 tokens × ($10/1M) = $0.093
Output: 12,000 tokens × ($30/1M) = $0.36
Total: $0.45 + safety margin = ~$2.50
```

---

## 6. Аюулгүй байдал ⚠️

### API Key хамгаалах:

✅ **Зөв арга:**
```
1. Environment variable ашиглах
2. .env файл (local only, Git-д БАЙХГҮЙ)
3. Password manager (LastPass, 1Password)
4. GitHub Secrets (CI/CD-д)
```

❌ **Буруу арга:**
```python
# ❌ Code дотор шууд бичих!
api_key = "sk-proj-abc123..."  # ХЭЗЭЭ Ч үүнийг битгий хий!

# ❌ GitHub-д push хийх
git add .env
git commit -m "Added API keys"  # АСУУДАЛ!
```

### Хэрэв API Key алдсан бол:

```
1. ШУУД OpenAI Platform руу орж key-г revoke хийнэ
2. Шинэ key үүсгэнэ
3. Алдсан key-г GitHub history-оос устгах хэрэгтэй бол:
   git filter-branch эсвэл BFG Repo-Cleaner ашигла
```

---

## 7. Rate Limits (Хэрэглээний хязгаар)

OpenAI хязгаарлалт:

| Данс түвшин | Requests/min | Tokens/min |
|-------------|--------------|------------|
| Free tier | 3 | 40,000 |
| Pay-as-you-go | 3,500 | 90,000 |
| Tier 1 ($5+) | 3,500 | 200,000 |
| Tier 2 ($50+) | 5,000 | 450,000 |

**Манай script:** 
- 2,385 requests needed
- 3,500 req/min хязгаартай бол 1 минутад бүгдийг нь илгээж болно
- Гэхдээ rate limiting-аас зайлсхийхийн тулд 1 секунд зогсоно (батах зөвлөгөө)

---

## 8. Бусад AI хувилбарууд

### Anthropic Claude (OpenAI-ийн өрсөлдөгч)

**Давуу тал:**
- Урт контекст (200K tokens)
- Medical terminology-д илүү сайн
- API илүү хямд ($15/1M vs $30/1M)

**API Key авах:**
```
1. https://console.anthropic.com руу орно
2. API Keys → Create Key
3. Кредит карт нэмнэ
```

**Python код:**
```python
import anthropic

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

message = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Translate to Mongolian: Hello"}
    ]
)

print(message.content[0].text)
```

### Google Gemini (Үнэгүй хувилбар бий)

**Давуу тал:**
- Free tier: 60 requests/minute
- Multimodal (зураг + текст)
- Хямд ($0.50/1M tokens)

**API Key авах:**
```
1. https://makersuite.google.com/app/apikey
2. Google account-аар нэвтэрнэ
3. "Create API Key" дарна
```

---

## 9. Туршилт хийх (Demo)

### Хурдан туршилт:

```powershell
# PowerShell дээр шууд туршиж үзэх
$env:OPENAI_API_KEY = "sk-proj-YOUR_KEY_HERE"

python -c "
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = client.chat.completions.create(
    model='gpt-4',
    messages=[
        {'role': 'user', 'content': 'Translate to Mongolian: Patient Registration'}
    ]
)

print(response.choices[0].message.content)
"
```

**Хүлээгдэж буй үр дүн:**
```
Өвчтөн бүртгэх
```

---

## 10. Асуулт & Хариулт

**Q: API Key-гүйгээр болох уу?**  
A: ChatGPT web (chat.openai.com) ашиглаж manual copy-paste хий. Удаан боловч API key-гүй.

**Q: $5 хүрэлцэх үү?**  
A: Тийм! 2,385 keys орчуулах нь ойролцоогоор $2.50. $5 deposit хангалттай.

**Q: Балансаа хэрхэн шалгах вэ?**  
A: OpenAI Platform → Usage → таны хэрэглээ + үлдэгдэл харагдана.

**Q: Монгол хэл дэмжигддэг үү?**  
A: Тийм! GPT-4 Cyrillic бичгийг маш сайн мэднэ. Mongolian орчуулгын чанар өндөр.

**Q: API key алдвал яах вэ?**  
A: Platform дээр шууд revoke хийгээд шинээр үүсгэ. Хуучин key нь ажиллахгүй болно.

**Q: Төлбөр хэзээ төлөгдөх вэ?**  
A: Real-time. Ашигласан даруйдаа балансаас хасагдана. Сарын эцэст credit card-с чарж хийнэ.

---

## Дүгнэлт

**API Key = Цахим хэрэглүүр:**

1. 💳 $5-10 deposit хий
2. 🔑 API key үүсгэ
3. 🤖 AI-д даалгавар өг (Python эсвэл web)
4. 📊 Үр дүн авч хадгал
5. 💰 Ашигласан хэмжээгээр л төлнө

**Манай тохиолдолд:**
- 2,385 UI strings орчуулна
- 15-20 минут хугацаа
- ~$2.50 зардал
- 3-5 хоног quality check

**AI-гүйгээр бол:** 2-3 долоо хоног + ₮3M зардал

---

🚀 **Дараагийн алхам:** API key аваад туршиж үз!
