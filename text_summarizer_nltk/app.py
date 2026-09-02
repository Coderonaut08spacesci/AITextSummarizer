import heapq
import re
import nltk
import streamlit as st
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
    clean_text= re.sub(r'\[[0-9]*\]',' ',text)
    clean_text=re.sub(r'\s+',' ',clean_text)
    sentences=sent_tokenize(text)
    words=word_tokenize(clean_text.lower())

    if len(sentences)<=num_sentences:
       return text
    stop_words=set(stopwords.words('english'))
    word_frequencies={}
    for word in words:
        if word.isalnum() and word not in stopwords:
            word_frequencies[word]=word_frequencies.get(word,0)+1
    max_frequency=max(word_frequencies.values(),default=1)
    for word in word_frequencies.keys():
        word_frequencies[word]/=max_frequency

    #4. Score Sentences
    sentence_scores={}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies:
                if len(sent.split(" "))<30:
                    sentence_scores[sent]=(
                        sentence_scores.get(sent,0)+word_frequencies[word]
                    )
    #5. Extract Top N sentences
    summary_sentences=heapq.nlargest(
        num_sentences, sentence_scores, key=sentence_scores.get
    )
    summary_sentences.sort(key=lambda s: sentences.index(s))

<<<<<<< HEAD
#---UI design---
st.title("AI Text Summarizer")
=======
# --- UI Design ---
st.title("📝 AI Text Summarizer")
st.subheader("Extract key insights from long articles in seconds using NLTK.")

#Sidebar controls
>>>>>>> 13ad14dce7762c6834cc340b5745c4f1b82d159b
st.subheader("Extract key insights from long articles in seconds using NLTK.")

# Sidebar Controls
st.sidebar.header("Settings")
sentence_count = st.sidebar.slider(
    "Number of sentences in summary:",
    min_value=1,
    max_value=10,
    value=3,
    step=1,
)

# Text Input Area
input_text = st.text_area(
    "Paste your text/article here:",
    height=250,
    placeholder="Paste a long news article, essay, or paper here...",
)

# Action Button
if st.button("Summarize Text", type="primary"):
    if not input_text.strip():
        st.warning("⚠️ Please paste some text first before summarizing!")
    else:
        with st.spinner("Analyzing word frequencies and generating summary..."):
            summary = summarize_text(input_text, num_sentences=sentence_count)

        st.success("Summary Generated!")
        st.markdown("### 📌 Summary Result:")
        st.write(summary)

        # Quick statistics metric
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Original Sentence Count", len(sent_tokenize(input_text)))
        with col2:
            st.metric(
                "Summary Sentence Count", len(sent_tokenize(summary))
            )
