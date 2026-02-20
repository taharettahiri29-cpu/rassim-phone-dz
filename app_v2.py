import streamlit as st
import pandas as pd
import urllib.parse
import os

# 1. إعدادات الهوية البصرية لـ RASSIM DZ
st.set_page_config(page_title="Rassim DZ | المحرك الذكي", layout="wide", page_icon="🔍")

# 2. تصميم الواجهة (CSS Custom Design)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; }
    
    .logo-container {
        text-align: center; background: #0f172a; padding: 40px;
        border-radius: 0 0 50px 50px; margin-top: -60px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3); color: white;
    }
    .main-title { color: #feca57; font-size: 3em; font-weight: 800; margin-bottom: 5px; }
    .sub-title { font-size: 1.2em; opacity: 0.9; letter-spacing: 1px; }
    
    .search-card {
        background: white; padding: 25px; border-radius: 20px;
        border-right: 10px solid #1e3799; margin-bottom: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08); transition: 0.3s;
    }
    .search-card:hover { transform: scale(1.01); }
    
    .price-tag { color: #27ae60; font-size: 1.5em; font-weight: bold; }
    .wa-btn {
        background-color: #25D366; color: white !important;
        padding: 12px 25px; border-radius: 15px;
        text-decoration: none; font-weight: bold; display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. واجهة الهيدر (Logo Section)
st.markdown("""
    <div class="logo-container">
        <div class="main-title">RASSIM DZ</div>
        <div class="sub-title">Moteur de recherche intelligent pour téléphones</div>
    </div>
    """, unsafe_allow_html=True)

# 4. محرك البحث والمنطق البرمجي
st.write("##")
tab1, tab2 = st.tabs(["🔍 محرك البحث الذكي", "📢 أنشر عرضك الآن"])

with tab1:
    # شريط البحث والفلترة حسب الموقع
    c1, c2 = st.columns([3, 1])
    with c1:
        query = st.text_input("", placeholder="🔍 ابحث عن هاتف، شاشة، أو قطعة غيار...")
    with c2:
        location = st.selectbox("📍 تصفية حسب المنطقة", ["كل البلديات", "فوكة", "تيبازة", "بوسماعيل", "القليعة", "حجوط"])

    if os.path.exists('users_database.csv'):
        df = pd.read_csv('users_database.csv')
        
        # تنفيذ الفلترة
        results = df.copy()
        if query:
            results = results[results['Product'].str.contains(query, case=False, na=False)]
        if location != "كل البلديات":
            results = results[results['City'] == location]

        # عرض النتائج
        if not results.empty:
            for _, row in results.iterrows():
                msg = urllib.parse.quote(f"سلام، شفت إعلانك {row['Product']} في RASSIM DZ.. هل متاح؟")
                wa_url = f"https://wa.me/213{str(row['Phone'])[1:]}?text={msg}"
                st.markdown(f"""
                    <div class="search-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h2 style="margin:0; color:#2c3e50;">{row['Product']}</h2>
                                <p class="price-tag">{row['Price']:,} دج</p>
                                <p style="color:#7f8c8d;">📍 {row['City']} | 👤 بائع محلي</p>
                                <p style="font-size:0.9em;">{row['Description']}</p>
                            </div>
                            <a href="{wa_url}" target="_blank" class="wa-btn">💬 تواصل واتساب</a>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("لا توجد نتائج مطابقة لبحثك حالياً.")
    else:
        st.warning("قاعدة البيانات قيد الإنشاء. كن أول من يضيف عرضاً!")

with tab2:
    st.markdown("### 📢 إضافة عرض جديد للمحرك")
    with st.form("pro_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            p_name = st.text_input("اسم المنتج")
            p_price = st.number_input("السعر (دج)", min_value=0)
        with col2:
            p_phone = st.text_input("رقم الواتساب (05/06/07)")
            p_city = st.selectbox("البلدية", ["فوكة", "تيبازة", "بوسماعيل", "القليعة", "حجوط"])
        
        p_desc = st.text_area("وصف الحالة")
        submitted = st.form_submit_button("🚀 نشر في RASSIM DZ")

    if submitted:
        if p_name and p_price and len(p_phone) >= 10:
            new_data = pd.DataFrame([[p_name, p_price, p_phone, p_city, p_desc]], 
                                    columns=['Product', 'Price', 'Phone', 'City', 'Description'])
            new_data.to_csv('users_database.csv', mode='a', header=False, index=False)
            st.success("✅ تم النشر بنجاح! عرضك الآن متاح للجميع.")
        else:
            st.error("يرجى التأكد من ملء جميع الخانات (الاسم، السعر، الهاتف).")

st.markdown("---")
st.markdown("<p style='text-align:center; color:grey;'>© 2026 Rassim DZ - Fouka, Tipaza</p>", unsafe_allow_html=True)

