import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client
import time

# ==========================================
# 1. إعدادات الصفحة والتصميم المتطور
# ==========================================
st.set_page_config(
    page_title="RASSIM OS • السحابة الذكية",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');

* {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl;
    box-sizing: border-box;
}

.stApp {
    background: linear-gradient(135deg, #0a0a1a, #1a1a2a);
    color: white;
}

/* ===== الشعار الرئيسي ===== */
.main-header {
    text-align: center;
    padding: 20px;
    margin-bottom: 20px;
}

.logo {
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, #00ffff, #ff00ff, #00ffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3s linear infinite;
}

@keyframes shine {
    to { background-position: 200% center; }
}

.subtitle {
    color: #888;
    font-size: 1.2rem;
    margin-top: -10px;
}

/* ===== حالة الاتصال ===== */
.connection-status {
    text-align: left;
    padding: 10px;
}

.status-badge {
    display: inline-block;
    padding: 5px 15px;
    border-radius: 50px;
    font-weight: bold;
    font-size: 0.9rem;
}

.status-online {
    background: rgba(0, 255, 0, 0.1);
    border: 1px solid #00ff00;
    color: #00ff00;
}

.status-offline {
    background: rgba(255, 0, 0, 0.1);
    border: 1px solid #ff0000;
    color: #ff0000;
}

/* ===== رادار الطلبات ===== */
.radar-section {
    background: linear-gradient(135deg, #1a1a2a, #2a2a3a);
    padding: 30px;
    border-radius: 30px;
    border: 2px solid #00ffff;
    margin-bottom: 30px;
    box-shadow: 0 20px 40px rgba(0,255,255,0.15);
    animation: pulse 3s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 20px 40px rgba(0,255,255,0.15); }
    50% { box-shadow: 0 20px 60px rgba(255,0,255,0.2); }
}

.radar-title {
    color: #00ffff;
    font-size: 2.2rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
}

/* ===== بطاقة الطلب ===== */
.request-card {
    background: #1a1a2a;
    border-right: 5px solid #00ffff;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 15px;
    transition: all 0.3s ease;
}

.request-card:hover {
    transform: translateX(-5px);
    background: #252a3a;
    border-right-color: #ff00ff;
}

.request-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
}

.request-category {
    background: #2a2a3a;
    padding: 5px 12px;
    border-radius: 20px;
    color: #00ffff;
    font-size: 0.8rem;
}

.request-time {
    color: #888;
    font-size: 0.8rem;
}

.request-title {
    color: white;
    font-size: 1.2rem;
    font-weight: bold;
    margin: 10px 0;
}

.request-details {
    display: flex;
    gap: 15px;
    color: #888;
    font-size: 0.9rem;
    margin: 10px 0;
}

.request-phone {
    background: #2a2a3a;
    padding: 3px 10px;
    border-radius: 15px;
    color: #ff00ff;
    font-size: 0.8rem;
    display: inline-block;
}

/* ===== بطاقة التاجر ===== */
.vendor-card {
    background: linear-gradient(135deg, #1a1a2a, #2a2a3a);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 15px;
    border: 1px solid #333;
    transition: all 0.3s ease;
}

.vendor-card:hover {
    border-color: #00ffff;
    transform: translateX(-5px);
    box-shadow: 0 10px 20px rgba(0,255,255,0.1);
}

.vendor-name {
    color: #00ffff;
    font-size: 1.3rem;
    font-weight: bold;
}

.vendor-badge {
    display: inline-block;
    background: #00aa00;
    color: white;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
}

.vendor-stats {
    display: flex;
    gap: 15px;
    color: #888;
    font-size: 0.9rem;
    margin: 10px 0;
}

/* ===== إحصائيات ===== */
.stat-card {
    background: #1a1a2a;
    border: 1px solid #333;
    border-radius: 15px;
    padding: 15px;
    text-align: center;
}

.stat-value {
    font-size: 2rem;
    color: #00ffff;
    font-weight: bold;
}

.stat-label {
    color: #888;
    font-size: 0.9rem;
}

/* ===== أزرار ===== */
.stButton > button {
    background: linear-gradient(135deg, #00ffff, #ff00ff) !important;
    border: none !important;
    color: black !important;
    font-weight: bold !important;
    border-radius: 15px !important;
    padding: 12px !important;
    width: 100%;
    transition: transform 0.2s !important;
}

.stButton > button:hover {
    transform: scale(1.02) !important;
    box-shadow: 0 10px 20px rgba(255,0,255,0.3) !important;
}

.contact-btn {
    background: #25D366;
    color: white;
    padding: 10px;
    border-radius: 10px;
    text-decoration: none;
    display: inline-block;
    text-align: center;
    font-weight: bold;
}

/* ===== عداد الزوار ===== */
.live-counter {
    position: fixed;
    bottom: 20px;
    left: 20px;
    background: #1a1a2a;
    border: 1px solid #00ffff;
    padding: 8px 15px;
    border-radius: 50px;
    z-index: 999;
    color: white;
    font-size: 0.85rem;
    backdrop-filter: blur(5px);
}

/* ===== فقاعة الدردشة ===== */
.chat-bubble {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: #00ffff;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 9999;
    animation: float 3s ease-in-out infinite;
    box-shadow: 0 5px 20px rgba(0,255,255,0.3);
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}

/* ===== تذييل ===== */
.footer {
    text-align: center;
    color: #666;
    font-size: 0.8rem;
    margin-top: 40px;
    padding: 20px;
    border-top: 1px solid #333;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. قائمة الولايات والفئات
# ==========================================
WILAYAS = [
    "16 - الجزائر", "31 - وهران", "25 - قسنطينة", "42 - تيبازة", "06 - بجاية",
    "19 - سطيف", "23 - عنابة", "13 - تلمسان", "09 - البليدة", "15 - تيزي وزو",
    "07 - بسكرة", "26 - المدية", "29 - معسكر", "35 - بومرداس", "41 - سوق أهراس",
    "47 - غرداية", "55 - توقرت", "57 - المغير", "58 - المنيع", "69 - عين الحجر",
    "01 - أدرار", "02 - الشلف", "03 - الأغواط", "04 - أم البواقي", "05 - باتنة",
    "08 - بشار", "10 - البويرة", "11 - تمنراست", "12 - تبسة", "14 - تيارت",
    "17 - الجلفة", "18 - جيجل", "20 - سعيدة", "21 - سكيكدة", "22 - سيدي بلعباس",
    "24 - قالمة", "27 - مستغانم", "28 - المسيلة", "30 - ورقلة", "32 - البيض",
    "33 - إليزي", "34 - برج بوعريريج", "36 - الطارف", "37 - تندوف", "38 - تيسمسيلт",
    "39 - الوادي", "40 - خنشلة", "43 - ميلة", "44 - عين الدفلى", "45 - النعامة",
    "46 - عين تموشنت", "48 - غليزان", "49 - تيميمون", "50 - برج باجي مختار"
]

CATEGORIES = [
    "🚗 قطع غيار سيارات",
    "🔧 خردة وأدوات",
    "🏠 عقارات (بيع/كراء)",
    "💄 تجميل / Cosmetique",
    "📱 هواتف وأجهزة",
    "🛋️ أثاث ومنزل",
    "👕 ملابس وأزياء",
    "🛠️ خدمات",
    "📦 أخرى"
]

# ==========================================
# 3. الربط مع Supabase
# ==========================================
@st.cache_resource
def init_connection():
    """تهيئة الاتصال بـ Supabase"""
    try:
        url = st.secrets["connections"]["supabase"]["url"]
        key = st.secrets["connections"]["supabase"]["key"]
        client = create_client(url, key)
        
        # اختبار الاتصال
        client.table("requests").select("*").limit(1).execute()
        return client, True
    except Exception as e:
        st.sidebar.error(f"⚠️ فشل الاتصال: {e}")
        return None, False

supabase, connected = init_connection()

# ==========================================
# 4. دوال التعامل مع قاعدة البيانات
# ==========================================
def fetch_requests():
    """جلب جميع الطلبات من قاعدة البيانات"""
    if not connected:
        return pd.DataFrame()
    
    try:
        response = supabase.table("requests").select("*").order("created_at", desc=True).execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except Exception as e:
        st.error(f"خطأ في جلب الطلبات: {e}")
        return pd.DataFrame()

def fetch_vendors():
    """جلب جميع البائعين من قاعدة البيانات"""
    if not connected:
        return pd.DataFrame()
    
    try:
        response = supabase.table("vendors").select("*").order("created_at", desc=True).execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except Exception as e:
        st.error(f"خطأ في جلب البائعين: {e}")
        return pd.DataFrame()

def save_request(item, category, phone, wilaya):
    """حفظ طلب جديد في قاعدة البيانات"""
    if not connected:
        st.error("لا يمكن الحفظ - الاتصال بالسحابة غير متوفر")
        return False
    
    try:
        data = {
            "item": item,
            "category": category,
            "phone": phone,
            "wilaya": wilaya,
            "status": "جاري البحث"
        }
        supabase.table("requests").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ الطلب: {e}")
        return False

def save_vendor(name, phone, wilaya, categories):
    """حفظ بائع جديد في قاعدة البيانات"""
    if not connected:
        st.error("لا يمكن الحفظ - الاتصال بالسحابة غير متوفر")
        return False
    
    try:
        # التحقق من عدم تكرار الرقم
        existing = supabase.table("vendors").select("*").eq("phone", phone).execute()
        if existing.data and len(existing.data) > 0:
            return False
        
        data = {
            "name": name,
            "phone": phone,
            "wilaya": wilaya,
            "category": ", ".join(categories)
        }
        supabase.table("vendors").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"خطأ في حفظ البائع: {e}")
        return False

def get_stats():
    """الحصول على إحصائيات"""
    requests_df = fetch_requests()
    vendors_df = fetch_vendors()
    
    requests_count = len(requests_df) if not requests_df.empty else 0
    vendors_count = len(vendors_df) if not vendors_df.empty else 0
    visitors = requests_count + vendors_count + 50
    
    return vendors_count, requests_count, visitors

# ==========================================
# 5. واجهة رادار الطلبات
# ==========================================
def buyer_radar_ui():
    """واجهة المشتري - إطلاق الرادار"""
    
    st.markdown("""
    <div class="radar-section">
        <div class="radar-title">🎯 رادار RASSIM</div>
        <p style="color: #888; text-align: center; margin-bottom: 30px;">
            اكتب ما تبحث عنه وسيبحث لك النظام في 69 ولاية
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        item_desc = st.text_area("🔍 ماذا تبحث بالضبط؟", 
                                placeholder="مثال: محرك رونو كليو 2 ديزل 2015",
                                height=100)
        category = st.selectbox("📂 الفئة", CATEGORIES)
    
    with col2:
        buyer_phone = st.text_input("📱 رقم هاتفك", 
                                   placeholder="0661234567")
        wilaya = st.selectbox("📍 الولاية", WILAYAS)
    
    col1, col2, col3 = st.columns(3)
    with col2:
        launch_button = st.button("🚀 إطلاق الرادار", use_container_width=True)
    
    if launch_button:
        if item_desc and buyer_phone:
            with st.spinner("📡 جاري البحث..."):
                time.sleep(1)
            
            if save_request(item_desc, category, buyer_phone, wilaya):
                st.success("✅ تم إطلاق الرادار! سيتواصل معك التجار قريباً.")
                st.balloons()
                time.sleep(2)
                st.rerun()
            else:
                st.error("❌ فشل في حفظ الطلب")
        else:
            st.error("❌ املأ الحقول المطلوبة")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 6. عرض الطلبات
# ==========================================
def show_requests():
    """عرض طلبات المشترين بشكل احترافي"""
    
    requests_df = fetch_requests()
    
    if requests_df.empty:
        st.info("😕 لا توجد طلبات حالياً")
        return
    
    for _, row in requests_df.iterrows():
        phone = row.get("phone", "")
        hidden_phone = phone[:4] + "••••" if len(phone) > 4 else phone
        
        created_at = row.get("created_at", "")
        if created_at and len(str(created_at)) > 16:
            created_at = str(created_at)[:16]
        
        st.markdown(f"""
        <div class="request-card">
            <div class="request-header">
                <span class="request-category">{row.get('category', '')}</span>
                <span class="request-time">🕐 {created_at}</span>
            </div>
            <div class="request-title">{row.get('item', '')[:100]}</div>
            <div class="request-details">
                <span>📍 {row.get('wilaya', '')}</span>
                <span class="request-phone">📞 {hidden_phone}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 7. تسجيل تاجر جديد
# ==========================================
def vendor_registration():
    """تسجيل بائع جديد"""
    st.markdown("### 📝 انضم كبائع")
    
    with st.form("vendor_form"):
        name = st.text_input("اسم المحل أو البائع *")
        phone = st.text_input("رقم الهاتف *")
        wilaya = st.selectbox("الولاية *", WILAYAS)
        categories = st.multiselect("ماذا تبيع؟ *", CATEGORIES)
        
        submitted = st.form_submit_button("🚀 تسجيل كبائع معتمد", use_container_width=True)
        
        if submitted:
            if name and phone and categories:
                if save_vendor(name, phone, wilaya, categories):
                    st.success("✅ أهلاً بك في شبكة وسطاء RASSIM OS!")
                    st.balloons()
                else:
                    st.error("❌ هذا الرقم مسجل مسبقاً أو فشل في التسجيل")
            else:
                st.error("❌ املأ الحقول المطلوبة (*)")

# ==========================================
# 8. عرض البائعين
# ==========================================
def show_vendors():
    """عرض قائمة البائعين"""
    
    vendors_df = fetch_vendors()
    
    if vendors_df.empty:
        st.info("😕 لا يوجد بائعون مسجلون بعد")
        return
    
    for _, row in vendors_df.iterrows():
        phone = row.get("phone", "")
        whatsapp = phone[1:] if phone.startswith('0') else phone
        
        created_at = row.get("created_at", "")
        if created_at and len(str(created_at)) > 10:
            created_at = str(created_at)[:10]
        
        st.markdown(f"""
        <div class="vendor-card">
            <div style="display: flex; justify-content: space-between;">
                <span class="vendor-name">{row.get('name', '')}</span>
                <span class="vendor-badge">✅ موثق</span>
            </div>
            <div class="vendor-stats">
                <span>📍 {row.get('wilaya', '')}</span>
                <span>📞 {phone}</span>
                <span>📅 {created_at}</span>
            </div>
            <p style="color: #aaa;">{row.get('category', '')}</p>
            <div style="display: flex; gap: 10px;">
                <a href="https://wa.me/213{whatsapp}" target="_blank" style="flex:1; background:#25D366; color:white; text-decoration:none; padding:10px; border-radius:10px; text-align:center;">📱 واتساب</a>
                <a href="tel:{phone}" style="flex:1; background:#00ffff; color:black; text-decoration:none; padding:10px; border-radius:10px; text-align:center;">📞 اتصال</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 9. لوحة المشرف
# ==========================================
def admin_panel():
    """لوحة تحكم المشرف"""
    st.markdown("### 🔐 لوحة المشرف")
    
    if not st.session_state.get('admin_logged_in', False):
        password = st.text_input("كلمة المرور", type="password")
        if st.button("دخول") and password == "rassim2026":
            st.session_state.admin_logged_in = True
            st.rerun()
        return
    
    tabs = st.tabs(["📊 إحصائيات", "👥 البائعين", "🎯 الطلبات"])
    
    with tabs[0]:
        vendors, requests, visitors = get_stats()
        col1, col2, col3 = st.columns(3)
        col1.metric("إجمالي البائعين", vendors)
        col2.metric("إجمالي الطلبات", requests)
        col3.metric("زوار اليوم", visitors)
    
    with tabs[1]:
        vendors_df = fetch_vendors()
        if not vendors_df.empty:
            st.dataframe(vendors_df, use_container_width=True)
    
    with tabs[2]:
        requests_df = fetch_requests()
        if not requests_df.empty:
            st.dataframe(requests_df, use_container_width=True)

# ==========================================
# 10. إحصائيات سريعة
# ==========================================
def show_stats():
    vendors, requests, visitors = get_stats()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{vendors}</div>
            <div class="stat-label">تاجر</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{requests}</div>
            <div class="stat-label">طلب</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{visitors}</div>
            <div class="stat-label">زائر</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 11. الصفحة الرئيسية
# ==========================================
def main():
    """الدالة الرئيسية"""
    
    # حالة الاتصال
    with st.sidebar:
        st.markdown("### 📊 حالة النظام")
        if connected:
            st.markdown('<span class="status-badge status-online">✅ متصل بالسحابة</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-badge status-offline">❌ غير متصل</span>', unsafe_allow_html=True)
        
        vendors, requests, visitors = get_stats()
        st.metric("إجمالي الطلبات", requests)
        st.metric("إجمالي البائعين", vendors)
    
    # عداد الزوار
    vendors, requests, visitors = get_stats()
    st.markdown(f"""
    <div class="live-counter">
        <span style="color:#00ffff;">●</span> {visitors} زائر • {vendors} تاجر • {requests} طلب
    </div>
    """, unsafe_allow_html=True)
    
    # فقاعة الدردشة
    st.markdown("""
    <div class="chat-bubble" onclick="window.open('https://wa.me/213555555555')">
        <img src="https://img.icons8.com/ios-filled/30/000000/speech-bubble.png">
    </div>
    """, unsafe_allow_html=True)
    
    # الشعار
    st.markdown("""
    <div class="main-header">
        <div class="logo">⚡ RASSIM OS</div>
        <div class="subtitle">منصة الوساطة الذكية • 69 ولاية</div>
    </div>
    """, unsafe_allow_html=True)
    
    show_stats()
    buyer_radar_ui()
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 طلبات المشترين",
        "👥 قائمة البائعين",
        "👨‍💼 تسجيل تاجر",
        "🔐 المشرف"
    ])
    
    with tab1:
        st.markdown("### 📋 جميع الطلبات")
        show_requests()
    
    with tab2:
        st.markdown("### 👥 البائعون المسجلون")
        show_vendors()
    
    with tab3:
        vendor_registration()
    
    with tab4:
        admin_panel()
    
    st.markdown("""
    <div class="footer">
        RASSIM OS 2026 • منصة الوساطة الذكية • جميع الحقوق محفوظة
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

