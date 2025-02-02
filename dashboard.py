import streamlit as st
import pandas as pd
import plotly.express as px
import jdatetime

# ✅ تنظیمات صفحه (باید اولین دستور باشد)
st.set_page_config(page_title="سامانه مدیریت معدن چاه دراز", layout="wide")

# 🎨 تغییر استایل و اضافه کردن فونت B Nazanin
st.markdown("""
    <style>
    @font-face {
        font-family: 'BNazanin';
        src: url('file:///C:/Users/mahdi/Documents/BNazanin.ttf') format('truetype');
    }
    * {
        font-family: 'BNazanin', sans-serif !important;
    }
    .css-18e3th9 {
        background-color: #f5f5f5;
    }
    .stMetric {
        font-size: 22px;
        font-weight: bold;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

# 📌 نام سایت و عنوان داشبورد
st.title("🚜 سامانه مدیریت معدن چاه دراز")

# مسیر فایل اکسل
file_path = r"C:\Users\mahdi\Documents\گزارش_نهایی_تناژ.xlsx"

# خواندن داده‌ها
try:
    df = pd.read_excel(file_path, engine="openpyxl")
    st.success("✅ فایل اکسل با موفقیت خوانده شد.")
except FileNotFoundError:
    st.error(f"❌ فایل {file_path} پیدا نشد. لطفاً مسیر را بررسی کنید.")
    st.stop()
except Exception as e:
    st.error(f"❌ خطای غیرمنتظره: {e}")
    st.stop()

# 🔄 تبدیل تاریخ‌های شمسی به میلادی
def shamsi_to_miladi(date_str):
    try:
        year, month, day = map(int, date_str.split("/"))  # تبدیل به عدد
        miladi_date = jdatetime.date(year, month, day).togregorian()
        return miladi_date.strftime("%Y-%m-%d")  # تبدیل به رشته میلادی
    except ValueError:
        return None  # مقدار نامعتبر برمی‌گرداند

df["تاریخ"] = df["تاریخ"].astype(str).apply(shamsi_to_miladi)
df.dropna(subset=["تاریخ"], inplace=True)  # حذف مقادیر نامعتبر
df["تاریخ"] = pd.to_datetime(df["تاریخ"])  # تبدیل به فرمت `datetime` برای پردازش بهتر

# 🗓️ اضافه کردن فیلتر بر اساس تاریخ
st.sidebar.header("📅 فیلتر تاریخی")
date_filter = st.sidebar.date_input("انتخاب تاریخ", df["تاریخ"].max())
df = df[df["تاریخ"] <= pd.to_datetime(date_filter)]

# 🔢 نمایش اطلاعات کلی به‌صورت کارت‌های متریک
col1, col2, col3 = st.columns(3)
col1.metric("📊 کل باطله‌برداری (تن)", f"{df['تناژ باطله (تن)'].sum():,}")
col2.metric("📦 کل ماده معدنی (تن)", f"{df['تناژ سنگ‌شکن (تن)'].sum():,}")
col3.metric("🚚 تعداد کل سرویس‌ها", f"{df['تعداد سرویس باطله'].sum() + df['تعداد سرویس سنگ‌شکن'].sum():,}")

# 📈 نمودار روند استخراج
fig1 = px.line(df, x="تاریخ", y=["تناژ باطله (تن)", "تناژ سنگ‌شکن (تن)"],
               labels={"value": "تناژ (تن)", "variable": "نوع"},
               title="📈 روند استخراج باطله و ماده معدنی")
st.plotly_chart(fig1, use_container_width=True)

# 📊 نمودار مقایسه تناژها
fig2 = px.bar(df, x="تاریخ", y=["تناژ باطله (تن)", "تناژ سنگ‌شکن (تن)"],
              barmode='group', labels={"value": "تناژ (تن)", "variable": "نوع"},
              title="📊 مقایسه تناژ روزانه")
st.plotly_chart(fig2, use_container_width=True)

# 📋 نمایش داده‌ها به‌صورت جدول
st.subheader("📋 داده‌های استخراج شده")
st.dataframe(df, use_container_width=True)

# 📥 قابلیت دانلود داده‌ها
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 دانلود داده‌ها به صورت CSV", csv, "گزارش_معدن.csv", "text/csv", key="download-csv")
