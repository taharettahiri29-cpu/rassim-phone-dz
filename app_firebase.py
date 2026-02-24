import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from datetime import datetime
import time

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="RASSIM OS • Firebase",
    page_icon="🔥",
    layout="wide"
)

# ==========================================
# 2. تهيئة Firebase
# ==========================================
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ==========================================
# 3. قائمة الولايات والفئات
# ==========================================
WILAYAS = ["16 - الجزائر", "31 - وهران", "25 - قسنطينة", "42 - تيبازة", "06 - بجاية"]
CATEGORIES = ["🚗 قطع غيار سيارات", "🔧 خردة وأدوات", "🏠 عقارات", "📱 هواتف", "📦 أخرى"]

# ==========================================
# 4. الدوال الرئيسية
# ==========================================
def get_requests(wilaya_filter=None):
    """جلب الطلبات من Firestore"""
    try:
        requests_ref = db.collection("requests").order_by("created_at", direction=firestore.Query.DESCENDING)
        docs = requests_ref.stream()
        
        data = []
        for doc in docs:
            item = doc.to_dict()
            item["id"] = doc.id
            if not wilaya_filter or wilaya_filter == "كل الولايات" or item.get("wilaya") == wilaya_filter:
                data.append(item)
        return pd.DataFrame(data)
    except Exception as e:
        return pd.DataFrame()

def save_request(item_desc, category, phone, wilaya):
    """حفظ طلب جديد"""
    try:
        db.collection("requests").add({
            "created_at": firestore.SERVER_TIMESTAMP,
            "item": item_desc,
            "category": category,
            "phone": phone,
            "wilaya": wilaya,
            "status": "جاري البحث"
        })
        return True
    except Exception as e:
        return False

def get_vendors(wilaya_filter=None):
    """جلب البائعين من Firestore"""
    try:
        vendors_ref = db.collection("vendors").order_by("created_at", direction=firestore.Query.DESCENDING)
        docs = vendors_ref.stream()
        
        data = []
        for doc in docs:
            vendor = doc.to_dict()
            vendor["id"] = doc.id
            if not wilaya_filter or wilaya_filter == "كل الولايات" or vendor.get("wilaya") == wilaya_filter:
                data.append(vendor)
        return pd.DataFrame(data)
    except Exception as e:
        return pd.DataFrame()

def save_vendor(name, phone, wilaya, categories):
    """حفظ بائع جديد"""
    try:
        # التحقق من عدم التكرار
        existing = db.collection("vendors").where("phone", "==", phone).limit(1).get()
        if len(existing) > 0:
            return False
        
        db.collection("vendors").add({
            "created_at": firestore.SERVER_TIMESTAMP,
            "name": name,
            "phone": phone,
            "wilaya": wilaya,
            "category": ", ".join(categories),
            "verified": False
        })
        return True
    except Exception as e:
        return False

# ==========================================
# 5. واجهة المستخدم
# ==========================================
st.markdown("""
<style>
/* نفس التصميم السابق مع ألوان Firebase */
.stApp { background: #0a0a1a; color: white; }
.logo { font-size: 3rem; text-align: center; color: #ffa611; padding: 20px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="logo">🔥 RASSIM OS FIREBASE</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🔍 رادار", "👥 البائعين", "📝 تسجيل", "🔐 المشرف"])

with tab1:
    st.subheader("🎯 أطلق رادارك")
    col1, col2 = st.columns(2)
    with col1:
        item = st.text_area("ماذا تبحث؟")
        cat = st.selectbox("الفئة", CATEGORIES)
    with col2:
        phone = st.text_input("رقم هاتفك")
        wilaya = st.selectbox("الولاية", ["كل الولايات"] + WILAYAS)
    
    if st.button("🚀 إطلاق الرادار") and item and phone:
        with st.spinner("جاري البحث..."):
            time.sleep(1)
        if save_request(item, cat, phone, wilaya):
            st.success("تم الإطلاق!")
            st.balloons()
        else:
            st.error("فشل الحفظ")
    
    st.subheader("📋 الطلبات الحالية")
    df_req = get_requests()
    if not df_req.empty:
        for _, row in df_req.head(10).iterrows():
            st.info(f"🔍 {row['item'][:50]} - {row['wilaya']}")

with tab2:
    st.subheader("👥 البائعون المسجلون")
    df_vend = get_vendors()
    if not df_vend.empty:
        for _, row in df_vend.iterrows():
            st.success(f"🏪 {row['name']} - {row['wilaya']}")

with tab3:
    st.subheader("📝 تسجيل كبائع")
    with st.form("vendor_form"):
        name = st.text_input("الاسم")
        phone = st.text_input("رقم الهاتف")
        wilaya = st.selectbox("الولاية", WILAYAS)
        cats = st.multiselect("التخصص", CATEGORIES)
        if st.form_submit_button("تسجيل"):
            if save_vendor(name, phone, wilaya, cats):
                st.success("تم التسجيل!")
            else:
                st.error("الرقم مسجل مسبقاً")

with tab4:
    st.subheader("🔐 المشرف")
    pw = st.text_input("كلمة المرور", type="password")
    if pw == "rassim2026":
        st.dataframe(get_requests())
        st.dataframe(get_vendors())
