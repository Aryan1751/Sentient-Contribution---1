import streamlit as st
from newsapi import NewsApiClient
from transformers import pipeline

# Inject custom CSS for clean UI and animations
st.markdown("""
    <style>
    /* Global styles */
    .main {
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
        font-family: Arial, sans-serif;
    }
    .title {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5em;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    .fetch-button {
        display: block;
        margin: 0 auto;
        background-color: #1f77b4;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 1.1em;
        transition: transform 0.2s ease, background-color 0.2s ease;
    }
    .fetch-button:hover {
        transform: scale(1.05);
        background-color: #165a8d;
    }
    .article-card {
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        padding: 20px;
        margin-bottom: 20px;
        animation: fadeIn 0.5s ease-in;
    }
    .article-title {
        color: #1f77b4;
        font-size: 1.4em;
        margin-bottom: 10px;
    }
    .article-source {
        color: #555;
        font-size: 0.9em;
        margin-bottom: 10px;
    }
    .article-summary {
        color: #333;
        font-size: 1em;
        margin-bottom: 10px;
    }
    .article-link {
        color: #1f77b4;
        text-decoration: none;
        font-weight: bold;
    }
    .article-link:hover {
        text-decoration: underline;
    }
    .divider {
        border-top: 1px solid #eee;
        margin: 20px 0;
    }
    .spinner {
        animation: bounce 1s infinite;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    /* Responsive design */
    @media (max-width: 600px) {
        .title { font-size: 2em; }
        .subtitle { font-size: 1em; }
        .article-card { padding: 15px; }
        .fetch-button { padding: 10px 20px; font-size: 1em; }
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

if st.button("Fetch & Summarize News", key="fetch-button", help="Click to get the latest crypto news"):
    with st.spinner("Grabbing news...", _class="spinner"):
        try:
            news = newsapi.get_everything(
                q="bitcoin OR ethereum OR crypto",
                language="en",
                sort_by="publishedAt",
                page_size=3
            )
            if news["status"] != "ok":
                st.error(f"News fetch failed: {news.get('message')}")
                st.stop()
            
            # Responsive columns
            col1, col2, col3 = st.columns([1, 4, 1])  # Middle column wider for content
            with col2:
                for article in news["articles"]:
                    title = article["title"]
                    desc = article["description"] or ""
                    text = f"{title}. {desc}"
                    
                    try:
                        summary = summarizer(text, max_length=60, min_length=20, do_sample=False)[0]["summary_text"]
                    except Exception as e:
                        summary = "Unable to summarize."
                    
                    # Card layout
                    st.markdown(f"""
                        <div class="article-card">
                            <div class="article-title">{title}</div>
                            <div class="article-source">Source: {article['source']['name']}</div>
                            <div class="article-summary">{summary}</div>
                            <a href="{article['url']}" class="article-link" target="_blank">Read more</a>
                        </div>
                        <div class="divider"></div>
                    """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown('<div class="subtitle">Built for Sentient News Agents 📰</div>', unsafe_allow_html=True)
