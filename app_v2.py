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
# 1. إعدادات الصفحة المتقدمة
# ==========================================
st.set_page_config(
    page_title="راسم تيتانيوم - سوق الهواتف الجزائري",
    page_icon="🇩🇿",
    layout="wide",
    initial_sidebar_state="auto"
)

# ==========================================
# 2. تحسين محركات البحث (SEO)
# ==========================================
st.markdown("""
st.markdown("""
<style>
/* ===== التصميم العام للصفحة ===== */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');

* {
    font-family: 'Cairo', sans-serif;
    direction: rtl;
}

.stApp {
    background: radial-gradient(circle at 10% 20%, rgba(0, 255, 136, 0.03) 0%, rgba(0, 189, 255, 0.03) 90%),
                linear-gradient(135deg, #0a0a1a 0%, #1a1a2f 50%, #0d0d1a 100%);
    color: #ffffff;
    position: relative;
}

/* إضافة تأثير النجوم المتحركة في الخلفية */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(2px 2px at 20px 30px, #eee, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 40px 70px, #fff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 80px 120px, #ddd, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 160px 90px, #ccc, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 240px 150px, #eee, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 320px 210px, #fff, rgba(0,0,0,0)),
        radial-gradient(3px 3px at 400px 50px, #00ff88, rgba(0,0,0,0)),
        radial-gradient(3px 3px at 480px 280px, #00bdff, rgba(0,0,0,0));
    background-repeat: repeat;
    background-size: 600px 600px;
    opacity: 0.3;
    animation: stars 200s linear infinite;
    pointer-events: none;
}

@keyframes stars {
    from { transform: translateY(0); }
    to { transform: translateY(-600px); }
}

/* ===== تحسين شكل الكروت (المستخدمين، الإعلانات، الزيارات) ===== */
.stMetric {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 25px;
    padding: 25px 20px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow: 
        0 20px 40px -10px rgba(0, 0, 0, 0.5),
        inset 0 1px 1px rgba(255, 255, 255, 0.1);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
}

.stMetric::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00ff88, #00bdff, transparent);
    animation: borderGlow 3s linear infinite;
}

@keyframes borderGlow {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.stMetric:hover {
    transform: translateY(-8px) scale(1.02);
    border: 1px solid rgba(0, 255, 136, 0.3);
    box-shadow: 
        0 30px 60px -15px rgba(0, 255, 136, 0.3),
        inset 0 1px 2px rgba(255, 255, 255, 0.2);
}

/* تنسيق النصوص داخل الكروت */
.stMetric label {
    color: rgba(255, 255, 255, 0.7) !important;
    font-size: 1rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.5px;
}

.stMetric div {
    color: #fff !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    text-shadow: 0 2px 10px rgba(0, 255, 136, 0.3);
}

/* ===== تحسين الأزرار لتصبح جذابة جداً ===== */
.stButton>button {
    width: 100%;
    border-radius: 60px;
    background: linear-gradient(135deg, #00ff88, #00bdff, #0066ff);
    background-size: 200% 200%;
    color: white;
    font-weight: 700;
    font-size: 1.1rem;
    border: none;
    height: 3.2em;
    padding: 0 30px;
    transition: 0.4s ease;
    box-shadow: 0 10px 20px -5px rgba(0, 255, 136, 0.3);
    position: relative;
    overflow: hidden;
    text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    letter-spacing: 1px;
}

.stButton>button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s ease;
}

.stButton>button:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 30px -5px rgba(0, 255, 136, 0.6);
    animation: gradientShift 3s ease infinite;
    background-size: 200% 200%;
}

.stButton>button:hover::before {
    left: 100%;
}

.stButton>button:active {
    transform: translateY(-2px);
    box-shadow: 0 15px 25px -5px rgba(0, 255, 136, 0.4);
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ===== تحسين الهيدر (العنوان الرئيسي) ===== */
.main-title {
    font-size: 4rem;
    font-weight: 900;
    background: linear-gradient(135deg, #00ff88, #00bdff, #0066ff, #00ff88);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin: 30px 0 20px;
    text-shadow: 
        0 0 30px rgba(0, 255, 136, 0.3),
        2px 2px 0 rgba(0,0,0,0.3);
    animation: gradientFlow 8s ease infinite, float 6s ease-in-out infinite;
    letter-spacing: 2px;
    position: relative;
    display: inline-block;
    width: 100%;
}

@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

.main-title::after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 100px;
    height: 4px;
    background: linear-gradient(90deg, transparent, #00ff88, #00bdff, transparent);
    border-radius: 2px;
    animation: widthPulse 3s ease infinite;
}

@keyframes widthPulse {
    0%, 100% { width: 100px; opacity: 0.5; }
    50% { width: 200px; opacity: 1; }
}

/* ===== تحسين صناديق الإدخال ===== */
.stTextInput>div>div>input, 
.stTextArea>div>div>textarea,
.stSelectbox>div>div>select {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 50px !important;
    color: white !important;
    padding: 15px 20px !important;
    font-size: 1rem !important;
    transition: all 0.3s ease;
}

.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus,
.stSelectbox>div>div>select:focus {
    border-color: #00ff88 !important;
    box-shadow: 0 0 20px rgba(0, 255, 136, 0.2) !important;
    transform: translateY(-2px);
}

.stTextInput>div>div>input:hover,
.stTextArea>div>div>textarea:hover,
.stSelectbox>div>div>select:hover {
    border-color: rgba(0, 255, 136, 0.5) !important;
}

/* ===== تحسين التبويبات (Tabs) ===== */
.stTabs [data-baseweb="tab-list"] {
    gap: 20px;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(10px);
    padding: 15px;
    border-radius: 60px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 50px !important;
    padding: 10px 30px !important;
    color: rgba(255, 255, 255, 0.7) !important;
    font-weight: 600 !important;
    transition: all 0.3s ease;
    border: 1px solid transparent;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(0, 255, 136, 0.1) !important;
    border-color: rgba(0, 255, 136, 0.3) !important;
    color: white !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #00ff88, #00bdff) !important;
    color: black !important;
    font-weight: 700 !important;
    box-shadow: 0 10px 20px -5px rgba(0, 255, 136, 0.4);
}

/* ===== تحسين الشريط الجانبي ===== */
.css-1d391kg, .css-12oz5g7 {
    background: rgba(10, 10, 26, 0.8);
    backdrop-filter: blur(20px);
    border-left: 1px solid rgba(255, 255, 255, 0.05);
}

.css-1d391kg:hover, .css-12oz5g7:hover {
    background: rgba(15, 15, 35, 0.9);
}

/* ===== تحسين الإطارات المنبثقة ===== */
div[data-baseweb="popover"] {
    background: rgba(20, 20, 40, 0.95) !important;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 20px !important;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4) !important;
}

/* ===== تحسين شريط التمرير ===== */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #00ff88, #00bdff);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #00bdff, #00ff88);
}

/* ===== تحسين رسائل النجاح والخطأ ===== */
.stAlert {
    background: rgba(255, 255, 255, 0.03) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 20px !important;
    color: white !important;
    animation: slideInRight 0.5s ease;
}

@keyframes slideInRight {
    from {
        transform: translateX(30px);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

/* ===== تأثيرات إضافية للكروت ===== */
.css-1r6slb0 {
    background: rgba(255, 255, 255, 0.02) !important;
    border-radius: 30px !important;
    padding: 25px !important;
    border: 1px solid rgba(255, 255, 255, 0.03) !important;
    transition: all 0.3s ease;
}

.css-1r6slb0:hover {
    border-color: rgba(0, 255, 136, 0.2) !important;
    box-shadow: 0 10px 30px -10px rgba(0, 255, 136, 0.2);
}

/* ===== تحسين عنوان الصفحة الثانوي ===== */
h1, h2, h3 {
    color: white !important;
    text-shadow: 0 2px 10px rgba(0, 255, 136, 0.2);
}

h1 {
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #fff, #e0e0e0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 30px !important;
}

/* ===== تحسين الفوتر ===== */
footer {
    background: rgba(0, 0, 0, 0.3) !important;
    backdrop-filter: blur(10px);
    border-top: 1px solid rgba(255, 255, 255, 0.05) !important;
    padding: 15px !important;
}

/* ===== تأثيرات حركية للعناصر ===== */
@keyframes pulseGlow {
    0%, 100% {
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
    }
    50% {
        box-shadow: 0 0 40px rgba(0, 255, 136, 0.4);
    }
}

.pulse-effect {
    animation: pulseGlow 3s ease infinite;
}

/* ===== تحسين التوافق مع الجوال ===== */
@media (max-width: 768px) {
    .main-title {
        font-size: 2.5rem;
    }
    
    .stMetric div {
        font-size: 1.8rem !important;
    }
    
    .stButton>button {
        height: 2.8em;
        font-size: 1rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        padding: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 8px 15px !important;
        font-size: 0.9rem !important;
    }
}

/* ===== تأثيرات الإضاءة الخلفية ===== */
.glow-effect {
    position: relative;
}

.glow-effect::after {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg, #00ff88, #00bdff, #0066ff, #00ff88);
    background-size: 400% 400%;
    border-radius: inherit;
    z-index: -1;
    filter: blur(20px);
    opacity: 0;
    transition: opacity 0.3s ease;
    animation: gradientShift 6s ease infinite;
}

.glow-effect:hover::after {
    opacity: 0.5;
}
</style>

<!-- إضافة عناوين متحركة -->
<div class="main-title">
    🇩🇿 راسم تيتانيوم ألترا
</div>

<div style="text-align: center; margin-bottom: 30px;">
    <p style="color: rgba(255,255,255,0.7); font-size: 1.2rem; animation: fadeInUp 1s ease;">
        ✨ أول سوق إلكتروني جزائري متخصص في الهواتف
    </p>
</div>

<script>
// إضافة تأثيرات حركية إضافية
document.addEventListener('DOMContentLoaded', function() {
    const elements = document.querySelectorAll('.stMetric, .stButton>button');
    elements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.1}s`;
        el.classList.add('fadeInUp');
    });
});
</script>
""", unsafe_allow_html=True)
<meta name="description" content="راسم تيتانيوم - أفضل سوق للهواتف في الجزائر. بيع وشراء الهواتف المستعملة والجديدة في 58 ولاية.">
<meta name="keywords" content="واد كنيس, Ouedkniss, هواتف, الجزائر, بيع وشراء, راسم فون, تيتانيوم">
<meta name="author" content="RASSIM DZ">
""", unsafe_allow_html=True)

# ==========================================
# 3. التصميم المتكامل (CSS)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

* {
    font-family: 'Cairo', sans-serif;
    direction: rtl;
    box-sizing: border-box;
}

.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* الهيدر الرئيسي */
.main-header {
    background: linear-gradient(135deg, #006633 0%, #006633 48%, #d21034 50%, #ffffff 52%, #ffffff 100%);
    padding: 40px 20px;
    border-radius: 30px;
    text-align: center;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    margin-bottom: 30px;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { box-shadow: 0 20px 40px rgba(0,102,51,0.3); }
    to { box-shadow: 0 20px 60px rgba(210,16,52,0.5); }
}

.main-header h1 {
    color: white;
    font-size: 2.5rem;
    font-weight: 900;
    margin-bottom: 10px;
}

.main-header p {
    color: white;
    font-size: 1.2rem;
}

/* أزرار المشاركة الاجتماعية */
.social-share {
    background: white;
    padding: 25px 20px;
    border-radius: 30px;
    margin: 25px 0;
    text-align: center;
    box-shadow: 0 15px 30px rgba(0,0,0,0.1);
    border: 2px solid #006633;
}

.social-share h3 {
    color: #006633;
    font-size: 1.5rem;
    margin-bottom: 10px;
}

.social-grid {
    display: flex;
    justify-content: center;
    gap: 15px;
    flex-wrap: wrap;
    margin: 20px 0;
}

.social-icon {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: #f8f9fa;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}

.social-icon:hover {
    transform: scale(1.1) translateY(-5px);
    box-shadow: 0 10px 20px rgba(210,16,52,0.2);
}

.social-icon img {
    width: 30px;
    height: 30px;
}

.share-badge {
    background: linear-gradient(135deg, #d21034, #ff6b6b);
    color: white;
    padding: 8px 25px;
    border-radius: 50px;
    display: inline-block;
    font-weight: bold;
}

/* قسم تيك توك */
.tiktok-section {
    background: linear-gradient(135deg, #25F4EE, #FE2C55);
    padding: 25px;
    border-radius: 30px;
    color: white;
    text-align: center;
    margin: 25px 0;
    border: 3px solid white;
    animation: shake 0.8s ease;
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    20%, 60% { transform: translateX(-5px); }
    40%, 80% { transform: translateX(5px); }
}

.tiktok-quote {
    font-size: 1.4rem;
    font-weight: bold;
    margin: 15px 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.tiktok-features {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin: 15px 0;
}

.feature-tag {
    background: rgba(255,255,255,0.2);
    padding: 5px 15px;
    border-radius: 50px;
    font-size: 0.9rem;
    backdrop-filter: blur(5px);
}

.tiktok-hashtags {
    display: flex;
    justify-content: center;
    gap: 8px;
    flex-wrap: wrap;
    margin: 15px 0;
}

.hashtag {
    background: white;
    color: #FE2C55;
    padding: 5px 15px;
    border-radius: 50px;
    font-size: 0.9rem;
    font-weight: bold;
}

/* بطاقات الإحصائيات */
.stats-container {
    display: flex;
    justify-content: space-between;
    gap: 15px;
    flex-wrap: wrap;
    margin: 25px 0;
}

.stat-card {
    flex: 1;
    min-width: 120px;
    background: white;
    padding: 20px 15px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    border-bottom: 4px solid #d21034;
}

.stat-value {
    font-size: 2.2rem;
    font-weight: 900;
    color: #d21034;
    line-height: 1.2;
}

.stat-label {
    font-size: 1rem;
    color: #006633;
    font-weight: 600;
    margin-top: 5px;
}

/* بطاقات الإعلانات */
.ad-card {
    background: white;
    border-radius: 25px;
    padding: 25px;
    margin-bottom: 20px;
    border-right: 8px solid #006633;
    box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    transition: all 0.3s;
    animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.ad-card:hover {
    transform: translateX(-5px);
    border-right-color: #d21034;
    box-shadow: 0 15px 30px rgba(210,16,52,0.15);
}

.ad-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #d21034;
    margin-bottom: 10px;
}

.ad-price {
    background: linear-gradient(135deg, #006633, #00a86b);
    color: white;
    padding: 8px 20px;
    border-radius: 50px;
    display: inline-block;
    font-weight: 700;
    font-size: 1.3rem;
}

.ad-details {
    display: flex;
    gap: 20px;
    color: #666;
    margin: 15px 0;
    font-size: 0.95rem;
}

.ad-actions {
    display: flex;
    gap: 10px;
    margin-top: 15px;
}

.ad-btn {
    flex: 1;
    background: #f8f9fa;
    border: none;
    border-radius: 50px;
    padding: 10px;
    font-size: 0.95rem;
    color: #006633;
    cursor: pointer;
    transition: all 0.3s;
    font-weight: 600;
}

.ad-btn:hover {
    background: #006633;
    color: white;
}

/* فقاعات الدردشة */
.chat-container {
    background: #f8f9fa;
    border-radius: 20px;
    padding: 20px;
    max-height: 400px;
    overflow-y: auto;
}

.chat-bubble {
    padding: 12px 18px;
    border-radius: 18px;
    margin: 8px 0;
    max-width: 80%;
    animation: popIn 0.3s ease;
}

@keyframes popIn {
    from { transform: scale(0.9); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
}

.chat-sent {
    background: #dcf8c6;
    margin-left: auto;
    border-bottom-left-radius: 5px;
}

.chat-received {
    background: white;
    margin-right: auto;
    border-bottom-right-radius: 5px;
    border: 1px solid #eee;
}

/* شارة المميز */
.featured-badge {
    background: linear-gradient(135deg, #ffd700, #ffa500);
    color: white;
    padding: 4px 15px;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: bold;
    display: inline-block;
    margin-right: 10px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

/* المساعد الذكي */
.ai-section {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 25px;
    border-radius: 25px;
    color: white;
    margin: 25px 0;
}

/* لوحة الإدارة */
.admin-section {
    background: linear-gradient(135deg, #2c3e50, #3498db);
    padding: 25px;
    border-radius: 25px;
    color: white;
    margin: 25px 0;
}

/* التجاوب مع الجوال */
@media (max-width: 768px) {
    .main-header h1 { font-size: 1.8rem; }
    .stat-value { font-size: 1.8rem; }
    .ad-title { font-size: 1.3rem; }
    .ad-price { font-size: 1.1rem; }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. إعدادات قاعدة البيانات (مصححة بالكامل)
# ==========================================
DB = "rassim_titanium.db"

def init_db():
    """تهيئة قاعدة البيانات مع جميع الجداول"""
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
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
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
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
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
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
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
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
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
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
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
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ad_id) REFERENCES ads(id),
            FOREIGN KEY (reporter) REFERENCES users(username)
        )
    """)
    
    # جدول الزوار (مصحح - مع حقل visit_date)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            page TEXT,
            visit_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    return conn

@st.cache_resource
def get_connection():
    """الحصول على اتصال قاعدة البيانات"""
    return sqlite3.connect(DB, check_same_thread=False)

# تهيئة قاعدة البيانات
init_db()

# ==========================================
# 5. دوال المساعدة الأساسية
# ==========================================
def hash_password(password, salt):
    """تشفير كلمة المرور"""
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()

def create_notification(username, message, notif_type="info"):
    """إنشاء إشعار جديد"""
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
    """تسجيل زائر جديد - مصحح"""
    try:
        conn = get_connection()
        conn.execute(
            "INSERT INTO visitors (ip, page) VALUES (?, ?)",
            (st.session_state.get('ip', 'unknown'), st.session_state.get('page', 'main'))
        )
        conn.commit()
    except Exception as e:
        print(f"خطأ في تسجيل الزائر: {e}")

def get_stats():
    """الحصول على إحصائيات الموقع"""
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
# 6. أزرار المشاركة الاجتماعية
# ==========================================
def show_social_share():
    """عرض أزرار المشاركة الاجتماعية"""
    site_url = "https://racim-phone.streamlit.app/"
    
    st.markdown(f"""
    <div class="social-share">
        <h3>📢 شارك الموقع مع أصدقائك</h3>
        <p style="color: #666;">ساعد في نشر الموقع واكسب الثواب 🤲</p>
        
        <div class="social-grid">
            <a href="https://www.facebook.com/sharer/sharer.php?u={site_url}" target="_blank" class="social-icon">
                <img src="https://img.icons8.com/color/48/facebook-new.png">
            </a>
            <a href="https://api.whatsapp.com/send?text=شوف هاد الموقع لبيع الهواتف: {site_url}" target="_blank" class="social-icon">
                <img src="https://img.icons8.com/color/48/whatsapp--v1.png">
            </a>
            <a href="https://t.me/share/url?url={site_url}" target="_blank" class="social-icon">
                <img src="https://img.icons8.com/color/48/telegram-app--v1.png">
            </a>
            <a href="#" onclick="navigator.clipboard.writeText('{site_url}'); alert('✅ تم نسخ الرابط!'); return false;" class="social-icon">
                <img src="https://img.icons8.com/color/48/link--v1.png">
            </a>
        </div>
        
        <div class="share-badge">
            👥 شارك مع 10 أصدقاء واكسب الدعاء
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 7. قسم تيك توك
# ==========================================
def show_tiktok_section():
    """عرض قسم تيك توك"""
    st.markdown("""
    <div class="tiktok-section">
        <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 15px;">
            <span style="font-size: 2.5rem;">🎵</span>
            <span style="font-size: 1.5rem; font-weight: bold;">تيك توك الجزائر</span>
        </div>
        
        <div class="tiktok-quote">
            "تهنينا من التقرعيج في فيسبوك، موقع راسم تيتانيوم للدزة راهو واجد! 🇩🇿"
        </div>
        
        <div class="tiktok-features">
            <span class="feature-tag">🔥 تسوق بسهولة</span>
            <span class="feature-tag">⚡ بيع بسرعة</span>
            <span class="feature-tag">💬 تواصل مباشر</span>
        </div>
        
        <div class="tiktok-hashtags">
            <span class="hashtag">#واد_كنيس</span>
            <span class="hashtag">#الجزائر</span>
            <span class="hashtag">#هواتف</span>
            <span class="hashtag">#راسم_تيتانيوم</span>
        </div>
        
        <div style="margin-top: 20px;">
            <span style="background: white; color: #FE2C55; padding: 8px 25px; border-radius: 50px; font-weight: bold;">
                📱 58 ولاية
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 8. بطاقات الإحصائيات
# ==========================================
def show_stats_cards():
    """عرض بطاقات الإحصائيات"""
    users, ads, visitors, views = get_stats()
    
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-value">{users}</div>
            <div class="stat-label">مستخدم</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{ads}</div>
            <div class="stat-label">إعلان</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{visitors}</div>
            <div class="stat-label">زيارة</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{views}</div>
            <div class="stat-label">مشاهدة</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 9. صفحة تسجيل الدخول
# ==========================================
def login_page():
    st.markdown("""
    <div class="main-header">
        <h1>🇩🇿 راسم تيتانيوم ألترا</h1>
        <p>أول سوق إلكتروني جزائري للهواتف</p>
    </div>
    """, unsafe_allow_html=True)
    
    # إحصائيات
    show_stats_cards()
    
    # أزرار المشاركة
    show_social_share()
    
    # قسم تيك توك
    show_tiktok_section()
    
    tab1, tab2 = st.tabs(["🔑 تسجيل الدخول", "📝 حساب جديد"])
    conn = get_connection()
    
    with tab1:
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        
        if st.button("دخول", use_container_width=True):
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
            except:
                st.error("❌ خطأ في تسجيل الدخول")
    
    with tab2:
        new_user = st.text_input("اسم المستخدم الجديد")
        new_pass = st.text_input("كلمة المرور الجديدة", type="password")
        email = st.text_input("البريد الإلكتروني")
        phone = st.text_input("رقم الهاتف")
        
        if st.button("تسجيل", use_container_width=True):
            if new_user and new_pass:
                try:
                    salt = secrets.token_hex(16)
                    hashed = hash_password(new_pass, salt)
                    
                    conn.execute("""
                        INSERT INTO users (username, password, salt, email, phone)
                        VALUES (?, ?, ?, ?, ?)
                    """, (new_user, hashed, salt, email, phone))
                    conn.commit()
                    
                    st.success("✅ تم التسجيل بنجاح! يمكنك الدخول الآن")
                except:
                    st.error("❌ اسم المستخدم موجود مسبقاً")

# ==========================================
# 10. صفحة السوق الذكي
# ==========================================
def show_market(conn):
    st.markdown('<div class="main-header"><h1>🛍️ السوق الذكي</h1><p>تصفح آلاف الهواتف في 58 ولاية</p></div>', unsafe_allow_html=True)
    
    # إحصائيات سريعة
    show_stats_cards()
    
    # أزرار المشاركة
    show_social_share()
    
    # قسم تيك توك
    show_tiktok_section()
    
    # فلاتر البحث
    with st.expander("🔍 فلترة البحث", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            wilaya = st.selectbox("الولاية", ["الكل"] + [f"{i:02d}" for i in range(1, 59)])
        with col2:
            category = st.selectbox("القسم", ["الكل", "سامسونج", "آيفون", "هواوي", "شاومي", "أخرى"])
        with col3:
            sort = st.selectbox("الترتيب", ["الأحدث", "الأكثر مشاهدة", "الأعلى سعراً", "الأقل سعراً"])
        
        search = st.text_input("🔎 بحث عن هاتف", placeholder="اكتب اسم الهاتف...")
        
        if st.button("🔍 بحث", use_container_width=True):
            st.success("جاري البحث...")
    
    # عرض الإعلانات
    try:
        ads = conn.execute("""
            SELECT * FROM ads 
            WHERE status='active' 
            ORDER BY featured DESC, created_at DESC 
            LIMIT 10
        """).fetchall()
        
        if ads:
            for ad in ads:
                featured_badge = '<span class="featured-badge">⭐ مميز</span>' if ad[9] else ''
                
                st.markdown(f"""
                <div class="ad-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span class="ad-title">{ad[1]}</span>
                            {featured_badge}
                        </div>
                        <span class="ad-price">{ad[2]:,} دج</span>
                    </div>
                    
                    <div class="ad-details">
                        <span>📍 {ad[4]}</span>
                        <span>👁️ {ad[8]} مشاهدة</span>
                        <span>📅 {ad[12][:10]}</span>
                    </div>
                    
                    <p style="color: #666; margin: 10px 0;">{ad[5][:100]}...</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("لا توجد إعلانات حالياً")
    except:
        st.info("جاري تحميل الإعلانات...")

# ==========================================
# 11. صفحة إضافة إعلان
# ==========================================
def post_ad(conn):
    st.markdown('<div class="main-header"><h1>📢 إضافة إعلان جديد</h1></div>', unsafe_allow_html=True)
    
    with st.form("new_ad_form"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("اسم الهاتف")
            category = st.selectbox("الفئة", ["سامسونج", "آيفون", "هواوي", "شاومي", "أخرى"])
        with col2:
            price = st.number_input("السعر (دج)", min_value=0, step=1000)
            wilaya = st.selectbox("الولاية", [f"{i:02d}" for i in range(1, 59)])
        
        phone = st.text_input("رقم الهاتف")
        description = st.text_area("وصف الهاتف")
        
        if st.form_submit_button("🚀 نشر الإعلان", use_container_width=True):
            if title and price > 0 and phone:
                try:
                    conn.execute("""
                        INSERT INTO ads (title, price, phone, wilaya, description, category, owner)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (title, price, phone, wilaya, description, category, st.session_state.user))
                    conn.commit()
                    st.success("✅ تم نشر الإعلان بنجاح!")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ حدث خطأ: {e}")
            else:
                st.error("❌ يرجى ملء جميع الحقول المطلوبة")

# ==========================================
# 12. صفحة الدردشة
# ==========================================
def show_chat(conn):
    st.markdown('<div class="main-header"><h1>💬 المحادثات</h1></div>', unsafe_allow_html=True)
    
    user = st.session_state.user
    
    try:
        conversations = conn.execute("""
            SELECT DISTINCT 
                CASE WHEN sender = ? THEN receiver ELSE sender END as contact,
                MAX(created_at) as last_msg
            FROM messages 
            WHERE sender = ? OR receiver = ?
            GROUP BY contact
            ORDER BY last_msg DESC
        """, (user, user, user)).fetchall()
        
        if not conversations:
            st.info("لا توجد محادثات حالياً")
            return
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("المحادثات")
            contacts = [c[0] for c in conversations]
            selected = st.radio("", contacts)
        
        with col2:
            if selected:
                st.subheader(f"الدردشة مع {selected}")
                
                messages = conn.execute("""
                    SELECT sender, message, created_at FROM messages
                    WHERE (sender = ? AND receiver = ?) OR (sender = ? AND receiver = ?)
                    ORDER BY created_at ASC
                """, (user, selected, selected, user)).fetchall()
                
                st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                for msg in messages:
                    if msg[0] == user:
                        st.markdown(f'<div class="chat-bubble chat-sent"><b>أنت:</b> {msg[1]}<br><small>{msg[2][11:16]}</small></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="chat-bubble chat-received"><b>{msg[0]}:</b> {msg[1]}<br><small>{msg[2][11:16]}</small></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                with st.form("send_message", clear_on_submit=True):
                    msg = st.text_input("اكتب رسالتك...")
                    if st.form_submit_button("إرسال", use_container_width=True) and msg:
                        conn.execute("""
                            INSERT INTO messages (sender, receiver, message)
                            VALUES (?, ?, ?)
                        """, (user, selected, msg))
                        conn.commit()
                        st.rerun()
    except:
        st.info("نظام المحادثات قيد التطوير")

# ==========================================
# 13. لوحة الإدارة
# ==========================================
def admin_dashboard(conn):
    st.markdown('<div class="admin-section"><h1 style="color:white; text-align:center;">🔐 لوحة الإدارة</h1></div>', unsafe_allow_html=True)
    
    try:
        users, ads, visitors, views = get_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("المستخدمين", users)
        col2.metric("الإعلانات", ads)
        col3.metric("الزيارات", visitors)
        col4.metric("المشاهدات", views)
        
        users_df = pd.read_sql_query("SELECT username, role, verified, banned, ad_count FROM users", conn)
        st.dataframe(users_df, use_container_width=True)
    except:
        st.info("جاري تحميل البيانات...")

# ==========================================
# 14. التشغيل الرئيسي
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
    
    if not st.session_state.user:
        login_page()
    else:
        conn = get_connection()
        
        # الشريط الجانبي
        with st.sidebar:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #006633, #d21034); padding: 20px; border-radius: 15px; text-align: center; color: white; margin-bottom: 20px;">
                <h3>🎖️ {st.session_state.user}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            menu = st.radio(
                "القائمة الرئيسية",
                ["🏠 السوق الذكي", "📢 إضافة إعلان", "💬 الرسائل", "🤖 المساعد الذكي"]
            )
            
            if st.session_state.role == "admin":
                if st.button("🛡️ لوحة الإدارة", use_container_width=True):
                    menu = "🛡️ الإدارة"
            
            if st.button("🚪 تسجيل الخروج", use_container_width=True):
                st.session_state.user = None
                st.rerun()
        
        # توجيه الصفحات
        if menu == "🏠 السوق الذكي":
            show_market(conn)
        elif menu == "📢 إضافة إعلان":
            post_ad(conn)
        elif menu == "💬 الرسائل":
            show_chat(conn)
        elif menu == "🤖 المساعد الذكي":
            st.markdown('<div class="ai-section"><h1 style="color:white;">🤖 المساعد الذكي</h1><p style="color:white;">قريباً...</p></div>', unsafe_allow_html=True)
        elif menu == "🛡️ الإدارة" and st.session_state.role == "admin":
            admin_dashboard(conn)

if __name__ == "__main__":
    main()

