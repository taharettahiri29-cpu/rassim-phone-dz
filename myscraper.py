import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import os
import time
import logging
import random
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import re
from concurrent.futures import ThreadPoolExecutor

# ==========================================
# 1️⃣ إعدادات النظام الاحترافية (TITANIUM MAX)
# ==========================================

BASE_FILE = "users_database.csv"
DB_FILE = "rassim_titanium_max_2026.db" # الربط مع قاعدة بيانات التطبيق
BACKUP_FOLDER = "backups"

# قائمة User-Agents محدثة لعام 2026 تشمل أجهزة حديثة
HEADERS_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | [%(threadName)s] %(message)s"
)

# ==========================================
# 2️⃣ Session ذكي مع نظام حماية (PRO PROXY-READY)
# ==========================================

def create_session():
    session = requests.Session()
    retries = Retry(
        total=7, # زيادة المحاولات لضمان الاستقرار
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# ==========================================
# 3️⃣ أدوات المعالجة المتقدمة
# ==========================================

def clean_phone(phone):
    cleaned = re.sub(r"\D", "", str(phone))
    return cleaned[-9:] if len(cleaned) >= 9 else cleaned

def create_backup():
    if not os.path.exists(BASE_FILE): return
    if not os.path.exists(BACKUP_FOLDER): os.makedirs(BACKUP_FOLDER)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_FOLDER, f"backup_{timestamp}.csv")
    pd.read_csv(BASE_FILE).to_csv(backup_path, index=False)
    logging.info(f"📦 تم تأمين نسخة احتياطية: {backup_path}")

# ==========================================
# 4️⃣ محرك استخراج البيانات الذكي
# ==========================================

def process_source(source):
    """دالة لمعالجة كل مصدر بشكل منفصل (دعم Multithreading)"""
    session = create_session()
    headers = {"User-Agent": random.choice(HEADERS_LIST), "Referer": "https://www.google.com/"}
    
    try:
        logging.info(f"🔎 فحص المنصة: {source['platform']}...")
        # هنا يتم وضع كود BeautifulSoup الحقيقي للموقع المستهدف
        # سنبقي البيانات الافتراضية كما طلبت مع تحسين هيكلها
        
        simulated_data = [
            ["iPhone 15 Pro Max", 195000, "0550112233", "16-الجزائر", "Titanium Natural - جلب آلي"],
            ["Samsung S24 Ultra", 210000, "0661445566", "31-وهران", "256GB - AI Features"],
            ["Google Pixel 8 Pro", 145000, "0770889900", "06-بجاية", "ممتاز كأنه جديد"],
            ["Xiaomi 14 Ultra", 168000, "0555223344", "25-قسنطينة", "Global Version"],
            ["Oppo Reno 11", 72000, "0666778899", "42-تيبازة", "همزة سوق النخبة"]
        ]
        
        results = []
        for item in simulated_data:
            item[2] = clean_phone(item[2])
            results.append(item)
            
        time.sleep(random.uniform(2, 4)) # تأخير عشوائي ذكي
        return results
    except Exception as e:
        logging.error(f"❌ خطأ في {source['platform']}: {e}")
        return []

# ==========================================
# 5️⃣ المزامنة مع قاعدة بيانات TITANIUM MAX
# ==========================================

def sync_to_sqlite(df):
    """مزامنة البيانات مباشرة مع التطبيق لضمان ظهورها للمستخدمين"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        for _, row in df.iterrows():
            # إدخال البيانات في جدول الإعلانات (ads) إذا لم تكن موجودة
            cursor.execute("""
                INSERT INTO ads (product, price, phone, wilaya, description, date, owner)
                SELECT ?, ?, ?, ?, ?, ?, 'Auto-Bot'
                WHERE NOT EXISTS (
                    SELECT 1 FROM ads WHERE product=? AND price=? AND phone=?
                )
            """, (row['Product'], row['Price'], row['Phone'], row['City'], row['Description'], 
                  datetime.now().strftime("%Y-%m-%d"), row['Product'], row['Price'], row['Phone']))
            
        conn.commit()
        conn.close()
        logging.info("🗄️ تمت المزامنة مع قاعدة بيانات SQL بنجاح")
    except Exception as e:
        logging.error(f"❌ خطأ أثناء مزامنة SQL: {e}")

# ==========================================
# 6️⃣ المحرك الرئيسي (Multithreaded Orchestrator)
# ==========================================

def run_titanium_scraper():
    logging.info("🚀 تشغيل محرك RASSIM DZ TITANIUM MAX [Intelligence Mode]")
    create_backup()

    sources = [
        {"url": "https://market-1.dz/phones", "platform": "Market_North"},
        {"url": "https://market-2.dz/phones", "platform": "Market_West"},
        {"url": "https://market-3.dz/phones", "platform": "Market_East"},
    ]

    all_data = []
    
    # استخدام ThreadPoolExecutor لسرعة البرق في جلب عدة مصادر معاً
    with ThreadPoolExecutor(max_workers=3, thread_name_prefix="Scraper") as executor:
        future_results = executor.map(process_source, sources)
        for result in future_results:
            all_data.extend(result)

    if not all_data:
        logging.warning("⚠️ لا توجد بيانات جديدة!")
        return

    # معالجة بـ Pandas
    df_new = pd.DataFrame(all_data, columns=["Product", "Price", "Phone", "City", "Description"])
    df_new["Last_Update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # دمج البيانات الذكي (بدون تكرار)
    if os.path.exists(BASE_FILE):
        df_old = pd.read_csv(BASE_FILE)
        df_final = pd.concat([df_old, df_new]).drop_duplicates(subset=["Product", "Price", "Phone"], keep='last')
    else:
        df_final = df_new

    # حفظ النتائج
    df_final.sort_values(by="Price", ascending=True, inplace=True)
    df_final.to_csv(BASE_FILE, index=False)
    
    # التحديث الفوري لتطبيق التيتانيوم
    sync_to_sqlite(df_new)

    logging.info(f"✅ المهمة تمت بنجاح | إجمالي السوق: {len(df_final)} إعلان")

if __name__ == "__main__":
    start = time.time()
    run_titanium_scraper()
    logging.info(f"⏱ الوقت الإجمالي: {round(time.time() - start, 2)} ثانية")
