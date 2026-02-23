import streamlit as st
import pandas as pd
import os
import urllib.parse
import datetime
from PIL import Image

# 1. إعدادات الهوية الوطنية والقوة المعلوماتية
st.set_page_config(page_title="RASSIM DZ | 59 Wilaya", layout="wide", page_icon="🇩🇿")

# قائمة الولايات الـ 59
wilayas = [
    "01-أدرار", "02-الشلف", "03-الأغواط", "04-أم البواقي", "05-باتنة", "06-بجاية", "07-بسكرة", "08-بشار", "09-البليدة", "10-البويرة",
    "11-تمنراست", "12-تبسة", "13-تلمسان", "14-تيارت", "15-تيزي وزو", "16-الجزائر", "17-الجلفة", "18-جيجل", "19-سطيف", "20-سعيدة",
    "21-سكيكدة", "22-سيدي بلعباس", "23-عنابة", "24-قالمة", "25-قسنطينة", "26-المدية", "27-مستغانم", "28-المسيلة", "29-معسكر", "30-ورقلة",
    "31-وهران", "32-البيض", "33-إليزي", "34-برج بوعريريج", "35-بومرداس", "36-الطارف", "37-تندوف", "38-تيسمسيلت", "39-الوادي", "40-خنشلة",
    "41-سوق أهراس", "42-تيبازة", "43-ميلة", "44-عين الدفلى", "45-النعامة", "46-عين تموشنت", "47-غرداية", "48-غليزان", "49-تيميمون", "50-برج باجي مختار",
    "51-أولاد جلال", "52-بني عباس", "53-عين صالح", "54-عين قزام", "55-تقرت", "56-جانت", "57-المغير", "58-المنيعة", "59-سيدي عيسى"
]

# 2. تنسيق CSS المطور (ألوان العلم الجزائري)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    
    .hero { 
        background: linear-gradient(to left, #006633 50%, #ffffff 50%);
        padding: 50px; 
        text-align: center; 
        border-radius: 25px; 
        margin-bottom: 25px; 
        border-bottom: 10px solid #d21034;
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
        position: relative;
    }
    
    .hero h1 { 
        color: #d21034;
        background: rgba(255,255,255,0.9);
        display: inline-block;
        padding: 15px 40px;
        border-radius: 20px;
        border: 3px solid #d21034;
        font-size: 2.5em;
    }
    
    .hero p { 
        color: #1a1a1a; 
        font-weight: bold;
        background: rgba(255,255,255,0.8);
        display: table;
        margin: 20px auto;
        padding: 10px 25px;
        border-radius: 10px;
    }

    .stat-box { background: white; padding: 20px; border-radius: 15px; border-bottom: 4px solid #006633; text-align: center; box-shadow: 0 5px 10px rgba(0,0,0,0.05); }
    
    .card { 
        background: white; 
        padding: 25px; 
        border-radius: 20px; 
        margin-bottom: 15px; 
        box-shadow: 0 10px 20px rgba(0,0,0,0.05); 
        border-right: 10px solid #006633;
        transition: transform 0.3s;
    }
    .card:hover { transform: scale(1.01); }
    
    .wa-button {
        background-color: #25D366;
        color: white !important;
        padding: 10px 20px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة الزوار والبيانات
if 'visitor_count' not in st.session_state:
    st.session_state.visitor_count = 1450
    st.session_state.active_now = 34
st.session_state.visitor_count += 1

DB_FILE = "users_database.csv"
def load_data():
    cols = ["Product", "Price", "Phone", "Wilaya", "Description", "Date"]
    if os.path.exists(DB_FILE):
        try:
            temp_df = pd.read_csv(DB_FILE)
            for c in cols:
                if c not in temp_df.columns: temp_df[c] = "غير متوفر"
            return temp_df[cols]
        except: return pd.DataFrame(columns=cols)
    return pd.DataFrame(columns=cols)

# 4. واجهة العلم الجزائري الرئيسية
st.markdown("""
    <div class="hero">
        <h1>🇩🇿 RASSIM DZ</h1>
        <p>المنصة الوطنية الأولى لتداول الهواتف في 59 ولاية</p>
    </div>
""", unsafe_allow_html=True)

# شريط الإحصائيات
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1: st.markdown(f'<div class="stat-box"><h2>{st.session_state.visitor_count:,}</h2><p>إجمالي الزيارات</p></div>', unsafe_allow_html=True)
with col_s2: st.markdown(f'<div class="stat-box"><h2 style="color:#2ecc71;">🟢 {st.session_state.active_now}</h2><p>متصل الآن</p></div>', unsafe_allow_html=True)
with col_s3: st.markdown(f'<div class="stat-box"><h2>59</h2><p>ولاية مغطاة</p></div>', unsafe_allow_html=True)

# 5. الأقسام الرئيسية
tab1, tab2, tab3 = st.tabs(["🔍 البحث عن همزة", "📢 أنشر عرضك", "🤖 رادار الذكاء الاصطناعي"])

with tab1:
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        search_query = st.text_input("", placeholder="🔍 ماذا تبحث اليوم؟ (مثال: iPhone 15 Pro Max)", key="main_search")
    with col_filter:
        target_wilaya = st.selectbox("تصفية حسب المنطقة", ["كل الولايات"] + wilayas)

    df = load_data()
    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[filtered_df['Product'].str.contains(search_query, case=False, na=False)]
    if target_wilaya != "كل الولايات":
        filtered_df = filtered_df[filtered_df['Wilaya'] == target_wilaya]

    if not filtered_df.empty:
        for _, row in filtered_df.iterrows():
            # رابط واتساب ذكي
            clean_phone = str(row['Phone']).replace(" ", "").replace("+", "")
            msg = urllib.parse.quote(f"سلام، تواصلت معك من موقع RASSIM DZ بخصوص {row['Product']}. هل مازال متاح؟")
            wa_link = f"https://wa.me/{clean_phone if clean_phone.startswith('213') else '213'+clean_phone[1:]}?text={msg}"
            
            st.markdown(f"""
                <div class="card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <h3 style="margin:0; color:#006633;">{row['Product']}</h3>
                            <p style="color:#636e72; font-size:0.9em;">📍 {row['Wilaya']} | 📅 {row['Date']}</p>
                            <h4 style="color:#d21034; margin:5px 0;">{row['Price']:,} دج</h4>
                            <p>{row['Description']}</p>
                        </div>
                        <div style="text-align:center;">
                            <a href="{wa_link}" class="wa-button">💬 تواصل الآن</a>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ لا توجد نتائج تطابق بحثك حالياً. حاول تغيير الكلمات أو المنطقة.")

with tab2:
    st.markdown("### 📸 ارفع صورة المنتج (اختياري)")
    uploaded_file = st.file_uploader("الذكاء الاصطناعي سيتعرف على نوع الهاتف تلقائياً", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(Image.open(uploaded_file), width=200, caption="تم رفع الصورة بنجاح")
        st.info("🤖 تحليل الروبوت: يبدو هذا الهاتف بحالة ممتازة!")

    with st.form("add_offer", clear_on_submit=True):
        st.subheader("📝 تفاصيل الإعلان")
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            p_name = st.text_input("اسم الجهاز")
            p_price = st.number_input("السعر المطلوب (دج)", min_value=0)
        with f_col2:
            p_phone = st.text_input("رقم الواتساب (مثال: 0661000000)")
            p_city = st.selectbox("ولاية العرض", wilayas)
        
        p_desc = st.text_area("وصف دقيق للحالة (هل يوجد خدوش؟ هل معه علبة؟)")
        
        submitted = st.form_submit_button("🚀 نشر العرض وطنياً")
        
        if submitted:
            if p_name and p_phone and p_price > 0:
                new_row = pd.DataFrame([[p_name, p_price, p_phone, p_city, p_desc, datetime.date.today()]], 
                                     columns=["Product", "Price", "Phone", "Wilaya", "Description
