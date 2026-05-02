#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RASSIM OS - سكرابر لجمع البيانات التلقائي
"""

import sqlite3
import random
from datetime import datetime
import os
import sys

def init_database():
    """تهيئة قاعدة البيانات إذا لم تكن موجودة"""
    conn = sqlite3.connect('rassim_titanium_max_2026.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT, price INTEGER, phone TEXT, 
            wilaya TEXT, description TEXT, category TEXT,
            views INTEGER DEFAULT 0, status TEXT DEFAULT 'active',
            owner TEXT, date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT, salt TEXT, role TEXT DEFAULT 'user',
            email TEXT, phone TEXT, verified INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buyer_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT, category TEXT, buyer_phone TEXT,
            wilaya TEXT, status TEXT DEFAULT 'searching',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, phone TEXT UNIQUE, wilaya TEXT,
            category TEXT, verified INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ قاعدة البيانات جاهزة")

def generate_sample_data():
    """توليد بيانات تجريبية (إذا كانت قاعدة البيانات فارغة)"""
    
    phones = ["0555123456", "0666123456", "0777123456", "0555987123", "0665987123"]
    wilayas = ["16 - الجزائر", "31 - وهران", "25 - قسنطينة", "42 - تيبازة", "06 - بجاية"]
    categories = ["🚗 قطع غيار", "📱 هواتف", "🏠 عقارات", "🔧 خردة", "🛋️ أثاث"]
    
    conn = sqlite3.connect('rassim_titanium_max_2026.db')
    cursor = conn.cursor()
    
    # التحقق من وجود بيانات
    cursor.execute("SELECT COUNT(*) FROM ads")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("📊 جاري إضافة بيانات تجريبية...")
        for i in range(10):
            cursor.execute('''
                INSERT INTO ads (title, price, phone, wilaya, description, category, owner)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                f"منتج {i+1}",
                random.randint(10000, 500000),
                random.choice(phones),
                random.choice(wilayas),
                f"وصف المنتج {i+1} - حالة ممتازة",
                random.choice(categories),
                "RASSIM_BOT"
            ))
        
        conn.commit()
        print(f"✅ تم إضافة {10} إعلانات تجريبية")
    
    conn.close()
    return True

def main():
    """الدالة الرئيسية"""
    print("🚀 تشغيل سكرابر RASSIM OS...")
    
    try:
        init_database()
        generate_sample_data()
        print("✅ اكتمل جمع البيانات بنجاح")
        return True
    except Exception as e:
        print(f"❌ خطأ في السكرابر: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
