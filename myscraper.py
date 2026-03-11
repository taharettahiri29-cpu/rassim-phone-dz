
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RASSIM OS - سكرابر لجمع البيانات
"""

import pandas as pd
import random
from datetime import datetime
import os

def generate_sample_data():
    """توليد بيانات تجريبية"""
    
    phones = [
        "0555123456", "0666123456", "0777123456", "0555987123", 
        "0665987123", "0775987123", "0555876123", "0665876123"
    ]
    
    titles = [
        "محل قطع غيار رونو",
        "خردة وبقايا حديد",
        "هاتف iPhone 13 للبيع",
        "محرك ديزل رونو كليو",
        "شقة للكراء في الجزائر",
        "عدد يدوية مستعملة"
    ]
    
    locations = [
        "16 - الجزائر", "31 - وهران", "25 - قسنطينة", 
        "42 - تيبازة", "06 - بجاية", "19 - سطيف"
    ]
    
    data = []
    for i in range(20):
        data.append({
            'title': random.choice(titles),
            'phone': random.choice(phones),
            'location': random.choice(locations),
            'price': random.randint(5000, 500000),
            'source': 'ouedkniss',
            'scraped_at': datetime.now().isoformat()
        })
    
    return data

def save_to_csv(data, filename):
    """حفظ البيانات إلى CSV"""
    df = pd.DataFrame(data)
    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", filename)
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    print(f"✅ تم حفظ {len(data)} سجل في {filepath}")
    return filepath

if __name__ == "__main__":
    print("🚀 جاري توليد بيانات تجريبية...")
    data = generate_sample_data()
    filename = f"leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = save_to_csv(data, filename)
    print(f"\n📊 لعرض البيانات: cat {filepath}")
    print(f"\n📤 لرفع البيانات: python upload_to_supabase.py {filepath}")
