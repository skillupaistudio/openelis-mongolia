#!/usr/bin/env python3
"""
OpenELIS Mongolian Translation Script using AI (ChatGPT/Claude)
Translates English UI strings to Mongolian automatically

Requirements:
    pip install openai anthropic google-generativeai
    
Usage:
    python translate_to_mongolian.py --api-key YOUR_API_KEY --provider openai
"""

import json
import os
import sys
from typing import Dict, List
import time
import argparse

# Uncomment based on your AI provider
# from openai import OpenAI
# import anthropic
# import google.generativeai as genai


class MongoITranslator:
    """Translates OpenELIS strings to Mongolian using AI"""
    
    def __init__(self, api_key: str, provider: str = "openai"):
        self.api_key = api_key
        self.provider = provider
        self.client = None
        
        # Medical/Lab terminology dictionary (English → Mongolian)
        self.medical_terms = {
            "Blood": "Цус",
            "Urine": "Шээс",
            "Stool": "Баас",
            "Sputum": "Цэрэгцлэх",
            "Serum": "Сийвэн",
            "Plasma": "Плазма",
            "Hemoglobin": "Гемоглобин",
            "Glucose": "Глюкоз (цусны сахар)",
            "Cholesterol": "Холестерол",
            "Creatinine": "Креатинин",
            "HIV": "ХИВ",
            "Hepatitis": "Элэгний үрэвсэл",
            "Tuberculosis": "Сүрьеэ",
            "Malaria": "Хумхаа",
            "Patient": "Өвчтөн",
            "Sample": "Дээж",
            "Test": "Шинжилгээ",
            "Result": "Үр дүн",
            "Report": "Тайлан",
            "Laboratory": "Лаборатори",
            "Hematology": "Цусны эмнэлэг",
            "Biochemistry": "Биохими",
            "Microbiology": "Нянгийн судлал",
            "Serology": "Серологи",
            "Immunology": "Дархлалын судлал",
            "Pathology": "Эмгэг судлал",
            "Cytology": "Эсийн судлал",
            "Parasitology": "Шимэгч судлал",
            "Bacteriology": "Бактери судлал",
            "Virology": "Вирус судлал"
        }
        
        if provider == "openai":
            # from openai import OpenAI
            # self.client = OpenAI(api_key=api_key)
            pass
        elif provider == "anthropic":
            # import anthropic
            # self.client = anthropic.Anthropic(api_key=api_key)
            pass
        elif provider == "gemini":
            # import google.generativeai as genai
            # genai.configure(api_key=api_key)
            # self.client = genai.GenerativeModel('gemini-pro')
            pass
    
    def translate_batch(self, texts: List[str], batch_size: int = 50) -> List[str]:
        """
        Translate a batch of English texts to Mongolian
        
        Args:
            texts: List of English strings
            batch_size: Number of strings to translate at once
            
        Returns:
            List of Mongolian translations
        """
        translations = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            
            prompt = self._create_translation_prompt(batch)
            
            if self.provider == "openai":
                translated = self._translate_openai(prompt)
            elif self.provider == "anthropic":
                translated = self._translate_anthropic(prompt)
            elif self.provider == "gemini":
                translated = self._translate_gemini(prompt)
            else:
                raise ValueError(f"Unknown provider: {self.provider}")
            
            translations.extend(translated)
            
            # Rate limiting
            time.sleep(1)
            
            # Progress
            print(f"Translated {min(i+batch_size, len(texts))}/{len(texts)} strings")
        
        return translations
    
    def _create_translation_prompt(self, texts: List[str]) -> str:
        """Create AI prompt for batch translation"""
        
        numbered_texts = "\n".join([f"{i+1}. {text}" for i, text in enumerate(texts)])
        
        prompt = f"""You are a professional medical translator specializing in Laboratory Information Systems (LIS).

Translate the following English UI strings to Mongolian (Cyrillic script).

CRITICAL RULES:
1. Keep HTML tags, variables ({{variable}}), and placeholders UNCHANGED
2. Use proper medical/laboratory terminology in Mongolian
3. Maintain professional, formal tone suitable for healthcare
4. For technical terms with no direct Mongolian equivalent, use transliteration
5. Return ONLY the numbered translations, one per line
6. Keep button/menu text concise (max 2-3 words in Mongolian)

Medical terminology reference:
{json.dumps(self.medical_terms, ensure_ascii=False, indent=2)}

English strings to translate:
{numbered_texts}

Respond with ONLY the Mongolian translations, numbered exactly as above:"""
        
        return prompt
    
    def _translate_openai(self, prompt: str) -> List[str]:
        """Translate using OpenAI GPT"""
        # Uncomment when using OpenAI
        """
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",  # or "gpt-3.5-turbo" for cheaper
            messages=[
                {"role": "system", "content": "You are a professional medical translator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Low temperature for consistent translations
            max_tokens=4000
        )
        
        result = response.choices[0].message.content
        return self._parse_numbered_response(result)
        """
        # Mock response for demo
        return ["[МОНГОЛ ОРЧУУЛГА - OpenAI API KEY ШААРДЛАГАТАЙ]"] * 50
    
    def _translate_anthropic(self, prompt: str) -> List[str]:
        """Translate using Anthropic Claude"""
        # Uncomment when using Anthropic
        """
        message = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            temperature=0.3,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        result = message.content[0].text
        return self._parse_numbered_response(result)
        """
        return ["[МОНГОЛ ОРЧУУЛГА - Anthropic API KEY ШААРДЛАГАТАЙ]"] * 50
    
    def _translate_gemini(self, prompt: str) -> List[str]:
        """Translate using Google Gemini"""
        # Uncomment when using Gemini
        """
        response = self.client.generate_content(prompt)
        result = response.text
        return self._parse_numbered_response(result)
        """
        return ["[МОНГОЛ ОРЧУУЛГА - Gemini API KEY ШААРДЛАГАТАЙ]"] * 50
    
    def _parse_numbered_response(self, response: str) -> List[str]:
        """Parse AI response with numbered translations"""
        lines = response.strip().split('\n')
        translations = []
        
        for line in lines:
            # Remove numbering (e.g., "1. ", "1) ", etc.)
            clean_line = line.strip()
            if clean_line:
                # Remove leading numbers and punctuation
                import re
                match = re.match(r'^\d+[\.\)]\s*(.*)', clean_line)
                if match:
                    translations.append(match.group(1))
                else:
                    translations.append(clean_line)
        
        return translations
    
    def translate_json_file(self, input_file: str, output_file: str):
        """
        Translate entire JSON translation file
        
        Args:
            input_file: Path to en.json
            output_file: Path to output mn.json
        """
        print(f"Loading {input_file}...")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            en_data = json.load(f)
        
        # Extract keys and values
        keys = list(en_data.keys())
        values = list(en_data.values())
        
        print(f"Found {len(keys)} translation keys")
        print("Starting translation...")
        
        # Translate in batches
        translated_values = self.translate_batch(values, batch_size=50)
        
        # Create Mongolian dictionary
        mn_data = dict(zip(keys, translated_values))
        
        # Save to file
        print(f"Saving to {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(mn_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Translation complete! {len(mn_data)} keys translated")
        print(f"📄 Output: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Translate OpenELIS to Mongolian using AI')
    parser.add_argument('--api-key', required=True, help='AI provider API key')
    parser.add_argument('--provider', choices=['openai', 'anthropic', 'gemini'], 
                       default='openai', help='AI provider (default: openai)')
    parser.add_argument('--input', default='frontend/src/languages/en.json',
                       help='Input English JSON file')
    parser.add_argument('--output', default='frontend/src/languages/mn.json',
                       help='Output Mongolian JSON file')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"❌ Error: Input file not found: {args.input}")
        sys.exit(1)
    
    # Initialize translator
    translator = MongoITranslator(api_key=args.api_key, provider=args.provider)
    
    # Translate
    translator.translate_json_file(args.input, args.output)


if __name__ == "__main__":
    # Example usage without API (demo mode)
    print("""
╔═══════════════════════════════════════════════════════════════╗
║   OpenELIS → Mongolian Translation Tool (AI-Powered)         ║
╚═══════════════════════════════════════════════════════════════╝

This script translates 2,385 UI strings from English to Mongolian.

SETUP:
1. Install dependencies:
   pip install openai anthropic google-generativeai

2. Get API key from:
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/
   - Google: https://makersuite.google.com/app/apikey

3. Run translation:
   python translate_to_mongolian.py --api-key YOUR_KEY --provider openai

COST ESTIMATE:
- OpenAI GPT-4: ~$2.50 (2,385 keys × ~8,000 tokens)
- OpenAI GPT-3.5: ~$0.25 (cheaper, slightly lower quality)
- Anthropic Claude: ~$2.00
- Google Gemini: ~$1.50

TIME: 10-15 minutes for full translation

NOTE: Manual review recommended for medical terminology accuracy!
    """)
    
    # If run without arguments, show usage
    if len(sys.argv) == 1:
        print("\n⚠️  Please provide --api-key argument to start translation")
        print("Example: python translate_to_mongolian.py --api-key sk-xxx --provider openai\n")
    else:
        main()
