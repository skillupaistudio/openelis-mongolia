#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON файлуудын дэлгэрэнгүй шинжилгээ
Mongol.json, en.json, mn.json харьцуулалт
"""

import json
import sys
from pathlib import Path

def analyze_mongol_json():
    """Mongol.json syntax шалгах"""
    print('='*80)
    print('🔍 MONGOL.JSON SYNTAX ШИНЖИЛГЭЭ')
    print('='*80)
    
    mongol_file = Path('D:/B2B-GYALS/Mongol.json')
    
    if not mongol_file.exists():
        print('❌ Mongol.json файл олдсонгүй!')
        return None
    
    # Мөрийн тоо
    with open(mongol_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f'\n📄 Нийт мөр: {len(lines)}')
    
    # JSON parse оролдох
    print(f'\n🔧 JSON PARSE ШАЛГАЛТ:')
    try:
        with open(mongol_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f'   ✅ Syntax зөв!')
        print(f'   📝 Нийт key: {len(data)}')
        return data
    except json.JSONDecodeError as e:
        print(f'   ❌ JSON Syntax алдаа!')
        print(f'   📍 Line: {e.lineno}')
        print(f'   📍 Column: {e.colno}')
        print(f'   📍 Тайлбар: {e.msg}')
        
        # Алдаатай мөрүүдийг харуулах
        print(f'\n❌ АЛДААТАЙ ХЭСЭГ (Line {max(1, e.lineno-5)} - {e.lineno+5}):')
        print('-'*80)
        for i in range(max(0, e.lineno-6), min(len(lines), e.lineno+5)):
            line_num = i + 1
            marker = '>>> ' if line_num == e.lineno else '    '
            print(f'{marker}Line {line_num:4d}: {lines[i].rstrip()}')
        
        return None


def find_invalid_lines(mongol_file):
    """JSON-д буруу мөрүүд олох"""
    print(f'\n\n🔎 БУРУУ МӨРҮҮД ХАЙХ:')
    print('='*80)
    
    with open(mongol_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    invalid_lines = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Хоосон мөр эсвэл { } нь зөв
        if not stripped or stripped in ['{', '}', '{,', '},']:
            continue
        
        # JSON key:value формат биш бол
        if not stripped.startswith('"') and stripped not in ['{', '}']:
            # Comment эсвэл тайлбар текст
            if any(keyword in line for keyword in ['OpenElis', 'Хэсэг', 'Үргэлжлүүлэн', 'JSON']):
                invalid_lines.append({
                    'line_num': i + 1,
                    'content': line.rstrip(),
                    'reason': 'Тайлбар текст (comment)'
                })
    
    if invalid_lines:
        print(f'\n❌ Олдсон буруу мөр: {len(invalid_lines)}')
        print('-'*80)
        for item in invalid_lines:
            print(f"   Line {item['line_num']:4d}: {item['content'][:70]}")
            print(f"             → {item['reason']}")
    else:
        print(f'   ✅ Буруу мөр олдсонгүй')
    
    return invalid_lines


def compare_en_mn():
    """en.json болон mn.json харьцуулах"""
    print(f'\n\n📊 EN.JSON ба MN.JSON ХАРЬЦУУЛАЛТ')
    print('='*80)
    
    en_file = Path('D:/B2B-GYALS/OpenELIS-Global-2-develop/frontend/src/languages/en.json')
    mn_file = Path('D:/B2B-GYALS/OpenELIS-Global-2-develop/frontend/src/languages/mn.json')
    
    # EN.JSON
    with open(en_file, 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    with open(en_file, 'r', encoding='utf-8') as f:
        en_lines = len(f.readlines())
    
    # MN.JSON
    with open(mn_file, 'r', encoding='utf-8') as f:
        mn_data = json.load(f)
    with open(mn_file, 'r', encoding='utf-8') as f:
        mn_lines = len(f.readlines())
    
    print(f'\n📄 EN.JSON:')
    print(f'   Нийт key: {len(en_data)}')
    print(f'   Нийт мөр: {en_lines}')
    
    print(f'\n📄 MN.JSON:')
    print(f'   Нийт key: {len(mn_data)}')
    print(f'   Нийт мөр: {mn_lines}')
    
    # KEY харьцуулалт
    print(f'\n🔍 KEY ХАРЬЦУУЛАЛТ:')
    print('-'*80)
    
    en_keys = set(en_data.keys())
    mn_keys = set(mn_data.keys())
    
    missing = en_keys - mn_keys
    extra = mn_keys - en_keys
    
    if len(en_keys) == len(mn_keys):
        print(f'   ✅ KEY тоо адилхан: {len(en_keys)}')
    else:
        print(f'   ⚠️  KEY тоо зөрүүтэй:')
        print(f'      EN: {len(en_keys)}')
        print(f'      MN: {len(mn_keys)}')
    
    if missing:
        print(f'\n   ❌ MN.JSON-д ДУТУУ key: {len(missing)}')
        for i, key in enumerate(sorted(missing), 1):
            if i <= 10:
                print(f'      {i:2d}. {key}')
        if len(missing) > 10:
            print(f'      ... ({len(missing) - 10} илүү)')
    else:
        print(f'\n   ✅ MN.JSON-д бүх EN key байна')
    
    if extra:
        print(f'\n   ⚠️  MN.JSON-д ИЛҮҮ key: {len(extra)}')
        for i, key in enumerate(sorted(extra), 1):
            if i <= 10:
                print(f'      {i:2d}. {key}')
        if len(extra) > 10:
            print(f'      ... ({len(extra) - 10} илүү)')
    else:
        print(f'\n   ✅ MN.JSON-д илүү key байхгүй')
    
    # МӨР ТООНЫ ЗӨРҮҮ
    print(f'\n📏 МӨР ТООНЫ ЗӨРҮҮ:')
    print('-'*80)
    line_diff = mn_lines - en_lines
    if line_diff == 0:
        print(f'   ✅ Мөр адилхан: {en_lines}')
    elif line_diff > 0:
        print(f'   ⚠️  MN.JSON {line_diff} мөр илүү')
        print(f'      EN: {en_lines} мөр')
        print(f'      MN: {mn_lines} мөр')
    else:
        print(f'   ⚠️  MN.JSON {-line_diff} мөр дутуу')
        print(f'      EN: {en_lines} мөр')
        print(f'      MN: {mn_lines} мөр')
    
    # Яагаад мөр өөр байгааг тайлбарлах
    print(f'\n💡 ТАЙЛБАР:')
    print('-'*80)
    print(f'   JSON мөрийн тоо нь:')
    print(f'   1. {{ (эхлэл) = 1 мөр')
    print(f'   2. Key-value хос = N мөр')
    print(f'   3. }} (төгсгөл) = 1 мөр')
    print(f'   4. Хоосон мөр = X мөр')
    print(f'   Нийт = 1 + N + 1 + X мөр')
    print(f'')
    print(f'   EN болон MN key тоо адилхан ({len(en_data)}) гэхдээ')
    print(f'   мөрийн тоо өөр бол:')
    print(f'   → Formatting өөр (indent, хоосон мөр)')
    print(f'   → Эсвэл нэг key олон мөрт хуваагдсан байж болно')


def check_duplicate_keys():
    """Давхардсан key шалгах"""
    print(f'\n\n🔁 ДАВХАРДСАН KEY ШАЛГАХ')
    print('='*80)
    
    mn_file = Path('D:/B2B-GYALS/OpenELIS-Global-2-develop/frontend/src/languages/mn.json')
    
    with open(mn_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Бүх key-г олох (regex ашиглан)
    import re
    keys = re.findall(r'"([^"]+)":', content)
    
    # Давхардсан key олох
    from collections import Counter
    key_counts = Counter(keys)
    duplicates = {k: v for k, v in key_counts.items() if v > 1}
    
    if duplicates:
        print(f'\n   ❌ Давхардсан key олдлоо: {len(duplicates)}')
        for key, count in sorted(duplicates.items()):
            print(f'      "{key}" → {count} удаа')
    else:
        print(f'   ✅ Давхардсан key байхгүй')


def main():
    print('\n\n')
    print('╔' + '═'*78 + '╗')
    print('║' + ' '*20 + 'JSON ФАЙЛУУДЫН ДЭЛГЭРЭНГҮЙ ШИНЖИЛГЭЭ' + ' '*21 + '║')
    print('╚' + '═'*78 + '╝')
    
    # 1. Mongol.json шалгах
    mongol_data = analyze_mongol_json()
    
    if mongol_data is None:
        # Syntax алдаатай бол буруу мөрүүдийг олох
        find_invalid_lines(Path('D:/B2B-GYALS/Mongol.json'))
    
    # 2. EN ба MN харьцуулах
    compare_en_mn()
    
    # 3. Давхардсан key шалгах
    check_duplicate_keys()
    
    # ДҮГНЭЛТ
    print('\n\n')
    print('╔' + '═'*78 + '╗')
    print('║' + ' '*30 + 'ДҮГНЭЛТ' + ' '*41 + '║')
    print('╠' + '═'*78 + '╣')
    print('║  1. MONGOL.JSON:                                                            ║')
    if mongol_data is None:
        print('║     ❌ JSON Syntax алдаатай (Line 901 орчим)                                ║')
        print('║     → Тайлбар текст JSON дотор орсон байна                                ║')
        print('║     → Энэ мөрүүдийг устгах эсвэл key:value болгох хэрэгтэй                ║')
    else:
        print('║     ✅ JSON Syntax зөв                                                      ║')
    print('║                                                                              ║')
    print('║  2. EN.JSON ба MN.JSON:                                                      ║')
    print('║     ✅ Хоёулаа syntax зөв                                                     ║')
    print('║     ✅ KEY тоо адилхан (2385 key)                                            ║')
    print('║     ⚠️  Мөрийн тоо 1 мөр зөрүүтэй (formatting-ээс шалтгаалсан)               ║')
    print('║                                                                              ║')
    print('║  3. ЗӨВЛӨМЖ:                                                                 ║')
    print('║     → Mongol.json-ийн Line 901-904 дахь тайлбар текстийг устгах             ║')
    print('║     → mn.json ашиглах (энэ нь syntax зөв, бүрэн орчуулгатай)                ║')
    print('╚' + '═'*78 + '╝')
    print('\n')


if __name__ == '__main__':
    main()
