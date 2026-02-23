import streamlit as st
import pandas as pd
import os
import urllib.parse

# 1. الإعدادات والجمالية (UI/UX)
st.set_page_config(page_title="RASSIM DZ | المحرك الذكي", layout="wide", page_icon="🔍")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .main-header { text-align:center; background: linear-gradient(90deg, #1e3799, #0f172a); padding:40px; border-radius:20px; color:white; margin-bottom:20px; box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
    .card { background: white; padding: 20px; border-radius: 15px; border-right: 10px solid #feca57; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: 0.3s; color: #2d3436; }
    .card:hover { transform: translateY(-5px); }
    .price { color: #27ae60; font-size: 1.4em; font-weight: bold; }
    .wa-link { background-color: #25D366; color: white !important; padding: 10px 20px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 10px; }
    </style>
    <div class="main-header">
        <h1 style="margin:0;">🔍 RASSIM DZ</h1>
        <p style="font-size:1.2em; opacity:0.9;">Moteur de recherche intelligent pour téléphones - Tipaza</p>
    </div>
""", unsafe_allow_html=True)

# 2. إدارة قاعدة البيانات
DB_FILE = "users_database.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["Product", "Price", "Phone", "City", "Description"])

def save_data(df):
    df.to_csv(DB_FILE, index=False)

# 3. المنطق البرمجي (التبويبات)
tab1, tab2 = st.tabs(["🔍 البحث عن الهواتف", "📢 أنشر عرضك مجاناً"])

with tab1:
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("", placeholder="ماذا تبحث اليوم؟ (iPhone, Samsung, شاشة...)", key="search_bar")
    with col2:
        filter_city = st.selectbox("📍 تصفية المنطقة", ["كل تيبازة", "فوكة", "بوسماعيل", "تيبازة", "القليعة", "حجوط"])

    df = load_data()
    
    # الفلترة الذكية
    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[filtered_df['Product'].str.contains(search_query, case=False, na=False)]
    if filter_city != "كل تيبازة":
        filtered_df = filtered_df[filtered_df['City'] == filter_city]

    if not filtered_df.empty:
        for index, row in filtered_df.iterrows():
            # رابط واتساب ذكي
            message = urllib.parse.quote(f"سلام، شفت إعلانك {row['Product']} في RASSIM DZ.. هل ما زال متوفر؟")
            wa_url = f"https://wa.me/213{str(row['Phone'])[1:]}?text={message}"
            
            st.markdown(f"""
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h3 style="margin:0;">{row['Product']}</h3>
                            <p style="margin:5px 0; color:#636e72;">📍 {row['City']} | 📝 {row['Description']}</p>
                            <span class="price">{row['Price']:,} دج</span>
                        </div>
                        <a href="{wa_url}" target="_blank" class="wa-link">💬 اطلب الآن</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("لم نجد نتائج مطابقة لبحثك. جرب كلمة أخرى أو كن أول من ينشر العرض!")

with tab2:
    st.subheader("📢 إضافة عرض جديد للمحرك")
    with st.form("add_offer", clear_on_submit=True):
        p_name = st.text_input("اسم الهاتف أو القطعة")
        p_price = st.number_input("السعر المعروض (دج)", min_value=0)
        p_phone = st.text_input("رقم هاتفك (WhatsApp)")
        p_city = st.selectbox("البلدية", ["فوكة", "بوسماعيل", "تيبازة", "القليعة", "حجوط"])
        p_desc = st.text_area("وصف قصير (مثلاً: الحالة 10/10، شاشة أصلية)")
        
        submitted = st.form_submit_button("🚀 نشر العرض في المحرك")
        
        if submitted:
            if p_name and p_price > 0 and len(p_phone) >= 10:
                new_row = pd.DataFrame([[p_name, p_price, p_phone, p_city, p_desc]], 
                                     columns=["Product", "Price", "Phone", "City", "Description"])
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df)
                st.success("✅ تم نشر عرضك بنجاح! سيظهر الآن في نتائج البحث.")
            else:
                st.error("يرجى ملء جميع الخانات بشكل صحيح.")

st.markdown("---")
st.markdown("<p style='text-align:center; color:#636e72;'>© 2026 Rassim DZ - Fouka, Tipaza. نظام ذكي لتجارة الهواتف.</p>", unsafe_allow_html=True)
