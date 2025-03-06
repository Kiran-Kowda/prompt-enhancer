import streamlit as st
from google.generativeai import GenerativeModel, configure
import time
from datetime import datetime, timedelta

# Initialize session state variables
if 'last_request_time' not in st.session_state:
    st.session_state.last_request_time = datetime.min
if 'request_count' not in st.session_state:
    st.session_state.request_count = 0

st.set_page_config(
    page_title="✨ Magical Prompt Enhancer",
    page_icon="🪄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced magical styling with better UX
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #e6f3ff 0%, #f0f9ff 100%);
    }
    .stTextInput > div > div > input {
        background-color: white;
        border-radius: 15px;
        border: 2px solid #e6f3ff;
        padding: 10px;
        box-shadow: 0 4px 15px rgba(0, 158, 255, 0.1);
    }
    .stTextArea > div > div > textarea {
        background-color: white;
        border-radius: 15px;
        border: 2px solid #e6f3ff;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0, 158, 255, 0.1);
    }
    .stButton > button {
        background: linear-gradient(135deg, #1e90ff 0%, #4169e1 100%);
        color: white;
        border-radius: 25px;
        padding: 10px 30px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 15px rgba(30, 144, 255, 0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30, 144, 255, 0.4);
    }
    h1 {
        background: linear-gradient(120deg, #1e90ff, #4169e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em !important;
    }
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.95);
    }
    .stCheckbox > label {
        font-size: 16px;
        color: #2c3e50;
    }
    .stSpinner > div {
        border-color: #1e90ff !important;
    }
</style>
""", unsafe_allow_html=True)

# Update button styling in the CSS
st.markdown("""
<style>
    .stButton > button {
        background: #1e90ff !important;
        color: white !important;
        border-radius: 25px;
        padding: 12px 30px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 15px rgba(30, 144, 255, 0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: #4169e1 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30, 144, 255, 0.4);
    }
    .stButton > button:disabled {
        background: #b0c4de !important;
        transform: none;
        box-shadow: none;
    }
</style>
""", unsafe_allow_html=True)

# Magical title with sparkles
st.markdown("# ✨ Magical Prompt Enhancer 🪄")
st.markdown("### Transform Your Prompts with a Touch of Magic ✨")

# Sidebar for API key and techniques
with st.sidebar:
    api_key = st.text_input("Enter your Gemini API key:", type="password")
    st.markdown("### Select Prompt Engineering Skills")
    
    techniques = {
        'Task/Context/Goal': 'Clearly define objectives',
        'Audience targeting': 'Specify target audience',
        'Affirmative Reinforcing': 'Use positive guidance',
        'Explicit Prompt': 'Be specific and direct',
        'Guidelines': 'Set clear parameters',
        'Constrained Format': 'Specify output format',
        'Zero-Shot Prompting': 'Direct task execution',
        'Guideline Inclusion': 'Include specific rules',
        'Use Delimiters': 'Clear section separation',
        'Imperative Talk': 'Command-like instructions',
        'Identity Warning': 'AI identity specification',
        'Role Assignment': 'Assign specific roles',
        'Echo Directive': 'Confirmation requests',
        'Task Decomposition': 'Break down complex tasks'
    }
    
    selected_techniques = []
    for technique, description in techniques.items():
        if st.checkbox(f"{technique}", help=description):
            selected_techniques.append(technique)

# Main content
# Replace the automatic generation with button-driven generation
prompt = st.text_area("Enter your prompt:", height=150)

if st.button("✨ Enhance Prompt", disabled=not (api_key and prompt and selected_techniques)):
    # Check rate limiting
    current_time = datetime.now()
    time_diff = current_time - st.session_state.last_request_time
    
    if time_diff.total_seconds() < 2:  # Minimum 2 seconds between requests
        st.warning("🪄 Magic needs a moment to recharge! Please wait a few seconds...")
    elif st.session_state.request_count >= 60:  # Maximum 60 requests per minute
        wait_time = 60 - time_diff.total_seconds()
        st.warning(f"✨ Magic quota reached! Please wait {int(wait_time)} seconds...")
    else:
        try:
            with st.spinner("✨ Weaving magical enhancements..."):
                configure(api_key=api_key)
                model = GenerativeModel(model_name="gemini-2.0-pro-exp-02-05")
                
                prompt_context = f"""
                As an AI prompt engineer, enhance the following prompt to be more effective and clear.
                Apply these specific techniques: {', '.join(selected_techniques)}.
                
                Original prompt: "{prompt}"
                
                Please provide an enhanced version that incorporates all selected techniques while maintaining the core intent of the original prompt.
                Just give only the enhanced prompt no explanation.
                """
                
                response = model.generate_content(prompt_context)
                st.markdown("### ✨ Enhanced Prompt:")
                st.text_area("", value=response.text, height=150, disabled=True)
                
                # Update rate limiting counters
                st.session_state.last_request_time = current_time
                st.session_state.request_count += 1
                
                # Reset counter after 1 minute
                if time_diff.total_seconds() >= 60:
                    st.session_state.request_count = 0
                
        except Exception as e:
            st.error("🎭 Oops! The magic encountered a hiccup. Please check your API key and try again.")
            st.exception(e)

# Update the footer
st.markdown("---")
st.markdown("<div style='text-align: center; padding: 20px;'>✨ Crafted with 🪄 Magic and 🥺 🤗 Love by Karthik ✨</div>", unsafe_allow_html=True)
