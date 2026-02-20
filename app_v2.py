import streamlit as st
import pandas as pd
import time
import urllib.parse
import os

# --- 1. إعدادات الهوية البصرية ---
st.set_page_config(page_title="Rassim de Recherche DZ", layout="wide", page_icon="🔍")

# --- 2. لغة التصميم المتطورة (Modern UI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; }
    
    .main-header {
        background: linear-gradient(135deg, #1e3799 0%, #0984e3 100%);
        padding: 40px;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .logo-text { font-size: 3.5em; font-weight: 800; letter-spacing: -1px; margin: 0; }
    .logo-sub { font-size: 1.2em; opacity: 0.9; }
    
    .search-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-right: 8px solid #25D366;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    .wa-btn {
        background-color: #25D366;
        color: white !important;
        padding: 10px 20px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. الهيدر مع اللوجو النصي الاحترافي ---
st.markdown("""
    <div class="main-header">
        <div class="logo-text">RASSIM <span style='color:#feca57'>DZ</span></div>
        <div class="logo-sub">Rassim de Recherche : Votre moteur de recherche intelligent</div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. جلب البيانات ---
def load_data():
    if os.path.exists('users_database.csv'):
        return pd.read_csv('users_database.csv')
    return pd.DataFrame(columns=['Product', 'Price', 'Phone', 'City', 'Description'])

# --- 5. التبويبات الرئيسية ---
tab1, tab2 = st.tabs(["🔍 ابحث عن همزة", "➕ أنشر عرضك"])

with tab1:
    # الفلترة الذكية
    col_a, col_b = st.columns([2, 1])
    with col_a:
        search_query = st.text_input("", placeholder="🔍 ابحث عن (iPhone, شاشة، Samsung...)", key="main_search")
    with col_b:
        city_filter = st.selectbox("📍 تصفية حسب الموقع", ["كل البلديات", "فوكة", "تيبازة", "القليعة", "بوسماعيل", "حجوط"])

    df = load_data()
    
    # تطبيق الفلاتر
    if not df.empty:
        filtered_df = df.copy()
        if search_query:
            filtered_df = filtered_df[filtered_df['Product'].str.contains(search_query, case=False, na=False)]
        if city_filter != "كل البلديات":
            filtered_df = filtered_df[filtered_df['City'] == city_filter]

        if not filtered_df.empty:
            st.write(f"### تم العثور على {len(filtered_df)} عرض:")
            for _, row in filtered_df.iterrows():
                msg = urllib.parse.quote(f"سلام، شفت إعلانك لـ {row['Product']} في Rassim DZ.. هل متوفر؟")
                wa_url = f"https://wa.me/213{str(row['Phone'])[1:]}?text={msg}"
                st.markdown(f"""
                    <div class="search-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h3 style="margin:0;">{row['Product']}</h3>
                                <p style="color:#27ae60; font-size:1.3em; font-weight:bold; margin:5px 0;">{row['Price']:,} دج</p>
                                <p style="color:#636e72; margin:0;">📍 {row['City']} | 📱 {row['Phone']}</p>
                            </div>
                            <a href="{wa_url}" target="_blank" class="wa-btn">💬 واتساب</a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("لم نجد نتائج تطابق بحثك في هذه المنطقة.")

with tab2:
    st.markdown("### 📢 أضف عرضك مجاناً")
    with st.form("add_form", clear_on_submit=True):
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            name = st.text_input("اسم الهاتف / القطعة")
            price = st.number_input("السعر (دج)", min_value=0)
        with f_col2:
            phone = st.text_input("رقم الهاتف (واتساب)")
            city = st.selectbox("البلدية", ["فوكة", "تيبازة", "القليعة", "بوسماعيل", "حجوط"])
        
        desc = st.text_area("وصف إضافي")
        submit = st.form_submit_button("نشر العرض الآن")

    if submit:
        if name and price and len(phone) >= 10:
            new_row = pd.DataFrame([[name, price, phone, city, desc]], 
                                  columns=['Product', 'Price', 'Phone', 'City', 'Description'])
            new_row.to_csv('users_database.csv', mode='a', header=False, index=False)
            st.success("✅ تم النشر بنجاح! سيظهر عرضك الآن في نتائج البحث.")
        else:
            st.error("يرجى ملء البيانات بشكل صحيح.")

# الفوتر
st.markdown("<p style='text-align:center; color:#95a5a6; margin-top:50px;'>Rassim de Recherche DZ - Fouka 2026</p>", unsafe_allow_html=True)
