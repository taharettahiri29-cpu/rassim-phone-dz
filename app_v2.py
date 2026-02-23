import streamlit as st
import sqlite3
import pandas as pd
import hashlib
import secrets
import time
import plotly.graph_objects as go
import warnings
import os
import base64
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re

warnings.filterwarnings('ignore')

# ==========================================
# 1. إعدادات الصفحة المتقدمة
# ==========================================
st.set_page_config(
    page_title="RASSIM OS ULTIMATE 2026 • 69 ولاية",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto"
)

# ==========================================
# 2. إنشاء مجلد uploads إذا لم يكن موجوداً
# ==========================================
UPLOADS_DIR = "uploads"
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

# ==========================================
# 3. قائمة الولايات الجزائرية (69 ولاية)
# ==========================================
ALGERIAN_WILAYAS = [
    "الكل",
    "01 - أدرار", "02 - الشلف", "03 - الأغواط", "04 - أم البواقي", "05 - باتنة",
    "06 - بجاية", "07 - بسكرة", "08 - بشار", "09 - البليدة", "10 - البويرة",
    "11 - تمنراست", "12 - تبسة", "13 - تلمسان", "14 - تيارت", "15 - تيزي وزو",
    "16 - الجزائر", "17 - الجلفة", "18 - جيجل", "19 - سطيف", "20 - سعيدة",
    "21 - سكيكدة", "22 - سيدي بلعباس", "23 - عنابة", "24 - قالمة", "25 - قسنطينة",
    "26 - المدية", "27 - مستغانم", "28 - المسيلة", "29 - معسكر", "30 - ورقلة",
    "31 - وهران", "32 - البيض", "33 - إليزي", "34 - برج بوعريريج", "35 - بومرداس",
    "36 - الطارف", "37 - تندوف", "38 - تيسمسيلت", "39 - الوادي", "40 - خنشلة",
    "41 - سوق أهراس", "42 - تيبازة", "43 - ميلة", "44 - عين الدفلى", "45 - النعامة",
    "46 - عين تموشنت", "47 - غرداية", "48 - غليزان", "49 - تيميمون", "50 - برج باجي مختار",
    "51 - أولاد جلال", "52 - بني عباس", "53 - عين صالح", "54 - عين قزام", "55 - توقرت",
    "56 - جانت", "57 - المغير", "58 - المنيع", "59 - الطيبات", "60 - أولاد سليمان",
    "61 - سيدي خالد", "62 - بوسعادة", "63 - عين وسارة", "64 - حاسي بحبح", "65 - عين الملح",
    "66 - سيدي عيسى", "67 - عين الباردة", "68 - عين آزال", "69 - عين الحجر"
]

# ==========================================
# 4. المتغيرات السرية في الجلسة
# ==========================================
if 'admin_access' not in st.session_state:
    st.session_state.admin_access = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'role' not in st.session_state:
    st.session_state.role = "user"
if 'verified' not in st.session_state:
    st.session_state.verified = 1
if 'ip' not in st.session_state:
    st.session_state.ip = secrets.token_hex(8)
if 'robot_active' not in st.session_state:
    st.session_state.robot_active = False
if 'last_alert' not in st.session_state:
    st.session_state.last_alert = None

# ==========================================
# 5. إعدادات قاعدة البيانات
# ==========================================
DB = "rassim_os_ultimate.db"

def init_db():
    try:
        conn = sqlite3.connect(DB, check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                salt TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                role TEXT DEFAULT 'user',
                verified INTEGER DEFAULT 1,
                banned INTEGER DEFAULT 0,
                ad_count INTEGER DEFAULT 0,
                last_login TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price INTEGER NOT NULL,
                phone TEXT NOT NULL,
                wilaya TEXT NOT NULL,
                description TEXT,
                category TEXT DEFAULT 'أخرى',
                views INTEGER DEFAULT 0,
                featured INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                owner TEXT NOT NULL,
                verified INTEGER DEFAULT 1,
                date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # إضافة حقل الصورة
        try:
            cursor.execute("ALTER TABLE ads ADD COLUMN image_path TEXT")
        except:
            pass
        
        # إضافة حقل رابط الصورة الخارجي
        try:
            cursor.execute("ALTER TABLE ads ADD COLUMN image_url TEXT")
        except:
            pass
        
        # جدول الإعلانات الممولة
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS promoted_ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                url TEXT NOT NULL,
                title TEXT NOT NULL,
                link TEXT,
                views INTEGER DEFAULT 0,
                clicks INTEGER DEFAULT 0,
                date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        return conn
    except Exception as e:
        st.error(f"خطأ في قاعدة البيانات: {e}")
        return None

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB, check_same_thread=False)

conn = init_db()

# ==========================================
# 6. دوال التشفير
# ==========================================
def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt.encode('utf-8'), 
        100000
    ).hex()

# ==========================================
# 7. دوال المساعدة
# ==========================================
def log_visitor():
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO visitors (ip, page) VALUES (?, ?)",
            (st.session_state.ip, st.session_state.get('page', 'main'))
        )
        conn.commit()
    except:
        pass

def get_stats():
    try:
        conn = get_connection()
        users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        ads = conn.execute("SELECT COUNT(*) FROM ads WHERE status='active'").fetchone()[0]
        visitors = conn.execute("SELECT COUNT(*) FROM visitors").fetchone()[0]
        views = conn.execute("SELECT SUM(views) FROM ads").fetchone()[0] or 0
        return users, ads, visitors, views
    except:
        return 0, 0, 0, 0

# ==========================================
# 8. بوت جلب الإعلانات من واد كنيس (Web Scraper)
# ==========================================
def scrape_ouedkniss_url(url):
    """جلب بيانات الإعلان من رابط واد كنيس"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # استخراج البيانات (هذه محاكاة - تحتاج تعديل حسب هيكل الموقع)
        title = soup.find('h1').text if soup.find('h1') else "عنوان غير معروف"
        
        # البحث عن السعر
        price_text = soup.find(text=re.compile(r'\d+[.,]?\d*\s*(دج|دينار|DA)', re.IGNORECASE))
        price = 0
        if price_text:
            numbers = re.findall(r'\d+', price_text)
            if numbers:
                price = int(numbers[0]) * 1000 if len(numbers[0]) < 4 else int(numbers[0])
        
        # البحث عن الوصف
        description = soup.find('meta', {'name': 'description'})
        description = description['content'] if description else "وصف غير متوفر"
        
        # البحث عن الصورة
        image = soup.find('meta', {'property': 'og:image'})
        image_url = image['content'] if image else None
        
        # البحث عن الولاية (افتراضية)
        wilaya = "16 - الجزائر"  # قيمة افتراضية
        
        return {
            'success': True,
            'title': title.strip()[:100],
            'price': price,
            'description': description[:200],
            'image_url': image_url,
            'wilaya': wilaya,
            'url': url
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def scrape_ads_ui():
    """واجهة جلب الإعلانات من الروابط"""
    st.markdown("### 🤖 بوت جلب الإعلانات الذكي")
    
    with st.expander("🔗 جلب إعلان من رابط واد كنيس", expanded=False):
        url = st.text_input("أدخل رابط الإعلان من واد كنيس:", placeholder="https://www.ouedkniss.com/...")
        
        if st.button("🚀 جلب البيانات", use_container_width=True) and url:
            with st.spinner("جاري جلب بيانات الإعلان..."):
                result = scrape_ouedkniss_url(url)
                
                if result['success']:
                    st.success("✅ تم جلب البيانات بنجاح!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**العنوان:** {result['title']}")
                        st.markdown(f"**السعر:** {result['price']:,} دج")
                        st.markdown(f"**الولاية:** {result['wilaya']}")
                    with col2:
                        if result['image_url']:
                            st.image(result['image_url'], caption="صورة الإعلان", use_container_width=True)
                    
                    # حفظ في قاعدة البيانات
                    if st.button("💾 حفظ الإعلان في قاعدة البيانات"):
                        try:
                            conn.execute("""
                                INSERT INTO ads (title, price, phone, wilaya, description, category, owner, status, verified, image_url)
                                VALUES (?, ?, ?, ?, ?, ?, 'SCRAPER_BOT', 'active', 1, ?)
                            """, (result['title'], result['price'], "0555000000", result['wilaya'], result['description'], "أخرى", result['image_url']))
                            conn.commit()
                            st.success("✅ تم حفظ الإعلان في قاعدة البيانات!")
                            time.sleep(2)
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ خطأ في الحفظ: {e}")
                else:
                    st.error(f"❌ فشل الجلب: {result.get('error', 'خطأ غير معروف')}")

# ==========================================
# 9. دالة إضافة الإعلانات التلقائية (السحرية)
# ==========================================
def seed_smart_ads():
    """إدخال إعلانات تجريبية احترافية تلقائياً"""
    
    fake_ads = [
        ("iPhone 15 Pro Max 512GB", 225000, "0555112233", "16 - الجزائر", "نظيف جداً 10/10 مع شاحن أصلي وسماعات، بطارية 100%", "آيفون"),
        ("iPhone 15 Pro 256GB", 195000, "0555112244", "31 - وهران", "مستعمل شهرين فقط، مع كامل الأكسسوارات، لون أزرق", "آيفون"),
        ("Samsung S24 Ultra 512GB", 185000, "0666445566", "31 - وهران", "مستعمل شهر واحد فقط، ضمان سنة، مع قلم S Pen", "سامسونج"),
        ("Samsung S23 Ultra", 145000, "0666445577", "16 - الجزائر", "حالة ممتازة، بطارية 98%، مع شاحن سريع", "سامسونج"),
        ("Google Pixel 8 Pro", 165000, "0777889900", "42 - تيبازة", "نسخة أمريكية، مفتوح على كل الشبكات، بطارية 98%", "جوجل"),
        ("Xiaomi 14 Pro", 98000, "0544332211", "25 - قسنطينة", "اللون الأسود، 12GB RAM, 512GB، جديد", "شاومي"),
        ("Huawei P60 Pro", 135000, "0888991122", "42 - تيبازة", "مع خدمات جوجل، نظيف، بطارية 100%", "هواوي"),
        ("Nothing Phone 2", 85000, "0999001122", "16 - الجزائر", "تصميم فريد، بطارية ممتازة، مع جراب", "أخرى"),
        ("OnePlus 12", 130000, "0999001133", "31 - وهران", "شاحن 100W سريع، مع كامل الأكسسوارات", "أخرى"),
        ("iPhone 12 Pro", 85000, "0555112277", "06 - بجاية", "باتري 90%، كل شيء أصلي، مع جراب", "آيفون")
    ]
    
    try:
        cursor = conn.cursor()
        count = 0
        for ad in fake_ads:
            existing = cursor.execute(
                "SELECT id FROM ads WHERE title=? AND price=? AND phone=?", 
                (ad[0], ad[1], ad[2])
            ).fetchone()
            
            if not existing:
                cursor.execute("""
                    INSERT INTO ads (title, price, phone, wilaya, description, category, owner, status, verified)
                    VALUES (?, ?, ?, ?, ?, ?, 'RASSIM_BOT', 'active', 1)
                """, ad)
                count += 1
        
        conn.commit()
        
        if count > 0:
            st.success(f"🚀 تمت إضافة {count} إعلان ذكي بنجاح!")
            st.balloons()
            time.sleep(2)
            st.rerun()
        else:
            st.info("✅ الإعلانات موجودة مسبقاً")
            
    except Exception as e:
        st.error(f"⚠️ خطأ في الإضافة: {e}")

# ==========================================
# 10. إضافة إعلانات ممولة من الذكاء الاصطناعي
# ==========================================
def seed_ai_promoted_ads():
    """إضافة إعلانات مولدة بالذكاء الاصطناعي"""
    
    ai_ads = [
        {"type": "image", "url": "https://images.unsplash.com/photo-1591337676887-a217a6970a8a?w=400", 
         "title": "🛍️ تخفيضات الصيف - حتى 40%", "link": "https://example.com/summer"},
        {"type": "image", "url": "https://images.unsplash.com/photo-1616348436168-de43ad0db179?w=400", 
         "title": "📱 iPhone 15 Pro - عروض حصرية", "link": "https://example.com/iphone"},
        {"type": "video", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", 
         "title": "🎬 إعلان تلفزيوني - Samsung Galaxy", "link": "https://example.com/samsung"},
        {"type": "image", "url": "https://images.unsplash.com/photo-1580910051074-78eb47e9b8a3?w=400", 
         "title": "⚡ Xiaomi 14 Pro - أقوى عروض السنة", "link": "https://example.com/xiaomi"},
    ]
    
    try:
        cursor = conn.cursor()
        count = 0
        for ad in ai_ads:
            existing = cursor.execute(
                "SELECT id FROM promoted_ads WHERE url=? AND title=?", 
                (ad['url'], ad['title'])
            ).fetchone()
            
            if not existing:
                cursor.execute("""
                    INSERT INTO promoted_ads (type, url, title, link)
                    VALUES (?, ?, ?, ?)
                """, (ad['type'], ad['url'], ad['title'], ad['link']))
                count += 1
        
        conn.commit()
        
        if count > 0:
            st.success(f"🎯 تمت إضافة {count} إعلان ممول بالذكاء الاصطناعي!")
    except Exception as e:
        st.error(f"⚠️ خطأ: {e}")

# ==========================================
# 11. عرض الإعلانات الممولة (Sponsored)
# ==========================================
def show_promoted_ads():
    """عرض الإعلانات الممولة في الصفحة الرئيسية"""
    
    # جلب الإعلانات من قاعدة البيانات
    try:
        promotions = conn.execute("SELECT * FROM promoted_ads ORDER BY date DESC LIMIT 4").fetchall()
    except:
        promotions = []
    
    if promotions:
        st.markdown("### ✨ عروض حصرية (Sponsored)")
        
        # عرض في صفوف من اثنين
        for i in range(0, len(promotions), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(promotions):
                    promo = promotions[i + j]
                    with cols[j]:
                        # إنشاء div للإعلان مع تأثير hover
                        st.markdown(f"""
                        <div style="background: rgba(20,20,30,0.4); border-radius: 20px; padding: 15px; margin-bottom: 15px; border: 1px solid rgba(255,0,255,0.3); transition: all 0.3s;" 
                             onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 10px 20px rgba(255,0,255,0.3)';"
                             onmouseout="this.style.transform=''; this.style.boxShadow='';">
                        """, unsafe_allow_html=True)
                        
                        if promo[1] == 'video':  # type
                            st.video(promo[2])  # url
                        else:
                            st.image(promo[2], use_container_width=True)  # url
                        
                        st.markdown(f"**{promo[3]}**")  # title
                        
                        if promo[4]:  # link
                            st.markdown(f"[🔗 زيارة المتجر]({promo[4]})")
                        
                        # تسجيل المشاهدة
                        conn.execute("UPDATE promoted_ads SET views = views + 1 WHERE id=?", (promo[0],))
                        conn.commit()
                        
                        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 12. نظام "الذكاء العصبي" للواجهة
# ==========================================
def set_ultimate_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');

    * {
        font-family: 'Cairo', 'Space Grotesk', 'Inter', sans-serif !important;
        box-sizing: border-box;
    }

    .stApp {
        background: radial-gradient(circle at 20% 20%, #1a1a2a, #0a0a0f);
        color: #ffffff;
        min-height: 100vh;
    }

    .logo-container {
        text-align: center;
        padding: 20px;
        margin-bottom: 20px;
    }

    .logo-text {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 5px;
        background: linear-gradient(90deg, #00ffff, #ff00ff, #00ffff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        display: inline-block;
        filter: drop-shadow(0 0 10px rgba(0,255,255,0.3));
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 40px !important;
        justify-content: center;
        direction: rtl !important;
        padding: 10px !important;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: nowrap !important;
    }

    .stTabs [data-baseweb="tab"] p {
        font-size: 1.2rem !important;
        font-weight: bold !important;
        color: white !important;
    }

    [class*="keyboard_ar"], [class*="keyboard"], [class*="translate"] {
        display: none !important;
    }

    body::after {
        content: "";
        display: none !important;
    }

    .stTextInput, .stTextArea {
        margin-bottom: 15px !important;
    }

    .stTextInput input, .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(0, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        color: white !important;
        padding: 12px 20px !important;
        direction: rtl !important;
        text-align: right !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #00ffff !important;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.3) !important;
    }

    .stTextInput label, .stTextArea label {
        color: #00ffff !important;
        font-size: 1rem !important;
        margin-bottom: 5px !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, #00ffff, #ff00ff) !important;
        border: none !important;
        color: black !important;
        font-weight: 800 !important;
        border-radius: 15px !important;
        padding: 12px 25px !important;
        transition: all 0.3s ease !important;
        font-size: 1.1rem !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(255, 0, 255, 0.3) !important;
    }

    .hologram-card {
        background: rgba(20, 20, 30, 0.4);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 255, 0.1);
        border-radius: 30px;
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.4s ease;
        direction: rtl;
        text-align: right;
    }

    .hologram-card:hover {
        border-color: #00ffff;
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 255, 255, 0.2);
    }

    .wilaya-badge {
        display: inline-block;
        background: rgba(0, 255, 255, 0.1);
        border: 1px solid #00ffff;
        border-radius: 50px;
        padding: 5px 10px;
        margin: 3px;
        font-size: 0.8rem;
        color: #00ffff;
        white-space: nowrap;
    }

    .stat-card {
        background: rgba(20, 20, 30, 0.5);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 255, 0.1);
        border-radius: 25px;
        padding: 20px;
        text-align: center;
    }

    .stat-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #00ffff;
        direction: ltr !important;
        font-family: 'Space Grotesk', monospace !important;
    }

    .stat-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1rem;
        margin-top: 5px;
    }

    .chat-bubble {
        position: fixed;
        bottom: 80px;
        right: 30px;
        background: linear-gradient(135deg, #00ffff, #ff00ff);
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        z-index: 9999;
        animation: float 3s ease-in-out infinite;
        box-shadow: 0 10px 20px rgba(0, 255, 255, 0.3);
    }

    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    .live-counter {
        position: fixed;
        bottom: 20px;
        left: 20px;
        background: rgba(0, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid #00ffff;
        padding: 10px 20px;
        border-radius: 50px;
        z-index: 999;
        display: flex;
        align-items: center;
        gap: 10px;
        animation: pulseGlow 2s infinite;
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 5px rgba(0, 255, 255, 0.2); }
        50% { box-shadow: 0 0 20px rgba(0, 255, 255, 0.5); }
        100% { box-shadow: 0 0 5px rgba(0, 255, 255, 0.2); }
    }

    .live-dot {
        color: #00ffff;
        font-weight: bold;
        font-size: 1.2rem;
        animation: blink 1s infinite;
    }

    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    .terms-box {
        background: rgba(20, 20, 30, 0.6);
        border: 1px solid #ff00ff;
        border-radius: 30px;
        padding: 20px;
        margin-top: 20px;
        color: white;
        font-size: 0.9rem;
        line-height: 1.8;
    }

    .terms-box h2 {
        color: #ff00ff;
        text-align: center;
        margin-bottom: 15px;
    }

    .terms-box hr {
        border-color: rgba(255, 0, 255, 0.2);
        margin: 15px 0;
    }

    .footer-note {
        text-align: center;
        font-size: 0.8rem;
        color: #888;
    }

    @media screen and (max-width: 768px) {
        .logo-text { font-size: 2.2rem; }
        .stat-value { font-size: 1.8rem; }
        .chat-bubble { width: 50px; height: 50px; bottom: 70px; right: 15px; }
        .live-counter { left: 15px; padding: 8px 15px; font-size: 0.8rem; }
        .stTabs [data-baseweb="tab-list"] { gap: 20px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 13. عداد الزوار الحي
# ==========================================
def show_live_counter():
    _, _, total_visitors, _ = get_stats()
    st.markdown(f"""
    <div class="live-counter">
        <span class="live-dot">●</span>
        <span style="color: white; font-family: 'Space Grotesk';">LIVE: <b style="color: #00ffff;">{total_visitors:,}</b></span>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 14. كاشف المشتري الجدي
# ==========================================
def serious_buyer_detector(message, price_offered=0):
    serious_keywords = [
        "حاب نشري", "نخلصك توت سويت", "وين نسكنو", 
        "كاش", "آخر سعر", "دابا", "نروحو نخلصو", "العنوان"
    ]
    
    message_lower = message.lower() if message else ""
    is_serious = any(word in message_lower for word in serious_keywords)
    
    if is_serious or price_offered > 0:
        st.session_state.last_alert = {
            'message': message,
            'price': price_offered,
            'time': datetime.now().strftime("%H:%M:%S")
        }
        st.toast("🚨 مشتري جدي!", icon="💰")
        return True
    return False

# ==========================================
# 15. روبوت RASSIM الذكي
# ==========================================
def rassim_robot_logic(user_message):
    user_message = user_message.lower()
    
    welcome_message = """
    🎯 يا أهلاً بيك في RASSIM OS ULTIMATE! 🇩🇿 
    
    راني هنا باش نعاونك تبيع ولا تشري تليفونك في 69 ولاية بكل سهولة.
    
    🔥 ميزتي الكبيرة؟ نعرف شكون المشتري "الصح" وشكون اللي جاي "يقصر".
    
    ⚡ أدخل، سجل، وحط إعلانك.. الرادار راهو خدام!
    
    💬 شحال تحب؟ (آيفون، سامسونج، ولا غرسة؟)
    """
    
    responses = {
        "سعر": "💰 الأسعار عندنا هي الأفضل! تفقد الإعلانات وشوف بنفسك",
        "متوفر": "✅ كل الإعلانات المعروضة متوفرة حالياً",
        "تيبازة": "📍 مقرنا في فوكة (42). التوصيل لـ69 ولاية",
        "سلام": "وعليكم السلام! نورت RASSIM OS",
        "آيفون": "📱 آيفون 15 بـ225,000 دج موجود",
        "سامسونج": "📱 S24 Ultra بـ185,000 دج",
        "هواوي": "📱 هواوي P60 Pro موجود",
        "شاومي": "📱 Xiaomi 14 Pro بـ95,000 دج",
        "واد كنيس": "🎯 نحن البديل العصري لواد كنيس",
        "الدزة": "⚡ الدزة الجزائرية واجدة!",
        "وين": "📍 فوكة، تيبازة (42) - نغطي 69 ولاية",
        "69": "✅ 69 ولاية جزائرية مدعومة",
        "كيفاش": "💡 سجل، دوز على الإعلان، وضغط واتساب",
        "توصيل": "📦 التوصيل لكل الولايات"
    }
    
    if user_message == "ترحيب_خاص":
        return welcome_message
    
    for key in responses:
        if key in user_message:
            if key in ["حاب نشري", "كاش", "وين"]:
                serious_buyer_detector(user_message)
            return responses[key]
    return "رسالتك وصلت! سأرد قريباً 🌟"

# ==========================================
# 16. رادار راسم الآلي
# ==========================================
def robotic_alert_ui():
    st.sidebar.markdown("---")
    st.sidebar.subheader("🛰️ رادار RASSIM")
    hunter_mode = st.sidebar.toggle("⚡ وضع الصياد", value=True)
    st.session_state.robot_active = hunter_mode
    
    if hunter_mode:
        st.sidebar.success("🟢 الرادار نشط")
        if st.session_state.last_alert:
            with st.sidebar.expander("🚨 آخر عرض"):
                st.markdown(f"**{st.session_state.last_alert['message']}**\n💰 {st.session_state.last_alert['price']} دج")
                st.markdown("[📞 تواصل](https://wa.me/213555555555)")
    else:
        st.sidebar.warning("🔴 الرادار متوقف")

# ==========================================
# 17. مولد الإعلانات الذكي
# ==========================================
def generate_auto_ads():
    hour = datetime.now().hour
    if 18 <= hour <= 22:
        st.sidebar.markdown("<p style='color:#00ffff;'>🔥 وقت الذروة! انشر الآن</p>", unsafe_allow_html=True)
    elif 9 <= hour <= 12:
        st.sidebar.markdown("<p style='color:#ff00ff;'>☀️ وقت الصباح الذهبي</p>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown("<p style='color:#888;'>⏳ وقت هادئ</p>", unsafe_allow_html=True)

# ==========================================
# 18. عداد وشبكة الولايات
# ==========================================
def show_wilaya_counter():
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <div style="background: linear-gradient(135deg, #00ffff, #ff00ff); border-radius: 60px; padding: 15px 30px; display: inline-block;">
            <span style="color: black; font-size: 2.5rem; font-weight: 900;">69</span>
            <span style="color: black; font-size: 1.2rem; margin-right: 10px;">ولاية جزائرية</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_wilaya_badges():
    sample_wilayas = ALGERIAN_WILAYAS[1:21]
    cols = st.columns(6)
    for i, wilaya in enumerate(sample_wilayas):
        with cols[i % 6]:
            display_text = wilaya if len(wilaya) <= 10 else wilaya[:10] + "..."
            st.markdown(f"<span class='wilaya-badge'>{display_text}</span>", unsafe_allow_html=True)
    
    with st.expander("📍 عرض جميع الولايات (69)"):
        cols = st.columns(5)
        for i, wilaya in enumerate(ALGERIAN_WILAYAS[1:]):
            with cols[i % 5]:
                st.markdown(f"<span class='wilaya-badge'>{wilaya}</span>", unsafe_allow_html=True)

# ==========================================
# 19. نظام الدردشة المباشرة
# ==========================================
def show_live_chat():
    st.markdown("""
    <div class="chat-bubble" onclick="document.getElementById('chat_trigger').click();">
        <img src="https://img.icons8.com/ios-filled/30/ffffff/speech-bubble.png" width="30">
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 💬 الدعم الذكي")
        generate_auto_ads()
        
        with st.expander("🗣️ تحدث مع روبوت RASSIM", expanded=False):
            st.write("أهلاً! أنا روبوت راسم الذكي بالدارجة الجزائرية")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("[![WhatsApp](https://img.icons8.com/color/40/whatsapp.png)](https://wa.me/213555555555)")
            with col2:
                st.markdown("[![Telegram](https://img.icons8.com/color/40/telegram-app.png)](https://t.me/RassimDZ)")
            
            msg = st.text_area("📝 اكتب رسالتك:", key="robot_input", height=80)
            if st.button("🤖 إرسال", use_container_width=True) and msg:
                reply = rassim_robot_logic(msg)
                st.info(f"🤖 {reply}")
                serious_buyer_detector(msg, 0)

# ==========================================
# 20. نظام التحليل التنبئي
# ==========================================
def show_market_trends(conn):
    st.markdown("### 📈 تحليلات السوق")
    try:
        if conn:
            df = pd.read_sql_query("SELECT category, COUNT(*) as count FROM ads WHERE status='active' GROUP BY category", conn)
            if not df.empty:
                fig = go.Figure(go.Bar(
                    x=df['count'],
                    y=df['category'],
                    orientation='h',
                    marker_color='#00ffff',
                    text=df['count'],
                    textposition='auto'
                ))
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    height=250
                )
                st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("جاري تحميل التحليلات...")

# ==========================================
# 21. محرك البحث الذكي
# ==========================================
def quantum_search_ui():
    col1, col2 = st.columns([3, 1])
    with col1:
        q = st.text_input("", placeholder="🔍 ابحث عن هاتف...")
    with col2:
        st.selectbox("", ["⚡ Flash", "🧠 ذكي"], label_visibility="collapsed")
    
    col_a, col_b = st.columns(2)
    with col_a:
        w = st.selectbox("الولاية", ALGERIAN_WILAYAS)
    with col_b:
        s = st.selectbox("الترتيب", ["الأحدث", "السعر", "المشاهدات"])
    return q, w, s

# ==========================================
# 22. دالة الإعلان مع عرض الصور
# ==========================================
def render_ad_pro(ad):
    verified = "✅ موثق" if ad.get('verified') else "⚠️ عادي"
    image_html = ""
    
    # عرض الصورة من الرابط الخارجي أو الملف المحلي
    if ad.get('image_url'):
        image_html = f"""
        <div style="width: 100%; height: 200px; overflow: hidden; border-radius: 15px; margin-bottom: 15px;">
            <img src="{ad['image_url']}" alt="{ad.get('title', '')}" style="width: 100%; height: 100%; object-fit: cover;">
        </div>
        """
    elif ad.get('image_path') and os.path.exists(ad['image_path']):
        try:
            with open(ad['image_path'], 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
                image_html = f"""
                <div style="width: 100%; height: 200px; overflow: hidden; border-radius: 15px; margin-bottom: 15px;">
                    <img src="data:image/jpeg;base64,{img_data}" alt="{ad.get('title', '')}" style="width: 100%; height: 100%; object-fit: cover;">
                </div>
                """
        except:
            image_html = ""
    
    st.markdown(f"""
    <div class="hologram-card">
        {image_html}
        <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 8px;">
            <span style="color: #00ffff;">📍 {ad.get('wilaya', '')}</span>
            <span style="color: #888;">👁️ {ad.get('views', 0)}</span>
            <span style="color: {'#00ffff' if ad.get('verified') else '#ff00ff'};">{verified}</span>
        </div>
        <h3 style="color: #00ffff; margin: 8px 0;">{ad.get('title', '')[:40]}</h3>
        <div style="font-size: 1.8rem; font-weight: bold; color: #ff00ff; margin: 10px 0;">
            {ad.get('price', 0):,} <span style="font-size: 0.9rem;">دج</span>
        </div>
        <p style="color: #aaa; margin: 10px 0;">{ad.get('description', '')[:80]}...</p>
        <div style="display: flex; gap: 10px;">
            <a href="tel:{ad.get('phone', '')}" style="flex: 1; text-decoration: none;">
                <button style="width:100%; padding:12px; background:#111; border:1px solid #00ffff; border-radius:10px; color:#00ffff; font-weight:bold; cursor:pointer;">📞 اتصال</button>
            </a>
            <a href="https://wa.me/{ad.get('phone', '')}" style="flex: 1; text-decoration: none;">
                <button style="width:100%; padding:12px; background:#25D366; border:none; border-radius:10px; color:white; font-weight:bold; cursor:pointer;">📱 واتساب</button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 23. اتفاقية الاستخدام
# ==========================================
def show_terms():
    st.markdown("""
    <div class="terms-box hologram-card">
        <h2 style="color: #ff00ff; text-align: center;">📜 قانون المنصة</h2>
        <p>
        ✅ <b>المصداقية:</b> الإعلان لازم يكون حقيقي.<br>
        ✅ <b>الاحترام:</b> أي كلام غير لائق يؤدي للحظر.<br>
        ✅ <b>69 ولاية:</b> تغطية كاملة للجزائر.<br>
        ⚠️ <b>إخلاء مسؤولية:</b> الموقع وسيط فقط.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 24. صفحة تسجيل الدخول
# ==========================================
def login_page(conn):
    st.markdown("""
    <div class="logo-container">
        <div class="logo-text">RASSIM OS</div>
        <div style="color: #00ffff;">ULTIMATE • 69 WILAYAS</div>
    </div>
    """, unsafe_allow_html=True)
    
    show_wilaya_counter()
    
    users, ads, visitors, views = get_stats()
    cols = st.columns(4)
    for i, (val, label) in enumerate(zip([users, ads, visitors, views], ["مستخدم", "إعلان", "زيارة", "مشاهدة"])):
        with cols[i]:
            st.markdown(f'<div class="stat-card"><div class="stat-value">{val:,}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)
    
    with st.expander("📍 الولايات"):
        show_wilaya_badges()
    
    tab1, tab2 = st.tabs(["🔑 دخول", "📝 تسجيل"])
    
    with tab1:
        with st.form("login_form"):
            u = st.text_input("👤 اسم المستخدم")
            p = st.text_input("🔐 كلمة المرور", type="password")
            if st.form_submit_button("⚡ دخول", use_container_width=True) and u and p:
                user = conn.execute("SELECT password, salt, role, verified FROM users WHERE username=?", (u,)).fetchone()
                if user and user[0] == hash_password(p, user[1]):
                    st.session_state.user = u
                    st.session_state.role = user[2]
                    st.session_state.verified = user[3]
                    st.success(f"✅ أهلاً {u}")
                    st.rerun()
                else:
                    st.error("❌ بيانات غير صحيحة")
    
    with tab2:
        with st.form("register_form"):
            nu = st.text_input("👤 اسم المستخدم الجديد")
            np = st.text_input("🔐 كلمة المرور", type="password")
            em = st.text_input("📧 البريد الإلكتروني")
            ph = st.text_input("📱 رقم الهاتف")
            if st.form_submit_button("✨ تسجيل", use_container_width=True) and nu and np:
                if len(np) >= 6:
                    salt = secrets.token_hex(16)
                    hashed = hash_password(np, salt)
                    try:
                        conn.execute("INSERT INTO users (username, password, salt, email, phone, role, verified) VALUES (?,?,?,?,?,'user',1)", 
                                   (nu, hashed, salt, em, ph))
                        conn.commit()
                        st.success("✅ تم التسجيل!")
                    except:
                        st.error("❌ اسم المستخدم موجود")
                else:
                    st.error("❌ كلمة المرور قصيرة")

# ==========================================
# 25. صفحة السوق الذكي
# ==========================================
def show_market():
    st.markdown("### 🛍️ السوق الذكي")
    
    # عرض الإعلانات الممولة أولاً
    show_promoted_ads()
    
    q, w, s = quantum_search_ui()
    
    with st.expander("📊 تحليلات السوق", expanded=False):
        show_market_trends(conn)
    
    # جلب الإعلانات من قاعدة البيانات
    try:
        query = "SELECT * FROM ads WHERE status='active'"
        params = []
        
        if w and w != "الكل":
            query += " AND wilaya=?"
            params.append(w)
        if q:
            query += " AND (title LIKE ? OR description LIKE ?)"
            params.append(f"%{q}%")
            params.append(f"%{q}%")
        
        query += " ORDER BY date DESC LIMIT 20"
        
        ads = conn.execute(query, params).fetchall()
        
        if ads:
            for ad in ads:
                ad_dict = {
                    'id': ad[0],
                    'title': ad[1],
                    'price': ad[2],
                    'phone': ad[3],
                    'wilaya': ad[4],
                    'description': ad[5],
                    'category': ad[6],
                    'views': ad[7],
                    'featured': ad[8],
                    'status': ad[9],
                    'owner': ad[10],
                    'verified': ad[11],
                    'date': ad[12],
                    'image_path': ad[13] if len(ad) > 13 else None,
                    'image_url': ad[14] if len(ad) > 14 else None
                }
                render_ad_pro(ad_dict)
        else:
            st.info("😕 لا توجد إعلانات")
            
            # زر لإضافة إعلانات تلقائية إذا كانت القاعدة فارغة
            if st.button("🚀 إضافة إعلانات تلقائية", use_container_width=True):
                seed_smart_ads()
                seed_ai_promoted_ads()
                
    except Exception as e:
        st.error(f"خطأ في تحميل الإعلانات: {e}")

# ==========================================
# 26. إضافة إعلان جديد
# ==========================================
def post_ad():
    st.markdown("### 📢 إعلان جديد")
    
    with st.form("new_ad_form"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("📱 اسم المنتج *")
            cat = st.selectbox("🏷️ الفئة", ["سامسونج", "آيفون", "هواوي", "شاومي", "جوجل", "أخرى"])
        with col2:
            price = st.number_input("💰 السعر (دج) *", min_value=0, step=1000)
            wilaya = st.selectbox("📍 الولاية *", ALGERIAN_WILAYAS[1:])
        
        phone = st.text_input("📞 رقم الهاتف *")
        desc = st.text_area("📝 الوصف", height=100)
        
        uploaded_file = st.file_uploader("🖼️ ارفع صورة", type=["png", "jpg", "jpeg"])
        image_path = None
        
        if uploaded_file:
            file_extension = uploaded_file.name.split('.')[-1]
            unique_filename = f"{secrets.token_hex(8)}.{file_extension}"
            image_path = os.path.join(UPLOADS_DIR, unique_filename)
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        
        if st.form_submit_button("🚀 نشر", use_container_width=True) and title and phone and price > 0:
            try:
                conn.execute("""
                    INSERT INTO ads (title, price, phone, wilaya, description, category, owner, status, verified, image_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'active', 1, ?)
                """, (title, price, phone, wilaya, desc, cat, st.session_state.user, image_path))
                conn.commit()
                st.success("✅ تم النشر!")
                st.balloons()
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"❌ خطأ: {e}")

# ==========================================
# 27. صفحة الحساب الشخصي
# ==========================================
def profile_page():
    st.markdown("### 👤 حسابي")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="hologram-card">
            <h4 style="color:#00ffff;">معلومات الحساب</h4>
            <p><b>👤 المستخدم:</b> {st.session_state.user}</p>
            <p><b>🔐 الصلاحية:</b> {'مسؤول' if st.session_state.role == 'admin' else 'عضو'}</p>
            <p><b>✅ الحالة:</b> {'مفعل' if st.session_state.verified else 'غير مفعل'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        try:
            user_ads = conn.execute("SELECT COUNT(*) FROM ads WHERE owner=?", (st.session_state.user,)).fetchone()[0]
            user_views = conn.execute("SELECT SUM(views) FROM ads WHERE owner=?", (st.session_state.user,)).fetchone()[0] or 0
        except:
            user_ads = 0
            user_views = 0
        
        st.markdown(f"""
        <div class="hologram-card">
            <h4 style="color:#ff00ff;">إحصائياتي</h4>
            <p><b>📊 إعلاناتي:</b> {user_ads}</p>
            <p><b>👁️ مشاهدات:</b> {user_views}</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 28. لوحة الإدارة
# ==========================================
def admin_dashboard():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00ffff20, #ff00ff20); border: 2px solid #00ffff; border-radius: 30px; padding: 20px; margin-bottom: 20px;">
        <h1 style="color: white; text-align: center;">🔐 لوحة القيادة</h1>
        <p style="color: #00ffff; text-align: center;">خاص بالطاهر الطاهري</p>
    </div>
    """, unsafe_allow_html=True)
    
    users, ads, visitors, views = get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("المستخدمين", f"{users:,}")
    with col2:
        st.metric("الإعلانات", f"{ads:,}")
    with col3:
        st.metric("الزيارات", f"{visitors:,}")
    with col4:
        st.metric("المشاهدات", f"{views:,}")
    
    # أدوات الإدارة
    st.markdown("### 🛠️ أدوات الإدارة")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        if st.button("🚀 إضافة إعلانات تلقائية", use_container_width=True):
            seed_smart_ads()
    
    with col_b:
        if st.button("🎯 إضافة إعلانات ممولة", use_container_width=True):
            seed_ai_promoted_ads()
            st.success("✅ تمت الإضافة")
    
    with col_c:
        if st.button("🤖 بوت جلب الإعلانات", use_container_width=True):
            st.session_state.show_scraper = True
    
    # بوت الجلب
    if st.session_state.get('show_scraper', False):
        scrape_ads_ui()
    
    st.markdown("### 🚨 تنبيهات الرادار")
    if st.session_state.last_alert:
        st.markdown(f"""
        <div style="background: rgba(255,0,0,0.2); border: 2px solid #ff00ff; border-radius: 15px; padding: 15px;">
            <h4 style="color: #ff00ff;">🔥 مشتري جدي!</h4>
            <p><b>{st.session_state.last_alert['message']}</b></p>
            <p>💰 {st.session_state.last_alert['price']} دج</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 29. الدالة الرئيسية
# ==========================================
def main():
    set_ultimate_theme()
    log_visitor()
    
    show_live_chat()
    show_live_counter()
    
    if st.session_state.user:
        with st.sidebar:
            st.markdown(f"### ✨ أهلاً {st.session_state.user}")
            choice = st.radio("القائمة", ["🛍️ السوق", "📢 نشر", "👤 حسابي", "🚪 خروج"])
            
            robotic_alert_ui()
            
            with st.expander("📜 الشروط"):
                show_terms()
            
            if choice == "🚪 خروج":
                st.session_state.user = None
                st.rerun()
        
        if choice == "🛍️ السوق":
            show_market()
        elif choice == "📢 نشر":
            post_ad()
        elif choice == "👤 حسابي":
            profile_page()
        
        if st.session_state.role == "admin" and st.sidebar.button("🔐 الإدارة"):
            admin_dashboard()
    else:
        login_page(conn)

# ==========================================
# 30. تشغيل التطبيق
# ==========================================
if __name__ == "__main__":
    main()

