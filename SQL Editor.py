-- ==========================================
-- RASSIM PRO - إنشاء قاعدة البيانات
-- ==========================================

-- 1. جدول الطلبات (رادار المشتري)
CREATE TABLE IF NOT EXISTS requests (
    id SERIAL PRIMARY KEY,
    item TEXT NOT NULL,
    category TEXT,
    phone TEXT NOT NULL,
    wilaya TEXT NOT NULL,
    min_price NUMERIC DEFAULT 0,
    max_price NUMERIC DEFAULT 0,
    condition TEXT DEFAULT 'الكل',
    status TEXT DEFAULT 'نشط',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. جدول التجار (المسجلين)
CREATE TABLE IF NOT EXISTS vendors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    wilaya TEXT NOT NULL,
    category TEXT,
    source TEXT DEFAULT 'direct',
    verified BOOLEAN DEFAULT false,
    trial BOOLEAN DEFAULT true,
    referral_code TEXT UNIQUE,
    referred_by TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. جدول المنافذ (الزبائن المحتملين)
CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    name TEXT,
    phone TEXT NOT NULL,
    wilaya TEXT,
    source TEXT,
    contacted BOOLEAN DEFAULT false,
    converted_to_vendor BOOLEAN DEFAULT false,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. جدول الإحصائيات اليومية
CREATE TABLE IF NOT EXISTS daily_stats (
    id SERIAL PRIMARY KEY,
    stat_date DATE UNIQUE DEFAULT CURRENT_DATE,
    total_requests INTEGER DEFAULT 0,
    total_vendors INTEGER DEFAULT 0,
    total_leads INTEGER DEFAULT 0,
    new_requests INTEGER DEFAULT 0,
    new_vendors INTEGER DEFAULT 0,
    new_leads INTEGER DEFAULT 0,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- إنشاء الفهارس لتحسين الأداء
CREATE INDEX idx_requests_wilaya ON requests(wilaya);
CREATE INDEX idx_requests_created_at ON requests(created_at DESC);
CREATE INDEX idx_vendors_wilaya ON vendors(wilaya);
CREATE INDEX idx_leads_phone ON leads(phone);
