import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  
GROQ_MODEL = "qwen-2.5-32b"

# Check API Key
if not GROQ_API_KEY:
    st.error("🔑 API key missing! Please set environment variables.")
    st.stop()

# Initialize Groq Client
groq_client = Groq(api_key=GROQ_API_KEY)

# 🎨 Streamlit UI Setup
st.set_page_config(page_title="🚀 AI Business Name & Tagline Generator", layout="wide")

st.markdown("""
    <h1 style='text-align: center; color: #FF5733;'>🚀 AI Business Name & Tagline Generator</h1>
    <p style='text-align: center; font-size: 18px;'>Enter your business idea, and AI will generate six creative names, each with a tagline and a 30-word description!</p>
""", unsafe_allow_html=True)

# User Input
st.sidebar.header("📝 Business Details")
business_type = st.sidebar.text_input("Enter your business type (e.g., Tech Startup, Clothing Brand, etc.)", "")
category = st.sidebar.selectbox("Select Business Category:", ["Tech", "Fashion", "Food", "Health", "Finance", "Other"])

# Function to generate business names and taglines
def generate_business_names_and_taglines(business_type, category):
    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL, 
            temperature=1,
            messages=[
                {"role": "system", "content": "Generate six creative business names with taglines and a 30-word description for each."},
                {"role": "user", "content": f"Generate six business names with taglines and 30-word descriptions for a {business_type} in the {category} industry."}
            ]
        )
        ai_output = response.choices[0].message.content.strip()
        return ai_output
    except Exception as e:
        st.error(f"❌ API request failed: {e}")
        return None

# Generate Button
if st.sidebar.button("✨ Generate Names & Taglines"):
    if business_type:
        st.subheader("🎉 Your AI-Generated Business Names & Taglines")
        result = generate_business_names_and_taglines(business_type, category)
        if result:
            names = result.split("\n\n")  # Assuming the AI returns names in paragraph format
            for i, name in enumerate(names, start=1):
                parts = name.split("\n")
                if len(parts) >= 3:
                    business_name = parts[0].strip()
                    tagline = parts[1].strip()
                    description = " ".join(parts[2:]).strip()

                    st.markdown(f"""
                        <div style='background-color:#f8f9fa; padding:15px; border-radius:10px; margin-bottom:10px;'>
                            <h3 style='color:#3498db;'>📌 {business_name}</h3>
                            <h5 style='color:#2c3e50;'>{tagline}</h5>
                            <p style='color:#7f8c8d;'>{description}</p>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Unable to generate names. Try again!")
    else:
        st.warning("⚠️ Please enter your business type!")

st.sidebar.markdown("<p style='text-align: center;'>🎵 Powered by <b>Groq AI</b></p>", unsafe_allow_html=True)
