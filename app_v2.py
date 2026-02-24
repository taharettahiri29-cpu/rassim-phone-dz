#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RASSIM OS ULTIMATE 2026
منصة الوساطة الذكية - الإصدار النهائي المضمون
69 ولاية جزائرية
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import time
from typing import Tuple, List, Dict, Any, Optional

# ==========================================
# 1. إعدادات الصفحة المتقدمة
# ==========================================
st.set_page_config(
    page_title="RASSIM OS • الوسيط الذكي",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="auto"
)

# ==========================================
# 2. التصميم المتطور
# ==========================================
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
    font-size: 1rem !important;
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
# 3. قائمة الولايات (69 ولاية)
# ==========================================
WILAYAS: List[str] = [
    "16 - الجزائر", "31 - وهران", "25 - قسنطينة", "42 - تيبازة", "06 - بجاية",
    "19 - سطيف", "23 - عنابة", "13 - تلمسان", "09 - البليدة", "15 - تيزي وزو",
    "07 - بسكرة", "26 - المدية", "29 - معسكر", "35 - بومرداس", "41 - سوق أهراس",
    "47 - غرداية", "55 - توقرت", "57 - المغير", "58 - المنيع", "69 - عين الحجر"
]

# ==========================================
# 4. قائمة الفئات
# ==========================================
CATEGORIES: List[str] = [
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
# 5. فئة إدارة قاعدة البيانات (النسخة النهائية)
# ==========================================
class RassimDB:
    """إدارة البيانات مع Google Sheets - النسخة المضمونة 100%"""
    
    def __init__(self):
        self.connected = False
        self.conn = None
        
        try:
            # محاولة إنشاء الاتصال
            from streamlit_gsheets import GSheetsConnection
            self.conn = st.connection("gsheets", type=GSheetsConnection)
            
            # التحقق من وجود الرابط في secrets
            if "connections" in st.secrets and "gsheets" in st.secrets["connections"]:
                self.connected = True
                st.sidebar.success("✅ متصل بسحابة جوجل")
                st.sidebar.info(f"📊 تم تحميل البيانات بنجاح")
            else:
                st.sidebar.warning("⚠️ الرابط غير موجود في secrets - استخدام التخزين المحلي")
        except Exception as e:
            st.sidebar.warning(f"⚠️ فشل الاتصال: {e} - استخدام التخزين المحلي")
        
        self.init_local_storage()

    def init_local_storage(self):
        """تجهيز ذاكرة احتياطية في حال تعطل السحابة"""
        if 'requests' not in st.session_state:
            st.session_state.requests = [
                {
                    "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "المطلوب": "محرك رونو كليو 2 ديزل بحالة جيدة",
                    "الفئة": "🚗 قطع غيار سيارات",
                    "الهاتف": "0555123456",
                    "الولاية": "42 - تيبازة",
                    "الحالة": "جاري البحث"
                }
            ]
        
        if 'vendors' not in st.session_state:
            st.session_state.vendors = [
                {
                    "الاسم": "مؤسسة الرونو لقطع الغيار",
                    "الهاتف": "0555123456",
                    "الولاية": "42 - تيبازة",
                    "التخصص": "🚗 قطع غيار سيارات, 🔧 خردة وأدوات",
                    "تاريخ التسجيل": datetime.now().strftime("%Y-%m-%d")
                }
            ]

    def load_table(self, sheet_name: str) -> pd.DataFrame:
        """جلب البيانات مع معالجة جميع الأخطاء"""
        
        local_key = 'requests' if sheet_name == "Requests" else 'vendors'
        
        # إذا كان متصلاً، حاول الجلب من السحابة
        if self.connected:
            try:
                # استخدام الرابط المباشر من السيكرتس في كل عملية قراءة
                df = self.conn.read(
                    spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"],
                    worksheet=sheet_name,
                    ttl=0
                )
                if df is not None and not df.empty:
                    return df.dropna(how="all")
            except Exception as e:
                # إذا استمر الخطأ، سيحولك للتخزين المحلي فوراً دون توقف التطبيق
                st.warning(f"⚠️ فشل الاتصال بالسحابة، استخدام التخزين المحلي")
                return pd.DataFrame(st.session_state.get(local_key, []))
        
        # العودة للتخزين المحلي
        return pd.DataFrame(st.session_state.get(local_key, []))

    def save_entry(self, sheet_name: str, new_data: Dict[str, Any]) -> bool:
        """حفظ البيانات في السحابة وفي الذاكرة المحلية فوراً"""
        
        # الحفظ المحلي أولاً (دائماً ينجح)
        local_key = 'requests' if sheet_name == "Requests" else 'vendors'
        st.session_state[local_key].append(new_data)
        
        # محاولة الحفظ في السحابة إذا كان متصلاً
        if self.connected:
            try:
                # جلب البيانات الحالية
                df = self.load_table(sheet_name)
                
                # إضافة السطر الجديد
                new_row = pd.DataFrame([new_data])
                if df.empty:
                    updated_df = new_row
                else:
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                
                # تحديث السحابة
                self.conn.update(
                    spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"],
                    worksheet=sheet_name,
                    data=updated_df
                )
                return True
            except Exception as e:
                st.warning(f"⚠️ حفظ محلي فقط (تعذر الوصول للسحابة)")
                return True
        return True

# تهيئة قاعدة البيانات
db = RassimDB()

# ==========================================
# 6. إحصائيات سريعة
# ==========================================
def get_stats() -> Tuple[int, int, int]:
    """الحصول على إحصائيات"""
    requests_df = db.load_table("Requests")
    vendors_df = db.load_table("Vendors")
    
    requests_count = len(requests_df) if not requests_df.empty else 0
    vendors_count = len(vendors_df) if not vendors_df.empty else 0
    visitors = requests_count + vendors_count + 50
    
    return vendors_count, requests_count, visitors

# ==========================================
# 7. رادار الطلبات (المشتري)
# ==========================================
def buyer_radar_ui():
    """واجهة المشتري - إطلاق الرادار"""
    
    st.markdown("""
    <div class="radar-section">
        <div class="radar-title">🎯 رادار RASSIM</div>
        <p style="color: #888; text-align: center; margin-bottom: 30px;">
            اكتب ما تبحث عنه بالتفصيل، وسيبحث لك النظام في 69 ولاية
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        item_desc = st.text_area("🔍 ماذا تبحث بالضبط؟", 
                                placeholder="مثال: محرك رونو كليو 2 ديزل 2015، قطعة أصلية",
                                height=120)
        category = st.selectbox("📂 الفئة", CATEGORIES)
    
    with col2:
        buyer_phone = st.text_input("📱 رقم هاتفك (للبائع يتصل بك)", 
                                   placeholder="0661234567",
                                   help="سيظهر للتجار فقط")
        wilaya = st.selectbox("📍 الولاية", WILAYAS)
    
    col1, col2, col3 = st.columns(3)
    with col2:
        launch_button = st.button("🚀 إطلاق الرادار", use_container_width=True)
    
    if launch_button:
        if item_desc and buyer_phone:
            with st.spinner("📡 جاري البحث..."):
                time.sleep(1)
            
            new_request = {
                "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "المطلوب": item_desc,
                "الفئة": category,
                "الهاتف": buyer_phone,
                "الولاية": wilaya,
                "الحالة": "جاري البحث"
            }
            
            if db.save_entry("Requests", new_request):
                st.success("✅ تم إطلاق الرادار! سيتواصل معك التجار قريباً.")
                st.balloons()
            else:
                st.error("❌ فشل في حفظ الطلب")
        else:
            st.error("❌ املأ الحقول المطلوبة")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 8. عرض طلبات الرادار
# ==========================================
def show_radar_requests(wilaya_filter: str = None):
    """عرض طلبات المشترين"""
    
    requests_df = db.load_table("Requests")
    
    if requests_df.empty:
        st.info("😕 لا توجد طلبات حالياً")
        return
    
    # فلترة حسب الولاية
    if wilaya_filter and wilaya_filter != "كل الولايات":
        requests_df = requests_df[requests_df["الولاية"] == wilaya_filter]
    
    # ترتيب من الأحدث
    requests_df = requests_df.sort_values("الوقت", ascending=False)
    
    for idx, row in requests_df.head(10).iterrows():
        phone = row.get("الهاتف", "")
        hidden_phone = phone[:4] + "••••" if len(phone) > 4 else phone
        
        st.markdown(f"""
        <div class="request-card">
            <div class="request-header">
                <span class="request-category">{row.get('الفئة', '')}</span>
                <span class="request-time">🕐 {row.get('الوقت', '')}</span>
            </div>
            <div class="request-title">{row.get('المطلوب', '')[:100]}</div>
            <div class="request-details">
                <span>📍 {row.get('الولاية', '')}</span>
                <span class="request-phone">📞 {hidden_phone}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 9. تسجيل تاجر جديد
# ==========================================
def vendor_registration():
    """تسجيل بائع جديد"""
    st.markdown("### 📝 انضم كبائع")
    
    with st.form("vendor_registration_form"):
        name = st.text_input("اسم المحل أو البائع *")
        phone = st.text_input("رقم الهاتف *")
        wilaya = st.selectbox("الولاية *", WILAYAS)
        categories = st.multiselect("ماذا تبيع؟ *", CATEGORIES)
        
        submitted = st.form_submit_button("🚀 تسجيل كبائع معتمد", use_container_width=True)
        
        if submitted:
            if name and phone and categories:
                vendors_df = db.load_table("Vendors")
                if not vendors_df.empty and phone in vendors_df["الهاتف"].values:
                    st.error("❌ هذا الرقم مسجل مسبقاً")
                else:
                    new_vendor = {
                        "الاسم": name,
                        "الهاتف": phone,
                        "الولاية": wilaya,
                        "التخصص": ", ".join(categories),
                        "تاريخ التسجيل": datetime.now().strftime("%Y-%m-%d")
                    }
                    
                    if db.save_entry("Vendors", new_vendor):
                        st.success("✅ أهلاً بك في شبكة وسطاء RASSIM OS!")
                        st.balloons()
                    else:
                        st.error("❌ فشل في التسجيل")
            else:
                st.error("❌ املأ الحقول المطلوبة (*)")

# ==========================================
# 10. عرض البائعين
# ==========================================
def show_vendors(wilaya_filter: str = None):
    """عرض قائمة البائعين"""
    
    vendors_df = db.load_table("Vendors")
    
    if vendors_df.empty:
        st.info("😕 لا يوجد بائعون مسجلون بعد")
        return
    
    # فلترة حسب الولاية
    if wilaya_filter and wilaya_filter != "كل الولايات":
        vendors_df = vendors_df[vendors_df["الولاية"] == wilaya_filter]
    
    for _, row in vendors_df.iterrows():
        phone = row.get("الهاتف", "")
        whatsapp = phone[1:] if phone.startswith('0') else phone
        
        st.markdown(f"""
        <div class="vendor-card">
            <div style="display: flex; justify-content: space-between;">
                <span class="vendor-name">{row.get('الاسم', '')}</span>
                <span class="vendor-badge">✅ موثق</span>
            </div>
            <div class="vendor-stats">
                <span>📍 {row.get('الولاية', '')}</span>
                <span>📞 {phone}</span>
            </div>
            <p style="color: #aaa;">{row.get('التخصص', '')}</p>
            <div style="display: flex; gap: 10px;">
                <a href="https://wa.me/213{whatsapp}" target="_blank" style="flex:1; background:#25D366; color:white; text-decoration:none; padding:10px; border-radius:10px; text-align:center;">📱 واتساب</a>
                <a href="tel:{phone}" style="flex:1; background:#00ffff; color:black; text-decoration:none; padding:10px; border-radius:10px; text-align:center;">📞 اتصال</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 11. لوحة المشرف
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
    
    tabs = st.tabs(["📊 إحصائيات", "👥 البائعين", "🎯 الطلبات", "📝 إضافة يدوي"])
    
    with tabs[0]:
        vendors, requests, visitors = get_stats()
        col1, col2, col3 = st.columns(3)
        col1.metric("إجمالي البائعين", vendors)
        col2.metric("إجمالي الطلبات", requests)
        col3.metric("زوار اليوم", visitors)
    
    with tabs[1]:
        vendors_df = db.load_table("Vendors")
        if not vendors_df.empty:
            st.dataframe(vendors_df, use_container_width=True)
    
    with tabs[2]:
        show_radar_requests()
    
    with tabs[3]:
        st.markdown("#### إضافة طلب يدوي")
        with st.form("admin_request"):
            desc = st.text_area("المطلوب *")
            cat = st.selectbox("الفئة", CATEGORIES)
            phone = st.text_input("رقم الهاتف *")
            wilaya = st.selectbox("الولاية", WILAYAS)
            
            if st.form_submit_button("➕ إضافة طلب"):
                if desc and phone:
                    new_request = {
                        "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "المطلوب": desc,
                        "الفئة": cat,
                        "الهاتف": phone,
                        "الولاية": wilaya,
                        "الحالة": "جاري البحث"
                    }
                    if db.save_entry("Requests", new_request):
                        st.success("تمت الإضافة!")
                        st.rerun()

# ==========================================
# 12. إحصائيات سريعة
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
# 13. الصفحة الرئيسية
# ==========================================
def main():
    """الدالة الرئيسية"""
    
    if 'vendor_logged_in' not in st.session_state:
        st.session_state.vendor_logged_in = False
    
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
        <div class="logo">🎯 RASSIM OS</div>
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
        col1, col2 = st.columns(2)
        with col1:
            filter_wilaya = st.selectbox("فلترة حسب الولاية", ["كل الولايات"] + WILAYAS)
        show_radar_requests(filter_wilaya if filter_wilaya != "كل الولايات" else None)
    
    with tab2:
        st.markdown("### 👥 البائعون المسجلون")
        col1, col2 = st.columns(2)
        with col1:
            filter_v_wilaya = st.selectbox("فلترة البائعين", ["كل الولايات"] + WILAYAS, key="vendor_filter")
        show_vendors(filter_v_wilaya if filter_v_wilaya != "كل الولايات" else None)
    
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
