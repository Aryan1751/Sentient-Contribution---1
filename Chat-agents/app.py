import streamlit as st
from newsapi import NewsApiClient
from transformers import pipeline

# Inject custom CSS for modern UI and animations
st.markdown("""
    <style>
    /* Import Poppins font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    /* Global styles */
    .main {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        font-family: 'Poppins', sans-serif;
    }
    .title {
        text-align: center;
        color: #007BFF;
        font-size: 2.8em;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .subtitle {
        text-align: center;
        color: #444;
        font-size: 1.3em;
        font-weight: 400;
        margin-bottom: 30px;
    }
    .fetch-button {
        display: block;
        margin: 20px auto;
        background-color: #007BFF;
        color: white;
        padding: 14px 28px;
        border-radius: 10px;
        font-size: 1.2em;
        font-weight: 600;
        transition: transform 0.2s ease, background-color 0.2s ease;
    }
    .fetch-button:hover {
        transform: scale(1.05);
        background-color: #0056b3;
    }
    .article-card {
        background: white;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        padding: 15px;
        margin: 10px;
        height: 100%;
        display: flex;
        flex-direction: column;
        animation: fadeIn 0.5s ease-in;
        transition: transform 0.2s ease;
    }
    .article-card:hover {
        transform: translateY(-5px);
    }
    .article-title {
        color: #007BFF;
        font-size: 1.3em;
        font-weight: 600;
        margin-bottom: 8px;
        line-height: 1.3;
    }
    .article-source {
        color: #666;
        font-size: 0.9em;
        font-weight: 400;
        margin-bottom: 8px;
    }
    .article-summary {
        color: #333;
        font-size: 1em;
        font-weight: 400;
        margin-bottom: 10px;
        flex-grow: 1;
    }
    .article-link {
        color: #007BFF;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.95em;
    }
    .article-link:hover {
        text-decoration: underline;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    /* Responsive design */
    @media (max-width: 768px) {
        .title { font-size: 2.2em; }
        .subtitle { font-size: 1.1em; }
        .fetch-button { padding: 12px 20px; font-size: 1em; }
        .article-card { margin: 10px 5px; padding: 12px; }
        .article-title { font-size: 1.2em; }
    }
    @media (max-width: 480px) {
        .title { font-size: 1.8em; }
        .subtitle { font-size: 0.9em; }
        .fetch-button { padding: 10px 16px; font-size: 0.9em; }
        .article-card { padding: 10px; }
    }
    </style>
""", unsafe_allow_html=True)

# Hardcoded NewsAPI key (temporary, insecure - revert to Secrets after testing)
NEWS_API_KEY = "5ba64418ac10448b872666e55e17298d"
if not NEWS_API_KEY:
    st.error("Error: NEWS_API_KEY not found.")
    st.stop()

# Initialize NewsAPI and summarizer
try:
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
except Exception as e:
    st.error(f"Init failed: {str(e)}")
    st.stop()

# Streamlit UI
with st.container():
    st.markdown('<div class="title">Crypto News Summarizer 🚀</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Latest crypto news, summarized in seconds!</div>', unsafe_allow_html=True)

if st.button("Fetch & Summarize News", key="fetch-button", help="Get the latest crypto news"):
    with st.spinner("Grabbing news..."):
        try:
            news = newsapi.get_everything(
                q="bitcoin OR ethereum OR crypto",
                language="en",
                sort_by="publishedAt",
                page_size=6  # Increased to 6 articles
            )
            if news["status"] != "ok":
                st.error(f"News fetch failed: {news.get('message')}")
                st.stop()
            
            # Horizontal layout: 3x2 grid
            articles = news["articles"]
            for i in range(0, len(articles), 3):  # Process 3 articles per row
                cols = st.columns(3)  # 3 columns for left-to-right
                for j, col in enumerate(cols):
                    if i + j < len(articles):  # Ensure we don't exceed article count
                        article = articles[i + j]
                        title = article["title"]
                        desc = article["description"] or ""
                        text = f"{title}. {desc}"
                        
                        try:
                            summary = summarizer(text, max_length=60, min_length=20, do_sample=False)[0]["summary_text"]
                        except Exception as e:
                            summary = "Unable to summarize."
                        
                        with col:
                            st.markdown(f"""
                                <div class="article-card">
                                    <div class="article-title">{title}</div>
                                    <div class="article-source">Source: {article['source']['name']}</div>
                                    <div class="article-summary">{summary}</div>
                                    <a href="{article['url']}" class="article-link" target="_blank">Read more</a>
                                </div>
                            """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown('<div class="subtitle">Built for Sentient News Agents 📰</div>', unsafe_allow_html=True)
