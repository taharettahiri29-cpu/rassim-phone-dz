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
import numpy as np
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

# ==========================================
# 1. إعدادات الصفحة - Ultimate 2026 Edition
# ==========================================
st.set_page_config(
    page_title="RASSIM OS ULTIMATE 2026 • الجزائر",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="auto"
)

# ==========================================
# 2. المتغيرات السرية في الجلسة
# ==========================================
if 'admin_access' not in st.session_state:
    st.session_state.admin_access = False

# ==========================================
# 3. SEO Meta Tags المتطورة
# ==========================================
st.markdown("""
<meta name="description" content="RASSIM OS ULTIMATE 2026 - أول سوق إلكتروني جزائري بتقنية Quantum AI">
<meta name="keywords" content="واد كنيس, هواتف الجزائر, Quantum OS, راسم تيتانيوم, ذكاء اصطناعي">
<meta name="author" content="RASSIM DZ">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
""", unsafe_allow_html=True)

# ==========================================
# 4. نظام "الذكاء العصبي" للواجهة (Neural UI)
# ==========================================
def set_ultimate_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Space Grotesk', 'Inter', sans-serif;
        direction: rtl;
        box-sizing: border-box;
    }

    /* واجهة الـ Liquid Glass - أحدث صيحات 2026 */
    .stApp {
        background: radial-gradient(circle at 20% 20%, #1a1a2a, #0a0a0f);
        color: #ffffff;
        position: relative;
    }

    /* تأثير الجسيمات الكمومية */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(2px 2px at 10px 10px, rgba(0, 255, 255, 0.2), transparent),
            radial-gradient(3px 3px at 50px 100px, rgba(255, 0, 255, 0.2), transparent),
            radial-gradient(2px 2px at 200px 200px, rgba(0, 255, 255, 0.15), transparent);
        background-repeat: repeat;
        background-size: 600px 600px;
        opacity: 0.3;
        pointer-events: none;
        z-index: 0;
        animation: quantumFloat 30s linear infinite;
    }

    @keyframes quantumFloat {
        0% { transform: translateY(0) rotate(0deg); }
        100% { transform: translateY(-100px) rotate(5deg); }
    }

    /* الهيدر العصبي */
    .neural-header {
        background: rgba(10, 10, 20, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(0, 255, 255, 0.2);
        padding: 20px 30px;
        margin-bottom: 30px;
        position: sticky;
        top: 0;
        z-index: 100;
        animation: neuralGlow 3s ease-in-out infinite;
    }

    @keyframes neuralGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 255, 0.2); }
        50% { box-shadow: 0 0 40px rgba(255, 0, 255, 0.3); }
    }

    .neural-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00ffff, #ff00ff, #00ffff);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientPulse 5s ease infinite;
    }

    @keyframes gradientPulse {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    /* كرت إعلاني بتأثير الهولوغرام */
    .hologram-card {
        background: rgba(20, 20, 30, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 255, 0.1);
        border-radius: 30px;
        padding: 28px;
        margin-bottom: 20px;
        transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1);
        position: relative;
        overflow: hidden;
    }

    .hologram-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(0, 255, 255, 0.1), transparent);
        opacity: 0;
        transition: opacity 0.6s;
        animation: rotate 10s linear infinite;
    }

    .hologram-card:hover::before {
        opacity: 1;
    }

    .hologram-card:hover {
        background: rgba(0, 255, 255, 0.05);
        border-color: #00ffff;
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 30px 80px rgba(0, 255, 255, 0.2);
    }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .hologram-card::after {
        content: '';
        position: absolute;
        top: -100%;
        right: -100%;
        width: 100%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(0, 255, 255, 0.05), transparent);
        transform: rotate(45deg);
        animation: shine 4s infinite;
    }

    @keyframes shine {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }

    /* زر الـ Cyber-Action */
    .stButton > button {
        background: linear-gradient(90deg, #00ffff, #ff00ff, #00ffff) !important;
        background-size: 200% 200% !important;
        border: none !important;
        color: black !important;
        font-weight: 800 !important;
        border-radius: 15px !important;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(0, 255, 255, 0.3) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
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
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }

    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        animation: gradientShift 3s ease infinite;
        box-shadow: 0 8px 25px rgba(255, 0, 255, 0.4) !important;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* صناديق البحث الكمومي */
    .quantum-input {
        background: rgba(20, 20, 30, 0.6) !important;
        backdrop-filter: blur(12px) !important;
        border: 2px solid rgba(0, 255, 255, 0.2) !important;
        border-radius: 50px !important;
        color: white !important;
        padding: 16px 24px !important;
        font-size: 1rem !important;
        transition: all 0.4s ease !important;
    }

    .quantum-input:focus {
        border-color: #ff00ff !important;
        box-shadow: 0 0 30px rgba(255, 0, 255, 0.3) !important;
        transform: scale(1.02);
    }

    /* شارة التوثيق */
    .verified-badge {
        background: rgba(0, 255, 255, 0.15);
        border: 1px solid #00ffff;
        color: #00ffff;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .unverified-badge {
        background: rgba(255, 0, 255, 0.15);
        border: 1px solid #ff00ff;
        color: #ff00ff;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* أيقونات المشاركة المتطورة */
    .os-share-icons {
        display: flex;
        gap: 12px;
        justify-content: center;
        flex-wrap: wrap;
    }

    .os-icon {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: rgba(30, 30, 40, 0.8);
        backdrop-filter: blur(8px);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.05);
        cursor: pointer;
        animation: quantumFloat 3s ease-in-out infinite;
    }

    .os-icon:nth-child(1) { animation-delay: 0s; }
    .os-icon:nth-child(2) { animation-delay: 0.2s; }
    .os-icon:nth-child(3) { animation-delay: 0.4s; }
    .os-icon:nth-child(4) { animation-delay: 0.6s; }

    .os-icon:hover {
        background: linear-gradient(135deg, #00ffff, #ff00ff);
        transform: scale(1.15) rotate(5deg);
        border-color: white;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
    }

    .os-icon img {
        width: 24px;
        height: 24px;
        transition: all 0.3s ease;
    }

    .os-icon:hover img {
        filter: brightness(0) invert(1);
        transform: scale(1.1);
    }

    /* القائمة الجانبية العصبية */
    section[data-testid="stSidebar"] {
        background: rgba(10, 10, 15, 0.8) !important;
        backdrop-filter: blur(20px);
        border-left: 1px solid rgba(0, 255, 255, 0.1);
        padding: 20px !important;
    }

    /* بطاقات الإحصائيات */
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
        box-shadow: 0 15px 40px rgba(255, 0, 255, 0.2);
    }

    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #00ffff;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    }

    .stat-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1rem;
        margin-top: 5px;
    }

    /* شريط التمرير */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00ffff, #ff00ff);
        border-radius: 10px;
    }

    /* التجاوب مع الجوال */
    @media screen and (max-width: 768px) {
        .neural-title { font-size: 1.8rem; }
        .stat-value { font-size: 2rem; }
        .os-icon { width: 40px; height: 40px; }
        .os-icon img { width: 20px; height: 20px; }
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 5. نظام التحليل التنبئي (Predictive Analytics)
# ==========================================
def show_market_trends(conn):
    st.markdown("### 📈 نبض السوق الجزائري (AI Live)")
    
    try:
        df = pd.read_sql_query("""
            SELECT category, COUNT(*) as count, AVG(price) as avg_price 
            FROM ads 
            WHERE status='active' 
            GROUP BY category 
            ORDER BY count DESC 
            LIMIT 8
        """, conn)
        
        if not df.empty:
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=df['count'],
                y=df['category'],
                orientation='h',
                marker=dict(
                    color=df['count'],
                    colorscale=[[0, '#00ffff'], [1, '#ff00ff']],
                    line=dict(color='rgba(255,255,255,0.3)', width=1)
                ),
                text=df['count'],
                textposition='auto',
                textfont=dict(color='white', size=12),
                hovertemplate='<b>%{y}</b><br>عدد الإعلانات: %{x}<br>متوسط السعر: %{customdata:,.0f} دج<extra></extra>',
                customdata=df['avg_price']
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', family='Space Grotesk'),
                height=350,
                margin=dict(l=20, r=20, t=30, b=20),
                xaxis=dict(
                    title='عدد الإعلانات',
                    gridcolor='rgba(255,255,255,0.1)',
                    zeroline=False
                ),
                yaxis=dict(
                    title='الفئة',
                    gridcolor='rgba(255,255,255,0.1)'
                ),
                hoverlabel=dict(
                    bgcolor='rgba(20,20,30,0.9)',
                    font=dict(color='white', size=12)
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("جاري تحميل التحليلات...")

# ==========================================
# 6. لوحة التحكم السرية للإدارة
# ==========================================
def rassim_os_admin_logic():
    """لوحة التحكم السرية - للمصرح لهم فقط"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00ffff20, #ff00ff20); 
    backdrop-filter: blur(12px); border: 2px solid #00ffff; border-radius: 30px; 
    padding: 30px; margin: 30px 0;">
        <h1 style="text-align: center; color: white; font-size: 3rem;">🔐 RASSIM OS ADMIN</h1>
        <p style="text-align: center; color: #00ffff;">مستوى الدخول: القائد 🛰️</p>
    </div>
    """, unsafe_allow_html=True)
    
    conn = get_connection()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 الإحصائيات الكمومية", 
        "👥 المستخدمين", 
        "📢 الإعلانات", 
        "💬 الرسائل", 
        "🚨 النظام"
    ])
    
    with tab1:
        users, ads, visitors, views = get_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="stat-card"><div class="stat-value">{users}</div><div class="stat-label">مستخدم</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="stat-card"><div class="stat-value">{ads}</div><div class="stat-label">إعلان</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="stat-card"><div class="stat-value">{visitors}</div><div class="stat-label">زيارة</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="stat-card"><div class="stat-value">{views}</div><div class="stat-label">مشاهدة</div></div>', unsafe_allow_html=True)
        
        show_market_trends(conn)
    
    with tab2:
        st.subheader("👥 إدارة المستخدمين")
        users_df = pd.read_sql_query("""
            SELECT username, role, verified, banned, ad_count, 
                   substr(last_login, 1, 10) as last_login,
                   email, phone
            FROM users ORDER BY last_login DESC
        """, conn)
        st.dataframe(users_df, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            username = st.selectbox("اختر مستخدم", users_df['username'].tolist())
        with col2:
            if st.button("✅ توثيق المستخدم", use_container_width=True):
                conn.execute("UPDATE users SET verified=1 WHERE username=?", (username,))
                conn.commit()
                st.success(f"تم توثيق {username}")
                st.rerun()
        with col3:
            if st.button("🚫 حظر المستخدم", use_container_width=True):
                conn.execute("UPDATE users SET banned=1 WHERE username=?", (username,))
                conn.commit()
                st.success(f"تم حظر {username}")
                st.rerun()
    
    with tab3:
        st.subheader("📢 إدارة الإعلانات")
        ads_df = pd.read_sql_query("""
            SELECT id, title, price, owner, views, featured, status, date
            FROM ads ORDER BY date DESC LIMIT 50
        """, conn)
        st.dataframe(ads_df, use_container_width=True)
        
        ad_id = st.number_input("معرف الإعلان", min_value=1)
        if st.button("⭐ تمييز كمميز", use_container_width=True):
            conn.execute("UPDATE ads SET featured=1 WHERE id=?", (ad_id,))
            conn.commit()
            st.success("تم التمييز")
            st.rerun()
    
    with tab4:
        st.subheader("💬 جميع الرسائل")
        msgs_df = pd.read_sql_query("""
            SELECT sender, receiver, message, read, date
            FROM messages ORDER BY date DESC LIMIT 100
        """, conn)
        st.dataframe(msgs_df, use_container_width=True)
    
    with tab5:
        st.subheader("🚨 تقارير النظام")
        reports_df = pd.read_sql_query("""
            SELECT r.id, a.title, r.reporter, r.reason, r.status, r.date
            FROM reports r JOIN ads a ON r.ad_id = a.id
            ORDER BY r.date DESC
        """, conn)
        st.dataframe(reports_df, use_container_width=True)

# ==========================================
# 7. محرك البحث الذكي (Quantum Search)
# ==========================================
def quantum_search_ui():
    st.markdown("### 🔍 البحث الكمومي")
    
    col1, col2, col3 = st.columns([3, 1.2, 1])
    
    with col1:
        search_query = st.text_input(
            "", 
            placeholder="🔍 ابحث بالصوت أو النص (مثلاً: آيفون 15 برو ماكس نظيف في الجزائر العاصمة)",
            key="quantum_search"
        )
    
    with col2:
        ai_mode = st.selectbox(
            "",
            ["🧠 أفضل سعر", "⚡ الأكثر ثقة", "🌟 الأحدث", "📈 الأكثر مشاهدة"],
            label_visibility="collapsed"
        )
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔮 Flash Scan", use_container_width=True):
            st.success("جاري المسح الكمومي...")
    
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        wilaya = st.selectbox("الولاية", ["الكل"] + [f"{i:02d}" for i in range(1, 59)])
    with col_b:
        price_range = st.selectbox("السعر", ["الكل", "أقل من 5 مليون", "5-10 مليون", "10-20 مليون", "أكثر من 20 مليون"])
    with col_c:
        condition = st.selectbox("الحالة", ["الكل", "جديد", "مستعمل", "مجدّد"])
    with col_d:
        sort = st.selectbox("الترتيب", ["الأحدث", "السعر", "المشاهدات"])
    
    return search_query, wilaya, price_range, condition, sort

# ==========================================
# 8. دالة الإعلان الذهبية (The Golden Ad)
# ==========================================
def render_ad_pro(ad, verified=False):
    verified_badge = "✅ موثوق" if verified else "⚠️ غير موثق"
    badge_class = "verified-badge" if verified else "unverified-badge"
    
    st.markdown(f"""
    <div class="hologram-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <div style="display: flex; gap: 15px; align-items: center;">
                <span style="color: #888; font-size: 0.85rem;">📍 {ad['wilaya']}</span>
                <span style="color: #888; font-size: 0.85rem;">🕐 {ad['date'][:10] if ad['date'] else ''}</span>
                <span style="color: #888; font-size: 0.85rem;">👁️ {ad['views']}</span>
            </div>
            <span class="{badge_class}">{verified_badge}</span>
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <h2 style="margin: 0; color: white; font-size: 1.8rem;">{ad['title']}</h2>
            <div style="display: flex; align-items: baseline; gap: 5px;">
                <span style="font-size: 2rem; font-weight: 800; color: #00ffff;">{ad['price']:,}</span>
                <span style="color: #ff00ff; font-weight: 600;">دج</span>
            </div>
        </div>
        
        <p style="color: #aaa; margin: 15px 0; line-height: 1.6;">{ad['description'][:150]}...</p>
        
        <div style="display: flex; gap: 10px; margin-top: 20px;">
            <div style="flex: 2;">
                <div style="display: flex; gap: 10px;">
                    <span style="background: rgba(255,255,255,0.05); padding: 5px 15px; border-radius: 50px; color: #00ffff;">#{ad['category']}</span>
                    <span style="background: rgba(255,255,255,0.05); padding: 5px 15px; border-radius: 50px; color: #ff00ff;">👤 {ad['owner']}</span>
                </div>
            </div>
            <div style="flex: 1; display: flex; gap: 10px; justify-content: flex-end;">
                <span class="os-icon" style="width: 45px; height: 45px;"><img src="https://img.icons8.com/color/48/whatsapp--v1.png"></span>
                <span class="os-icon" style="width: 45px; height: 45px;"><img src="https://img.icons8.com/color/48/phone--v1.png"></span>
                <span class="os-icon" style="width: 45px; height: 45px;"><img src="https://img.icons8.com/color/48/favorite--v1.png"></span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"📞 اتصل بالبائع", key=f"call_{ad['id']}", use_container_width=True):
            st.info(f"رقم الهاتف: {ad['phone']}")
    with col2:
        if st.button(f"⚡ شراء سريع", key=f"buy_{ad['id']}", use_container_width=True):
            st.success("تم إرسال طلبك إلى البائع")

# ==========================================
# 9. أزرار المشاركة المتطورة
# ==========================================
def show_social_share():
    site_url = "https://racim-phone.streamlit.app/"
    
    st.markdown(f"""
    <div style="text-align: center; margin: 30px 0;">
        <div class="os-share-icons">
            <a href="https://www.facebook.com/sharer/sharer.php?u={site_url}" target="_blank">
                <div class="os-icon"><img src="https://img.icons8.com/color/48/facebook-new.png"></div>
            </a>
            <a href="https://api.whatsapp.com/send?text=🔥 الدزة الجزائرية: {site_url}" target="_blank">
                <div class="os-icon"><img src="https://img.icons8.com/color/48/whatsapp--v1.png"></div>
            </a>
            <a href="https://t.me/share/url?url={site_url}&text=🇩🇿 أول سوق إلكتروني جزائري" target="_blank">
                <div class="os-icon"><img src="https://img.icons8.com/color/48/telegram-app--v1.png"></div>
            </a>
            <div class="os-icon" onclick="copyLink()">
                <img src="https://img.icons8.com/color/48/link--v1.png">
            </div>
        </div>
    </div>
    
    <script>
    function copyLink() {{
        navigator.clipboard.writeText('{site_url}');
        alert('✅ تم نسخ الرابط - شاركه مع صحابك! 🇩🇿');
        
        const btn = event.currentTarget;
        btn.style.background = 'linear-gradient(135deg, #00ffff, #ff00ff)';
        setTimeout(() => btn.style.background = '', 300);
    }}
    </script>
    """, unsafe_allow_html=True)

# ==========================================
# 10. إعدادات قاعدة البيانات
# ==========================================
DB = "rassim_os_ultimate.db"

def init_db():
    """تهيئة قاعدة البيانات المتطورة"""
    try:
        conn = sqlite3.connect(DB, check_same_thread=False)
        cursor = conn.cursor()
        
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
                verified INTEGER DEFAULT 0,
                date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner) REFERENCES users(username)
            )
        """)
        
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
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS visitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT,
                page TEXT,
                date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                event_data TEXT,
                username TEXT,
                date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        return conn
    except Exception as e:
        st.error(f"Ultimate Error: {e}")
        return None

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB, check_same_thread=False)

init_db()

# ==========================================
# 11. دوال المساعدة المتطورة
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

def get_verified_status(username):
    try:
        conn = get_connection()
        verified = conn.execute("SELECT verified FROM users WHERE username=?", (username,)).fetchone()
        return verified[0] if verified else 0
    except:
        return 0

# ==========================================
# 12. صفحة تسجيل الدخول المتطورة
# ==========================================
def login_page():
    users, ads, visitors, views = get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{users}</div><div class="stat-label">مستخدم</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{ads}</div><div class="stat-label">إعلان</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{visitors}</div><div class="stat-label">زيارة</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{views}</div><div class="stat-label">مشاهدة</div></div>', unsafe_allow_html=True)
    
    show_social_share()
    
    tab1, tab2 = st.tabs(["🔑 دخول", "📝 حساب جديد"])
    conn = get_connection()
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("👤 اسم المستخدم")
            password = st.text_input("🔐 كلمة المرور", type="password")
            
            if st.form_submit_button("⚡ دخول سريع", use_container_width=True):
                if not username or not password:
                    st.error("❌ يرجى ملء جميع الحقول")
                else:
                    try:
                        user = conn.execute(
                            "SELECT password, salt, role, verified FROM users WHERE username=?",
                            (username,)
                        ).fetchone()
                        
                        if user and user[0] == hash_password(password, user[1]):
                            st.session_state.user = username
                            st.session_state.role = user[2]
                            st.session_state.verified = user[3]
                            st.rerun()
                        else:
                            st.error("❌ بيانات غير صحيحة")
                    except:
                        st.error("❌ خطأ في تسجيل الدخول")
    
    with tab2:
        with st.form("register_form"):
            new_user = st.text_input("👤 اسم المستخدم")
            new_pass = st.text_input("🔐 كلمة المرور", type="password")
            email = st.text_input("📧 البريد الإلكتروني")
            phone = st.text_input("📱 رقم الهاتف")
            
            if st.form_submit_button("✨ تسجيل متقدم", use_container_width=True):
                if not new_user or not new_pass:
                    st.error("❌ الحقول مطلوبة")
                elif len(new_user) < 3:
                    st.error("❌ اسم مستخدم قصير")
                elif len(new_pass) < 6:
                    st.error("❌ كلمة مرور قصيرة")
                else:
                    try:
                        salt = secrets.token_hex(16)
                        hashed = hash_password(new_pass, salt)
                        
                        conn.execute("""
                            INSERT INTO users (username, password, salt, email, phone, role, verified)
                            VALUES (?, ?, ?, ?, ?, 'user', 0)
                        """, (new_user, hashed, salt, email, phone))
                        conn.commit()
                        
                        st.success("✅ تم التسجيل بنجاح!")
                    except:
                        st.error("❌ اسم المستخدم موجود")

# ==========================================
# 13. صفحة السوق الذكي
# ==========================================
def show_market(conn):
    st.markdown("### 🛍️ السوق الذكي Quantum")
    
    search_query, wilaya, price_range, condition, sort = quantum_search_ui()
    
    with st.expander("📊 تحليلات السوق الحية", expanded=False):
        show_market_trends(conn)
    
    show_social_share()
    
    try:
        query = "SELECT * FROM ads WHERE status='active'"
        params = []
        
        if search_query:
            query += " AND (title LIKE ? OR description LIKE ?)"
            params.extend([f"%{search_query}%", f"%{search_query}%"])
        if wilaya and wilaya != "الكل":
            query += " AND wilaya=?"
            params.append(wilaya)
        
        if sort == "السعر":
            query += " ORDER BY price"
        elif sort == "المشاهدات":
            query += " ORDER BY views DESC"
        else:
            query += " ORDER BY date DESC"
        
        query += " LIMIT 10"
        
        ads = conn.execute(query, params).fetchall()
        
        if ads:
            for ad in ads:
                verified = get_verified_status(ad[11])
                ad_dict = {
                    'id': ad[0],
                    'title': ad[1],
                    'price': ad[2],
                    'phone': ad[3],
                    'wilaya': ad[4],
                    'description': ad[5],
                    'category': ad[6],
                    'views': ad[8],
                    'owner': ad[11],
                    'date': ad[12] if len(ad) > 12 else ''
                }
                render_ad_pro(ad_dict, verified)
        else:
            st.info("لا توجد إعلانات حالياً")
    except Exception as e:
        st.error(f"خطأ: {e}")

# ==========================================
# 14. صفحة إضافة إعلان
# ==========================================
def post_ad(conn):
    st.markdown("### 📢 إضافة إعلان ذهبي")
    
    with st.form("new_ad_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("📱 اسم المنتج *")
            category = st.selectbox("🏷️ الفئة", ["سامسونج", "آيفون", "هواوي", "شاومي", "أخرى"])
        with col2:
            price = st.number_input("💰 السعر (دج) *", min_value=0, step=1000)
            wilaya = st.selectbox("📍 الولاية *", [f"{i:02d}" for i in range(1, 59)])
        
        phone = st.text_input("📞 رقم الهاتف *")
        description = st.text_area("📝 الوصف التفصيلي")
        
        if price == 0:
            st.info("💡 اترك السعر صفر للحصول على توصية ذكية من السوق")
        
        if st.form_submit_button("🚀 نشر الإعلان", use_container_width=True):
            if not title or not phone:
                st.error("❌ يرجى ملء الحقول المطلوبة")
            else:
                try:
                    if price == 0:
                        avg_price = conn.execute("""
                            SELECT AVG(price) FROM ads 
                            WHERE category=? AND wilaya=? AND status='active'
                        """, (category, wilaya)).fetchone()[0]
                        if avg_price:
                            price = int(avg_price)
                            st.info(f"💰 السعر المقترح: {price:,} دج")
                    
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
                    st.error(f"❌ خطأ: {e}")

# ==========================================
# 15. صفحة الدردشة المتطورة
# ==========================================
def show_chat(conn):
    st.markdown("### 💬 المحادثات الكمومية")
    
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
            st.markdown(f"#### الدردشة مع {selected}")
            
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
                    st.markdown(f"""
                    <div style="background: rgba(0,255,255,0.1); border: 1px solid #00ffff; 
                    padding: 12px; border-radius: 20px 20px 5px 20px; margin: 10px 0; max-width: 80%; margin-left: auto;">
                        <b>أنت:</b> {msg[1]}<br>
                        <small style="color: #888;">{msg[2][11:16]}</small>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: rgba(255,0,255,0.1); border: 1px solid #ff00ff; 
                    padding: 12px; border-radius: 20px 20px 20px 5px; margin: 10px 0; max-width: 80%;">
                        <b>{msg[0]}:</b> {msg[1]}<br>
                        <small style="color: #888;">{msg[2][11:16]}</small>
                    </div>
                    """, unsafe_allow_html=True)
            
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
        st.error(f"خطأ: {e}")

# ==========================================
# 16. التشغيل الرئيسي النهائي مع النظام السري
# ==========================================
def main():
    set_ultimate_theme()
    
    st.markdown("""
    <div class="neural-header">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <span class="neural-title">RASSIM OS ULTIMATE</span>
                <span style="background: rgba(255,255,255,0.1); padding: 4px 12px; border-radius: 30px; font-size: 0.8rem; margin-right: 10px;">2026</span>
            </div>
            <div style="display: flex; gap: 20px;">
                <span style="color: #00ffff;">⚡ Quantum</span>
                <span style="color: #ff00ff;">🔮 AI</span>
                <span style="color: rgba(255,255,255,0.3);">📶 5G</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if "user" not in st.session_state:
        st.session_state.user = None
    if "role" not in st.session_state:
        st.session_state.role = "user"
    if "verified" not in st.session_state:
        st.session_state.verified = 0
    if "ip" not in st.session_state:
        st.session_state.ip = secrets.token_hex(8)
    if 'admin_access' not in st.session_state:
        st.session_state.admin_access = False
    
    log_visitor()
    
    if not st.session_state.user:
        login_page()
    else:
        conn = get_connection()
        
        with st.sidebar:
            verified_badge = "✅ موثوق" if st.session_state.verified else "⏳ غير موثق"
            badge_color = "#00ffff" if st.session_state.verified else "#ff00ff"
            
            st.markdown(f"""
            <div style="background: rgba(20,20,30,0.5); backdrop-filter: blur(12px); 
            border: 1px solid rgba(0,255,255,0.1); border-radius: 25px; padding: 25px; 
            text-align: center; margin-bottom: 25px;">
                <div style="font-size: 4rem; margin-bottom: 10px;">⚡</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: white;">{st.session_state.user}</div>
                <div style="color: {badge_color}; font-size: 0.9rem; margin-top: 8px;">{verified_badge}</div>
                <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem; margin-top: 5px;">{st.session_state.role}</div>
            </div>
            """, unsafe_allow_html=True)
            
            menu_options = ["🛍️ السوق الذكي", "📢 إضافة إعلان", "💬 المحادثات", "🤖 المساعد الذكي"]
            if st.session_state.role == "admin":
                menu_options.append("🔐 لوحة الإدارة")
            
            choice = st.radio("", menu_options, label_visibility="collapsed")
            
            st.divider()
            
            # ===== النظام السري للإدارة =====
            with st.expander("🔧 النظام", expanded=False):
                secret_key = st.text_input("System Code", type="password", help="للمصرح لهم فقط")
                
                if secret_key == "RASSIM-42-2026":
                    st.session_state.admin_access = True
                    st.success("تم تفعيل وضع القائد 🛰️")
                elif secret_key != "":
                    st.error("كود خاطئ ⚠️")
            
            if st.button("🚪 خروج", use_container_width=True):
                st.session_state.user = None
                st.rerun()
        
        # عرض لوحة الإدارة السرية إذا تم التفعيل
        if st.session_state.admin_access:
            rassim_os_admin_logic()
            if st.sidebar.button("إغلاق لوحة التحكم 🔒", use_container_width=True):
                st.session_state.admin_access = False
                st.rerun()
        
        # توجيه الصفحات العادية
        elif choice == "🛍️ السوق الذكي":
            show_market(conn)
        elif choice == "📢 إضافة إعلان":
            post_ad(conn)
        elif choice == "💬 المحادثات":
            show_chat(conn)
        elif choice == "🤖 المساعد الذكي":
            st.markdown("### 🤖 المساعد الكمومي")
            st.info("قيد التطوير - قريباً")
        elif choice == "🔐 لوحة الإدارة" and st.session_state.role == "admin":
            # لوحة الإدارة العادية (للمسؤولين العاديين)
            st.info("لوحة الإدارة العادية - استخدم النظام السري للوصول الكامل")

if __name__ == "__main__":
    main()

