import streamlit as st
import base64
import os
import time
from datetime import datetime
import pandas as pd

# ==========================================
# دوال التعامل مع الصور
# ==========================================
def get_image_base64(path):
    """تحويل الصورة إلى base64 لعرضها"""
    if path and os.path.exists(path):
        try:
            with open(path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except:
            return None
    return None

def save_uploaded_file(uploaded_file, uploads_dir="uploads"):
    """حفظ ملف مرفوع وتوليد اسم فريد"""
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1]
        unique_filename = f"{secrets.token_hex(8)}.{file_extension}"
        file_path = os.path.join(uploads_dir, unique_filename)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    return None

# ==========================================
# إحصائيات الموقع
# ==========================================
def get_stats(conn):
    """الحصول على إحصائيات الموقع"""
    try:
        users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        ads = conn.execute("SELECT COUNT(*) FROM ads WHERE status='active'").fetchone()[0]
        visitors = conn.execute("SELECT COUNT(*) FROM visitors").fetchone()[0]
        views = conn.execute("SELECT SUM(views) FROM ads").fetchone()[0] or 0
        return users, ads, visitors, views
    except:
        return 0, 0, 0, 0

# ==========================================
# كاشف المشتري الجدي
# ==========================================
def serious_buyer_detector(message, price_offered=0, st_session=None):
    """يكشف المشتري الجدي ويطلق إنذاراً"""
    serious_keywords = [
        "حاب نشري", "نخلصك توت سويت", "وين نسكنو", 
        "كاش", "آخر سعر", "دابا", "نروحو نخلصو", "العنوان",
        "واش راك", "الوقتية", "نجي نشوفو"
    ]
    
    message_lower = message.lower() if message else ""
    is_serious = any(word in message_lower for word in serious_keywords)
    
    if is_serious or price_offered > 0:
        if st_session:
            st_session.last_alert = {
                'message': message,
                'price': price_offered,
                'time': datetime.now().strftime("%H:%M:%S")
            }
        st.toast("🚨 مشتري جدي!", icon="💰")
        return True
    return False

# ==========================================
# روبوت RASSIM الذكي
# ==========================================
def rassim_robot_logic(user_message, st_session=None):
    """محرك الردود الذكي للروبوت"""
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
            if key in ["حاب نشري", "كاش", "وين"] and st_session:
                serious_buyer_detector(user_message, 0, st_session)
            return responses[key]
    return "رسالتك وصلت! سأرد قريباً 🌟"

# ==========================================
# إضافة إعلانات تلقائية
# ==========================================
def seed_smart_ads(conn):
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
        return count
    except Exception as e:
        print(f"خطأ في إضافة الإعلانات: {e}")
        return 0

# ==========================================
# إضافة إعلانات ممولة من الذكاء الاصطناعي
# ==========================================
def seed_ai_promoted_ads(conn):
    """إضافة إعلانات مولدة بالذكاء الاصطناعي"""
    
    ai_ads = [
        {"type": "image", "url": "https://images.unsplash.com/photo-1591337676887-a217a6970a8a?w=400", 
         "title": "🛍️ تخفيضات الصيف - حتى 40%", "link": "#"},
        {"type": "image", "url": "https://images.unsplash.com/photo-1616348436168-de43ad0db179?w=400", 
         "title": "📱 iPhone 15 Pro - عروض حصرية", "link": "#"},
        {"type": "image", "url": "https://images.unsplash.com/photo-1580910051074-78eb47e9b8a3?w=400", 
         "title": "⚡ Xiaomi 14 Pro - أقوى عروض السنة", "link": "#"},
        {"type": "image", "url": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400", 
         "title": "📸 Samsung S24 Ultra - كاميرا احترافية", "link": "#"},
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
        return count
    except Exception as e:
        print(f"خطأ في إضافة الإعلانات الممولة: {e}")
        return 0

# ==========================================
# عرض تحليلات السوق
# ==========================================
def show_market_trends(conn):
    """عرض تحليلات السوق باستخدام Plotly"""
    try:
        df = pd.read_sql_query("SELECT category, COUNT(*) as count FROM ads WHERE status='active' GROUP BY category", conn)
        if not df.empty:
            import plotly.graph_objects as go
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
            return fig
    except:
        pass
    return None
