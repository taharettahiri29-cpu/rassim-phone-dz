import streamlit as st
import pandas as pd
import os

# إعدادات الموقع
st.set_page_config(page_title="RASSIM DZ", layout="wide")

# تصميم الهيدر (Header)
st.markdown("""
    <div style="text-align:center; background:#1e3799; padding:30px; border-radius:15px; color:white;">
        <h1>🔍 RASSIM DZ</h1>
        <p>Moteur de recherche intelligent pour téléphones - Tipaza</p>
    </div>
""", unsafe_allow_html=True)

# التبويبات
tab1, tab2 = st.tabs(["🔍 البحث عن همزة", "📢 أنشر عرضك"])

with tab1:
    st.subheader("ابحث عن هاتفك المفضل")
    # منطق البحث يوضع هنا

with tab2:
    st.subheader("أضف عرضك مجاناً")
    with st.form("add_form"):
        name = st.text_input("اسم الهاتف")
        price = st.number_input("السعر (دج)")
        city = st.selectbox("البلدية", ["فوكة", "تيبازة", "بوسماعيل", "القليعة"])
        if st.form_submit_button("نشر الآن"):
            st.success("تم النشر!")
