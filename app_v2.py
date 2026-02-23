import streamlit as st
import sqlite3
import pandas as pd
import hashlib
import re
import datetime
import urllib.parse
import secrets
import os
import time
import random
import json
import base64
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import warnings
from functools import wraps

warnings.filterwarnings('ignore')

# ==========================================
# 1. إعدادات النخبة TITANIUM MAX
# ==========================================
st.set_page_config(
    page_title="RASSIM DZ TITANIUM ULTRA - سوق الهواتف في الجزائر", 
    layout="wide", 
    page_icon="🇩🇿",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://t.me/RassimDZ',
        'Report a bug': 'https://t.me/RassimDZ',
        'About': '# RASSIM DZ TITANIUM ULTRA\nأول سوق إلكتروني جزائري متخصص في الهواتف'
    }
)

DB = "rassim_titanium_max_2026.db"
OLD_DB = "rassim_titanium_pro_2026.db" 

# إعدادات متقدمة
AI_ENABLED = True
CHATBOT_ENABLED = True
PRICE_PREDICTION_ENABLED = True

# ==========================================
# 2. إضافة Meta Tags لتحسين SEO (طلبك الأول)
# ==========================================
st.markdown("""
    <meta name="description" content="راسم تيتانيوم - أفضل سوق للهواتف في الجزائر. بيع وشراء الهواتف المستعملة والجديدة في 58 ولاية. موقع مشابه لوادي كنيس ولكن أسرع وأسهل">
    <meta name="keywords" content="واد كنيس, Ouedkniss, هواتف, الجزائر, بيع وشراء, Racim Phone, Titanium, سامسونج, ايفون, هواوي, تليفون, téléphone Algerie, واد كنيس تيليفون, سوق الهواتف, هواتف مستعملة, هواتف جديدة, الجزائر العاصمة, وهران, قسنطينة, عنابة">
    <meta name="author" content="RASSIM DZ">
    <meta name="robots" content="index, follow">
    <meta name="language" content="Arabic">
    <meta property="og:title" content="RASSIM DZ TITANIUM - سوق الهواتف الجزائري">
    <meta property="og:description" content="أول سوق إلكتروني جزائري متخصص في الهواتف - بيع وشراء في 58 ولاية">
    <meta property="og:image" content="https://i.ibb.co/logo.jpg">
    <meta property="og:url" content="https://racim-phone.streamlit.app/">
    <meta property="og:type" content="website">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="RASSIM DZ TITANIUM">
    <meta name="twitter:description" content="أول سوق إلكتروني جزائري للهواتف">
    <link rel="canonical" href="https://racim-phone.streamlit.app/">
""", unsafe_allow_html=True)

# ==========================================
# 3. التصميم المتطور (مع كل التأثيرات)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; box-sizing: border-box; }
    
    .stApp { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* تنسيق الهيدر الرئيسي */
    .main-header {
        background: linear-gradient(135deg, #006633 0%, #006633 48%, #d21034 50%, #ffffff 52%, #ffffff 100%);
        padding: 60px 20px;
        border-radius: 40px;
        text-align: center;
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        border-bottom: 12px solid #d21034;
        margin-bottom: 40px;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 25px 50px rgba(0,102,51,0.3); }
        to { box-shadow: 0 25px 70px rgba(210,16,52,0.5); }
    }
    
    /* تنسيق أزرار المشاركة الاجتماعية (طلبك الثاني) */
    .social-share {
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        padding: 30px 20px;
        border-radius: 30px;
        margin: 30px 0;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        animation: bounceIn 1s ease;
        border: 2px solid #006633;
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.05); }
        70% { transform: scale(0.95); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .social-share a {
        display: inline-block;
        margin: 0 15px;
        transition: all 0.3s;
        text-decoration: none;
    }
    
    .social-share a:hover {
        transform: translateY(-10px) scale(1.1);
        filter: drop-shadow(0 10px 20px rgba(0,0,0,0.2));
    }
    
    .social-share img {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* تنسيق الإحصائيات */
    .stats-container {
        display: flex;
        justify-content: space-around;
        background: white;
        padding: 30px;
        border-radius: 30px;
        margin-bottom: 30px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        animation: slideUp 0.5s ease-out;
        flex-wrap: wrap;
        gap: 20px;
    }
    
    @keyframes slideUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .stat-box { 
        text-align: center; 
        flex: 1; 
        padding: 20px;
        min-width: 150px;
        background: linear-gradient(135deg, #f8f9fa, #ffffff);
        border-radius: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    
    .stat-val { 
        font-size: 2.8rem; 
        font-weight: 900; 
        color: #d21034;
        text-shadow: 2px 2px 4px rgba(210,16,52,0.2);
    }
    
    .stat-label { 
        font-size: 1.2rem; 
        color: #006633;
        font-weight: 700;
        margin-top: 10px;
    }
    
    /* تنسيق بطاقات الإعلانات */
    .ad-card { 
        background: white; 
        border-radius: 30px; 
        padding: 35px; 
        border-right: 15px solid #006633; 
        margin-bottom: 30px; 
        box-shadow: 0 15px 40px rgba(0,0,0,0.1); 
        transition: 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: fadeIn 0.5s ease-in;
        position: relative;
        overflow: hidden;
    }
    
    .ad-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #006633, #d21034, #006633);
        animation: slide 3s linear infinite;
    }
    
    @keyframes slide {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .ad-card:hover { 
        transform: scale(1.02) translateY(-5px); 
        border-right-color: #d21034;
        box-shadow: 0 25px 50px rgba(210,16,52,0.3);
    }
    
    .price-tag { 
        background: linear-gradient(135deg, #006633, #00a86b); 
        color: white; 
        padding: 12px 35px; 
        border-radius: 50px; 
        font-weight: 900; 
        font-size: 1.8rem; 
        box-shadow: 0 10px 25px rgba(0,102,51,0.3);
        display: inline-block;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* تنسيق فقاعات الدردشة */
    .chat-container {
        background: #f0f2f5;
        border-radius: 20px;
        padding: 20px;
        max-height: 500px;
        overflow-y: auto;
    }
    
    .chat-bubble { 
        padding: 15px 20px; 
        border-radius: 20px; 
        margin: 10px 0; 
        max-width: 80%; 
        animation: popIn 0.3s ease-out;
        word-wrap: break-word;
    }
    
    @keyframes popIn {
        from { transform: scale(0.8); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    
    .chat-sent { 
        background: linear-gradient(135deg, #dcf8c6, #c8e6c9); 
        margin-left: auto; 
        border-bottom-right-radius: 5px;
        box-shadow: -5px 5px 10px rgba(0,0,0,0.1);
    }
    
    .chat-received { 
        background: linear-gradient(135deg, #ffffff, #f5f5f5); 
        margin-right: auto; 
        border-bottom-left-radius: 5px;
        box-shadow: 5px 5px 10px rgba(0,0,0,0.1);
    }
    
    /* تنسيق شارة المميز */
    .badge-premium {
        background: linear-gradient(135deg, #ffd700, #ffa500);
        color: white;
        padding: 8px 20px;
        border-radius: 50px;
        font-weight: bold;
        display: inline-block;
        animation: shimmer 2s infinite;
        font-size: 0.9rem;
    }
    
    @keyframes shimmer {
        0% { background-position: -100% 0; }
        100% { background-position: 200% 0; }
    }
    
    /* تنسيق المساعد الذكي */
    .ai-suggestion {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 30px;
        border-radius: 30px;
        margin: 30px 0;
        animation: slideIn 0.5s ease-out;
        box-shadow: 0 20px 40px rgba(102,126,234,0.3);
    }
    
    @keyframes slideIn {
        from { transform: translateX(-50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* تنسيق قسم تيك توك (طلبك الثالث) */
    .tiktok-style {
        background: linear-gradient(135deg, #25F4EE, #FE2C55);
        padding: 30px;
        border-radius: 30px;
        color: white;
        text-align: center;
        margin: 30px 0;
        animation: shake 0.8s ease;
        box-shadow: 0 20px 40px rgba(254,44,85,0.3);
        border: 3px solid white;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-8px); }
        20%, 40%, 60%, 80% { transform: translateX(8px); }
    }
    
    .tiktok-tag {
        background: white;
        color: #FE2C55;
        padding: 8px 20px;
        border-radius: 50px;
        display: inline-block;
        margin: 5px;
        font-weight: bold;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    /* تنسيق لوحة الإدارة */
    .admin-section {
        background: linear-gradient(135deg, #2c3e50, #3498db);
        padding: 30px;
        border-radius: 30px;
        color: white;
        margin: 30px 0;
        box-shadow: 0 20px 40px rgba(52,152,219,0.3);
    }
    
    /* تحسينات للموبايل */
    @media (max-width: 768px) {
        .main-header { padding: 30px 15px; }
        .stat-val { font-size: 2rem; }
        .stat-label { font-size: 1rem; }
        .social-share img { width: 40px; height: 40px; }
        .ad-card { padding: 25px; }
    }
    
    /* تنسيق الأزرار */
    .stButton > button {
        width: 100%;
        border-radius: 50px;
        background: linear-gradient(135deg, #006633, #00a86b);
        color: white;
        font-weight: bold;
        border: none;
        padding: 15px;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0,102,51,0.3);
    }
    
    /* تنسيق التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: white;
        padding: 10px;
        border-radius: 50px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 50px;
        padding: 10px 20px;
        font-weight: bold;
    }
    
    /* تنسيق الإشعارات */
    .notification-badge {
        background: #d21034;
        color: white;
        border-radius: 50%;
        padding: 2px 8px;
        font-size: 0.8rem;
        position: absolute;
        top: -5px;
        right: -5px;
    }
    
    /* تنسيق التمرير */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #006633, #d21034);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #d21034, #006633);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. دالة أزرار المشاركة الاجتماعية (طلبك الثاني)
# ==========================================
def add_social_share_buttons():
    """إضافة أزرار المشاركة على وسائل التواصل الاجتماعي - تم التطوير حسب طلبك"""
    site_url = "https://racim-phone.streamlit.app/"
    site_title = "RASSIM DZ TITANIUM - سوق الهواتف في الجزائر"
    
    st.markdown(f"""
    <div class="social-share">
        <h2 style="color: #006633; margin-bottom: 20px;">📢 شارك الموقع مع أصدقائك 🇩🇿</h2>
        <p style="color: #666; margin-bottom: 25px; font-size: 1.2rem;">ساعد في نشر الموقع واكسب الثواب 🤲</p>
        
        <div style="display: flex; justify-content: center; gap: 25px; flex-wrap: wrap; margin-bottom: 20px;">
            <!-- Facebook -->
            <a href="https://www.facebook.com/sharer/sharer.php?u={site_url}" target="_blank" title="شارك على فيسبوك">
                <img src="https://img.icons8.com/color/48/000000/facebook-new.png" width="50">
            </a>
            
            <!-- WhatsApp -->
            <a href="https://api.whatsapp.com/send?text=شوف هاد الموقع لبيع وشراء الهواتف في الجزائر: {site_url}" target="_blank" title="شارك على واتساب">
                <img src="https://img.icons8.com/color/48/000000/whatsapp--v1.png" width="50">
            </a>
            
            <!-- Messenger -->
            <a href="https://www.facebook.com/dialog/send?link={site_url}&app_id=123456789&redirect_uri={site_url}" target="_blank" title="شارك على ماسنجر">
                <img src="https://img.icons8.com/color/48/000000/facebook-messenger--v1.png" width="50">
            </a>
            
            <!-- Twitter/X -->
            <a href="https://twitter.com/intent/tweet?text={site_title}&url={site_url}" target="_blank" title="شارك على تويتر">
                <img src="https://img.icons8.com/color/48/000000/twitter--v1.png" width="50">
            </a>
            
            <!-- Telegram -->
            <a href="https://t.me/share/url?url={site_url}&text={site_title}" target="_blank" title="شارك على تيليغرام">
                <img src="https://img.icons8.com/color/48/000000/telegram-app--v1.png" width="50">
            </a>
            
            <!-- LinkedIn -->
            <a href="https://www.linkedin.com/sharing/share-offsite/?url={site_url}" target="_blank" title="شارك على لينكد إن">
                <img src="https://img.icons8.com/color/48/000000/linkedin.png" width="50">
            </a>
            
            <!-- Copy Link -->
            <a href="#" onclick="navigator.clipboard.writeText('{site_url}'); alert('✅ تم نسخ الرابط! شاركه مع أصدقائك'); return false;" title="نسخ الرابط">
                <img src="https://img.icons8.com/color/48/000000/link--v1.png" width="50">
            </a>
        </div>
        
        <div style="margin-top: 25px; padding: 15px; background: linear-gradient(135deg, #f0f0f0, #ffffff); border-radius: 50px;">
            <p style="color: #d21034; font-weight: bold; font-size: 1.1rem;">
                👥 شارك الموقع مع 10 أصدقاء واكسب دعواتهم 🤲
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. دالة قسم تيك توك (طلبك الثالث)
# ==========================================
def add_tiktok_style():
    """إضافة قسم تيك توك للترويج - حسب طلبك بالضبط"""
    st.markdown("""
    <div class="tiktok-style">
        <h2 style="color: white; margin-bottom: 20px; font-size: 2rem;">🎵 تيك توك الجزائر</h2>
        
        <div style="background: rgba(255,255,255,0.2); padding: 20px; border-radius: 20px; margin: 20px 0;">
            <p style="font-size: 1.5rem; font-weight: bold; margin-bottom: 15px;">
                تهنينا من التقرعيج في فيسبوك، موقع راسم تيتانيوم للدزة راهو واجد 🇩🇿
            </p>
            
            <p style="font-size: 1.2rem; margin-bottom: 20px;">
                🔥 تسوق بسهولة | بيع بسرعة | تواصل مباشر مع البائعين
            </p>
        </div>
        
        <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin-top: 25px;">
            <span class="tiktok-tag">#واد_كنيس</span>
            <span class="tiktok-tag">#الجزائر</span>
            <span class="tiktok-tag">#هواتف</span>
            <span class="tiktok-tag">#تيليفون</span>
            <span class="tiktok-tag">#راسم_تيتانيوم</span>
            <span class="tiktok-tag">#الدزة_واجدة</span>
        </div>
        
        <div style="margin-top: 30px;">
            <p style="color: white; font-size: 1.1rem;">
                📱 حمّل التطبيق الآن وتصفح آلاف الهواتف في 58 ولاية
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 6. نظام إدارة حالة الفلاتر الذكي
# ==========================================
if "filters" not in st.session_state:
    st.session_state.filters = {
        "wilaya": "الكل",
        "min_price": 0,
        "max_price": 10000000,
        "search_query": "",
        "sort_by": "الأحدث",
        "category": "الكل",
        "featured_only": False,
        "verified_only": False,
        "with_images": False,
        "date_range": "الكل",
        "price_range": [0, 10000000]
    }
    
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = "user"
if "ip" not in st.session_state:
    st.session_state.ip = secrets.token_hex(8)

def update_filters(**kwargs):
    """تحديث الفلاتر مع الحفاظ على القيم الأخرى"""
    st.session_state.filters.update(kwargs)
    st.session_state.filters["last_updated"] = datetime.datetime.now().strftime("%H:%M:%S")

def reset_filters():
    """إعادة ضبط جميع الفلاتر"""
    st.session_state.filters.update({
        "wilaya": "الكل",
        "min_price": 0,
        "max_price": 10000000,
        "search_query": "",
        "sort_by": "الأحدث",
        "category": "الكل",
        "featured_only": False,
        "verified_only": False,
        "with_images": False,
        "date_range": "الكل",
        "price_range": [0, 10000000]
    })
    st.session_state.filters["last_reset"] = datetime.datetime.now().strftime("%H:%M:%S")
    st.rerun()

def render_filters_ui():
    """عرض واجهة الفلاتر"""
    with st.expander("🔍 خيارات البحث المتقدم", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            wilaya_options = ["الكل"] + [f"{i:02d}" for i in range(1, 59)]
            selected_wilaya = st.selectbox(
                "📍 الولاية",
                wilaya_options,
                index=wilaya_options.index(st.session_state.filters.get("wilaya", "الكل")),
                key="wilaya_filter"
            )
            
            category_options = ["الكل", "إلكترونيات", "عقارات", "سيارات", "خدمات", "أخرى"]
            selected_category = st.selectbox(
                "🏷️ الفئة",
                category_options,
                index=category_options.index(st.session_state.filters.get("category", "الكل")),
                key="category_filter"
            )
        
        with col2:
            min_p, max_p = st.slider(
                "💰 نطاق السعر (دج)",
                min_value=0,
                max_value=10000000,
                value=st.session_state.filters.get("price_range", [0, 10000000]),
                step=10000,
                key="price_slider"
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                featured_only = st.checkbox("⭐ مميز فقط", value=st.session_state.filters.get("featured_only", False))
            with col_b:
                verified_only = st.checkbox("✅ موثق فقط", value=st.session_state.filters.get("verified_only", False))
        
        with col3:
            date_range = st.selectbox(
                "📅 الفترة الزمنية",
                ["الكل", "اليوم", "الأسبوع", "الشهر"],
                index=["الكل", "اليوم", "الأسبوع", "الشهر"].index(st.session_state.filters.get("date_range", "الكل")),
                key="date_filter"
            )
            
            sort_options = ["الأحدث", "الأقدم", "الأعلى سعراً", "الأقل سعراً", "الأكثر مشاهدة", "الأعلى تقييماً"]
            selected_sort = st.selectbox(
                "📊 ترتيب حسب",
                sort_options,
                index=sort_options.index(st.session_state.filters.get("sort_by", "الأحدث")),
                key="sort_filter"
            )
        
        search_query = st.text_input("🔎 كلمة البحث", value=st.session_state.filters.get("search_query", ""), key="search_input")
        
        col_x, col_y = st.columns(2)
        with col_x:
            if st.button("🔍 تطبيق الفلاتر", use_container_width=True):
                update_filters(
                    wilaya=selected_wilaya,
                    category=selected_category,
                    price_range=[min_p, max_p],
                    min_price=min_p,
                    max_price=max_p,
                    featured_only=featured_only,
                    verified_only=verified_only,
                    date_range=date_range,
                    sort_by=selected_sort,
                    search_query=search_query
                )
                st.rerun()
        
        with col_y:
            if st.button("♻️ إعادة ضبط", use_container_width=True):
                reset_filters()

# ==========================================
# 7. محرك قاعدة البيانات المتقدم
# ==========================================
def init_db():
    """تهيئة قاعدة البيانات مع نظام الترقية الذكي"""
    conn = sqlite3.connect(DB, check_same_thread=False)
    cursor = conn.cursor()
    
    # إنشاء الجداول الأساسية
    tables = [
        """CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY, 
            password TEXT, 
            salt TEXT, 
            role TEXT DEFAULT 'user',
            last_login TEXT,
            banned INTEGER DEFAULT 0, 
            ad_count INTEGER DEFAULT 0,
            email TEXT, 
            phone TEXT, 
            verified INTEGER DEFAULT 0, 
            premium_until TEXT
        )""",
        
        """CREATE TABLE IF NOT EXISTS ads(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            product TEXT, 
            price REAL, 
            phone TEXT, 
            wilaya TEXT, 
            description TEXT, 
            date TEXT, 
            owner TEXT, 
            views INTEGER DEFAULT 0, 
            featured INTEGER DEFAULT 0, 
            category TEXT DEFAULT 'أخرى', 
            images TEXT, 
            status TEXT DEFAULT 'active'
        )""",
        
        """CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            from_user TEXT, 
            to_user TEXT, 
            message TEXT, 
            date TEXT, 
            read INTEGER DEFAULT 0,
            ad_id INTEGER
        )""",
        
        """CREATE TABLE IF NOT EXISTS site_analytics(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            ip TEXT, 
            visit_date TEXT,
            page TEXT
        )""",
        
        """CREATE TABLE IF NOT EXISTS notifications(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT, 
            message TEXT,
            date TEXT, 
            read INTEGER DEFAULT 0, 
            type TEXT
        )""",
        
        """CREATE TABLE IF NOT EXISTS reports(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            ad_id INTEGER, 
            reported_by TEXT,
            reason TEXT, 
            date TEXT, 
            status TEXT DEFAULT 'pending'
        )""",
        
        """CREATE TABLE IF NOT EXISTS activity_log(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT, 
            action TEXT,
            details TEXT, 
            date TEXT, 
            ip TEXT
        )""",
        
        """CREATE TABLE IF NOT EXISTS favorites(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT, 
            ad_id INTEGER,
            saved_date TEXT
        )""",
        
        """CREATE TABLE IF NOT EXISTS ratings(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            ad_id INTEGER, 
            rating INTEGER,
            user TEXT, 
            comment TEXT, 
            date TEXT
        )""",
        
        """CREATE TABLE IF NOT EXISTS login_attempts(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT, 
            attempt_time TEXT
        )"""
    ]
    
    for table in tables:
        cursor.execute(table)
    
    conn.commit()
    return conn

@st.cache_resource
def get_connection():
    """الحصول على اتصال قاعدة البيانات"""
    return sqlite3.connect(DB, check_same_thread=False)

def migrate_old_data():
    """ترحيل البيانات من قاعدة البيانات القديمة"""
    if os.path.exists(OLD_DB):
        conn = get_connection()
        try:
            conn.execute(f"ATTACH DATABASE '{OLD_DB}' AS old_db")
            conn.execute("INSERT OR IGNORE INTO users SELECT * FROM old_db.users")
            conn.execute("INSERT OR IGNORE INTO ads SELECT * FROM old_db.ads")
            conn.execute("INSERT OR IGNORE INTO site_analytics SELECT * FROM old_db.visitors")
            conn.commit()
            conn.execute("DETACH DATABASE old_db")
            print("✅ تم ترحيل البيانات القديمة بنجاح")
        except Exception as e:
            print(f"⚠️ خطأ في ترحيل البيانات: {e}")

def log_visitor():
    """تسجيل زائر جديد"""
    conn = get_connection()
    ip = st.session_state.get("ip", secrets.token_hex(8))
    st.session_state.ip = ip
    conn.execute(
        "INSERT INTO site_analytics (ip, visit_date, page) VALUES (?, datetime('now'), ?)",
        (ip, st.session_state.get("current_page", "main"))
    )
    conn.commit()

def get_stats():
    """الحصول على إحصائيات الموقع"""
    conn = get_connection()
    try:
        users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        visitors = conn.execute("SELECT COUNT(*) FROM site_analytics").fetchone()[0]
        ads = conn.execute("SELECT COUNT(*) FROM ads WHERE status='active'").fetchone()[0]
        views = conn.execute("SELECT SUM(views) FROM ads").fetchone()[0] or 0
        return users, visitors, ads, views
    except:
        return 0, 0, 0, 0

# تهيئة قاعدة البيانات
init_db()
migrate_old_data()

# ==========================================
# 8. نظام الذكاء الاصطناعي المتقدم
# ==========================================
class AIEngine:
    def __init__(self):
        self.conn = get_connection()
    
    def predict_price(self, category, description, wilaya):
        """توقع السعر بناءً على بيانات مشابهة"""
        similar_ads = self.conn.execute("""
            SELECT price FROM ads 
            WHERE category=? AND wilaya=? AND status='active'
            AND price > 0 AND price < 10000000
            ORDER BY date DESC LIMIT 20
        """, (category, wilaya)).fetchall()
        
        if len(similar_ads) < 3:
            return None
        
        prices = [a[0] for a in similar_ads]
        avg_price = sum(prices) / len(prices)
        sorted_prices = sorted(prices)
        mid = len(sorted_prices) // 2
        median_price = sorted_prices[mid] if len(sorted_prices) % 2 else (sorted_prices[mid-1] + sorted_prices[mid]) / 2
        
        return {
            'predicted': int((avg_price * 0.4 + median_price * 0.6)),
            'min': int(min(prices)),
            'max': int(max(prices)),
            'avg': int(avg_price),
            'median': int(median_price),
            'sample_size': len(prices)
        }
    
    def get_trending_categories(self):
        """الحصول على الفئات الرائجة"""
        return self.conn.execute("""
            SELECT category, COUNT(*) as count, AVG(views) as avg_views
            FROM ads 
            WHERE date > datetime('now', '-30 days')
            AND category IS NOT NULL
            GROUP BY category
            ORDER BY count DESC
            LIMIT 5
        """).fetchall()
    
    def get_similar_ads(self, ad_id, limit=3):
        """الحصول على إعلانات مشابهة"""
        try:
            current_ad = self.conn.execute(
                "SELECT product, description, category FROM ads WHERE id=?", 
                (ad_id,)
            ).fetchone()
            
            if not current_ad:
                return []
            
            similar = self.conn.execute("""
                SELECT id, product, price, wilaya, views 
                FROM ads 
                WHERE category=? AND id!=? AND status='active'
                ORDER BY views DESC, date DESC
                LIMIT ?
            """, (current_ad[2], ad_id, limit)).fetchall()
            
            return similar
        except:
            return []

# ==========================================
# 9. نظام الإشعارات والمراسلة
# ==========================================
def create_notification(username, message, notif_type="info"):
    """إنشاء إشعار جديد"""
    conn = get_connection()
    conn.execute(
        "INSERT INTO notifications(username, message, date, type) VALUES(?,?,datetime('now'),?)",
        (username, message, notif_type)
    )
    conn.commit()

def get_unread_notifications(username):
    """الحصول على عدد الإشعارات غير المقروءة"""
    conn = get_connection()
    return conn.execute(
        "SELECT COUNT(*) FROM notifications WHERE username=? AND read=0",
        (username,)
    ).fetchone()[0]

def get_unread_messages(username):
    """الحصول على عدد الرسائل غير المقروءة"""
    conn = get_connection()
    return conn.execute(
        "SELECT COUNT(*) FROM messages WHERE to_user=? AND read=0",
        (username,)
    ).fetchone()[0]

def toggle_favorite(username, ad_id):
    """إضافة أو إزالة من المفضلة"""
    conn = get_connection()
    existing = conn.execute(
        "SELECT id FROM favorites WHERE username=? AND ad_id=?",
        (username, ad_id)
    ).fetchone()
    
    if existing:
        conn.execute("DELETE FROM favorites WHERE id=?", (existing[0],))
        conn.commit()
        return False
    else:
        conn.execute(
            "INSERT INTO favorites(username, ad_id, saved_date) VALUES(?,?,datetime('now'))",
            (username, ad_id)
        )
        conn.commit()
        return True

def report_ad(ad_id, username, reason):
    """الإبلاغ عن إعلان مخالف"""
    conn = get_connection()
    conn.execute(
        "INSERT INTO reports(ad_id, reported_by, reason, date) VALUES(?,?,?,datetime('now'))",
        (ad_id, username, reason)
    )
    conn.commit()
    create_notification("admin", f"🚨 بلاغ جديد: إعلان {ad_id}", "warning")

def log_activity(username, action, details=""):
    """تسجيل نشاط المستخدم"""
    conn = get_connection()
    conn.execute(
        "INSERT INTO activity_log(username, action, details, date, ip) VALUES(?,?,?,datetime('now'),?)",
        (username, action, details, st.session_state.get("ip", "unknown"))
    )
    conn.commit()

def hash_password(password, salt):
    """تشفير كلمة المرور"""
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()

# ==========================================
# 10. نظام الدردشة المتطور
# ==========================================
def show_chat_system(conn):
    """عرض نظام المحادثات"""
    st.header("💬 صندوق الرسائل")
    user = st.session_state.user
    
    # الحصول على قائمة المحادثات
    contacts = conn.execute("""
        SELECT DISTINCT 
            CASE WHEN from_user = ? THEN to_user ELSE from_user END as contact,
            MAX(date) as last_msg,
            (SELECT COUNT(*) FROM messages WHERE to_user=? AND from_user=contact AND read=0) as unread
        FROM messages 
        WHERE from_user = ? OR to_user = ?
        GROUP BY contact
        ORDER BY last_msg DESC
    """, (user, user, user, user)).fetchall()
    
    if not contacts:
        st.info("📭 لا توجد محادثات نشطة حالياً.")
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📋 المحادثات")
        contact_list = []
        contact_ids = []
        for c in contacts:
            unread_badge = f" 🔴 ({c[2]})" if c[2] > 0 else ""
            contact_list.append(f"{c[0]}{unread_badge}")
            contact_ids.append(c[0])
        
        if contact_list:
            selected_idx = st.radio("اختر محادثة:", range(len(contact_list)), 
                                   format_func=lambda x: contact_list[x])
            selected_contact = contact_ids[selected_idx]
    
    with col2:
        if selected_contact:
            st.subheader(f"💭 الدردشة مع {selected_contact}")
            
            # تحديث الرسائل كمقروءة
            conn.execute("UPDATE messages SET read=1 WHERE from_user=? AND to_user=?", 
                        (selected_contact, user))
            conn.commit()
            
            # عرض الرسائل
            messages = conn.execute("""
                SELECT from_user, message, date 
                FROM messages 
                WHERE (from_user=? AND to_user=?) OR (from_user=? AND to_user=?)
                ORDER BY date ASC
            """, (user, selected_contact, selected_contact, user)).fetchall()
            
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for msg in messages:
                if msg[0] == user:
                    st.markdown(f"""
                        <div style="display: flex; justify-content: flex-end; margin: 10px;">
                            <div class="chat-bubble chat-sent">
                                <b>أنت:</b><br>{msg[1]}<br>
                                <small style="color: #666;">{msg[2][11:16]}</small>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div style="display: flex; justify-content: flex-start; margin: 10px;">
                            <div class="chat-bubble chat-received">
                                <b>{msg[0]}:</b><br>{msg[1]}<br>
                                <small style="color: #666;">{msg[2][11:16]}</small>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # إرسال رسالة جديدة
            with st.form(f"send_msg_{selected_contact}", clear_on_submit=True):
                new_msg = st.text_input("✍️ اكتب رسالتك هنا...")
                sent = st.form_submit_button("📤 إرسال")
                
                if sent and new_msg:
                    conn.execute(
                        "INSERT INTO messages(from_user, to_user, message, date) VALUES(?,?,?,datetime('now'))",
                        (user, selected_contact, new_msg)
                    )
                    conn.commit()
                    create_notification(selected_contact, f"📨 رسالة جديدة من {user}", "message")
                    st.rerun()

# ==========================================
# 11. المساعد الذكي
# ==========================================
def show_ai_assistant():
    """عرض المساعد الذكي"""
    st.markdown('<div class="ai-suggestion">', unsafe_allow_html=True)
    st.header("🤖 المساعد الذكي")
    
    conn = get_connection()
    ai = AIEngine()
    
    # إحصائيات ذكية
    st.subheader("📈 رؤى وتحليلات")
    
    # أفضل وقت للنشر
    peak_hours = conn.execute("""
        SELECT strftime('%H', visit_date) as hour, COUNT(*) as views
        FROM site_analytics
        WHERE visit_date > datetime('now', '-7 days')
        GROUP BY hour
        ORDER BY views DESC
        LIMIT 1
    """).fetchone()
    
    if peak_hours:
        st.success(f"⏰ أفضل وقت لنشر إعلانك: الساعة {peak_hours[0]}:00")
    
    # الفئات الرائجة
    trending = ai.get_trending_categories()
    if trending:
        st.info(f"🔥 الفئات الأكثر طلباً: {', '.join([t[0] for t in trending[:3]])}")
        
        # رسم بياني للفئات
        fig = px.bar(
            x=[t[0] for t in trending],
            y=[t[1] for t in trending],
            title="📊 الفئات الأكثر نشاطاً",
            labels={'x': 'الفئة', 'y': 'عدد الإعلانات'},
            color_discrete_sequence=['#006633', '#d21034', '#ffd700']
        )
        fig.update_layout(
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Cairo", size=12)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 12. لوحة تحكم الإدارة السرية
# ==========================================
def admin_dashboard(conn):
    """لوحة تحكم الإدارة"""
    st.markdown("""
        <div class="admin-section">
            <h2 style="color:white; text-align:center;">🔐 لوحة تحكم الإدارة السرية</h2>
            <p style="color:white; text-align:center; opacity:0.9;">مرحباً بك أيها المسؤول</p>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👥 المستخدمين", 
        "📊 إحصائيات متقدمة", 
        "🚫 إدارة المحتوى",
        "📝 سجل النشاطات",
        "🚨 التقارير"
    ])
    
    with tab1:
        st.subheader("👥 قائمة المستخدمين")
        users_df = pd.read_sql_query("""
            SELECT username, role, email, phone, verified, banned, ad_count, last_login 
            FROM users ORDER BY last_login DESC
        """, conn)
        st.dataframe(users_df, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            user_to_manage = st.selectbox("اختر مستخدم", users_df['username'].tolist())
            if st.button("🚫 حظر/إلغاء حظر", use_container_width=True):
                current = conn.execute("SELECT banned FROM users WHERE username=?", (user_to_manage,)).fetchone()[0]
                conn.execute("UPDATE users SET banned=? WHERE username=?", (1 if current == 0 else 0, user_to_manage))
                conn.commit()
                st.success(f"✅ تم تحديث حالة المستخدم {user_to_manage}")
                st.rerun()
        
        with col2:
            if st.button("⭐ جعل مسؤول", use_container_width=True):
                conn.execute("UPDATE users SET role='admin' WHERE username=?", (user_to_manage,))
                conn.commit()
                st.success(f"✅ تم ترقية {user_to_manage} إلى مسؤول")
    
    with tab2:
        # إحصائيات الزوار
        visits_df = pd.read_sql_query("""
            SELECT date(visit_date) as visit_date, COUNT(*) as visits 
            FROM site_analytics 
            GROUP BY date(visit_date)
            ORDER BY visit_date DESC
            LIMIT 30
        """, conn)
        
        if not visits_df.empty:
            fig = px.line(visits_df, x='visit_date', y='visits', 
                         title="📈 إحصائيات الزيارات اليومية",
                         labels={'visit_date': 'التاريخ', 'visits': 'عدد الزيارات'},
                         line_shape='spline')
            fig.update_traces(line_color='#d21034', line_width=3)
            st.plotly_chart(fig, use_container_width=True)
        
        # إحصائيات سريعة
        col1, col2, col3, col4 = st.columns(4)
        users, visitors, ads, views = get_stats()
        with col1:
            st.metric("👥 المستخدمين", users)
        with col2:
            st.metric("👁️ الزيارات", visitors)
        with col3:
            st.metric("📦 الإعلانات", ads)
        with col4:
            st.metric("⭐ المشاهدات", views)
        
        # أحدث الزيارات
        st.subheader("🕐 أحدث الزيارات")
        recent_visits = pd.read_sql_query("""
            SELECT ip, visit_date, page FROM site_analytics 
            ORDER BY visit_date DESC LIMIT 20
        """, conn)
        st.dataframe(recent_visits, use_container_width=True)
    
    with tab3:
        st.subheader("🚫 إدارة الإعلانات")
        ads_to_manage = conn.execute("""
            SELECT id, product, owner, views, status, featured 
            FROM ads ORDER BY id DESC LIMIT 50
        """).fetchall()
        
        for ad in ads_to_manage:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            col1.write(f"📦 **{ad[1]}** (بواسطة: {ad[2]}) - 👁️ {ad[3]}")
            
            if col2.button("⭐ تمييز", key=f"feature_{ad[0]}"):
                conn.execute("UPDATE ads SET featured=1 WHERE id=?", (ad[0],))
                conn.commit()
                st.rerun()
            
            if col3.button("🚫 إخفاء", key=f"hide_{ad[0]}"):
                conn.execute("UPDATE ads SET status='hidden' WHERE id=?", (ad[0],))
                conn.commit()
                st.rerun()
            
            if col4.button("❌ حذف", key=f"del_{ad[0]}"):
                conn.execute("DELETE FROM ads WHERE id=?", (ad[0],))
                conn.commit()
                st.rerun()
    
    with tab4:
        st.subheader("📝 سجل النشاطات")
        logs_df = pd.read_sql_query("""
            SELECT username, action, details, date, ip 
            FROM activity_log 
            ORDER BY date DESC LIMIT 100
        """, conn)
        st.dataframe(logs_df, use_container_width=True)
    
    with tab5:
        st.subheader("🚨 التقارير المعلقة")
        reports = conn.execute("""
            SELECT r.id, a.product, r.reported_by, r.reason, r.date 
            FROM reports r JOIN ads a ON r.ad_id = a.id 
            WHERE r.status='pending'
        """).fetchall()
        
        if reports:
            for report in reports:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    col1.warning(f"📌 {report[1]} - {report[3]} (مبلغ: {report[2]})")
                    if col2.button("✅ معالجة", key=f"resolve_{report[0]}"):
                        conn.execute("UPDATE reports SET status='resolved' WHERE id=?", (report[0],))
                        conn.commit()
                        st.rerun()
                    if col3.button("❌ حذف الإعلان", key=f"delete_ad_{report[0]}"):
                        conn.execute("DELETE FROM ads WHERE id=?", (report[1],))
                        conn.execute("UPDATE reports SET status='resolved' WHERE id=?", (report[0],))
                        conn.commit()
                        st.rerun()
        else:
            st.info("✅ لا توجد تقارير معلقة")

# ==========================================
# 13. صفحة السوق الذكي
# ==========================================
def show_market(conn):
    """عرض السوق مع الفلاتر"""
    st.header("🛍️ السوق الذكي")
    
    # تسجيل زيارة الصفحة
    st.session_state.current_page = "market"
    
    # عرض الفلاتر
    render_filters_ui()
    
    # بناء الاستعلام
    query = """
        SELECT a.*, 
               IFNULL(AVG(r.rating),0) as avg_r, 
               COUNT(r.rating) as count_r,
               (SELECT COUNT(*) FROM favorites f WHERE f.ad_id = a.id) as fav_count
        FROM ads a 
        LEFT JOIN ratings r ON a.id = r.ad_id 
        WHERE a.status='active'
    """
    params = []
    
    filters = st.session_state.filters
    
    # تطبيق الفلاتر
    if filters["wilaya"] != "الكل":
        query += " AND a.wilaya LIKE ?"
        params.append(f"%{filters['wilaya']}%")
    
    if filters["category"] != "الكل":
        query += " AND a.category = ?"
        params.append(filters["category"])
    
    query += " AND a.price BETWEEN ? AND ?"
    params.extend([filters["min_price"], filters["max_price"]])
    
    if filters["featured_only"]:
        query += " AND a.featured = 1"
    
    if filters["date_range"] == "اليوم":
        query += " AND date(a.date) = date('now')"
    elif filters["date_range"] == "الأسبوع":
        query += " AND a.date > datetime('now', '-7 days')"
    elif filters["date_range"] == "الشهر":
        query += " AND a.date > datetime('now', '-30 days')"
    
    query += " GROUP BY a.id"
    
    # الترتيب
    if filters["sort_by"] == "الأحدث":
        query += " ORDER BY a.id DESC"
    elif filters["sort_by"] == "الأقدم":
        query += " ORDER BY a.id ASC"
    elif filters["sort_by"] == "الأعلى سعراً":
        query += " ORDER BY a.price DESC"
    elif filters["sort_by"] == "الأقل سعراً":
        query += " ORDER BY a.price ASC"
    elif filters["sort_by"] == "الأكثر مشاهدة":
        query += " ORDER BY a.views DESC"
    elif filters["sort_by"] == "الأعلى تقييماً":
        query += " ORDER BY avg_r DESC"
    
    # تنفيذ الاستعلام
    ads = conn.execute(query, params).fetchall()
    
    # تحويل إلى DataFrame
    columns = ["id","product","price","phone","wilaya","description","date","owner","views",
               "featured","category","images","status","avg_r","count_r","fav_count"]
    df = pd.DataFrame(ads, columns=columns)
    
    # تطبيق البحث النصي
    if filters["search_query"]:
        search = filters["search_query"].lower()
        df = df[
            df["product"].str.contains(search, case=False, na=False) | 
            df["description"].str.contains(search, case=False, na=False)
        ]
    
    st.markdown(f"### 📊 النتائج: {len(df)} إعلان")
    
    if len(df) > 0:
        ai = AIEngine()
        items_per_page = 5
        total_pages = max(1, (len(df) + items_per_page - 1) // items_per_page)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            page = st.number_input("الصفحة", min_value=1, max_value=total_pages, value=1)
        with col2:
            st.write(f"من {len(df)} إعلان")
        
        start_idx = (page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, len(df))
        
        for _, ad in df.iloc[start_idx:end_idx].iterrows():
            # تحديث المشاهدات
            conn.execute("UPDATE ads SET views = views + 1 WHERE id=?", (ad['id'],))
            conn.commit()
            
            # عرض الإعلان
            with st.container():
                st.markdown(f"""
                <div class="ad-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:20px;">
                        <div style="flex:2;">
                            <h2 style="margin:0; color:#d21034; font-size:1.8rem;">{ad['product']} 
                            {f'<span class="badge-premium">⭐ مميز</span>' if ad['featured'] else ''}</h2>
                            <p style="margin:15px 0; color:#555; line-height:1.6;">{ad['description'][:200]}...</p>
                            <p style="margin:10px 0;">
                                <span style="background:#f0f0f0; padding:5px 15px; border-radius:50px;">📍 {ad['wilaya']}</span>
                                <span style="background:#f0f0f0; padding:5px 15px; border-radius:50px; margin-right:10px;">📅 {ad['date'][:10]}</span>
                            </p>
                            <p style="color:#666;">
                                👁️ {ad['views']} مشاهدة | 
                                ⭐ {ad['avg_r']:.1f} ({ad['count_r']}) | 
                                💖 {ad['fav_count']} تفضيل
                            </p>
                        </div>
                        <div style="flex:1; text-align:center;">
                            <div class="price-tag">{ad['price']:,} دج</div>
                            <p style="margin-top:10px; color:#006633;">👤 {ad['owner']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("📞 واتساب", key=f"wa_{ad['id']}", use_container_width=True):
                        clean_phone = re.sub(r'\D', '', str(ad['phone']))
                        wa_link = f"https://wa.me/213{clean_phone[-9:]}"
                        js = f"window.open('{wa_link}')"
                        st.components.v1.html(f"<script>{js}</script>", height=0)
                
                with col2:
                    if st.button("❤️ حفظ", key=f"fav_{ad['id']}", use_container_width=True):
                        toggle_favorite(st.session_state.user, ad['id'])
                        st.rerun()
                
                with col3:
                    if st.button("💬 مراسلة", key=f"msg_{ad['id']}", use_container_width=True):
                        st.session_state[f"chat_{ad['owner']}"] = True
                
                with col4:
                    if st.button("🚨 إبلاغ", key=f"report_{ad['id']}", use_container_width=True):
                        st.session_state[f"report_{ad['id']}"] = True
                
                # نافذة الإبلاغ
                if st.session_state.get(f"report_{ad['id']}", False):
                    with st.expander("سبب الإبلاغ", expanded=True):
                        reason = st.selectbox("السبب", ["إعلان مزيف", "محتوى غير لائق", "احتيال", "تكرار"], key=f"reason_{ad['id']}")
                        if st.button("تأكيد الإبلاغ", key=f"confirm_{ad['id']}"):
                            report_ad(ad['id'], st.session_state.user, reason)
                            st.success("✅ تم استلام البلاغ، شكراً لمساعدتك")
                            st.session_state[f"report_{ad['id']}"] = False
                            st.rerun()
                
                # إعلانات مشابهة
                if st.checkbox("🔍 اقتراحات مشابهة", key=f"similar_{ad['id']}"):
                    similar = ai.get_similar_ads(ad['id'])
                    if similar:
                        st.markdown("#### 🎯 قد يعجبك أيضاً:")
                        for sim in similar:
                            st.markdown(f"""
                            <div style="background:#f8f9fa; padding:15px; border-radius:15px; margin:10px 0;">
                                <b>{sim[1]}</b> - {sim[2]:,} دج (ولاية {sim[3]}) 👁️ {sim[4]}
                            </div>
                            """, unsafe_allow_html=True)
    else:
        st.info("😕 لا توجد إعلانات تطابق معايير البحث")

# ==========================================
# 14. صفحة نشر الإعلان
# ==========================================
def post_ad(conn):
    """نشر إعلان جديد"""
    st.header("📢 نشر إعلان جديد")
    
    ai = AIEngine()
    
    with st.form("new_ad"):
        col1, col2 = st.columns(2)
        with col1:
            product = st.text_input("اسم المنتج")
            category = st.selectbox("التصنيف", ["إلكترونيات", "عقارات", "سيارات", "خدمات", "أخرى"])
        with col2:
            price = st.number_input("السعر (دج)", min_value=0, step=100)
            wilaya = st.selectbox("الولاية", [f"{i:02d}" for i in range(1, 59)])
        
        phone = st.text_input("رقم الهاتف")
        description = st.text_area("وصف المنتج")
        
        # توقع السعر الذكي
        if PRICE_PREDICTION_ENABLED and price == 0:
            prediction = ai.predict_price(category, description, wilaya)
            if prediction:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #e8f5e8, #c8e6c9); padding: 25px; border-radius: 20px; margin: 20px 0; border-right: 8px solid #006633;">
                        <h4 style="color: #006633; margin-bottom: 15px;">🔮 توقع السعر الذكي</h4>
                        <p style="font-size: 1.3rem;"><b>{prediction['predicted']:,} دج</b> (السعر المتوقع)</p>
                        <p>النطاق السعري: {prediction['min']:,} - {prediction['max']:,} دج</p>
                        <p>متوسط السوق: {prediction['avg']:,} دج</p>
                        <small>بناءً على {prediction['sample_size']} إعلان مشابه في ولاية {wilaya}</small>
                    </div>
                """, unsafe_allow_html=True)
        
        submitted = st.form_submit_button("🚀 نشر الإعلان", use_container_width=True)
        
        if submitted:
            if product and price > 0 and phone:
                # التحقق من عدد الإعلانات
                ad_count = conn.execute(
                    "SELECT ad_count FROM users WHERE username=?", 
                    (st.session_state.user,)
                ).fetchone()[0]
                
                if ad_count >= 10 and st.session_state.role != "admin":
                    st.error("⚠️ لقد وصلت للحد الأقصى (10 إعلانات)")
                else:
                    conn.execute("""
                        INSERT INTO ads(product, price, phone, wilaya, description, date, owner, category) 
                        VALUES(?,?,?,?,?,datetime('now'),?,?)
                    """, (product, price, phone, wilaya, description, st.session_state.user, category))
                    
                    conn.execute(
                        "UPDATE users SET ad_count = ad_count + 1 WHERE username=?", 
                        (st.session_state.user,)
                    )
                    conn.commit()
                    
                    log_activity(st.session_state.user, "post_ad", f"نشر: {product}")
                    create_notification(st.session_state.user, "✅ تم نشر إعلانك بنجاح!", "success")
                    
                    st.success("✅ تم نشر الإعلان بنجاح!")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
            else:
                st.error("❌ يرجى ملء جميع الحقول المطلوبة")

# ==========================================
# 15. صفحة المفضلة
# ==========================================
def show_favorites(conn):
    """عرض الإعلانات المفضلة"""
    st.header("⭐ المفضلة")
    
    favorites = conn.execute("""
        SELECT a.* FROM favorites f 
        JOIN ads a ON f.ad_id = a.id 
        WHERE f.username=?
        ORDER BY f.saved_date DESC
    """, (st.session_state.user,)).fetchall()
    
    if favorites:
        for fav in favorites:
            with st.container():
                st.markdown(f"""
                <div class="ad-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <h3 style="color:#d21034;">{fav[1]}</h3>
                            <p>{fav[5][:100]}</p>
                            <p>💰 {fav[2]:,} دج | 📍 {fav[4]}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("🗑️ إزالة من المفضلة", key=f"remove_{fav[0]}", use_container_width=True):
                    toggle_favorite(st.session_state.user, fav[0])
                    st.rerun()
    else:
        st.info("💔 لا توجد إعلانات في المفضلة")

# ==========================================
# 16. صفحة الإشعارات
# ==========================================
def show_notifications(conn):
    """عرض الإشعارات"""
    st.header("🔔 الإشعارات")
    
    notifications = conn.execute("""
        SELECT id, message, date, type, read 
        FROM notifications 
        WHERE username=?
        ORDER BY date DESC
    """, (st.session_state.user,)).fetchall()
    
    if notifications:
        for notif in notifications:
            icon = "📌" if notif[3] == "info" else "⚠️" if notif[3] == "warning" else "🎉" if notif[3] == "success" else "📢"
            with st.container():
                col1, col2 = st.columns([10, 1])
                with col1:
                    bg_color = "#f0f0f0" if notif[4] else "#ffffff"
                    st.markdown(f"""
                    <div style="background:{bg_color}; padding:20px; border-radius:15px; margin:10px 0; border-right:5px solid #d21034;">
                        <div style="display:flex; align-items:center; gap:10px;">
                            <span style="font-size:1.5rem;">{icon}</span>
                            <div>
                                <p style="font-size:1.1rem; margin:0;"><b>{notif[1]}</b></p>
                                <p style="color:#666; margin:5px 0 0 0;">🕐 {notif[2][:16]}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if not notif[4] and st.button("✓", key=f"read_{notif[0]}", help="تحديد كمقروء"):
                        conn.execute("UPDATE notifications SET read=1 WHERE id=?", (notif[0],))
                        conn.commit()
                        st.rerun()
    else:
        st.info("📭 لا توجد إشعارات")

# ==========================================
# 17. نظام المصادقة المتكامل
# ==========================================
def auth_page():
    """صفحة تسجيل الدخول والتسجيل"""
    
    # إضافة أزرار المشاركة الاجتماعية (طلبك)
    add_social_share_buttons()
    
    # إضافة ستايل تيك توك (طلبك)
    add_tiktok_style()
    
    st.markdown("""
        <div class="main-header">
            <h1 style="color:white; font-size:3rem;">🇩🇿 راسم تيتانيوم ألترا</h1>
            <p style="font-size:1.5rem; margin-top:20px;">أول سوق إلكتروني جزائري متخصص في الهواتف</p>
            <p style="font-size:1.2rem; opacity:0.9;">بيع وشراء في 58 ولاية - آمن وسريع ومجاني</p>
        </div>
    """, unsafe_allow_html=True)
    
    # عرض الإحصائيات
    users, visitors, ads, views = get_stats()
    st.markdown(f"""
        <div class="stats-container">
            <div class="stat-box"><div class="stat-val">{users:,}</div><div class="stat-label">مستخدم مسجل</div></div>
            <div class="stat-box"><div class="stat-val">{visitors:,}</div><div class="stat-label">زيارة إجمالية</div></div>
            <div class="stat-box"><div class="stat-val">{ads:,}</div><div class="stat-label">إعلان نشط</div></div>
            <div class="stat-box"><div class="stat-val">{views:,}</div><div class="stat-label">مشاهدة</div></div>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 تسجيل الدخول", "📝 حساب جديد"])
    conn = get_connection()
    
    with tab1:
        username = st.text_input("اسم المستخدم", key="login_user")
        password = st.text_input("كلمة المرور", type="password", key="login_pass")
        
        if st.button("دخول", use_container_width=True):
            # التحقق من محاولات الدخول الفاشلة
            attempts = conn.execute("""
                SELECT COUNT(*) FROM login_attempts 
                WHERE username=? AND attempt_time > datetime('now', '-15 minutes')
            """, (username,)).fetchone()[0]
            
            if attempts >= 5:
                st.error("🚫 تم حظر الدخول مؤقتاً بسبب كثرة المحاولات الفاشلة")
            else:
                user = conn.execute(
                    "SELECT password, salt, role, banned FROM users WHERE username=?", 
                    (username,)
                ).fetchone()
                
                if user:
                    if user[3] == 1:
                        st.error("🚫 هذا الحساب محظور")
                    elif user[0] == hash_password(password, user[1]):
                        st.session_state.user = username
                        st.session_state.role = user[2]
                        
                        conn.execute(
                            "UPDATE users SET last_login=? WHERE username=?", 
                            (datetime.datetime.now(), username)
                        )
                        conn.commit()
                        
                        log_activity(username, "login", "تسجيل دخول ناجح")
                        st.rerun()
                    else:
                        conn.execute(
                            "INSERT INTO login_attempts(username, attempt_time) VALUES(?,datetime('now'))",
                            (username,)
                        )
                        conn.commit()
                        st.error("❌ كلمة مرور خاطئة")
                else:
                    st.error("❌ المستخدم غير موجود")
    
    with tab2:
        new_user = st.text_input("اسم المستخدم", key="new_user")
        new_pass = st.text_input("كلمة المرور", type="password", key="new_pass")
        email = st.text_input("البريد الإلكتروني")
        phone = st.text_input("رقم الهاتف")
        
        if st.button("تسجيل", use_container_width=True):
            if new_user and new_pass:
                if len(new_user) < 3:
                    st.error("❌ اسم المستخدم قصير جداً (3 أحرف على الأقل)")
                elif len(new_pass) < 6:
                    st.error("❌ كلمة المرور قصيرة جداً (6 أحرف على الأقل)")
                elif email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    st.error("❌ بريد إلكتروني غير صالح")
                else:
                    try:
                        salt = secrets.token_hex(16)
                        hashed = hash_password(new_pass, salt)
                        
                        conn.execute("""
                            INSERT INTO users (username, password, salt, email, phone, role, last_login) 
                            VALUES (?,?,?,?,?,?,datetime('now'))
                        """, (new_user, hashed, salt, email, phone, 'user'))
                        conn.commit()
                        
                        create_notification(new_user, "🎉 مرحباً بك في RASSIM DZ! ابدأ الآن بنشر إعلانك الأول", "success")
                        log_activity(new_user, "register", "تسجيل حساب جديد")
                        
                        st.success("✅ تم التسجيل بنجاح! سجل الدخول الآن")
                    except Exception as e:
                        st.error("⚠️ اسم المستخدم موجود مسبقاً")
            else:
                st.error("❌ يرجى ملء الحقول المطلوبة")

# ==========================================
# 18. الصفحة الرئيسية (Dashboard)
# ==========================================
def dashboard():
    """لوحة التحكم الرئيسية"""
    log_visitor()
    
    conn = get_connection()
    
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center; padding:20px; background:linear-gradient(135deg,#006633,#d21034); border-radius:15px; margin-bottom:20px;">
            <h3 style="color:white; margin:0;">🎖️ {st.session_state.user}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # عدد الإشعارات غير المقروءة
        unread_notif = get_unread_notifications(st.session_state.user)
        unread_msgs = get_unread_messages(st.session_state.user)
        total_unread = unread_notif + unread_msgs
        notif_badge = f" 🔔 ({total_unread})" if total_unread > 0 else " 🔔"
        
        # إحصائيات سريعة
        online = conn.execute(
            "SELECT COUNT(DISTINCT ip) FROM site_analytics WHERE visit_date > datetime('now', '-5 minutes')"
        ).fetchone()[0]
        st.info(f"🟢 الزوار النشطون: {online}")
        
        # القائمة الرئيسية
        menu_options = ["🏠 السوق الذكي", "📢 إعلان جديد", "⭐ المفضلة", "💬 الرسائل", notif_badge, "🤖 المساعد الذكي"]
        
        # إضافة لوحة الإدارة للمسؤولين
        if st.session_state.role == "admin":
            menu_options.append("🛡️ لوحة الإدارة")
        
        choice = st.radio("القائمة", menu_options, key="main_menu")
        
        with st.expander("🔐 المنطقة الشخصية"):
            if st.button("🚪 تسجيل الخروج", use_container_width=True):
                log_activity(st.session_state.user, "logout", "تسجيل خروج")
                st.session_state.user = None
                st.rerun()
            
            if st.session_state.role == "admin":
                st.success("👑 أنت مسؤول")
        
        with st.expander("🎯 الفلاتر النشطة"):
            st.json(st.session_state.filters)
    
    # توجيه الصفحات
    if choice == "🏠 السوق الذكي":
        show_market(conn)
    elif choice == "📢 إعلان جديد":
        post_ad(conn)
    elif choice == "⭐ المفضلة":
        show_favorites(conn)
    elif choice == "💬 الرسائل":
        show_chat_system(conn)
    elif choice == notif_badge:
        show_notifications(conn)
    elif choice == "🤖 المساعد الذكي":
        show_ai_assistant()
    elif choice == "🛡️ لوحة الإدارة" and st.session_state.role == "admin":
        admin_dashboard(conn)

# ==========================================
# 19. التشغيل الرئيسي
# ==========================================
def main():
    """الدالة الرئيسية للتشغيل"""
    
    # تشغيل الصفحة المناسبة
    if st.session_state.user:
        dashboard()
    else:
        auth_page()

if __name__ == "__main__":
    main()
