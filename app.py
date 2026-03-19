import streamlit as st
import openai  # or your preferred LLM library
import re

# 1. AESTHETIC: Mid-Century Modern Styling
st.set_page_config(page_title="BBD Engine v1.0", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #FDF6E3; color: #073642; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { background-color: #268BD2; color: white; border-radius: 0px; border: none; font-weight: bold; }
    .stTextArea textarea { border: 2px solid #93A1A1; background-color: #EEE8D5; }
    h1, h2, h3 { color: #D33682; border-bottom: 2px solid #D33682; padding-bottom: 10px; }
    .bs-score { font-size: 48px; font-weight: bold; color: #CB4B16; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. THE MASTER PROMPT
SYSTEM_PROMPT = """
You are the BBD Engine, a high-precision linguistic analyst. 
Analyze the provided text to identify evasive language and hidden organizational intent.
Output your response STRICTLY in this format:
[BRUTAL REALITY]: (One sentence)
[TRANSLATION]: (The radical honesty version)
[DECODER]: (A markdown table of Jargon vs. Reality)
[INTENT]: (A brief note on the 'Why')
"""

# 3. CORE LOGIC
def analyze_bs(input_text):
    # This is where you'd connect your API key
    # For this example, we assume the API returns a structured response
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": input_text}
        ]
    )
    return response.choices[0].message.content

# 4. THE INTERFACE
st.title("BBD: Business Bullshit Detector")
st.subheader("Deconstructing corporate theater with radical honesty.")

col1, col2 = st.columns([1, 1])

with col1:
    input_text = st.text_area("Paste Corporate Comms Here:", height=300, 
                              placeholder="We are optimizing our human capital ecosystem...")
    analyze_btn = st.button("RUN DIAGNOSTIC")

if analyze_btn and input_text:
    with st.spinner("Decoding institutional abstractions..."):
        raw_output = analyze_bs(input_text)
        
        # Parsing parts for the Score calculation
        # Simple regex to find the 'Translation' section
        translation_match = re.search(r"\[TRANSLATION\]:(.*?)\[", raw_output, re.DOTALL)
        translation_text = translation_match.group(1).strip() if translation_match else input_text
        
        # Calculate BS Score
        original_count = len(input_text.split())
        truth_count = len(translation_text.split())
        bs_score = round(original_count / max(truth_count, 1), 2)

    with col2:
        st.markdown("### The Diagnostic Report")
        st.markdown(f"<div class='bs-score'>{bs_score}</div>", unsafe_allow_html=True)
        st.caption("BS Score ($BS_s$): Higher is more evasive.")
        
        # Display the formatted LLM output
        st.markdown(raw_output)

# 5. FOOTER
st.markdown("---")
st.caption("v1.0 | Architected for Clarity | Builder: Bruce")
