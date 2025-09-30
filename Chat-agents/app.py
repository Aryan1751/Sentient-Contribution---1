import streamlit as st
from newsapi import NewsApiClient
from transformers import pipeline

# Hardcoded NewsAPI key (temporary, insecure - revert to Secrets after testing)
NEWS_API_KEY = "5ba64418ac10448b872666e55e17298d"
if not NEWS_API_KEY:
    st.error("Error: NEWS_API_KEY not found.")
    st.stop()

try:
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
except Exception as e:
    st.error(f"Init failed: {str(e)}")
    st.stop()

st.title("Crypto News Summarizer 🚀")
st.write("Latest crypto news, summarized fast!")

if st.button("Fetch & Summarize News"):
    with st.spinner("Grabbing news..."):
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
            
            for article in news["articles"]:
                title = article["title"]
                desc = article["description"] or ""
                text = f"{title}. {desc}"
                
                try:
                    summary = summarizer(text, max_length=60, min_length=20, do_sample=False)[0]["summary_text"]
                except Exception as e:
                    summary = "Unable to summarize."
                
                st.subheader(title)
                st.write(f"**Source**: {article['source']['name']}")
                st.write(f"**Summary**: {summary}")
                st.write(f"[Read more]({article['url']})")
                st.markdown("---")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.write("Built for Sentient News Agents 📰")
