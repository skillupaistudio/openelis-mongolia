#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автомат Монгол орчуулга - OpenELIS
Бүх англи key-г монгол руу орчуулна
"""

import json
import sys
from pathlib import Path

# Медицины нэр томъёо толь бичиг
MEDICAL_TERMS = {
    # Дээжийн төрөл
    "Blood": "Цус",
    "Urine": "Шээс", 
    "Stool": "Баас",
    "Sputum": "Цэрэгцлэх",
    "Serum": "Сийвэн",
    "Plasma": "Плазма",
    "Saliva": "Шүлс",
    "CSF": "Нугасны шингэн",
    "Tissue": "Эд",
    "Swab": "Арчдас",
    
    # Шинжилгээний төрөл
    "Hematology": "Цусны шинжилгээ",
    "Biochemistry": "Биохими",
    "Microbiology": "Нян судлал",
    "Immunology": "Дархлал судлал",
    "Serology": "Сийвэн судлал",
    "Virology": "Вирус судлал",
    "Parasitology": "Шимэгч судлал",
    "Cytology": "Эс судлал",
    "Histology": "Эд судлал",
    "Molecular Biology": "Молекул биологи",
    
    # Үр дүн
    "Positive": "Эерэг",
    "Negative": "Сөрөг",
    "Normal": "Хэвийн",
    "Abnormal": "Хэвийн бус",
    "Pending": "Хүлээгдэж буй",
    "In Progress": "Гүйцэтгэж буй",
    "Completed": "Дууссан",
    "Validated": "Баталгаажсан",
    "Rejected": "Татгалзсан",
    
    # Эмнэлгийн үзүүлэлт
    "Hemoglobin": "Гемоглобин",
    "Glucose": "Глюкоз",
    "Cholesterol": "Холестерол",
    "Creatinine": "Креатинин",
    "Bilirubin": "Билирубин",
    "WBC": "Цагаан цус",
    "RBC": "Улаан цус",
    "Platelet": "Тромбоцит",
}

# Ерөнхий орчуулгын толь
COMMON_TRANSLATIONS = {
    # Үйлдэл
    "Add": "Нэмэх",
    "Edit": "Засах",
    "Delete": "Устгах",
    "Save": "Хадгалах",
    "Cancel": "Цуцлах",
    "Submit": "Илгээх",
    "Search": "Хайх",
    "Print": "Хэвлэх",
    "Back": "Буцах",
    "Next": "Дараах",
    "Previous": "Өмнөх",
    "Finish": "Дуусгах",
    "Close": "Хаах",
    "Accept": "Зөвшөөрөх",
    "Reject": "Татгалзах",
    "Confirm": "Баталгаажуулах",
    "View": "Харах",
    "Load": "Ачаалах",
    "Export": "Экспортлох",
    "Import": "Импортлох",
    
    # Ерөнхий
    "Home": "Нүүр",
    "Patient": "Өвчтөн",
    "Order": "Захиалга",
    "Sample": "Дээж",
    "Test": "Шинжилгээ",
    "Result": "Үр дүн",
    "Report": "Тайлан",
    "Admin": "Удирдлага",
    "Help": "Тусламж",
    "Version": "Хувилбар",
    "Date": "Огноо",
    "Time": "Цаг",
    "Status": "Төлөв",
    "Name": "Нэр",
    "Description": "Тайлбар",
    "Value": "Утга",
    "Type": "Төрөл",
    "Active": "Идэвхитэй",
    "Inactive": "Идэвхгүй",
    
    # Хүмүүс
    "First Name": "Нэр",
    "Last Name": "Овог",
    "Gender": "Хүйс",
    "Male": "Эрэгтэй",
    "Female": "Эмэгтэй",
    "Birth Date": "Төрсөн огноо",
    "Age": "Нас",
    "Phone": "Утас",
    "Email": "Цахим шуудан",
    "Address": "Хаяг",
    
    # Мессеж
    "Success": "Амжилттай",
    "Error": "Алдаа",
    "Warning": "Анхааруулга",
    "Info": "Мэдээлэл",
    "Saved successfully": "Амжилттай хадгалагдлаа",
    "Deleted successfully": "Амжилттай устгагдлаа",
    "Are you sure": "Та итгэлтэй байна уу",
    "Required": "Заавал",
    "Optional": "Заавал биш",
    "Yes": "Тийм",
    "No": "Үгүй",
    "OK": "ОК",
    "Access Denied": "Нэвтрэх эрхгүй",
}


def smart_translate(english_text):
    """
    Англи текстийг монгол руу ухаалаг орчуулна
    """
    # Хоосон эсвэл маш богино текст
    if not english_text or len(english_text) < 2:
        return english_text
    
    # Эхлээд бүтэн өгүүлбэрээр хайх
    if english_text in MEDICAL_TERMS:
        return MEDICAL_TERMS[english_text]
    if english_text in COMMON_TRANSLATIONS:
        return COMMON_TRANSLATIONS[english_text]
    
    # Үг бүрээр хайж орчуулах
    words = english_text.split()
    translated_words = []
    
    for word in words:
        # Цэг, таслал зэргийг салгах
        clean_word = word.strip('.,!?:;()[]{}\'\"')
        
        if clean_word in MEDICAL_TERMS:
            translated_words.append(MEDICAL_TERMS[clean_word])
        elif clean_word in COMMON_TRANSLATIONS:
            translated_words.append(COMMON_TRANSLATIONS[clean_word])
        else:
            # Орчуулагдаагүй үлдээх (техник нэр томъёо)
            translated_words.append(word)
    
    return ' '.join(translated_words)


def translate_all():
    """
    en.json-ийн бүх key-г mn.json руу орчуулна
    """
    base_dir = Path(__file__).parent.parent
    en_file = base_dir / 'frontend' / 'src' / 'languages' / 'en.json'
    mn_file = base_dir / 'frontend' / 'src' / 'languages' / 'mn.json'
    
    # Англи файл уншиx
    print(f"📖 Уншиж байна: {en_file}")
    with open(en_file, 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    # Одоогийн монгол файл уншиx (хэрэв байвал)
    mn_data = {}
    if mn_file.exists():
        print(f"📖 Одоогийн монгол орчуулга: {mn_file}")
        with open(mn_file, 'r', encoding='utf-8') as f:
            mn_data = json.load(f)
    
    print(f"\n📊 Тоо:")
    print(f"   Англи: {len(en_data)} key")
    print(f"   Монгол (одоо): {len(mn_data)} key")
    print(f"   Дутуу: {len(en_data) - len(mn_data)} key")
    
    # Орчуулга эхлүүлэх
    print(f"\n🔄 Орчуулга эхэлж байна...\n")
    
    translated_count = 0
    skipped_count = 0
    
    for key, english_value in en_data.items():
        # Аль хэдийн орчуулсан бол алгасах
        if key in mn_data:
            skipped_count += 1
            continue
        
        # Орчуулах
        mongolian_value = smart_translate(english_value)
        mn_data[key] = mongolian_value
        translated_count += 1
        
        # Progress харуулах (хэрэв 100 key бүр)
        if translated_count % 100 == 0:
            print(f"   ✅ {translated_count} key орчуулагдлаа...")
    
    print(f"\n📊 Дүн:")
    print(f"   ✅ Шинээр орчуулсан: {translated_count}")
    print(f"   ⏭️  Алгассан (өмнө нь орчуулсан): {skipped_count}")
    print(f"   📝 Нийт: {len(mn_data)} key")
    
    # Хадгалах
    print(f"\n💾 Хадгалж байна: {mn_file}")
    with open(mn_file, 'w', encoding='utf-8') as f:
        json.dump(mn_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Амжилттай дууслаа!")
    print(f"   Coverage: {len(mn_data)/len(en_data)*100:.1f}%")
    
    return translated_count


if __name__ == '__main__':
    try:
        translate_all()
    except Exception as e:
        print(f"\n❌ Алдаа: {e}", file=sys.stderr)
        sys.exit(1)
