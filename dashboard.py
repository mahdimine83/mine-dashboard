import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import BytesIO

# 📌 **تنظیمات صفحه**
st.set_page_config(page_title="📊 داشبورد معدن چاه دراز", layout="wide")

# 📌 **لینک `Raw` فایل اکسل در GitHub (لینک خودتان را جایگزین کنید!)**
file_url = "https://raw.githubusercontent.com/mahdimine83/mine-dashboard/main/گزارش_نهایی_تناژ.xlsx"

@st.cache_data
def load_data():
    """دانلود فایل اکسل از GitHub و بارگذاری آن در DataFrame"""
    try:
        response = requests.get(file_url)
        response.raise_for_status()  # بررسی موفقیت دانلود

        df = pd.read_excel(BytesIO(response.content), engine='openpyxl')
        df["تاریخ"] = pd.to_datetime(df["تاریخ"], format="%Y/%m/%d")  # تبدیل تاریخ به فرمت استاندارد
        return df
    except requests.exceptions.RequestException as e:
        st.error(f"❌ خطا در دریافت داده‌ها از `GitHub`: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ خطای نامشخص: {e}")
        return pd.DataFrame()

# 📌 دریافت داده‌ها از `GitHub`
df = load_data()

# 📌 بررسی اینکه داده‌ای برای نمایش وجود دارد یا نه
if df.empty:
    st.warning("⚠️ داده‌ای برای نمایش وجود ندارد. لطفاً فایل ورودی را بررسی کنید.")
    st.stop()

st.success("✅ فایل اکسل با موفقیت از `GitHub` دانلود شد!")

# 📌 **فیلتر تاریخ**
date_filter = st.sidebar.date_input("📅 انتخاب تاریخ", df["تاریخ"].max())

# 📌 **نمایش داده‌های فیلتر شده**
df_filtered = df[df["تاریخ"] == pd.to_datetime(date_filter)]

if df_filtered.empty:
    st.warning("⚠️ برای این تاریخ داده‌ای وجود ندارد!")
else:
    st.dataframe(df_filtered, use_container_width=True)

# 📌 **نمایش کارت‌های آماری**
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📊 کل باطله‌برداری (تن)", df["تناژ باطله (تن)"].sum())

with col2:
    st.metric("📊 کل ماده معدنی (تن)", df["تناژ سنگ‌شکن (تن)"].sum())

with col3:
    st.metric("🚚 تعداد کل سرویس‌ها", df["تعداد سرویس باطله"].sum() + df["تعداد سرویس سنگ‌شکن"].sum())

# 📌 **نمودار روند استخراج**
st.subheader("📈 روند استخراج باطله و ماده معدنی")
fig1 = px.line(df, x="تاریخ", y=["تناژ باطله (تن)", "تناژ سنگ‌شکن (تن)"],
               labels={"value": "تناژ (تن)", "variable": "نوع"}, title="📈 روند استخراج روزانه")
st.plotly_chart(fig1, use_container_width=True)

# 📌 **نمودار مقایسه تناژها**
st.subheader("📊 مقایسه تناژ روزانه")
fig2 = px.bar(df, x="تاریخ", y=["تناژ باطله (تن)", "تناژ سنگ‌شکن (تن)"],
              barmode='group', labels={"value": "تناژ (تن)", "variable": "نوع"},
              title="📊 مقایسه تناژ باطله و ماده معدنی")
st.plotly_chart(fig2, use_container_width=True)

# 📌 **ذخیره داده‌ها به‌صورت CSV**
df.to_csv("گزارش_معدن.csv", index=False)
st.download_button(label="📥 دانلود گزارش CSV", data=df.to_csv().encode('utf-8'), file_name="گزارش_معدن.csv", mime="text/csv")
