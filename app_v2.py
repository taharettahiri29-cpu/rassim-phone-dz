import streamlit as st
import pandas as pd
import time
import urllib.parse

# 1. إعدادات المنصة (السرعة والهوية)
st.set_page_config(page_title="Rassim de Recherche DZ", layout="wide")

# --- دالة التخزين الذكي (هذا ما سيحل مشكلة الثقل) ---
@st.cache_data(ttl=3600) # يخزن النتائج لمدة ساعة كاملة لتسريع البحث
def get_fast_data(query):
    # هنا محاكاة جلب البيانات (ستستبدل لاحقاً بسكرابر حقيقي)
    time.sleep(0.5) # وقت انتظار قصير جداً
    return [
        {"item": f"{query} - حالة جيدة", "price": "45,000 DA", "seller": "0550123456", "loc": "فوكة"},
        {"item": f"{query} - كابا", "price": "72,000 DA", "seller": "0660987654", "loc": "القليعة"},
        {"item": f"{query} - خردة", "price": "10,000 DA", "seller": "0770112233", "loc": "تيبازة"}
    ]

# --- واجهة التصميم ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .search-card { background: white; padding: 20px; border-radius: 15px; border-right: 5px solid #1e3799; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .wa-btn { background-color: #25D366; color: white; padding: 8px 15px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

# 2. الهيدر الموحد
st.markdown("<h1 style='text-align: center; color: #1e3799;'>RASSIM DE RECHERCHE DZ 🚀</h1>", unsafe_allow_html=True)

# 3. محرك البحث السريع
query = st.text_input("🔍 ابحث عن هاتف أو قطعة غيار (النتائج فورية):", placeholder="مثال: Samsung S21 Ultra")

if query:
    start = time.time()
    results = get_fast_data(query) # استدعاء البيانات من الذاكرة المؤقتة
    
    st.subheader(f"📍 نتائج البحث لـ '{query}':")
    
    for res in results:
        # تجهيز رابط واتساب
        msg = urllib.parse.quote(f"سلام، شفت إعلانك {res['item']} في تطبيق رسيم فون.. هل متوفر؟")
        wa_url = f"https://wa.me/213{res['seller'][1:]}?text={msg}"
        
        st.markdown(f"""
            <div class="search-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin:0;">{res['item']}</h4>
                        <p style="margin:5px 0; color:#27ae60; font-weight:bold; font-size:1.2em;">{res['price']}</p>
                        <p style="margin:0; color:#666; font-size:0.9em;">📍 {res['loc']} | 👤 بائع موثوق</p>
                    </div>
                    <a href="{wa_url}" target="_blank" class="wa-btn">💬 تواصل واتساب</a>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.caption(f"⚡ المحرك عالج البيانات في {round(time.time()-start, 3)} ثانية.")

# 4. تذييل الصفحة (إضافة عرض)
st.write("---")
if st.button("➕ أريد إضافة عرض بيع (جديد، مستعمل، أو خردة)"):
    st.info("سجل دخولك أولاً لتتمكن من إضافة عروضك في القاعدة الوطنية.")
    # --- شريط التصنيفات الاحترافي ---
st.write("### 🏷️ تصفح حسب الصنف:")

# تصميم الأيقونات بشكل جذاب
col_cat1, col_cat2, col_cat3, col_cat4, col_cat5 = st.columns(5)

with col_cat1:
    if st.button("📱 هواتف كاملة", use_container_width=True):
        st.session_state['query_input'] = "هاتف"
        st.rerun()

with col_cat2:
    if st.button("⚙️ قطع غيار", use_container_width=True):
        st.session_state['query_input'] = "قطعة"
        st.rerun()

with col_cat3:
    if st.button("🖥️ شاشات", use_container_width=True):
        st.session_state['query_input'] = "شاشة"
        st.rerun()

with col_cat4:
    if st.button("🔋 بطاريات", use_container_width=True):
        st.session_state['query_input'] = "بطارية"
        st.rerun()

with col_cat5:
    if st.button("🎧 أكسسوارات", use_container_width=True):
        st.session_state['query_input'] = "سماعات"
        st.rerun()

st.markdown("---")
# --- خوارزمية اكتشاف الصفقات (Hot Deals) ---
st.markdown("### 🔥 همزات اليوم (تخفيضات حقيقية)")

# محاكاة لبيانات بها تخفيضات (Price Drop)
deals = [
    {"item": "iPhone 12 Pro", "old_price": "85,000", "new_price": "78,000", "loc": "فوكة"},
    {"item": "Ecran S21 Ultra", "old_price": "42,000", "new_price": "35,000", "loc": "تيبازة"},
    {"item": "Battery iPhone X", "old_price": "6,500", "new_price": "4,500", "loc": "القليعة"}
]

# عرض الصفقات في شريط أفقي جذاب
deal_cols = st.columns(len(deals))

for i, deal in enumerate(deals):
    with deal_cols[i]:
        st.markdown(f"""
            <div style="background: #fff5f5; padding: 15px; border-radius: 12px; border: 1px solid #ff7675; text-align: center;">
                <span style="background: #ff7675; color: white; padding: 2px 8px; border-radius: 5px; font-size: 0.7em;">Affaire!</span>
                <h5 style="margin: 10px 0 5px 0;">{deal['item']}</h5>
                <p style="text-decoration: line-through; color: #636e72; margin: 0; font-size: 0.8em;">{deal['old_price']} DA</p>
                <p style="color: #d63031; font-weight: bold; font-size: 1.2em; margin: 0;">{deal['new_price']} DA</p>
                <p style="color: #2d3436; font-size: 0.7em; margin-top: 5px;">📍 {deal['loc']}</p>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")
# --- قسم ترويج الإعلانات (النظام الربحي المستقبلي) ---
st.write("---")
with st.expander("🚀 هل تريد بيع سلعتك بسرعة أكبر؟"):
    st.markdown("""
        <div style="background-color: #fff3cd; padding: 20px; border-radius: 10px; border-right: 5px solid #ffc107;">
            <h4>خدمة الإعلانات المميزة (Featured Ads)</h4>
            <p>اجعل إعلانك يظهر في مقدمة نتائج البحث وفي صفحة "همزات اليوم" ليصل إلى آلاف المشترين في ولايتك.</p>
            <ul>
                <li>✅ ظهور في القمة لمدة 7 أيام.</li>
                <li>✅ علامة "بائع موثوق" بجانب اسمك.</li>
                <li>✅ إرسال إشعار للمشتركين المهتمين بنوع هاتفك.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("##")
    if st.button("اطلب الترويج لإعلاني الآن ⚡"):
        # توجيه البائع مباشرة لواتساب الخاص بك (صاحب المنصة) للاتفاق
        admin_phone = "0550XXXXXX" # ضع رقمك هنا
        promo_msg = urllib.parse.quote("سلام، حاب نروج الإعلان تاعي في منصة رسيم فون. كيفاش نخلصكم؟")
        wa_admin_url = f"https://wa.me/213{admin_phone[1:]}?text={promo_msg}"
        
        st.success("رائع! سيتم توجيهك للتحدث مع الإدارة لتفعيل الترويج.")
        st.markdown(f'<a href="{wa_admin_url}" target="_blank" style="background-color: #25D366; color: white; padding: 10px 20px; border-radius: 10px; text-decoration: none; display: block; text-align: center; font-weight: bold;">ارسل طلب الترويج عبر WhatsApp</a>', unsafe_allow_html=True)

# --- تذييل الصفحة الإحصائي ---
st.sidebar.markdown("---")
st.sidebar.subheader("📈 إحصائيات Rassim Phone")
st.sidebar.write("عدد المستخدمين: 1,240")
st.sidebar.write("السلع المعروضة: 450")
st.sidebar.info("المنصة مجانية بالكامل للمستخدمين العاديين")
# --- خوارزمية مستشار الأسعار الذكي ---
def price_advisor(model_name, user_price):
    # قاعدة بيانات تجريبية لمتوسط الأسعار في السوق حالياً
    market_prices = {
        "iphone 13": 95000,
        "iphone 12": 75000,
        "samsung s21": 65000,
        "redmi note 12": 32000
    }
    
    # محاولة إيجاد السعر المقارب
    model_key = model_name.lower()
    for key in market_prices:
        if key in model_key:
            avg_price = market_prices[key]
            try:
                price_val = float(user_price.replace(",", "").replace(" ", ""))
                
                if price_val < avg_price * 0.9:
                    return "🔥 صفقة رائعة! سعرك أقل من متوسط السوق، ستبيع بسرعة كبيرة."
                elif price_val > avg_price * 1.1:
                    return f"⚠️ تنبيه: متوسط سعر هذا الهاتف هو {avg_price:,} دج. قد يتأخر البيع بسبب السعر المرتفع."
                else:
                    return "✅ سعرك مناسب جداً ومتوافق مع أسعار السوق الحالية."
            except:
                return "💡 أدخل السعر بالأرقام لنعطيك نصيحة البيع."
    return "📊 لم نجد بيانات كافية لهذا الموديل، لكن ننصحك بمقارنة سعرك مع 'همزات اليوم'."

# --- كيفية دمجها في واجهة إضافة السلعة ---
# (يوضع هذا الكود تحت خانة إدخال السعر مباشرة)
if p_name and p_price:
    advice = price_advisor(p_name, p_price)
    st.info(advice)