import streamlit as st
  import os
  from newsapi import NewsApiClient
  from transformers import pipeline

  # Check for NewsAPI key
  NEWS_API_KEY = os.getenv("NEWS_API_KEY")
  if not NEWS_API_KEY:
      st.error("Error: NEWS_API_KEY not found. Add it to Streamlit Secrets or get one at newsapi.org.")
      st.stop()

  # Initialize NewsAPI and summarizer
  try:
      newsapi = NewsApiClient(api_key=NEWS_API_KEY)
      summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
  except Exception as e:
      st.error(f"Failed to initialize app: {str(e)}")
      st.stop()

  # Streamlit UI
  st.title("Crypto News Summarizer 🚀")
  st.write("Get the latest crypto news summarized in seconds! Powered by NewsAPI and BART.")

  if st.button("Fetch & Summarize News"):
      with st.spinner("Grabbing crypto news..."):
          try:
              # Fetch top crypto news
              news = newsapi.get_everything(
                  q="bitcoin OR ethereum OR crypto",
                  sources="coindesk,cointelegraph",
                  language="en",
                  sort_by="publishedAt",
                  page_size=3
              )
              
              if news["status"] != "ok":
                  st.error("Failed to fetch news. Check your API key or internet connection.")
                  st.stop()
              
              # Summarize each article
              for article in news["articles"]:
                  title = article["title"]
                  desc = article["description"] or ""
                  text = f"{title}. {desc}"
                  
                  # Summarize with BART
                  try:
                      summary = summarizer(text, max_length=60, min_length=20, do_sample=False)[0]["summary_text"]
                  except Exception as e:
                      st.warning(f"Summary failed for '{title}': {str(e)}")
                      summary = "Unable to summarize this article."
                  
                  # Display results
                  st.subheader(title)
                  st.write(f"**Source**: {article['source']['name']}")
                  st.write(f"**Summary**: {summary}")
                  st.write(f"[Read more]({article['url']})")
                  st.markdown("---")
                  
          except Exception as e:
              st.error(f"Oops, something broke: {str(e)}")
              st.write("Check your API key, internet, or try again later.")

  st.write("Built for the Sentient News Agents track 📰")
