import streamlit as st
import time
import os
import secrets

# استيراد الملفات الأخرى
from ui_styles import set_ultimate_theme
from database import init_db, get_connection, hash_password, hash_pass
from functions import (
    get_stats, get_image_base64, save_uploaded_file,
    serious_buyer_detector, rassim_robot_logic,
    seed_smart_ads, seed_ai_promoted_ads,
    show_market_trends, scrape_ouedkniss_url
)

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
# 2. قائمة الولايات الجزائرية (69 ولاية)
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
# 3. المتغيرات السرية في الجلسة
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
if 'show_scraper' not in st.session_state:
    st.session_state.show_scraper = False

# ==========================================
# 4. تهيئة قاعدة البيانات
# ==========================================
conn = init_db()

# ==========================================
# 5. دوال عرض الواجهات
# ==========================================

def show_live_counter():
    """عرض عداد الزوار الحي"""
    _, _, total_visitors, _ = get_stats(conn)
    st.markdown(f"""
    <div class="live-counter">
        <span class="live-dot">●</span>
        <span style="color: white;">LIVE: <b style="color: #00ffff;">{total_visitors:,}</b></span>
    </div>
    """, unsafe_allow_html=True)

def show_wilaya_counter():
    """عرض عداد الولايات"""
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <div style="background: linear-gradient(135deg, #00ffff, #ff00ff); border-radius: 60px; padding: 15px 30px; display: inline-block;">
            <span style="color: black; font-size: 2.5rem; font-weight: 900;">69</span>
            <span style="color: black; font-size: 1.2rem; margin-right: 10px;">ولاية جزائرية</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_wilaya_badges():
    """عرض شارات الولايات"""
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

def show_live_chat():
    """عرض فقاعة الدردشة"""
    st.markdown("""
    <div class="chat-bubble" onclick="document.getElementById('chat_trigger').click();">
        <img src="https://img.icons8.com/ios-filled/30/ffffff/speech-bubble.png" width="30">
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 💬 الدعم الذكي")
        
        with st.expander("🗣️ تحدث مع روبوت RASSIM", expanded=False):
            st.write("أهلاً! أنا روبوت راسم الذكي")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("[![WhatsApp](https://img.icons8.com/color/40/whatsapp.png)](https://wa.me/213555555555)")
            with col2:
                st.markdown("[![Telegram](https://img.icons8.com/color/40/telegram-app.png)](https://t.me/RassimDZ)")
            
            msg = st.text_area("📝 اكتب رسالتك:", key="robot_input", height=80)
            if st.button("🤖 إرسال", use_container_width=True) and msg:
                reply = rassim_robot_logic(msg, st.session_state)
                st.info(f"🤖 {reply}")

def show_terms():
    """عرض شروط الاستخدام"""
    st.markdown("""
    <div class="terms-box">
        <h2>📜 قانون المنصة</h2>
        <p>
        ✅ <b>المصداقية:</b> الإعلان لازم يكون حقيقي.<br>
        ✅ <b>الاحترام:</b> أي كلام غير لائق يؤدي للحظر.<br>
        ✅ <b>69 ولاية:</b> تغطية كاملة للجزائر.<br>
        ⚠️ <b>إخلاء مسؤولية:</b> الموقع وسيط فقط.
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_promoted_ads():
    """عرض الإعلانات الممولة"""
    try:
        promotions = conn.execute("SELECT * FROM promoted_ads ORDER BY date DESC LIMIT 4").fetchall()
    except:
        promotions = []
    
    if promotions:
        st.markdown("### ✨ عروض حصرية (Sponsored)")
        for i in range(0, len(promotions), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(promotions):
                    promo = promotions[i + j]
                    with cols[j]:
                        st.image(promo[2], use_container_width=True)  # url
                        st.caption(f"**{promo[3]}**")  # title
                        # تسجيل المشاهدة
                        conn.execute("UPDATE promoted_ads SET views = views + 1 WHERE id=?", (promo[0],))
                        conn.commit()

def quantum_search_ui():
    """واجهة البحث الذكي"""
    col1, col2 = st.columns([3, 1])
    with col1:
        q = st.text_input("", placeholder="🔍 ابحث عن هاتف...", key="search_input")
    with col2:
        st.selectbox("", ["⚡ Flash", "🧠 ذكي"], label_visibility="collapsed", key="search_mode")
    
    col_a, col_b = st.columns(2)
    with col_a:
        w = st.selectbox("الولاية", ALGERIAN_WILAYAS, key="wilaya_filter")
    with col_b:
        s = st.selectbox("الترتيب", ["الأحدث", "السعر", "المشاهدات"], key="sort_filter")
    return q, w, s

def render_ad_pro(ad):
    """عرض الإعلان بشكل أنيق"""
    verified = "✅ موثق" if ad.get('verified') else "⚠️ عادي"
    verified_color = "#00ffff" if ad.get('verified') else "#ff00ff"
    image_html = ""
    
    # عرض الصورة
    if ad.get('image_url'):
        image_html = f"""
        <div style="width: 100%; height: 200px; overflow: hidden; border-radius: 15px; margin-bottom: 15px;">
            <img src="{ad['image_url']}" alt="{ad.get('title', '')}" style="width: 100%; height: 100%; object-fit: cover;">
        </div>
        """
    elif ad.get('image_path'):
        img_base64 = get_image_base64(ad['image_path'])
        if img_base64:
            image_html = f"""
            <div style="width: 100%; height: 200px; overflow: hidden; border-radius: 15px; margin-bottom: 15px;">
                <img src="data:image/jpeg;base64,{img_base64}" alt="{ad.get('title', '')}" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            """
    
    phone_display = ad['phone'][:4] + "••••" + ad['phone'][-4:] if len(ad.get('phone', '')) > 8 else ad.get('phone', '')
    
    st.markdown(f"""
    <div class="ad-card">
        {image_html}
        <div style="display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 8px;">
            <span style="color: #00ffff;">📍 {ad.get('wilaya', '')}</span>
            <span style="color: #888;">👁️ {ad.get('views', 0)}</span>
            <span style="color: {verified_color};">{verified}</span>
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
    
    # تحديث المشاهدات
    try:
        conn.execute("UPDATE ads SET views = views + 1 WHERE id=?", (ad['id'],))
        conn.commit()
    except:
        pass

def scrape_ads_ui():
    """واجهة جلب الإعلانات من الروابط"""
    st.markdown("### 🤖 بوت جلب الإعلانات الذكي")
    
    url = st.text_input("🔗 رابط الإعلان من واد كنيس:", placeholder="https://www.ouedkniss.com/...")
    
    if st.button("🚀 جلب البيانات", use_container_width=True) and url:
        with st.spinner("جاري جلب بيانات الإعلان..."):
            result = scrape_ouedkniss_url(url)
            
            if result['success']:
                st.success("✅ تم جلب البيانات بنجاح!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**العنوان:** {result['title']}")
                    st.markdown(f"**السعر:** {result['price']:,} دج")
                with col2:
                    if result['image_url']:
                        st.image(result['image_url'], caption="صورة الإعلان", use_container_width=True)
                
                if st.button("💾 حفظ الإعلان في قاعدة البيانات"):
                    try:
                        conn.execute("""
                            INSERT INTO ads (title, price, phone, wilaya, description, category, owner, status, verified, image_url)
                            VALUES (?, ?, ?, ?, ?, ?, 'SCRAPER_BOT', 'active', 1, ?)
                        """, (result['title'], result['price'], "0555000000", result['wilaya'], result['description'], "أخرى", result['image_url']))
                        conn.commit()
                        st.success("✅ تم حفظ الإعلان!")
                        time.sleep(2)
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ: {e}")
            else:
                st.error(f"❌ فشل الجلب: {result.get('error', 'خطأ غير معروف')}")

# ==========================================
# 6. صفحات الموقع الرئيسية
# ==========================================

def login_page():
    """صفحة تسجيل الدخول"""
    st.markdown("""
    <div class="logo-container">
        <div class="logo-text">RASSIM OS</div>
        <div class="logo-subtitle">ULTIMATE • 69 WILAYAS</div>
    </div>
    """, unsafe_allow_html=True)
    
    show_wilaya_counter()
    
    users, ads, visitors, views = get_stats(conn)
    cols = st.columns(4)
    for i, (val, label) in enumerate(zip([users, ads, visitors, views], ["مستخدم", "إعلان", "زيارة", "مشاهدة"])):
        with cols[i]:
            st.markdown(f'<div class="stat-card"><div class="stat-value">{val:,}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)
    
    with st.expander("📍 الولايات المدعومة (69)"):
        show_wilaya_badges()
    
    tab1, tab2 = st.tabs(["🔑 دخول", "📝 تسجيل جديد"])
    
    with tab1:
        with st.form("login_form"):
            u = st.text_input("👤 اسم المستخدم")
            p = st.text_input("🔐 كلمة المرور", type="password")
            if st.form_submit_button("⚡ دخول", use_container_width=True) and u and p:
                user = conn.execute("SELECT password, salt, role, verified FROM users WHERE username=?", (u,)).fetchone()
                if user:
                    if user[0] == hash_password(p, user[1]) or user[0] == hash_pass(p):
                        st.session_state.user = u
                        st.session_state.role = user[2]
                        st.session_state.verified = user[3]
                        st.success(f"✅ أهلاً {u}")
                        st.rerun()
                    else:
                        st.error("❌ كلمة المرور غير صحيحة")
                else:
                    st.error("❌ المستخدم غير موجود")
    
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
                        conn.execute("""
                            INSERT INTO users (username, password, salt, email, phone, role, verified)
                            VALUES (?, ?, ?, ?, ?, 'user', 1)
                        """, (nu, hashed, salt, em, ph))
                        conn.commit()
                        st.success("✅ تم التسجيل! يمكنك الدخول الآن")
                    except:
                        st.error("❌ اسم المستخدم موجود")
                else:
                    st.error("❌ كلمة المرور قصيرة (6 أحرف على الأقل)")

def show_market():
    """صفحة السوق الذكي"""
    st.markdown("### 🛍️ السوق الذكي")
    
    # عرض الإعلانات الممولة
    show_promoted_ads()
    
    q, w, s = quantum_search_ui()
    
    with st.expander("📊 تحليلات السوق", expanded=False):
        fig = show_market_trends(conn)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("لا توجد بيانات كافية للتحليل")
    
    # جلب الإعلانات من قاعدة البيانات
    try:
        query = "SELECT * FROM ads WHERE status='active'"
        params = []
        
        if w and w != "الكل":
            query += " AND wilaya LIKE ?"
            params.append(f"%{w}%")
        if q:
            query += " AND (title LIKE ? OR description LIKE ?)"
            params.append(f"%{q}%")
            params.append(f"%{q}%")
        
        if s == "السعر":
            query += " ORDER BY price"
        elif s == "المشاهدات":
            query += " ORDER BY views DESC"
        else:
            query += " ORDER BY date DESC"
        
        query += " LIMIT 20"
        
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
            
            # زر لإضافة إعلانات تلقائية
            if st.button("🚀 إضافة إعلانات تلقائية", use_container_width=True):
                count = seed_smart_ads(conn)
                seed_ai_promoted_ads(conn)
                if count > 0:
                    st.success(f"✅ تمت إضافة {count} إعلان!")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.info("الإعلانات موجودة مسبقاً")
                
    except Exception as e:
        st.error(f"خطأ في تحميل الإعلانات: {e}")

def post_ad():
    """صفحة إضافة إعلان جديد"""
    st.markdown("### 📢 إعلان جديد")
    
    with st.form("new_ad_form"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("📱 اسم المنتج *")
            cat = st.selectbox("🏷️ الفئة", ["سامسونج", "آيفون", "هواوي", "شاومي", "جوجل", "أخرى"])
        with col2:
            price = st.number_input("💰 السعر (دج) *", min_value=0, step=1000)
            wilaya = st.selectbox("📍 الولاية *", ALGERIAN_WILAYAS[1:])
        
        phone = st.text_input("📞 رقم الهاتف *", placeholder="مثال: 0555123456")
        desc = st.text_area("📝 الوصف", height=100, placeholder="اكتب وصفاً مفصلاً للمنتج...")
        
        uploaded_file = st.file_uploader("🖼️ ارفع صورة للهاتف", type=["png", "jpg", "jpeg", "webp"])
        
        if st.form_submit_button("🚀 نشر إعلان", use_container_width=True) and title and phone and price > 0:
            image_path = save_uploaded_file(uploaded_file) if uploaded_file else None
            
            try:
                conn.execute("""
                    INSERT INTO ads (title, price, phone, wilaya, description, category, owner, status, verified, image_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'active', 1, ?)
                """, (title, price, phone, wilaya, desc, cat, st.session_state.user, image_path))
                conn.commit()
                st.success("✅ تم نشر إعلانك بنجاح!")
                st.balloons()
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"❌ خطأ: {e}")

def profile_page():
    """صفحة الحساب الشخصي"""
    st.markdown("### 👤 حسابي الشخصي")
    
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

def admin_dashboard():
    """لوحة الإدارة السرية"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00ffff20, #ff00ff20); border: 2px solid #00ffff; border-radius: 30px; padding: 20px; margin-bottom: 20px;">
        <h1 style="color: white; text-align: center;">🔐 لوحة القيادة</h1>
        <p style="color: #00ffff; text-align: center;">خاص بالطاهر الطاهري</p>
    </div>
    """, unsafe_allow_html=True)
    
    users, ads, visitors, views = get_stats(conn)
    
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
            count = seed_smart_ads(conn)
            if count > 0:
                st.success(f"✅ تمت إضافة {count} إعلان!")
            else:
                st.info("الإعلانات موجودة مسبقاً")
    
    with col_b:
        if st.button("🎯 إضافة إعلانات ممولة", use_container_width=True):
            count = seed_ai_promoted_ads(conn)
            st.success(f"✅ تمت إضافة {count} إعلان ممول!")
    
    with col_c:
        if st.button("🤖 بوت جلب الإعلانات", use_container_width=True):
            st.session_state.show_scraper = True
    
    # بوت الجلب
    if st.session_state.get('show_scraper', False):
        scrape_ads_ui()
        if st.button("🔒 إخفاء البوت"):
            st.session_state.show_scraper = False
            st.rerun()
    
    st.markdown("### 🚨 تنبيهات الرادار")
    if st.session_state.last_alert:
        st.markdown(f"""
        <div style="background: rgba(255,0,0,0.2); border: 2px solid #ff00ff; border-radius: 15px; padding: 15px;">
            <h4 style="color: #ff00ff;">🔥 مشتري جدي!</h4>
            <p><b>{st.session_state.last_alert['message']}</b></p>
            <p>💰 {st.session_state.last_alert['price']} دج</p>
        </div>
        """, unsafe_allow_html=True)

def robotic_alert_ui():
    """واجهة الرادار في الشريط الجانبي"""
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

def generate_auto_ads():
    """مولد الإعلانات الذكي حسب الوقت"""
    hour = datetime.now().hour
    if 18 <= hour <= 22:
        st.sidebar.markdown("<p style='color:#00ffff; font-weight:bold;'>🔥 وقت الذروة! انشر الآن</p>", unsafe_allow_html=True)
    elif 9 <= hour <= 12:
        st.sidebar.markdown("<p style='color:#ff00ff; font-weight:bold;'>☀️ وقت الصباح الذهبي</p>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown("<p style='color:#888;'>⏳ وقت هادئ</p>", unsafe_allow_html=True)

# ==========================================
# 7. الدالة الرئيسية
# ==========================================
def main():
    # تطبيق الثيم
    set_ultimate_theme()
    
    # تسجيل الزائر
    conn.execute("INSERT OR IGNORE INTO visitors (ip, page) VALUES (?, 'main')", (st.session_state.ip,))
    conn.commit()
    
    # عرض العناصر الثابتة
    show_live_chat()
    show_live_counter()
    
    if st.session_state.user:
        with st.sidebar:
            st.markdown(f"### ✨ أهلاً {st.session_state.user}")
            choice = st.radio("القائمة", ["🛍️ السوق", "📢 نشر إعلان", "👤 حسابي", "🚪 خروج"])
            
            robotic_alert_ui()
            generate_auto_ads()
            
            with st.expander("📜 شروط الاستخدام"):
                show_terms()
            
            if choice == "🚪 خروج":
                st.session_state.user = None
                st.session_state.admin_access = False
                st.rerun()
        
        if choice == "🛍️ السوق":
            show_market()
        elif choice == "📢 نشر إعلان":
            post_ad()
        elif choice == "👤 حسابي":
            profile_page()
        
        # زر لوحة الإدارة للمسؤول
        if st.session_state.role == "admin" and st.sidebar.button("🔐 لوحة الإدارة", use_container_width=True):
            admin_dashboard()
    else:
        login_page()

# ==========================================
# 8. تشغيل التطبيق
# ==========================================
if __name__ == "__main__":
    main()

