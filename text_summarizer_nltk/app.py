from deep_translator import GoogleTranslator
import streamlit as st
from summarizer import advanced_summarize

#---Streamlit Page Configuration---
st.set_page_config(
    page_title="SummarizeAI Pro", page_icon="⚡", layout="wide"
)
# Custom CSS Injection
st.markdown(
    """
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        background-color: #4F46E5;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover { background-color: #4338CA; color: white; }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("⚡ SummarizeAI Pro")
st.caption(
    "Advanced TF-IDF Extractive Engine with Multi-Language Translation"
)

# Sidebar
st.sidebar.header("⚙️ Configuration")
sentence_count = st.sidebar.slider("Summary Length", 1, 10, 3)
target_lang = st.sidebar.selectbox(
    "Output Language",
    ["English", "Spanish", "French", "German", "Hindi", "Marathi"],
)
lang_codes = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Marathi": "mr",
}

input_text = st.text_area("Source Text", height=200, placeholder="Paste here...")

if st.button("Generate Smart Summary"):
    if input_text.strip():
        # 1. Advanced TF-IDF Summarization
        raw_summary = advanced_summarize(input_text, num_sentences=sentence_count)
        # 2. Multi-language translation
        if target_lang != "English":
            translated_summary = GoogleTranslator(
                source="auto", target=lang_codes[target_lang]
            ).translate(raw_summary)
        else:
            translated_summary = raw_summary

        st.markdown("### 📌 Summary Result")
        st.info(translated_summary)
