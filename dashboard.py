import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# 📌 تنظیمات صفحه
st.set_page_config(page_title="📊 داشبورد معدن", layout="wide")

# 📌 **لینک `Raw` فایل اکسل از `GitHub` (لینک خودتان را جایگزین کنید!)**
file_url = "https://raw.githubusercontent.com/mahdimine83/mine-dashboard/main/گزارش_نهایی_تناژ.xlsx"

@st.cache_data
def load_data():
    """دانلود فایل اکسل از GitHub و بارگذاری آن در DataFrame"""
    try:
        response = requests.get(file_url)
        response.raise_for_status()  # بررسی موفقیت دانلود

        df = pd.read_excel(BytesIO(response.content), engine='openpyxl')
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
st.dataframe(df)
