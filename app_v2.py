import streamlit as st
import sqlite3
import pandas as pd
import hashlib
import re
import datetime
import secrets
import os
import time
import plotly.express as px
import plotly.graph_objects as go
import warnings
from functools import wraps

warnings.filterwarnings('ignore')

# ==========================================
# 1. إعدادات الصفحة - مع الشعار المطلوب
# ==========================================
st.set_page_config(
    page_title="RASSIM OS PRO • الجزائر",
    page_icon="💠",  # يمكنك تغييرها إلى رابط صورتك
    layout="wide",
    initial_sidebar_state="auto"
)

# ==========================================
# 2. SEO Meta Tags
# ==========================================
st.markdown("""
<meta name="description" content="RASSIM OS PRO - أول سوق إلكتروني جزائري بتقنية OS Style المتطورة">
<meta name="keywords" content="واد كنيس, هواتف الجزائر, OS Pro, sleek design, راسم تيتانيوم">
<meta name="author" content="RASSIM DZ">
""", unsafe_allow_html=True)

# ==========================================
# 3. JavaScript للنسخ المحسن
# ==========================================
st.markdown("""
<script>
// نظام النسخ المتطور مع تأثيرات
function copyLink() {
    navigator.clipboard.writeText('https://racim-phone.streamlit.app/');
    
    // تغيير لون الزر
    const btn = document.getElementById('copyBtn');
    if (btn) {
        btn.style.background = 'linear-gradient(135deg, #00ffff, #ff00ff)';
        btn.style.transform = 'scale(1.2) rotate(360deg)';
    }
    
    // رسائل تشجيعية متنوعة
    const messages = [
        '✅ تم نسخ الرابط - الدزة واجدة! 🇩🇿',
        '🔥 شارك مع صحابك واكسب الثواب!',
        '⚡ راهي الدزة - راهي التوانسة!',
        '💫 58 ولاية - كلها في رابط وحدة!',
        '🎯 واد كنيس الجديد - أحسن وأسرع!'
    ];
    const randomMsg = messages[Math.floor(Math.random() * messages.length)];
    alert(randomMsg);
    
    // إعادة الزر لحالته الطبيعية
    setTimeout(() => {
        if (btn) {
            btn.style.background = '';
            btn.style.transform = '';
        }
    }, 500);
    
    // تسجيل النشاط (للتحليلات)
    console.log('تم نسخ الرابط - ' + new Date().toLocaleTimeString());
}

// تأثير المشاركة الجماعية
function shareAll() {
    const icons = document.querySelectorAll('.os-icon');
    icons.forEach((icon, index) => {
        setTimeout(() => {
            icon.style.transform = 'scale(1.3) rotate(10deg)';
            icon.style.background = 'rgba(0, 255, 255, 0.3)';
            setTimeout(() => {
                icon.style.transform = '';
                icon.style.background = '';
            }, 300);
        }, index * 150);
    });
    
    // رسالة حماسية
    setTimeout(() => {
        alert('🚀 الدزة راهي تمشي! شارك في كل مكان!');
    }, 600);
}
</script>
""", unsafe_allow_html=True)

# ==========================================
# 4. التصميم المتطور - Sleek OS Style Pro
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    direction: rtl;
    box-sizing: border-box;
}

/* ===== خلفية متحركة ===== */
.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2a 50%, #0a0a0f 100%);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: #ffffff;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ===== تأثير الجسيمات المتحركة ===== */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(2px 2px at 10px 10px, rgba(0, 255, 255, 0.3), transparent),
        radial-gradient(2px 2px at 50px 100px, rgba(255, 0, 255, 0.3), transparent),
        radial-gradient(3px 3px at 200px 200px, rgba(0, 255, 255, 0.2), transparent),
        radial-gradient(2px 2px at 400px 300px, rgba(255, 0, 255, 0.2), transparent);
    background-repeat: repeat;
    background-size: 600px 600px;
    opacity: 0.1;
    pointer-events: none;
    z-index: 0;
    animation: float 20s linear infinite;
}

@keyframes float {
    0% { transform: translateY(0) translateX(0); }
    100% { transform: translateY(-100px) translateX(50px); }
}

/* ===== Glass Morphism متطور ===== */
.glass-panel {
    background: rgba(20, 20, 30, 0.6);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 24px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.glass-panel:hover {
    border-color: rgba(0, 255, 255, 0.2);
    box-shadow: 0 12px 48px rgba(0, 255, 255, 0.15);
}

/* ===== الهيدر المتطور ===== */
.os-header {
    background: rgba(10, 10, 20, 0.8);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    padding: 20px 30px;
    margin-bottom: 30px;
    position: sticky;
    top: 0;
    z-index: 100;
    animation: slideDown 0.5s ease;
}

@keyframes slideDown {
    from { transform: translateY(-100%); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

.os-title {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #00ffff, #ff00ff, #00ffff);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block;
    animation: gradientShift 5s ease infinite;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.os-version {
    background: rgba(255, 255, 255, 0.1);
    padding: 4px 12px;
    border-radius: 30px;
    font-size: 0.8rem;
    color: #888;
    margin-right: 10px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

/* ===== كروت إحصائية متطورة ===== */
.stMetric {
    background: rgba(20, 20, 30, 0.7) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 24px !important;
    padding: 25px 20px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative;
    overflow: hidden;
}

.stMetric::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(0, 255, 255, 0.1), transparent);
    opacity: 0;
    transition: opacity 0.4s;
}

.stMetric:hover::before {
    opacity: 1;
    animation: rotate 4s linear infinite;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.stMetric:hover {
    transform: translateY(-8px) scale(1.02);
    border-color: rgba(0, 255, 255, 0.3) !important;
    box-shadow: 0 16px 48px rgba(0, 255, 255, 0.2) !important;
}

.stMetric label {
    color: rgba(255, 255, 255, 0.6) !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px;
}

.stMetric [data-testid="stMetricValue"] {
    color: white !important;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    text-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
}

/* ===== أزرار متطورة ===== */
.stButton > button {
    background: rgba(30, 30, 40, 0.8) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 50px !important;
    color: white !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    padding: 14px 28px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative;
    overflow: hidden;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.2);
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
}

.stButton > button:hover::before {
    width: 300px;
    height: 300px;
}

.stButton > button:hover {
    background: rgba(50, 50, 60, 0.9) !important;
    border-color: rgba(0, 255, 255, 0.4) !important;
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(0, 255, 255, 0.2) !important;
}

/* ===== صناديق الإدخال المتطورة ===== */
.stTextInput input, 
.stTextArea textarea,
.stSelectbox select {
    background: rgba(20, 20, 30, 0.7) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 50px !important;
    color: white !important;
    padding: 14px 24px !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease;
}

.stTextInput input:focus, 
.stTextArea textarea:focus,
.stSelectbox select:focus {
    border-color: rgba(0, 255, 255, 0.4) !important;
    box-shadow: 0 0 0 4px rgba(0, 255, 255, 0.1) !important;
    transform: scale(1.02);
}

.stTextInput label, 
.stTextArea label,
.stSelectbox label {
    color: rgba(255, 255, 255, 0.8) !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    margin-bottom: 8px !important;
}

/* ===== القائمة الجانبية المتطورة ===== */
section[data-testid="stSidebar"] {
    background: rgba(10, 10, 15, 0.95) !important;
    backdrop-filter: blur(20px);
    border-left: 1px solid rgba(255, 255, 255, 0.05);
    padding: 20px !important;
}

section[data-testid="stSidebar"] .stRadio > div {
    gap: 8px;
}

section[data-testid="stSidebar"] .stRadio label {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 12px 16px;
    transition: all 0.3s ease;
    color: white !important;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(0, 255, 255, 0.1);
    border-color: rgba(0, 255, 255, 0.3);
    transform: translateX(-4px);
}

/* ===== بطاقات الإعلانات المتطورة ===== */
.os-card {
    background: rgba(20, 20, 30, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 28px;
    padding: 28px;
    margin-bottom: 20px;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.os-card::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 100%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(0, 255, 255, 0.05), transparent);
    transform: rotate(45deg);
    animation: shine 3s infinite;
}

@keyframes shine {
    0% { transform: translateX(-100%) rotate(45deg); }
    100% { transform: translateX(100%) rotate(45deg); }
}

.os-card:hover {
    transform: translateX(-8px) translateY(-4px);
    border-color: rgba(0, 255, 255, 0.3);
    box-shadow: 0 20px 48px rgba(0, 255, 255, 0.2);
}

.os-card-title {
    font-size: 1.6rem;
    font-weight: 600;
    color: white;
    margin-bottom: 12px;
    background: linear-gradient(135deg, #fff, #e0e0e0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.os-card-price {
    background: rgba(0, 255, 255, 0.15);
    border: 1px solid rgba(0, 255, 255, 0.3);
    color: #00ffff;
    padding: 10px 24px;
    border-radius: 50px;
    display: inline-block;
    font-weight: 600;
    font-size: 1.3rem;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
}

/* ===== أزرار المشاركة المتطورة ===== */
.os-share {
    background: rgba(20, 20, 30, 0.8);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 60px;
    padding: 12px 24px;
    margin: 20px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 255, 0.1); }
    50% { box-shadow: 0 0 40px rgba(255, 0, 255, 0.2); }
}

.os-share-icons {
    display: flex;
    gap: 12px;
}

.os-icon {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.05);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid rgba(255, 255, 255, 0.05);
    animation: float 3s ease-in-out infinite;
    cursor: pointer;
}

.os-icon:nth-child(1) { animation-delay: 0s; }
.os-icon:nth-child(2) { animation-delay: 0.1s; }
.os-icon:nth-child(3) { animation-delay: 0.2s; }
.os-icon:nth-child(4) { animation-delay: 0.3s; }

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}

.os-icon:hover {
    background: rgba(0, 255, 255, 0.15);
    border-color: rgba(0, 255, 255, 0.4);
    transform: scale(1.15) rotate(5deg);
}

.os-icon img {
    width: 22px;
    height: 22px;
    opacity: 0.8;
    transition: all 0.3s ease;
}

.os-icon:hover img {
    opacity: 1;
    filter: brightness(0) invert(1);
}

/* ===== فقاعات الدردشة المتطورة ===== */
.os-chat-sent {
    background: linear-gradient(135deg, rgba(0, 255, 255, 0.15), rgba(0, 200, 255, 0.15));
    border: 1px solid rgba(0, 255, 255, 0.3);
    color: white;
    padding: 14px 20px;
    border-radius: 24px 24px 8px 24px;
    margin: 12px 0;
    max-width: 80%;
    margin-left: auto;
    box-shadow: 0 8px 24px rgba(0, 255, 255, 0.1);
    animation: slideInLeft 0.3s ease;
}

.os-chat-received {
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
    padding: 14px 20px;
    border-radius: 24px 24px 24px 8px;
    margin: 12px 0;
    max-width: 80%;
    margin-right: auto;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    animation: slideInRight 0.3s ease;
}

@keyframes slideInLeft {
    from { transform: translateX(30px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes slideInRight {
    from { transform: translateX(-30px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

/* ===== العناوين ===== */
h1, h2, h3 {
    color: white !important;
    font-weight: 600 !important;
    letter-spacing: -0.5px;
}

h1 {
    font-size: 2.4rem !important;
    border-bottom: 2px solid rgba(0, 255, 255, 0.3);
    padding-bottom: 16px;
    margin-bottom: 28px !important;
    display: inline-block;
}

/* ===== شريط التمرير المتطور ===== */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.02);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #00ffff, #ff00ff);
    border-radius: 10px;
    transition: all 0.3s ease;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #ff00ff, #00ffff);
}

/* ===== التجاوب مع الجوال ===== */
@media screen and (max-width: 768px) {
    .os-header {
        padding: 15px 20px;
    }
    
    .os-title {
        font-size: 1.8rem;
    }
    
    .os-card-title {
        font-size: 1.3rem;
    }
    
    .os-card-price {
        font-size: 1.1rem;
        padding: 8px 16px;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        font-size: 2rem !important;
    }
}

/* ===== تنسيق الشعار ===== */
.sidebar-logo {
    text-align: center;
    padding: 10px;
    margin-bottom: 20px;
}

.sidebar-logo img {
    max-width: 80%;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 255, 255, 0.3);
    transition: all 0.3s ease;
}

.sidebar-logo img:hover {
    transform: scale(1.05);
    box-shadow: 0 15px 40px rgba(255, 0, 255, 0.4);
}

/* ===== تأثير خاص لزر النسخ ===== */
#copyBtn {
    position: relative;
    overflow: hidden;
}

#copyBtn::after {
    content: '📋';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(0);
    font-size: 1.5rem;
    opacity: 0;
    transition: all 0.3s;
}

#copyBtn:hover::after {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
}

#copyBtn:hover img {
    opacity: 0;
}

/* ===== عداد المشاركات ===== */
.share-counter {
    background: rgba(0,0,0,0.3);
    border-radius: 30px;
    padding: 4px 12px;
    font-size: 0.8rem;
    color: #00ffff;
    border: 1px solid rgba(0,255,255,0.3);
}

/* ===== رسالة عائمة ===== */
.floating-message {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: linear-gradient(135deg, #00ffff, #ff00ff);
    color: white;
    padding: 12px 24px;
    border-radius: 50px;
    font-weight: bold;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    z-index: 9999;
    animation: floatMessage 3s ease-in-out infinite;
    border: 2px solid white;
    cursor: pointer;
}

@keyframes floatMessage {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}
</style>

<!-- OS Header Pro -->
<div class="os-header">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div>
            <span class="os-title">RASSIM OS PRO</span>
            <span class="os-version">v3.0.0 • الجزائر</span>
        </div>
        <div style="display: flex; gap: 16px;">
            <span style="color: rgba(0,255,255,0.5);">⚡ 5G</span>
            <span style="color: rgba(255,0,255,0.5);">🔋 100%</span>
            <span style="color: rgba(255,255,255,0.3);">📶</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. إعدادات قاعدة البيانات
# ==========================================
DB = "rassim_os_pro.db"

def init_db():
    """تهيئة قاعدة البيانات"""
    try:
        conn = sqlite3.connect(DB, check_same_thread=False)
        cursor = conn.cursor()
        
        # جدول المستخدمين
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                salt TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                role TEXT DEFAULT 'user',
                verified INTEGER DEFAULT 0,
                banned INTEGER DEFAULT 0,
                ad_count INTEGER DEFAULT 0,
                last_login TEXT,
                date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # جدول الإعلانات
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price INTEGER NOT NULL,
                phone TEXT NOT NULL,
                wilaya TEXT NOT NULL,
                description TEXT,
                category TEXT DEFAULT 'أخرى',
                images TEXT,
                views INTEGER DEFAULT 0,
                featured INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                owner TEXT NOT NULL,
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner) REFERENCES users(username)
            )
        """)
        
        # جدول الرسائل
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                receiver TEXT NOT NULL,
                message TEXT NOT NULL,
                read INTEGER DEFAULT 0,
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sender) REFERENCES users(username),
                FOREIGN KEY (receiver) REFERENCES users(username)
            )
        """)
        
        # جدول المفضلة
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                ad_id INTEGER NOT NULL,
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users(username),
                FOREIGN KEY (ad_id) REFERENCES ads(id),
                UNIQUE(username, ad_id)
            )
        """)
        
        # جدول الإشعارات
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                message TEXT NOT NULL,
                type TEXT DEFAULT 'info',
                read INTEGER DEFAULT 0,
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        """)
        
        # جدول البلاغات
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad_id INTEGER NOT NULL,
                reporter TEXT NOT NULL,
                reason TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ad_id) REFERENCES ads(id),
                FOREIGN KEY (reporter) REFERENCES users(username)
            )
        """)
        
        # جدول الزوار
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS visitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT,
                page TEXT,
                date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        return conn
    except Exception as e:
        st.error(f"OS Error: {e}")
        return None

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB, check_same_thread=False)

# تهيئة قاعدة البيانات
init_db()

# ==========================================
# 6. دوال المساعدة
# ==========================================
def hash_password(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()

def create_notification(username, message, notif_type="info"):
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO notifications (username, message, type) VALUES (?, ?, ?)",
            (username, message, notif_type)
        )
        conn.commit()
    except:
        pass

def log_visitor():
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO visitors (ip, page) VALUES (?, ?)",
            (st.session_state.get('ip', 'unknown'), st.session_state.get('page', 'main'))
        )
        conn.commit()
    except:
        pass

def get_stats():
    try:
        conn = get_connection()
        users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        ads = conn.execute("SELECT COUNT(*) FROM ads WHERE status='active'").fetchone()[0]
        visitors = conn.execute("SELECT COUNT(*) FROM visitors").fetchone()[0]
        views = conn.execute("SELECT SUM(views) FROM ads").fetchone()[0] or 0
        return users, ads, visitors, views
    except:
        return 0, 0, 0, 0

# ==========================================
# 7. أزرار المشاركة OS Style Pro مع كود النسخ
# ==========================================
def show_social_share():
    site_url = "https://racim-phone.streamlit.app/"
    
    st.markdown(f"""
    <div class="os-share">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="background: linear-gradient(135deg, #00ffff, #ff00ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 1.3rem;">
                    🔥 الدزة
                </span>
                <span class="share-counter">🚀 58 ولاية</span>
            </div>
            
            <div class="os-share-icons">
                <a href="https://www.facebook.com/sharer/sharer.php?u={site_url}" target="_blank" title="فيسبوك - شارك مع العائلة" onclick="shareAll()">
                    <div class="os-icon"><img src="https://img.icons8.com/color/48/facebook-new.png"></div>
                </a>
                <a href="https://api.whatsapp.com/send?text=🔥 الدزة الجزائرية: {site_url}" target="_blank" title="واتساب - بزاف صحاب" onclick="shareAll()">
                    <div class="os-icon"><img src="https://img.icons8.com/color/48/whatsapp--v1.png"></div>
                </a>
                <a href="https://t.me/share/url?url={site_url}&text=🇩🇿 أول سوق إلكتروني جزائري" target="_blank" title="تيليغرام - قنوات الدزة" onclick="shareAll()">
                    <div class="os-icon"><img src="https://img.icons8.com/color/48/telegram-app--v1.png"></div>
                </a>
                <div id="copyBtn" class="os-icon" onclick="copyLink()" title="انسخ الرابط ووزع الدزة">
                    <img src="https://img.icons8.com/color/48/link--v1.png">
                </div>
            </div>
        </div>
        
        <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 16px; flex-wrap: wrap; gap: 12px;">
            <div style="display: flex; gap: 8px;">
                <span style="background: rgba(0,255,255,0.1); color: #00ffff; padding: 4px 12px; border-radius: 30px; font-size: 0.8rem; border: 1px solid rgba(0,255,255,0.3);">
                    ⚡ واد كنيس الجديد
                </span>
                <span style="background: rgba(255,0,255,0.1); color: #ff00ff; padding: 4px 12px; border-radius: 30px; font-size: 0.8rem; border: 1px solid rgba(255,0,255,0.3);">
                    🎯 أسرع وأحسن
                </span>
            </div>
            
            <div style="display: flex; align-items: center; gap: 16px;">
                <span style="color: rgba(255,255,255,0.4); font-size: 0.8rem;">
                    👥 شارك مع 10 صحاب
                </span>
                <span style="background: linear-gradient(135deg, #00ffff, #ff00ff); color: white; padding: 4px 16px; border-radius: 30px; font-size: 0.9rem; font-weight: 600;">
                    +1000 إعلان
                </span>
            </div>
        </div>
    </div>
    
    <!-- رسالة عائمة تشجيعية (تظهر بعد 3 ثواني) -->
    <script>
    setTimeout(function() {{
        const msg = document.createElement('div');
        msg.className = 'floating-message';
        msg.innerHTML = '🎯 راهي الدزة - شارك مع صحابك!';
        msg.onclick = function() {{ copyLink(); this.remove(); }};
        document.body.appendChild(msg);
        
        setTimeout(function() {{
            if (msg.parentNode) msg.remove();
        }}, 5000);
    }}, 3000);
    </script>
    
    <!-- رسالة سرية للمطور -->
    <div style="display: none;">
        تم تفعيل نظام الترويج المتطور - الدزة واجدة في 58 ولاية! 🚀
        <!-- نظام التتبع: نسخ الرابط: {site_url} -->
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 8. قسم تيك توك OS Style Pro
# ==========================================
def show_tiktok_section():
    st.markdown("""
    <div class="os-share" style="background: linear-gradient(135deg, rgba(0,255,255,0.1), rgba(255,0,255,0.1));">
        <div style="display: flex; align-items: center; gap: 16px; flex-wrap: wrap;">
            <span style="font-size: 1.2rem;">🎵</span>
            <span style="color: white; font-weight: 500;">"تهنينا من التقرعيج، الدزة راهو واجد! 🇩🇿"</span>
        </div>
        <div style="display: flex; gap: 8px;">
            <span style="background: rgba(255,255,255,0.1); padding: 4px 12px; border-radius: 50px; font-size: 0.85rem;">#واد_كنيس</span>
            <span style="background: rgba(255,255,255,0.1); padding: 4px 12px; border-radius: 50px; font-size: 0.85rem;">#الجزائر</span>
            <span style="background: rgba(255,255,255,0.1); padding: 4px 12px; border-radius: 50px; font-size: 0.85rem;">#هواتف</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 9. بطاقات الإحصائيات
# ==========================================
def show_stats_cards():
    users, ads, visitors, views = get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("المستخدمين", f"{users:,}")
    with col2:
        st.metric("الإعلانات", f"{ads:,}")
    with col3:
        st.metric("الزيارات", f"{visitors:,}")
    with col4:
        st.metric("المشاهدات", f"{views:,}")

# ==========================================
# 10. صفحة تسجيل الدخول
# ==========================================
def login_page():
    show_stats_cards()
    show_social_share()
    show_tiktok_section()
    
    tab1, tab2 = st.tabs(["🔑 تسجيل الدخول", "📝 حساب جديد"])
    conn = get_connection()
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("👤 اسم المستخدم")
            password = st.text_input("🔐 كلمة المرور", type="password")
            submitted = st.form_submit_button("🚀 دخول", use_container_width=True)
            
            if submitted:
                if not username or not password:
                    st.error("❌ يرجى ملء جميع الحقول")
                else:
                    try:
                        user = conn.execute(
                            "SELECT password, salt, role FROM users WHERE username=?",
                            (username,)
                        ).fetchone()
                        
                        if user and user[0] == hash_password(password, user[1]):
                            st.session_state.user = username
                            st.session_state.role = user[2]
                            st.rerun()
                        else:
                            st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
                    except Exception as e:
                        st.error(f"❌ خطأ في تسجيل الدخول: {e}")
    
    with tab2:
        with st.form("register_form"):
            new_user = st.text_input("👤 اسم المستخدم الجديد")
            new_pass = st.text_input("🔐 كلمة المرور الجديدة", type="password")
            email = st.text_input("📧 البريد الإلكتروني (اختياري)")
            phone = st.text_input("📱 رقم الهاتف (اختياري)")
            submitted = st.form_submit_button("✨ تسجيل", use_container_width=True)
            
            if submitted:
                if not new_user or not new_pass:
                    st.error("❌ اسم المستخدم وكلمة المرور مطلوبان")
                elif len(new_user) < 3:
                    st.error("❌ اسم المستخدم قصير جداً")
                elif len(new_pass) < 6:
                    st.error("❌ كلمة المرور قصيرة جداً")
                else:
                    try:
                        salt = secrets.token_hex(16)
                        hashed = hash_password(new_pass, salt)
                        
                        conn.execute("""
                            INSERT INTO users (username, password, salt, email, phone, role)
                            VALUES (?, ?, ?, ?, ?, 'user')
                        """, (new_user, hashed, salt, email, phone))
                        conn.commit()
                        
                        st.success("✅ تم التسجيل بنجاح!")
                    except sqlite3.IntegrityError:
                        st.error("❌ اسم المستخدم موجود مسبقاً")
                    except Exception as e:
                        st.error(f"❌ حدث خطأ: {e}")

# ==========================================
# 11. صفحة السوق الذكي
# ==========================================
def show_market(conn):
    st.header("🛍️ السوق الذكي")
    
    show_stats_cards()
    show_social_share()
    show_tiktok_section()
    
    with st.expander("🔍 فلترة البحث", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            wilaya = st.selectbox("📍 الولاية", ["الكل"] + [f"{i:02d}" for i in range(1, 59)])
        with col2:
            category = st.selectbox("🏷️ القسم", ["الكل", "سامسونج", "آيفون", "هواوي", "شاومي", "أخرى"])
        
        search = st.text_input("🔎 بحث عن هاتف", placeholder="اكتب اسم الهاتف...")
        
        if st.button("🔍 بحث", use_container_width=True):
            st.success("جاري البحث...")
    
    try:
        query = "SELECT * FROM ads WHERE status='active'"
        params = []
        
        if wilaya != "الكل":
            query += " AND wilaya=?"
            params.append(wilaya)
        if category != "الكل":
            query += " AND category=?"
            params.append(category)
        if search:
            query += " AND (title LIKE ? OR description LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%"])
        
        query += " ORDER BY featured DESC, date DESC LIMIT 10"
        
        ads = conn.execute(query, params).fetchall()
        
        if ads:
            for ad in ads:
                st.markdown(f"""
                <div class="os-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div class="os-card-title">{ad[1]}</div>
                        <div class="os-card-price">{ad[2]:,} دج</div>
                    </div>
                    
                    <div style="display: flex; gap: 24px; color: rgba(255,255,255,0.5); margin: 16px 0;">
                        <span>📍 {ad[4]}</span>
                        <span>👁️ {ad[8]}</span>
                        {f'<span>📅 {ad[12][:10]}</span>' if ad[12] else ''}
                    </div>
                    
                    <div style="color: rgba(255,255,255,0.7); margin: 16px 0;">
                        {ad[5][:150]}...
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📞 واتساب", key=f"wa_{ad[0]}", use_container_width=True):
                        st.info(f"📱 {ad[3]}")
                with col2:
                    if st.button("💬 مراسلة", key=f"msg_{ad[0]}", use_container_width=True):
                        st.session_state[f"chat_{ad[7]}"] = True
                
                st.divider()
        else:
            st.info("لا توجد إعلانات حالياً")
    except Exception as e:
        st.error(f"خطأ في تحميل الإعلانات: {e}")

# ==========================================
# 12. صفحة إضافة إعلان
# ==========================================
def post_ad(conn):
    st.header("📢 إضافة إعلان جديد")
    
    with st.form("new_ad_form"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("📱 اسم الهاتف *")
            category = st.selectbox("🏷️ الفئة", ["سامسونج", "آيفون", "هواوي", "شاومي", "أخرى"])
        with col2:
            price = st.number_input("💰 السعر (دج) *", min_value=0, step=1000)
            wilaya = st.selectbox("📍 الولاية *", [f"{i:02d}" for i in range(1, 59)])
        
        phone = st.text_input("📞 رقم الهاتف *")
        description = st.text_area("📝 وصف الهاتف")
        
        if st.form_submit_button("🚀 نشر الإعلان", use_container_width=True):
            if not title or price <= 0 or not phone:
                st.error("❌ يرجى ملء جميع الحقول المطلوبة (*)")
            else:
                try:
                    conn.execute("""
                        INSERT INTO ads (title, price, phone, wilaya, description, category, owner)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (title, price, phone, wilaya, description, category, st.session_state.user))
                    conn.commit()
                    
                    conn.execute("UPDATE users SET ad_count = ad_count + 1 WHERE username=?", 
                               (st.session_state.user,))
                    conn.commit()
                    
                    st.success("✅ تم نشر الإعلان بنجاح!")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ حدث خطأ: {e}")

# ==========================================
# 13. صفحة الدردشة
# ==========================================
def show_chat(conn):
    st.header("💬 المحادثات")
    
    user = st.session_state.user
    
    try:
        conversations = conn.execute("""
            SELECT DISTINCT 
                CASE WHEN sender = ? THEN receiver ELSE sender END as contact,
                MAX(date) as last_msg,
                (SELECT COUNT(*) FROM messages WHERE receiver=? AND sender=contact AND read=0) as unread
            FROM messages 
            WHERE sender = ? OR receiver = ?
            GROUP BY contact
            ORDER BY last_msg DESC
        """, (user, user, user, user)).fetchall()
        
        if not conversations:
            st.info("لا توجد محادثات حالياً")
            return
        
        contacts = [f"{c[0]} 🔴" if c[2] > 0 else c[0] for c in conversations]
        selected = st.selectbox("اختر محادثة", contacts)
        selected = selected.replace(" 🔴", "")
        
        if selected:
            st.subheader(f"الدردشة مع {selected}")
            
            conn.execute("UPDATE messages SET read=1 WHERE sender=? AND receiver=?", 
                        (selected, user))
            conn.commit()
            
            messages = conn.execute("""
                SELECT sender, message, date FROM messages
                WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?)
                ORDER BY date ASC
            """, (user, selected, selected, user)).fetchall()
            
            for msg in messages:
                if msg[0] == user:
                    st.markdown(f"<div class='os-chat-sent'><b>أنت:</b> {msg[1]}<br><small>{msg[2][11:16] if msg[2] else ''}</small></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='os-chat-received'><b>{msg[0]}:</b> {msg[1]}<br><small>{msg[2][11:16] if msg[2] else ''}</small></div>", unsafe_allow_html=True)
            
            with st.form("send_message", clear_on_submit=True):
                msg = st.text_input("✍️ اكتب رسالتك...")
                if st.form_submit_button("📤 إرسال", use_container_width=True) and msg:
                    conn.execute("""
                        INSERT INTO messages (sender, receiver, message)
                        VALUES (?, ?, ?)
                    """, (user, selected, msg))
                    conn.commit()
                    st.rerun()
    except Exception as e:
        st.error(f"خطأ في تحميل المحادثات: {e}")

# ==========================================
# 14. لوحة الإدارة
# ==========================================
def admin_dashboard(conn):
    st.header("🔐 لوحة الإدارة")
    
    users, ads, visitors, views = get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("المستخدمين", f"{users:,}")
    with col2:
        st.metric("الإعلانات", f"{ads:,}")
    with col3:
        st.metric("الزيارات", f"{visitors:,}")
    with col4:
        st.metric("المشاهدات", f"{views:,}")
    
    tab1, tab2, tab3 = st.tabs(["👥 المستخدمين", "📊 الإحصائيات", "🚨 البلاغات"])
    
    with tab1:
        st.subheader("👥 قائمة المستخدمين")
        try:
            users_df = pd.read_sql_query("""
                SELECT username, role, verified, banned, ad_count, 
                       substr(last_login, 1, 10) as last_login
                FROM users ORDER BY last_login DESC
            """, conn)
            st.dataframe(users_df, use_container_width=True)
        except Exception as e:
            st.error(f"خطأ في تحميل البيانات: {e}")
    
    with tab2:
        st.subheader("📊 إحصائيات متقدمة")
        try:
            category_stats = conn.execute("""
                SELECT category, COUNT(*) as count 
                FROM ads 
                WHERE status='active' 
                GROUP BY category
            """).fetchall()
            
            if category_stats:
                df_cats = pd.DataFrame(category_stats, columns=["الفئة", "العدد"])
                fig = px.pie(df_cats, values='العدد', names='الفئة', 
                            title="توزيع الإعلانات حسب الفئة",
                            color_discrete_sequence=px.colors.sequential.Blues_r)
                st.plotly_chart(fig, use_container_width=True)
        except:
            pass
    
    with tab3:
        st.subheader("🚨 البلاغات المعلقة")
        try:
            reports = conn.execute("""
                SELECT r.id, a.title, r.reporter, r.reason, r.date
                FROM reports r JOIN ads a ON r.ad_id = a.id
                WHERE r.status='pending'
                ORDER BY r.date DESC
            """).fetchall()
            
            if reports:
                for report in reports:
                    with st.container():
                        st.warning(f"📌 إعلان: {report[1]}")
                        st.write(f"المبلغ: {report[2]} | السبب: {report[3]} | التاريخ: {report[4][:10]}")
                        if st.button("✅ معالجة", key=f"resolve_{report[0]}"):
                            conn.execute("UPDATE reports SET status='resolved' WHERE id=?", (report[0],))
                            conn.commit()
                            st.rerun()
                        st.divider()
            else:
                st.info("لا توجد بلاغات معلقة")
        except Exception as e:
            st.error(f"خطأ في تحميل البلاغات: {e}")

# ==========================================
# 15. التشغيل الرئيسي المتكامل مع الشعار
# ==========================================
def main():
    # تهيئة حالة الجلسة
    if "user" not in st.session_state:
        st.session_state.user = None
    if "role" not in st.session_state:
        st.session_state.role = "user"
    if "ip" not in st.session_state:
        st.session_state.ip = secrets.token_hex(8)
    if "page" not in st.session_state:
        st.session_state.page = "main"
    
    # تسجيل الزائر
    log_visitor()
    
    # التحقق من تسجيل الدخول
    if not st.session_state.user:
        login_page()
    else:
        conn = get_connection()
        
        # القائمة الجانبية المتطورة مع الشعار (حسب طلبك)
        with st.sidebar:
            # إضافة الشعار (إذا كان موجوداً)
            try:
                st.sidebar.image("logo.png", use_container_width=True)
            except:
                st.sidebar.markdown("""
                <div style="text-align: center; padding: 10px;">
                    <div style="font-size: 4rem;">💠</div>
                </div>
                """, unsafe_allow_html=True)
            
            # عنوان RASSIM OS
            st.sidebar.markdown("""
            <h1 style='text-align: center; color: #00ffff; font-size: 2rem; margin-bottom: 20px; 
            background: linear-gradient(135deg, #00ffff, #ff00ff); -webkit-background-clip: text; 
            -webkit-text-fill-color: transparent; font-weight: 800;'>
            RASSIM OS
            </h1>
            """, unsafe_allow_html=True)
            
            # بروفايل المستخدم
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(0,255,255,0.15), rgba(255,0,255,0.15)); 
            backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.05); padding: 24px; 
            border-radius: 28px; text-align: center; margin-bottom: 24px;">
                <div style="font-size: 3rem; margin-bottom: 8px;">💠</div>
                <div style="color: white; font-size: 1.4rem; font-weight: 600; 
                background: linear-gradient(135deg, #00ffff, #ff00ff); -webkit-background-clip: text; 
                -webkit-text-fill-color: transparent;">
                    {st.session_state.user}
                </div>
                <div style="color: rgba(255,255,255,0.5); font-size: 0.9rem; margin-top: 8px;">
                    {st.session_state.role}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # قائمة الخيارات
            menu_options = ["🛍️ السوق الذكي", "📢 إضافة إعلان", "💬 المحادثات"]
            if st.session_state.role == "admin":
                menu_options.append("🔐 لوحة الإدارة")
            
            choice = st.radio("", menu_options, label_visibility="collapsed")
            
            st.divider()
            
            # زر الخروج
            if st.button("🚪 تسجيل الخروج", use_container_width=True):
                st.session_state.user = None
                st.session_state.role = "user"
                st.rerun()
            
            # إحصائيات سريعة في الشريط الجانبي
            users, ads, visitors, views = get_stats()
            st.markdown(f"""
            <div style="background: rgba(20,20,30,0.6); backdrop-filter: blur(12px); 
            border: 1px solid rgba(255,255,255,0.05); border-radius: 20px; padding: 16px; margin-top: 24px;">
                <div style="display: flex; justify-content: space-between; color: rgba(255,255,255,0.6); 
                font-size: 0.9rem; margin-bottom: 8px;">
                    <span>المستخدمين</span>
                    <span style="color: #00ffff;">{users}</span>
                </div>
                <div style="display: flex; justify-content: space-between; color: rgba(255,255,255,0.6); 
                font-size: 0.9rem; margin-bottom: 8px;">
                    <span>الإعلانات</span>
                    <span style="color: #ff00ff;">{ads}</span>
                </div>
                <div style="display: flex; justify-content: space-between; color: rgba(255,255,255,0.6); 
                font-size: 0.9rem;">
                    <span>المشاهدات</span>
                    <span style="color: #00ffff;">{views}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # توجيه الصفحات حسب الاختيار
        if choice == "🛍️ السوق الذكي":
            show_market(conn)
        elif choice == "📢 إضافة إعلان":
            post_ad(conn)
        elif choice == "💬 المحادثات":
            show_chat(conn)
        elif choice == "🔐 لوحة الإدارة" and st.session_state.role == "admin":
            admin_dashboard(conn)

if __name__ == "__main__":
    main()

