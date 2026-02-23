import streamlit as st

def set_ultimate_theme():
    """تصميم الهولوجرام وواجهة سايبر بانك"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');

    * {
        font-family: 'Cairo', 'Space Grotesk', 'Inter', sans-serif !important;
        box-sizing: border-box;
    }

    .stApp {
        background: radial-gradient(circle at 20% 20%, #1a1a2a, #0a0a0f);
        color: #ffffff;
        min-height: 100vh;
    }

    /* تصميم الشعار */
    .logo-container {
        text-align: center;
        padding: 30px;
        margin-bottom: 20px;
    }

    .logo-text {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 4rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 8px;
        background: linear-gradient(90deg, #00ffff, #ff00ff, #00ffff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        display: inline-block;
        filter: drop-shadow(0 0 15px rgba(0,255,255,0.5));
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    .logo-subtitle {
        color: #00ffff;
        font-size: 0.9rem;
        letter-spacing: 3px;
        margin-top: -10px;
        opacity: 0.8;
    }

    /* كرت الهولوجرام */
    .hologram-card {
        background: rgba(20, 20, 30, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 255, 0.2);
        border-radius: 30px;
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    .hologram-card:hover {
        border-color: #00ffff;
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 255, 255, 0.2);
    }

    /* بطاقة الإعلان */
    .ad-card {
        background: rgba(30, 30, 40, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 0, 255, 0.2);
        border-radius: 25px;
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.4s ease;
    }

    .ad-card:hover {
        border-color: #ff00ff;
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(255, 0, 255, 0.2);
    }

    .ad-title {
        color: #00ffff;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .ad-price {
        color: #ff00ff;
        font-size: 2rem;
        font-weight: 800;
    }

    .ad-details {
        display: flex;
        justify-content: space-between;
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.9rem;
        margin: 15px 0;
        padding: 10px 0;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* شارات الولايات */
    .wilaya-badge {
        display: inline-block;
        background: rgba(0, 255, 255, 0.1);
        border: 1px solid #00ffff;
        border-radius: 50px;
        padding: 5px 12px;
        margin: 3px;
        font-size: 0.8rem;
        color: #00ffff;
        white-space: nowrap;
        transition: all 0.3s ease;
    }

    .wilaya-badge:hover {
        background: #00ffff;
        color: black;
        transform: scale(1.05);
    }

    /* بطاقة الإحصائيات */
    .stat-card {
        background: rgba(20, 20, 30, 0.5);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 255, 0.1);
        border-radius: 25px;
        padding: 20px;
        text-align: center;
        transition: all 0.4s ease;
    }

    .stat-card:hover {
        border-color: #ff00ff;
        transform: translateY(-5px);
    }

    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #00ffff;
        font-family: 'Space Grotesk', monospace !important;
        direction: ltr;
    }

    .stat-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1rem;
        margin-top: 5px;
    }

    /* فقاعة الدردشة */
    .chat-bubble {
        position: fixed;
        bottom: 80px;
        right: 30px;
        background: linear-gradient(135deg, #00ffff, #ff00ff);
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        z-index: 9999;
        animation: float 3s ease-in-out infinite;
        box-shadow: 0 10px 20px rgba(0, 255, 255, 0.3);
    }

    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    /* عداد الزوار الحي */
    .live-counter {
        position: fixed;
        bottom: 20px;
        left: 20px;
        background: rgba(0, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid #00ffff;
        padding: 10px 20px;
        border-radius: 50px;
        z-index: 999;
        display: flex;
        align-items: center;
        gap: 10px;
        animation: pulseGlow 2s infinite;
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 5px rgba(0, 255, 255, 0.2); }
        50% { box-shadow: 0 0 20px rgba(0, 255, 255, 0.5); }
        100% { box-shadow: 0 0 5px rgba(0, 255, 255, 0.2); }
    }

    .live-dot {
        color: #00ffff;
        font-weight: bold;
        font-size: 1.2rem;
        animation: blink 1s infinite;
    }

    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    /* صندوق الشروط */
    .terms-box {
        background: rgba(20, 20, 30, 0.6);
        border: 1px solid #ff00ff;
        border-radius: 20px;
        padding: 20px;
        margin-top: 20px;
        color: white;
        font-size: 0.9rem;
        line-height: 1.8;
    }

    .terms-box h2 {
        color: #ff00ff;
        text-align: center;
        margin-bottom: 15px;
    }

    /* أزرار */
    .stButton > button {
        background: linear-gradient(90deg, #00ffff, #ff00ff) !important;
        border: none !important;
        color: black !important;
        font-weight: 800 !important;
        border-radius: 15px !important;
        padding: 12px 25px !important;
        transition: all 0.3s ease !important;
        font-size: 1rem !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(255, 0, 255, 0.3) !important;
    }

    /* حقول الإدخال */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(0, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        color: white !important;
        padding: 12px 20px !important;
        direction: rtl !important;
        text-align: right !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #00ffff !important;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.3) !important;
    }

    /* تبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 40px !important;
        justify-content: center;
        direction: rtl !important;
        padding: 10px !important;
        background: rgba(20, 20, 30, 0.3);
        border-radius: 50px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: nowrap !important;
    }

    .stTabs [data-baseweb="tab"] p {
        font-size: 1.1rem !important;
        font-weight: bold !important;
        color: white !important;
    }

    /* الشريط الجانبي */
    section[data-testid="stSidebar"] {
        background: rgba(10, 10, 15, 0.9) !important;
        backdrop-filter: blur(20px);
        border-left: 1px solid rgba(0, 255, 255, 0.1);
        padding: 20px !important;
    }

    /* التجاوب مع الجوال */
    @media screen and (max-width: 768px) {
        .logo-text { font-size: 2.5rem; }
        .stat-value { font-size: 2rem; }
        .chat-bubble { width: 50px; height: 50px; bottom: 70px; right: 15px; }
        .live-counter { left: 15px; padding: 8px 15px; font-size: 0.8rem; }
        .stTabs [data-baseweb="tab-list"] { gap: 20px !important; }
    }
    </style>
    """, unsafe_allow_html=True)
