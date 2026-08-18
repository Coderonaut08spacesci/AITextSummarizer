import heapq
import re
import nltk
import streamlit as streamlit
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
#---Streamlit Page Configuration---
st.set_page_config(
    page_title="AI Text Summarizer",page_icon="📝",layout="centered"
)
#---NLTK Resource Downloader (Cached so it runs only once)---
@st.cache_resource
def download_nltk_resources():
    nltk.download("punkt",quiet=True)
    nltk.download("stopwords",quiet=True)
    nltk.download("punkt_tab",quiet=True)

download_nltk_resources
#---Core Summarization Logic---
def summarize_text(text, num_sentences=3):
    #1. Clean text
    clean_text= re.sub(r"")
