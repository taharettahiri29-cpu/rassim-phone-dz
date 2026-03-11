#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RASSIM OS - رفع البيانات إلى Supabase
استخدام: python upload_to_supabase.py data/leads_20260311_143022.csv
"""

import pandas as pd
import os
import sys
from supabase import create_client
import streamlit as st
from datetime import datetime
import logging

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('upload.log'),
        logging.StreamHandler()
    ]
)

def load_secrets():
    """تحميل الأسرار من ملف secrets.toml"""
    try:
        import toml
        secrets_path = os.path.join('.streamlit', 'secrets.toml')
        if os.path.exists(secrets_path):
            secrets = toml.load(secrets_path)
            return secrets
        else:
            logging.error(f"❌ ملف secrets.toml غير موجود في {secrets_path}")
            return None
    except Exception as e:
        logging.error(f"❌ خطأ في تحميل الأسرار: {e}")
        return None

def upload_csv_to_supabase(csv_file: str):
    """رفع بيانات CSV إلى Supabase"""
    
    logging.info(f"🚀 بدء رفع الملف: {csv_file}")
    
    # تحميل الأسرار
    secrets = load_secrets()
    if not secrets:
        return False
    
    # الاتصال بـ Supabase
    try:
        url = secrets["connections"]["supabase"]["url"]
        key = secrets["connections"]["supabase"]["key"]
        supabase = create_client(url, key)
        logging.info("✅ تم الاتصال بـ Supabase")
    except Exception as e:
        logging.error(f"❌ فشل الاتصال بـ Supabase: {e}")
        return False
    
    # التحقق من وجود الملف
    if not os.path.exists(csv_file):
        logging.error(f"❌ الملف غير موجود: {csv_file}")
        return False
    
    # قراءة البيانات
    try:
        df = pd.read_csv(csv_file)
        logging.info(f"📊 تم قراءة {len(df)} سجل من الملف")
        logging.info(f"📋 الأعمدة الموجودة: {list(df.columns)}")
    except Exception as e:
        logging.error(f"❌ خطأ في قراءة الملف: {e}")
        return False
    
    # تحقق من وجود الأعمدة المطلوبة
    required_columns = ['phone']
    for col in required_columns:
        if col not in df.columns:
            logging.error(f"❌ العمود المطلوب '{col}' غير موجود في الملف")
            return False
    
    # تحويل إلى قاموس ورفع
    records = df.to_dict('records')
    success_count = 0
    skip_count = 0
    error_count = 0
    
    logging.info(f"🔄 جاري رفع {len(records)} سجل...")
    
    for i, record in enumerate(records):
        try:
            # تنظيف رقم الهاتف
            phone = str(record.get('phone', '')).strip()
            if not phone or len(phone) < 10:
                logging.warning(f"⚠️ رقم هاتف غير صالح في السجل {i+1}: {phone}")
                skip_count += 1
                continue
            
            # التحقق من عدم التكرار
            existing = supabase.table("leads").select("*").eq("phone", phone).execute()
            
            if not existing.data:
                # تحضير البيانات للإدراج
                data_to_insert = {
                    "name": str(record.get('title', record.get('name', '')))[:100],
                    "phone": phone,
                    "wilaya": str(record.get('location', record.get('wilaya', 'غير معروف')))[:50],
                    "source": str(record.get('source', 'scraper'))[:50],
                    "contacted": False,
                    "created_at": datetime.now().isoformat()
                }
                
                # إدراج في قاعدة البيانات
                supabase.table("leads").insert(data_to_insert).execute()
                success_count += 1
                
                # عرض تقدم كل 10 سجلات
                if success_count % 10 == 0:
                    logging.info(f"✅ تم رفع {success_count} سجل...")
            else:
                logging.info(f"⏭️ موجود مسبقاً: {phone}")
                skip_count += 1
                
        except Exception as e:
            logging.error(f"❌ خطأ في السجل {i+1}: {e}")
            error_count += 1
    
    # عرض التقرير النهائي
    logging.info("=" * 50)
    logging.info("📊 تقرير الرفع النهائي:")
    logging.info(f"   ✅ تم الرفع بنجاح: {success_count}")
    logging.info(f"   ⏭️ تم التخطي (موجود مسبقاً): {skip_count}")
    logging.info(f"   ❌ أخطاء: {error_count}")
    logging.info("=" * 50)
    
    return True

def main():
    """الدالة الرئيسية"""
    
    print("\n" + "=" * 60)
    print("🚀 RASSIM OS - أداة رفع البيانات إلى Supabase")
    print("=" * 60 + "\n")
    
    # التحقق من وجود مسار الملف
    if len(sys.argv) < 2:
        print("❌ خطأ: يجب تحديد مسار ملف CSV")
        print("\n📌 الاستخدام الصحيح:")
        print("   python upload_to_supabase.py data/leads_20260311_143022.csv")
        print("\n📁 الملفات المتاحة في مجلد data/:")
        data_dir = "data"
        if os.path.exists(data_dir):
            files = os.listdir(data_dir)
            for f in files:
                if f.endswith('.csv'):
                    print(f"   - data/{f}")
        else:
            print("   (لا توجد ملفات في مجلد data/)")
        return
    
    csv_file = sys.argv[1]
    upload_csv_to_supabase(csv_file)

if __name__ == "__main__":
    main()
