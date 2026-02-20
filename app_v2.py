import streamlit as st
import pandas as pd
import time
import urllib.parse

# 1. إعدادات المنصة
st.set_page_config(page_title="Rassim de Recherche DZ", layout="wide")

# --- دالة مستشار الأسعار الذكي ---
def price_advisor(model_name, user_price):
    market_prices = {
        "iphone 13": 95000,
        "iphone 12": 75000,
        "samsung s21": 65000,
        "redmi note 12": 32000
    }
    model_key = model_name.lower()
    for key in market_prices:
        if key in model_key:
            avg_price = market_prices[key]
            if user_price < avg_price * 0.9:
                return f"🔥 صفقة رائعة! سعرك أقل من متوسط السوق ({avg_price:,} دج)، ستبيع بسرعة."
            elif user_price > avg_price * 1.1:
                return f"⚠️ تنبيه: متوسط السعر هو {avg_price:,} دج. سعرك مرتفع قليلاً."
            else:
                return "✅ سعرك مناسب ومتوافق مع السوق."
    return "📊 لم نجد بيانات كافية، قارن سعرك مع 'همزات اليوم'."

# --- التنسيق الجمالي ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .search-card { background: white; padding: 20px; border-radius: 15px; border-right: 5px solid #1e3799; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .wa-btn { background-color: #25D366; color: white; padding: 8px 15px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1e3799;'>RASSIM DE RECHERCHE DZ 🚀</h1>", unsafe_allow_html=True)

# 2. نظام التبويبات لتنظيم الواجهة
tab1, tab2 = st.tabs(["🔍 ابحث عن هاتف", "➕ أضف عرضك"])

with tab1:
    query = st.text_input("🔍 ابحث عن هاتف أو قطعة غيار:", placeholder="مثال: Samsung S21")
    if query:
        st.info(f"📍 يتم الآن جلب أفضل العروض لـ '{query}'...")
        # هنا يمكن إضافة كود جلب البيانات من CSV لاحقاً

with tab2:
    st.header("📢 أنشر إعلانك مجاناً")
    # استخدام Form لضمان عدم حدوث NameError
    with st.form("add_offer_form"):
        p_name = st.text_input("اسم الهاتف / الموديل")
        p_price = st.number_input("السعر (دج)", min_value=0, step=500)
        p_city = st.selectbox("البلدية", ["فوكة", "القليعة", "تيبازة", "بوسماعيل", "الجزائر"])
        p_desc = st.text_area("وصف قصير")
        
        submitted = st.form_submit_button("تحليل السعر ونشر العرض")

    if submitted:
        if p_name and p_price > 0:
            # تشغيل مستشار الأسعار
            advice = price_advisor(p_name, p_price)
            st.info(f"💡 مستشار رسيم يقول: {advice}")
            
            # حفظ في قاعدة البيانات (CSV)
            try:
                new_entry = pd.DataFrame([[p_name, p_price, p_city, p_desc]], 
                                        columns=['Product', 'Price', 'City', 'Description'])
                new_entry.to_csv('users_database.csv', mode='a', header=False, index=False)
                st.success(f"✅ تم نشر عرضك لـ {p_name} بنجاح!")
            except:
                st.warning("⚠️ تم عرض النصيحة، لكن هناك مشكلة في ملف قاعدة البيانات.")
        else:
            st.error("❌ يرجى ملء اسم الهاتف والسعر أولاً.")

# 3. قسم الهمزات (دائم الظهور)
st.write("---")
st.markdown("### 🔥 همزات اليوم (تخفيضات حقيقية)")
deals = [
    {"item": "iPhone 12 Pro", "old": "85,000", "new": "78,000", "loc": "فوكة"},
    {"item": "Ecran S21 Ultra", "old": "42,000", "new": "35,000", "loc": "تيبازة"}
]
cols = st.columns(len(deals))
for i, d in enumerate(deals):
    with cols[i]:
        st.markdown(f"""
            <div style="background: white; padding: 15px; border-radius: 12px; border: 1px solid #ff7675; text-align: center;">
                <h5 style="margin: 0;">{d['item']}</h5>
                <p style="color: #d63031; font-weight: bold; font-size: 1.1em; margin: 5px 0;">{d['new']} DA</p>
                <p style="color: #636e72; font-size: 0.8em;">📍 {d['loc']}</p>
            </div>
        """, unsafe_allow_html=True)
