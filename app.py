# main.py
import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
from utils.load_data import load_airbnb_reviews

st.set_page_config(page_title="Airbnb Review Dashboard", layout="wide", page_icon="📊")
st.title("📊 Airbnb Review Dashboard")
st.markdown("**Analisis Data Review Airbnb** – Versi Lokal Terbaru")

# Load data
@st.cache_data
def get_data():
    return load_airbnb_reviews()

df = get_data()

# Hitung Sentimen
@st.cache_data
def calculate_sentiment(df):
    df = df.copy()
    df['sentiment'] = df['comments'].dropna().apply(
        lambda x: TextBlob(str(x)).sentiment.polarity
    )
    return df

df = calculate_sentiment(df)

# Sidebar Filter
st.sidebar.header("🔍 Filter Data")
available_years = sorted(df['year'].dropna().unique().astype(int))
year_filter = st.sidebar.multiselect("Pilih Tahun", options=available_years, default=available_years)
df_filtered = df[df['year'].isin(year_filter)]

# Metrik Utama
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Review", f"{len(df_filtered):,}")
col2.metric("Listing Unik", f"{df_filtered['listing_id'].nunique():,}")
col3.metric("Reviewer Unik", f"{df_filtered['reviewer_id'].nunique():,}")
col4.metric("Tahun Terakhir", f"{int(df_filtered['year'].max())}")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Tren Review", 
    "📅 Heatmap Hari", 
    "📊 Distribusi Bulan/Tahun",
    "🔤 Top 10 Kata",
    "☁️ Word Cloud & Sentimen",
    "📋 Data Mentah"
])

with tab1:
    st.subheader("Tren Jumlah Review per Bulan")
    monthly = df_filtered.groupby(['year', 'month']).size().reset_index(name='review_count')
    monthly['date'] = pd.to_datetime(monthly[['year', 'month']].assign(day=1))
    fig = px.line(monthly, x='date', y='review_count')
    st.plotly_chart(fig, width='stretch')

with tab2:
    st.subheader("📅 Heatmap Review per Hari")
    heatmap_data = df_filtered.groupby(['day_name', 'month']).size().unstack(fill_value=0)
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = heatmap_data.reindex(days_order)
    fig = px.imshow(heatmap_data, text_auto=True, aspect="auto")
    st.plotly_chart(fig, width='stretch')

with tab3:
    st.subheader("📊 Distribusi Review per Tahun & Bulan")
    col_a, col_b = st.columns(2)
    with col_a:
        yearly = df_filtered['year'].value_counts().sort_index()
        st.plotly_chart(px.bar(x=yearly.index, y=yearly.values), width='stretch')
    with col_b:
        monthly_dist = df_filtered['month'].value_counts().sort_index()
        st.plotly_chart(px.bar(x=monthly_dist.index, y=monthly_dist.values), width='stretch')

with tab4:
    st.subheader("🔤 Top 10 Kata Paling Sering")
    text = " ".join(df_filtered['comments'].dropna().astype(str)).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    stopwords = {'the','and','to','of','a','in','for','is','on','that','this','with','it','you','was','are','at','by','from','as','be','have','i','we','not','but','or','an','if','they','their','them','he','she','his','her','our','your'}
    words = [w for w in words if w not in stopwords and len(w) > 2]
    word_counts = Counter(words).most_common(10)
    word_df = pd.DataFrame(word_counts, columns=['Kata', 'Jumlah'])
    st.plotly_chart(px.bar(word_df, x='Kata', y='Jumlah'), width='stretch')
    st.dataframe(word_df)

with tab5:
    st.subheader("☁️ Word Cloud & Analisis Sentimen")
    comments = df_filtered['comments'].dropna().astype(str)
    
    if len(comments) > 0:
        st.write("**Word Cloud**")
        text = " ".join(comments).lower()
        text = re.sub(r'[^a-z\s]', '', text)
        wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords).generate(text)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

    st.write("**Distribusi Sentimen Review**")
    sentiment_count = pd.Series(['Positif' if s > 0.05 else 'Negatif' if s < -0.05 else 'Netral' 
                                for s in df_filtered['sentiment']]).value_counts()
    fig = px.pie(names=sentiment_count.index, values=sentiment_count.values)
    st.plotly_chart(fig, width='stretch')

with tab6:
    st.subheader("Data Mentah (1000 baris pertama)")
    st.dataframe(df_filtered.head(1000), width='stretch')
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Data CSV", csv, "airbnb_review_filtered.csv", "text/csv")

st.success("✅ Dashboard sudah sinkron dengan file reviews.csv")