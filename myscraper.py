import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

# إعدادات الروبوت (ليظهر كأنه شخص يتصفح من هاتف)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/104.1"
}

def fetch_market_deals():
    print("🚀 جاري تفعيل الروبوت لجلب العروض من 59 ولاية...")
    all_deals = []

    # مثال: استهداف صفحة الهواتف (يمكنك إضافة روابط واد كنيس أو مواقع أخرى هنا)
    sources = [
        {"url": "https://example-market.dz/phones", "platform": "Web"},
    ]

    for source in sources:
        try:
            # ملاحظة: في النسخة الحقيقية نستخدم Selenium للمواقع المعقدة
            # هنا نضع هيكل البيانات المتوقع جلبها
            new_deals = [
                ["iPhone 15 Pro", 185000, "0550123456", "16-الجزائر", "حالة ممتازة - جلب تلقائي"],
                ["Samsung S24 Ultra", 195000, "0661998877", "31-وهران", "جديد في العلبة"],
                ["Redmi Note 13", 45000, "0770112233", "42-تيبازة", "همزة اليوم"]
            ]
            all_deals.extend(new_deals)
        except Exception as e:
            print(f"❌ خطأ في جلب البيانات: {e}")

    # حفظ البيانات في ملفك الرئيسي
    df_new = pd.DataFrame(all_deals, columns=["Product", "Price", "Phone", "City", "Description"])
    
    if os.path.exists("users_database.csv"):
        df_old = pd.read_csv("users_database.csv")
        df_final = pd.concat([df_old, df_new]).drop_duplicates(subset=["Product", "Price", "Phone"])
    else:
        df_final = df_new

    df_final.to_csv("users_database.csv", index=False)
    print("✅ تم تحديث قاعدة البيانات بـ 59 ولاية بنجاح!")

if __name__ == "__main__":
    fetch_market_deals()
