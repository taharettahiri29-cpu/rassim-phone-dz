import streamlit as st
import pandas as pd
import time
import urllib.parse
import os

# --- 1. إعدادات الهوية العالمية لعام 2026 ---
st.set_page_config(
    page_title="Rassim de Recherche DZ",
    layout="wide",
    page_icon="🔍",
    initial_sidebar_state="collapsed"
)

# --- 2. دالة مستشار الأسعار الذكي (الذكاء الاصطناعي للمنصة) ---
def price_advisor(model_name, user_price):
    market_prices = {
        "iphone 13": 95000, "iphone 12": 75000, 
        "samsung s21": 65000, "redmi note 12": 32000,
        "oppo a54": 38000
    }
    model_key = model_name.lower()
    for key, avg_price in market_prices.items():
        if key in model_key:
            if user_price < avg_price * 0.9:
                return f"🔥 صفقة ذهبية! سعرك (دج {user_price:,}) مغري جداً مقارنة بسعر السوق ({avg_price:,} دج)."
            elif user_price > avg_price * 1.1:
                return f"⚠️ تنبيه: متوسط السعر هو {avg_price:,} دج. قد تجد صعوبة في البيع بهذا السعر."
            else:
                return "✅ سعر احترافي! أنت في النطاق الصحيح للسوق الجزائري."
    return "📊 لم نجد بيانات تاريخية دقيقة لهذا الموديل، ننصحك بمتابعة 'همزات اليوم'."

# --- 3. لغة التصميم المتطورة CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; }
    
    .header-container {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #1e3799 0%, #0984e3 100%);
        border-radius: 0 0 50px 50px;
        color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .search-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        border-right: 8px solid #341f97;
        margin-bottom: 15px;
        transition: transform 0.3s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .search-card:hover { transform: translateY(-5px); }
    
    .wa-btn {
        background-color: #25D366;
        color: white !important;
        padding: 10px 20px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
    }
    
    .stButton>button {
        border-radius: 20px;
        border: none;
        background-color: #341f97;
        color: white;
        transition: 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. واجهة الهيدر ---
st.markdown("""
    <div class="header-container">
        <h1 style="font-size: 3.5em; margin: 0;">Rassim de Recherche DZ</h1>
        <p style="font-size: 1.2em; opacity: 0.9;">المحرك الأول في الجزائر للبحث عن الهواتف وقطع الغيار</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. نظام التبويبات الذكي ---
st.write("##")
tab1, tab2, tab3 = st.tabs(["🔍 محرك البحث الفوري", "📢 أنشر عرضك (بائع)", "🔥 همزات اليوم"])

# --- التبويب الأول: البحث ---
with tab1:
    col_s1, col_s2, col_s3 = st.columns([1, 4, 1])
    with col_s2:
        query = st.text_input("", placeholder="🔍 ماذا تريد أن تجد اليوم؟ (مثال: iPhone 13, شاشة Oppo...)", key="search_bar")
        
    if query:
        if os.path.exists('users_database.csv'):
            df = pd.read_csv('users_database.csv')
            results = df[df['Product'].str.contains(query, case=False, na=False)]
            
            if not results.empty:
                st.subheader(f"📍 نتائج البحث لـ '{query}':")
                for _, row in results.iterrows():
                    msg = urllib.parse.quote(f"سلام، شفت إعلانك لـ {row['Product']} في Rassim de Recherche DZ.. هل متوفر؟")
                    wa_url = f"https://wa.me/213{str(row['Phone'])[1:]}?text={msg}"
                    st.markdown(f"""
                        <div class="search-card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <h3 style="margin:0; color:#2c3e50;">{row['Product']}</h3>
                                    <p style="margin:5px 0; color:#27ae60; font-size:1.4em; font-weight:bold;">{row['Price']:,} دج</p>
                                    <p style="margin:0; color:#636e72;">📍 {row['City']} | 👤 بائع موثوق</p>
                                    <p style="font-size:0.9em; color:#2980b9;">📝 {row['Description']}</p>
                                </div>
                                <a href="{wa_url}" target="_blank" class="wa-btn">💬 تواصل واتساب</a>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("لم نجد نتائج مطابقة، جرب كلمات أخرى.")
        else:
            st.info("قاعدة البيانات فارغة حالياً، كن أول من ينشر عرضاً!")

# --- التبويب الثاني: إضافة عرض ---
with tab2:
    st.markdown("### 📤 سجل سلعتك في المحرك الوطني")
    with st.form("pro_add_form", clear_on_submit=True):
        c_a, c_b = st.columns(2)
        with c_a:
            p_name = st.text_input("اسم الهاتف أو القطعة")
            p_price = st.number_input("السعر المقترح (دج)", min_value=0, step=1000)
        with c_b:
            p_phone = st.text_input("رقم الواتساب (مثال: 0550112233)")
            p_city = st.selectbox("البلدية / الولاية", ["فوكة", "تيبازة", "القليعة", "حجوط", "بوسماعيل", "الجزائر العاصمة"])
        
        p_desc = st.text_area("وصف دقيق للحالة (مثلاً: كابا، شاشة أصلية، بدون ملحقات)")
        submitted = st.form_submit_button("🚀 تحليل السعر ونشر العرض")

    if submitted:
        if p_name and p_price > 0 and len(p_phone) >= 10:
            advice = price_advisor(p_name, p_price)
            st.info(f"💡 نصيحة Rassim Advisor: {advice}")
            
            # الحفظ في الملف
            new_data = pd.DataFrame([[p_name, p_price, p_phone, p_city, p_desc]], 
                                    columns=['Product', 'Price', 'Phone', 'City', 'Description'])
            new_data.to_csv('users_database.csv', mode='a', header=False, index=False)
            st.success(f"✅ مبروك! عرضك لـ {p_name} متاح الآن في Rassim de Recherche DZ")
        else:
            st.error("⚠️ يرجى ملء كافة الخانات بشكل صحيح لضمان النشر.")

# --- التبويب الثالث: الهمزات ---
with tab3:
    st.markdown("### 🔥 أفضل الصفقات المقترحة اليوم")
    # هنا تظهر الهمزات التي تختارها أنت يدوياً لتشجيع المستخدمين
    st.info("هذا القسم مخصص للسلع التي يقل سعرها عن سعر السوق بـ 20% فأكثر.")

# --- الفوتر الاحترافي ---
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #95a5a6;'>© 2026 Rassim de Recherche DZ - Fouka, Tipaza<br>صُمم بكل فخر في الجزائر بمشاركة طاهر ورسيم</p>", unsafe_allow_html=True)
