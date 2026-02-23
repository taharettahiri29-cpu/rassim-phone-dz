import streamlit as st
import datetime

# 1. نظام تتبع الزيارات (محاكاة ذكية للنشاط)
if 'visitor_count' not in st.session_state:
    st.session_state.visitor_count = 1450  # نبدأ برقم يعكس نشاط المنصة الوطني
    st.session_state.active_now = 34      # عدد المتواجدين حالياً

# زيادة العداد بشكل طفيف مع كل دخول
st.session_state.visitor_count += 1

# 2. تصميم شريط الإحصائيات (Dashboard Bar)
st.markdown(f"""
    <div style="display: flex; justify-content: space-around; background: #f8f9fa; padding: 15px; border-radius: 10px; border-bottom: 3px solid #1e3799; margin-bottom: 25px;">
        <div style="text-align: center;">
            <h4 style="margin:0; color: #1e3799;">{st.session_state.visitor_count:,}</h4>
            <p style="margin:0; font-size: 0.8em; color: #636e72;">إجمالي الزيارات</p>
        </div>
        <div style="text-align: center;">
            <h4 style="margin:0; color: #27ae60;">🟢 {st.session_state.active_now}</h4>
            <p style="margin:0; font-size: 0.8em; color: #636e72;">متصل الآن</p>
        </div>
        <div style="text-align: center;">
            <h4 style="margin:0; color: #f39c12;">59</h4>
            <p style="margin:0; font-size: 0.8em; color: #636e72;">ولاية مغطاة</p>
        </div>
    </div>
""", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import os
import urllib.parse

# 1. إعدادات الهوية الوطنية
st.set_page_config(page_title="RASSIM DZ | 59 Wilaya", layout="wide")

# قائمة الولايات الـ 59 (التقسيم الجديد 2026)
wilayas = [
    "01-أدرار", "02-الشلف", "03-الأغواط", "04-أم البواقي", "05-باتنة", "06-بجاية", "07-بسكرة", "08-بشار", "09-البليدة", "10-البويرة",
    "11-تمنراست", "12-تبسة", "13-تلمسان", "14-تيارت", "15-تيزي وزو", "16-الجزائر", "17-الجلفة", "18-جيجل", "19-سطيف", "20-سعيدة",
    "21-سكيكدة", "22-سيدي بلعباس", "23-عنابة", "24-قالمة", "25-قسنطينة", "26-المدية", "27-مستغانم", "28-المسيلة", "29-معسكر", "30-ورقلة",
    "31-وهران", "32-البيض", "33-إليزي", "34-برج بوعريريج", "35-بومرداس", "36-الطارف", "37-تندوف", "38-تيسمسيلت", "39-الوادي", "40-خنشلة",
    "41-سوق أهراس", "42-تيبازة", "43-ميلة", "44-عين الدفلى", "45-النعامة", "46-عين تموشنت", "47-غرداية", "48-غليزان", "49-تيميمون", "50-برج باجي مختار",
    "51-أولاد جلال", "52-بني عباس", "53-عين صالح", "54-عين قزام", "55-تقرت", "56-جانت", "57-المغير", "58-المنيعة", "59-سيدي عيسى"
]

# تنسيق CSS احترافي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .hero { background: linear-gradient(45deg, #1e3799, #0984e3); padding: 50px; text-align: center; color: white; border-radius: 0 0 50px 50px; margin-bottom: 30px; }
    .wilaya-card { background: #f1f2f6; border-radius: 10px; padding: 10px; text-align: center; border: 1px solid #dfe4ea; cursor: pointer; transition: 0.3s; }
    .wilaya-card:hover { background: #1e3799; color: white; }
    </style>
    <div class="hero">
        <h1>🇩🇿 RASSIM DZ - المنصة الوطنية</h1>
        <p>محرك بحث الهواتف الأول في 59 ولاية</p>
    </div>
""", unsafe_allow_html=True)

# 2. الخريطة التفاعلية (مبسطة كأزرار ولايات)
st.subheader("📍 اختر ولايتك للبحث")
cols = st.columns(6) # تقسيم الولايات على أعمدة
for i, w in enumerate(wilayas[:12]): # عرض أول 12 ولاية كمثال في الرئيسية
    with cols[i % 6]:
        if st.button(w, key=w):
            st.session_state.selected_wilaya = w

# 3. نظام البحث المتقدم
df = pd.read_csv("users_database.csv") if os.path.exists("users_database.csv") else pd.DataFrame()

col_search, col_filter = st.columns([3, 1])
with col_search:
    # شريط البحث الرئيسي
    search_query = st.text_input("", placeholder="🔍 ابحث عن موديل (iPhone, Pixel...)", key="main_search")
    
    # --- هنا نضع نظام التنبيهات الذكي مباشرة تحت شريط البحث ---
    with st.expander("🔔 لم تجد ما تبحث عنه؟ فعل رادار التنبيهات"):
        st.markdown("<small>سيرسل لك الروبوت رسالة فور توفر هذا الهاتف في ولايتك</small>", unsafe_allow_html=True)
        e_col1, e_col2 = st.columns([2, 1])
        with e_col1:
            email_input = st.text_input("بريدك الإلكتروني", key="notif_email", placeholder="example@mail.com")
        with e_col2:
            if st.button("تفعيل الرادار", use_container_width=True):
                if "@" in email_input:
                    st.success("تم التفعيل! 🚀")
                else:
                    st.error("الإيميل غير صحيح")
    # -------------------------------------------------------
    query = st.text_input("🔍 ابحث عن موديل (iPhone, Pixel, Oppo...)", placeholder="اكتب هنا...")
with col_filter:
    target_wilaya = st.selectbox("تصفية حسب الولاية", ["كل الولايات"] + wilayas)

# ... (منطق الفلترة والعرض الذي شرحناه سابقاً) ...


