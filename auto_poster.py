import time
import random
import requests
from datetime import datetime
import schedule

# إعدادات الروبوت
SITE_URL = "https://rassim-os-ultimate.streamlit.app"  # رابط موقعك
POST_INTERVAL_HOURS = 3  # ينشر كل 3 ساعات

# قائمة المجموعات المستهدفة
FACEBOOK_GROUPS = [
    "https://www.facebook.com/groups/ouedkniss.algerie",
    "https://www.facebook.com/groups/algeria.market",
    # ... أضف مجموعات أكثر هنا
]

# قوالب المنشورات (يتغير كل مرة)
POST_TEMPLATES = [
    """🔥 RASSIM OS ULTIMATE 2026 - أول سوق إلكتروني جزائري بالذكاء الاصطناعي!
    
    📱 69 ولاية جزائرية مدعومة بالكامل!
    
    🔗 الرابط: {url}
    """,
    # ... قوالب أخرى
]

def get_random_post():
    """يختار قالب عشوائي ويضيف الرابط"""
    template = random.choice(POST_TEMPLATES)
    return template.format(url=SITE_URL)

def post_to_facebook(group_url, message):
    """ينشر في مجموعة فيسبوك (يحتاج إلى Facebook API)"""
    print(f"📤 جاري النشر في: {group_url}")
    print(f"📝 المنشور: {message[:100]}...")
    return True

def publish_round():
    """جولة نشر واحدة"""
    group = random.choice(FACEBOOK_GROUPS)
    post = get_random_post()
    post_to_facebook(group, post)

def run_bot():
    """تشغيل الروبوت"""
    print("🤖 روبوت RASSIM الناشر - بدأ العمل")
    schedule.every(POST_INTERVAL_HOURS).hours.do(publish_round)
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # يتحقق كل دقيقة

if __name__ == "__main__":
    run_bot()
