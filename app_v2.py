import streamlit as st
import pandas as pd
import time
import urllib.parse
import os

# 1. إعدادات المنصة
st.set_page_config(page_title="Rassim Phone DZ", layout="wide")

# --- دالة مستشار الأسعار ---
def price_advisor(model_name, user_price):
    market_prices = {"iphone 13": 95000, "iphone 12": 75000, "samsung s21": 65000, "redmi note 12": 32000}
    model_key = model_name.lower()
    for key, avg_price in market_prices.items():
        if key in model_key:
            if user_price < avg_price * 0.9: return f"🔥 صفقة رائعة! أقل من السوق ({avg_price:,} دج)."
            elif user_price > avg_price * 1.1: return f"⚠️ السعر مرتفع عن المتوسط ({avg_price:,} دج)."
            else: return "✅ سعرك مناسب للموق."
    return "📊 لم نجد بيانات كافية لهذا الموديل."

# --- التنسيق الجمالي ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .search-card { background: white; padding: 20px; border-radius: 15px; border-right: 5px solid #1e3799; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .wa-btn { background-color: #25D366; color: white; padding: 8px 15px; border-radius: 8px; text-decoration: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1e3799;'>RASSIM DE RECHERCHE DZ 🚀</h1>", unsafe_allow_html=True)

# 2. نظام التبويبات
tab1, tab2 = st.tabs(["🔍 ابحث عن هاتف", "➕ أضف عرضك"])

with tab1:
    query = st.text_input("🔍 ابحث عن هاتف أو قطعة غيار:", placeholder="مثال: Oppo")
    if query:
        if os.path.exists('users_database.csv'):
            df = pd.read_csv('users_database.csv')
            # البحث في قاعدة البيانات الحقيقية
            results = df[df['Product'].str.contains(query, case=False, na=False)]
            
            if not results.empty:
                for index, row in results.iterrows():
                    msg = urllib.parse.quote(f"سلام، شفت إعلانك {row['Product']} في تطبيق رسيم فون.. هل مازال متوفر؟")
                    wa_url = f"https://wa.me/213{str(row['Phone'])[1:]}?text={msg}"
                    st.markdown(f"""
                        <div class="search-card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <h4 style="margin:0;">{row['Product']}</h4>
                                    <p style="margin:5px 0; color:#27ae60; font-weight:bold;">{row['Price']:,} DA</p>
                                    <p style="margin:0; color:#666; font-size:0.9em;">📍 {row['City']} | 📱 {row['Phone']}</p>
                                </div>
                                <a href="{wa_url}" target="_blank" class="wa-btn">💬 تواصل واتساب</a>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("لم نجد نتائج لهذا البحث حالياً.")

with tab2:
    st.header("📢 أنشر إعلانك مجاناً")
    with st.form("add_offer_form"):
        p_name = st.text_input("اسم الهاتف / الموديل")
        p_price = st.number_input("السعر (دج)", min_value=0, step=500)
        p_phone = st.text_input("رقم الهاتف (مثال: 0550112233)")
        p_city = st.selectbox("البلدية", ["فوكة", "القليعة", "تيبازة", "بوسماعيل", "حجوط"])
        p_desc = st.text_area("وصف الحالة (مثال: شاشة مكسورة، كابا...)")
        submitted = st.form_submit_button("تحليل السعر ونشر العرض")

    if submitted:
        if p_name and p_price > 0 and len(p_phone) >= 10:
            advice = price_advisor(p_name, p_price)
            st.info(f"💡 مستشار رسيم: {advice}")
            
            # حفظ البيانات مع رقم الهاتف
            new_entry = pd.DataFrame([[p_name, p_price, p_phone, p_city, p_desc]], 
                                    columns=['Product', 'Price', 'Phone', 'City', 'Description'])
            new_entry.to_csv('users_database.csv', mode='a', header=False, index=False)
            st.success(f"✅ تم نشر عرض {p_name} برقمك {p_phone}")
        else:
            st.error("❌ تأكد من إدخال الاسم، السعر، ورقم هاتف صحيح.")
