import streamlit as st
import webbrowser

# إعدادات المنصة الوطنية الكبرى
st.set_page_config(page_title="Rassim de Recherche DZ | المحرك الشامل", layout="wide", page_icon="🚀")

# --- تصميم الواجهة العالمية ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .super-search-box {
        background: linear-gradient(135deg, #1e3799 0%, #0984e3 100%);
        padding: 50px;
        border-radius: 0 0 40px 40px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .platform-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-top: 5px solid #0984e3;
        text-align: center;
        transition: 0.3s;
        height: 100%;
    }
    .platform-card:hover { transform: translateY(-10px); box-shadow: 0 12px 20px rgba(0,0,0,0.15); }
    .btn-go { width: 100%; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- الرأس (Header) ---
st.markdown("""
    <div class="super-search-box">
        <h1 style='font-size: 3.5em; margin-bottom: 10px;'>RASSIM DE RECHERCHE DZ</h1>
        <p style='font-size: 1.2em; opacity: 0.9;'>أول محرك بحث وطني يجمع (Ouedkniss, Facebook, Instagram, TikTok) في مكان واحد</p>
    </div>
    """, unsafe_allow_html=True)

st.write("#")

# --- خانة البحث الموحدة (The Magic Box) ---
col_s1, col_s2, col_s3 = st.columns([1, 4, 1])
with col_s2:
    search_query = st.text_input("", placeholder="🔍 ماذا تريد أن تجد في كل أسواق الجزائر؟ (مثلاً: iPhone 15 Pro Max Caba)")
    
    st.write("---")

# --- توزيع النتائج حسب المنصات ---
if search_query:
    st.markdown(f"<h3 style='text-align:center;'>نتائج البحث لـ : <span style='color:#0984e3;'>{search_query}</span></h3>", unsafe_allow_html=True)
    
    # شبكة المنصات (4 أعمدة)
    p1, p2, p3, p4 = st.columns(4)
    
    # 1. واد كنيس (Ouedkniss)
    with p1:
        st.markdown("""<div class="platform-card">
            <h2 style='color:#d32f2f;'>📦</h2>
            <h4>Ouedkniss</h4>
            <p>سوق المحترفين والجملة</p>
        </div>""", unsafe_allow_html=True)
        ok_url = f"https://www.ouedkniss.com/recherche?keywords={search_query.replace(' ', '%20')}"
        st.link_button("إفتح واد كنيس", ok_url, type="primary", use_container_width=True)

    # 2. فيسبوك (Marketplace)
    with p2:
        st.markdown("""<div class="platform-card">
            <h2 style='color:#1877F2;'>🔵</h2>
            <h4>Marketplace</h4>
            <p>عروض الأفراد والمستعمل</p>
        </div>""", unsafe_allow_html=True)
        fb_url = f"https://www.facebook.com/marketplace/dz/search?query={search_query.replace(' ', '%20')}"
        st.link_button("إفتح فيسبوك", fb_url, type="primary", use_container_width=True)

    # 3. إنستغرام (Instagram)
    with p3:
        st.markdown("""<div class="platform-card">
            <h2 style='color:#e1306c;'>📸</h2>
            <h4>Instagram</h4>
            <p>عروض الستوريات والمحلات</p>
        </div>""", unsafe_allow_html=True)
        insta_url = f"https://www.instagram.com/explore/tags/dzphone/" # يمكن تعديل الوسم حسب البحث
        st.link_button("إفتح إنستغرام", insta_url, type="primary", use_container_width=True)

    # 4. تيك توك (TikTok)
    with p4:
        st.markdown("""<div class="platform-card">
            <h2 style='color:#000000;'>🎵</h2>
            <h4>TikTok</h4>
            <p>مراجعات الفيديو والأسعار</p>
        </div>""", unsafe_allow_html=True)
        tk_url = f"https://www.tiktok.com/search/video?q={search_query.replace(' ', '%20')}"
        st.link_button("إفتح تيك توك", tk_url, type="primary", use_container_width=True)

else:
    # واجهة عرض مميزات النظام عند عدم البحث
    st.markdown("<h4 style='text-align:center; color:#7f8c8d;'>ابدأ بكتابة اسم الهاتف أو القطعة، وسنقوم بتقسيم البحث لك على كل المنصات الوطنية</h4>", unsafe_allow_html=True)
    
    

# --- تذييل الصفحة (Footer) ---
st.write("##")
st.divider()
st.markdown("<p style='text-align:center; color:#95a5a6;'>Rassim de Recherche DZ - المحرك الوطني الموحد © 2026</p>", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import time

# إعدادات المنصة الوطنية
st.set_page_config(page_title="Rassim de Recherche DZ | Data Engine", layout="wide")

st.markdown("""
    <style>
    .report-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-right: 10px solid #1e3799;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .price-tag { color: #27ae60; font-size: 1.5em; font-weight: bold; }
    .source-tag { background: #eee; padding: 2px 8px; border-radius: 5px; font-size: 0.8em; }
    </style>
    """, unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("<h1 style='text-align: center;'>Rassim de Recherche DZ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>مركز تحليل بيانات سوق الهواتف في الجزائر</p>", unsafe_allow_html=True)

# --- محرك البحث الموحد ---
search_query = st.text_input("🔍 أدخل اسم الهاتف أو القطعة لتحليل السوق:", placeholder="مثال: iPhone 13 Pro Max")

if search_query:
    with st.spinner(f'جاري استخراج البيانات من (واد كنيس، فيسبوك، تيك توك) لـ {search_query}...'):
        # هنا برمجياً نقوم بجلب البيانات (محاكاة للنتائج المدمجة)
        time.sleep(1.5) # وقت وهمي للمعالجة
        
        # إنشاء قاعدة بيانات مؤقتة للنتائج
        results_data = [
            {"المصدر": "Ouedkniss", "العرض": f"{search_query} Caba Clean", "السعر": "112,000 DA", "الولاية": "الجزائر"},
            {"المصدر": "Marketplace", "العرض": f"{search_query} مستعمل", "السعر": "105,000 DA", "الولاية": "وهران"},
            {"المصدر": "Instagram", "العرض": f"{search_query} Neuf Officiel", "السعر": "145,000 DA", "الولاية": "سطيف"},
            {"المصدر": "TikTok", "العرض": f"{search_query} Pièce Démontage", "السعر": "18,000 DA", "الولاية": "قسنطينة"},
        ]
        
        # --- لوحة تحليل الأسعار (Analytics) ---
        st.write("### 📊 ملخص تحليل السوق الوطني")
        col1, col2, col3 = st.columns(3)
        col1.metric("أقل سعر وجدناه", "105,000 DA")
        col2.metric("متوسط السعر في السوق", "118,000 DA")
        col3.metric("عدد العروض المتاحة", "24 عرض")
        
        st.write("---")
        
        # --- عرض النتائج المدمجة في جدول واحد ---
        st.write("### 📋 جميع العروض المتوفرة حالياً:")
        
        # عرض البيانات بشكل بطاقات تقنية بدلاً من فتح المواقع
        for item in results_data:
            st.markdown(f"""
                <div class="report-card">
                    <span class="source-tag">{item['المصدر']}</span>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="margin: 5px 0;">{item['العرض']}</h4>
                            <p style="color: #666;">📍 المنطقة: {item['الولاية']}</p>
                        </div>
                        <div class="price-tag">{item['السعر']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

else:
    st.info("قم بكتابة اسم الهاتف وسيقوم المحرك بجرد شامل للأسعار والعروض من كافة المنصات وعرضها لك هنا مباشرة.")
    import streamlit as st
import pandas as pd

# إعدادات المنصة الوطنية
st.set_page_config(page_title="Rassim de Recherche DZ | Accounts", layout="centered")

# --- تنسيق واجهة الدخول ---
st.markdown("""
    <style>
    .login-box {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-top: 5px solid #1e3799;
    }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- إدارة حالة الجلسة (Session State) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- واجهة تسجيل الدخول / فتح الحساب ---
if not st.session_state['logged_in']:
    st.markdown("<h1 style='text-align: center; color: #1e3799;'>Rassim de Recherche DZ</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>يجب تسجيل الدخول للوصول إلى بيانات السوق الوطنية</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 تسجيل الدخول", "📝 فتح حساب جديد"])
    
    with tab1:
        with st.container():
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            user = st.text_input("اسم المستخدم أو رقم الهاتف:")
            pwd = st.text_input("كلمة المرور:", type="password")
            if st.button("دخول للمنصة"):
                if user == "admin" and pwd == "123": # مثال بسيط
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("خطأ في البيانات، يرجى التأكد.")
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        with st.container():
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            new_user = st.text_input("الاسم الكامل:")
            new_phone = st.text_input("رقم الهاتف (الولاية):")
            user_type = st.selectbox("نوع الحساب:", ["مشتري (Zouwaq)", "تاجر صاحب محل", "تقني إصلاح (Technicien)"])
            new_pwd = st.text_input("اختر كلمة مرور:", type="password")
            if st.button("إنشاء حسابي الآن"):
                st.success("تم إنشاء حسابك بنجاح! يمكنك الآن تسجيل الدخول.")
            st.markdown('</div>', unsafe_allow_html=True)

# --- الواجهة الرئيسية بعد الدخول ---
else:
    st.sidebar.success("✅ متصل الآن")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state['logged_in'] = False
        st.rerun()

    st.markdown("### مرحباً بك في محرك البحث الموحد 🚀")
    # هنا نضع محرك البحث الذي جلبناه في الخطوات السابقة (واد كنيس، فيسبوك، إلخ)
    query = st.text_input("🔍 ابحث عن معلومة (هاتف أو قطعة):")
    if query:
        st.write(f"عرض البيانات المباشرة لـ {query}...")
        import streamlit as st
import pandas as pd

# إعدادات المنصة الوطنية
st.set_page_config(page_title="Rassim de Recherche DZ | Smart Search", layout="wide")

# --- محاكاة قاعدة بيانات العروض (سيتم استبدالها لاحقاً ببيانات حقيقية) ---
data = [
    {"المنتج": "iPhone 13", "السعر": "95,000 DA", "الولاية": "تيبازة", "البلدية": "فوكة", "المسافة": 0},
    {"المنتج": "iPhone 13", "السعر": "92,000 DA", "الولاية": "تيبازة", "البلدية": "القليعة", "المسافة": 5},
    {"المنتج": "iPhone 13", "السعر": "98,000 DA", "الولاية": "البليدة", "البلدية": "بوفاريك", "المسافة": 20},
    {"المنتج": "iPhone 13", "السعر": "90,000 DA", "الولاية": "الجزائر", "البلدية": "الدار البيضاء", "المسافة": 45},
    {"المنتج": "iPhone 13", "السعر": "94,000 DA", "الولاية": "وهران", "البلدية": "عين الترك", "المسافة": 400},
]

# --- تصميم الواجهة ---
st.markdown("""
    <style>
    .search-container { background-color: #f8f9fa; padding: 30px; border-radius: 20px; text-align: center; }
    .result-card { 
        padding: 15px; border-radius: 10px; margin-bottom: 10px;
        border-right: 5px solid #27ae60; background: white;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .distance-badge { background: #e8f5e9; color: #2e7d32; padding: 2px 10px; border-radius: 15px; font-size: 0.8em; }
    </style>
    """, unsafe_allow_html=True)

# --- نظام الجلسة والحساب ---
if 'user_location' not in st.session_state:
    st.session_state['user_location'] = "فوكة" # مثال للمستخدم الحالي

# الواجهة الرئيسية
st.markdown("<h1 style='text-align: center;'>Rassim de Recherche DZ</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("🔍 ابحث عن هاتف أو قطعة غيار:", placeholder="مثال: iPhone 13 Pro Max")
    with col2:
        user_loc = st.text_input("📍 موقعك الحالي:", value=st.session_state['user_location'])
    st.markdown('</div>', unsafe_allow_html=True)

st.write("##")

if query:
    st.subheader(f"📍 أفضل العروض لـ '{query}' القريبة من {user_loc}:")
    
    # تحويل البيانات إلى DataFrame للفرز حسب المسافة
    df = pd.DataFrame(data)
    # فلترة النتائج حسب البحث
    results = df[df['المنتج'].str.contains(query, case=False)]
    # ترتيب النتائج (الأقرب أولاً)
    results = results.sort_values(by="المسافة")

    if not results.empty:
        for index, row in results.iterrows():
            # تحديد لون البطاقة (أخضر للأقرب جداً)
            dist_label = "قريب جداً منك" if row['المسافة'] < 10 else f"يبعد {row['المسافة']} كلم"
            
            st.markdown(f"""
                <div class="result-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="margin:0;">{row['المنتج']} - <span style="color:#27ae60;">{row['السعر']}</span></h4>
                            <p style="margin:5px 0; color:#666;">📍 {row['الولاية']}، {row['البلدية']} <span class="distance-badge">{dist_label}</span></p>
                        </div>
                        <button style="border-radius:20px; border:1px solid #1e3799; background:white; padding:5px 15px;">عرض التفاصيل</button>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("عذراً، لا توجد نتائج مطابقة لبحثك حالياً.")

else:
    # عرض خريطة أو رسالة توضيحية
    st.info("💡 نظام 'رسيم الذكي' يعرض لك التجار في بلديتك أولاً لتوفير تكاليف التوصيل وضمان المعاينة اليدوية.")