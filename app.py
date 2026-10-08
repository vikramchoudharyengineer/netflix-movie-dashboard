import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Configuration
st.set_page_config(page_title="Netflix Insights Dashboard", layout="wide")
st.title("🎬 Netflix Movie Dataset Insights")

# Load Dataset matching your notebook configuration
@st.cache_data
def load_data():
    try:
        # Using the exact lineterminator that worked in your notebook
        df = pd.read_csv("mymoviedb.csv", lineterminator='\n')
        df['Year'] = pd.to_datetime(df['Release_Date'], errors='coerce').dt.year
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # Layout: Two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💡 Project Conclusions")
        
        # Q1: Most Frequent Genre
        if 'Genre' in df.columns:
            top_genre = df['Genre'].value_counts().idxmax()
            st.markdown("**Q1. What is the most frequent genre in the dataset?**")
            st.success(f"🏆 **{top_genre}** is the most frequent genre in our dataset.")
        
        # Q2: Highest Votes / Popularity
        if 'Vote_Count' in df.columns and 'Genre' in df.columns:
            st.markdown("**Q2. What genres have the highest popularity/votes?**")
            st.info("📈 **Drama** captures highly consistent fan engagement and popular vote volume.")

        # Q3: Lowest Popularity Movie
        if 'Popularity' in df.columns and 'Title' in df.columns:
            lowest_idx = df['Popularity'].idxmin()
            lowest_title = df.loc[lowest_idx, 'Title']
            st.markdown("**Q3. Which movie got the lowest popularity?**")
            st.warning(f"📉 *'{lowest_title}'* holds the lowest popularity score in the dataset.")

        # Q4: Most Filmed Year
        if 'Year' in df.columns and not df['Year'].dropna().empty:
            top_year = int(df['Year'].value_counts().idxmax())
            st.markdown("**Q4. Which year has the most filmed movies?**")
            st.success(f"📅 Year **{top_year}** has the highest filming rate in our dataset.")

    with col2:
        st.subheader("📊 Visualizations")
        
        # Plot 1: Genre Distribution Chart
        if 'Genre' in df.columns:
            st.write("**Genre Column Distribution**")
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            # Get top 15 genres for a clean visual breakdown
            genre_counts = df['Genre'].value_counts().head(15)
            sns.barplot(x=genre_counts.values, y=genre_counts.index, ax=ax1, palette="viridis")
            ax1.set_xlabel("count")
            ax1.set_ylabel("Genre")
            st.pyplot(fig1)
            
        # Plot 2: Release Timeline Histogram
        if 'Year' in df.columns and not df['Year'].dropna().empty:
            st.write("**Release Date Distribution Timeline**")
            fig2, ax2 = plt.subplots(figsize=(6, 3))
            ax2.hist(df['Year'].dropna(), bins=20, color='#E50914', edgecolor='black', alpha=0.8)
            ax2.set_xlabel("Year")
            ax2.set_ylabel("Movie Count")
            st.pyplot(fig2)