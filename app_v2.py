import streamlit as st
import pandas as pd
import time
import urllib.parse
import os

# 1. إعدادات الهوية البصرية
st.set_page_config(page_title="Rassim de Recherche DZ", layout="wide", page_icon="🔍")

# --- التصميم ---
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1e3799 0%, #0984e3 100%);
        padding: 40px; border-radius: 25px; color: white; text-align: center;
    }
    .wa-btn { background-color: #25D366; color: white !important; padding: 10px; border-radius: 10px; text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>RASSIM DZ</h1><p>Moteur de recherche intelligent</p></div>', unsafe_allow_html=True)

# 2. التبويبات
tab1, tab2 = st.tabs(["🔍 البحث عن همزة", "➕ أنشر عرضك"])

with tab1:
    search = st.text_input("ماذا تبحث؟")
    # هنا كود البحث (الذي بنيناه)

with tab2:
    with st.form("add_form"):
        name = st.text_input("اسم الهاتف")
        price = st.number_input("السعر")
        phone = st.text_input("رقم الهاتف")
        city = st.selectbox("البلدية", ["فوكة", "تيبازة", "القليعة"])
        submit = st.form_submit_button("نشر العرض")
        if submit and name and phone:
            # كود حفظ البيانات في CSV
            st.success("تم النشر!")
