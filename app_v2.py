import streamlit as st
import pandas as pd
import urllib.parse
import os

# 1. Configuration RASSIM DZ
st.set_page_config(page_title="Rassim DZ", layout="wide")

# 2. Interface (UI)
st.markdown("""
    <style>
    .header { background:#0f172a; padding:30px; border-radius:20px; text-align:center; color:white; }
    .card { background:white; padding:20px; border-radius:15px; border-right:8px solid #1e3799; margin:10px 0; box-shadow:0 4px 10px rgba(0,0,0,0.1); }
    .wa-btn { background:#25D366; color:white !important; padding:8px 15px; border-radius:10px; text-decoration:none; font-weight:bold; }
    </style>
    <div class="header">
        <h1>RASSIM DZ</h1>
        <p>Moteur de recherche intelligent pour téléphones</p>
    </div>
    """, unsafe_allow_html=True)

# 3. Logic
tab1, tab2 = st.tabs(["🔍 البحث (Acheter)", "📢 النشر (Vendre)"])

with tab1:
    q = st.text_input("ابحث عن هاتف أو قطعة غيار...")
    city = st.selectbox("المنطقة", ["كل المناطق", "فوكة", "تيبازة", "بوسماعيل", "القليعة"])
    
    if os.path.exists('users_database.csv'):
        df = pd.read_csv('users_database.csv')
        # عرض النتائج هنا
        st.write("النتائج تظهر هنا...")
    else:
        st.info("قاعدة البيانات فارغة.")

with tab2:
    with st.form("add"):
        name = st.text_input("المنتج")
        price = st.number_input("السعر (دج)")
        tel = st.text_input("رقم الواتساب")
        loc = st.selectbox("البلدية", ["فوكة", "تيبازة", "بوسماعيل", "القليعة"])
        if st.form_submit_button("نشر الآن"):
            new_data = pd.DataFrame([[name, price, tel, loc]], columns=['Product', 'Price', 'Phone', 'City'])
            new_data.to_csv('users_database.csv', mode='a', header=not os.path.exists('users_database.csv'), index=False)
            st.success("تم النشر!")
