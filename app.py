# Import required libraries
import streamlit as st
import streamlit_ext as stx
from google.generativeai import GenerativeModel, configure, errors
import time
from datetime import datetime, timedelta

# Initialize session state for rate limiting
# last_request_time: Tracks the timestamp of the last API request
# request_count: Keeps count of requests made within a minute
if 'last_request_time' not in st.session_state:
    st.session_state.last_request_time = datetime.min
if 'request_count' not in st.session_state:
    st.session_state.request_count = 0

# Initialize session state for UI elements
if 'prompt_input' not in st.session_state:
    st.session_state.prompt_input = ""
if 'enhanced_prompt_content' not in st.session_state:
    st.session_state.enhanced_prompt_content = ""

# Configure Streamlit page settings
# - Sets page title with emoji
# - Configures wide layout
# - Keeps sidebar expanded by default
st.set_page_config(
    page_title="✨ Magical Prompt Enhancer",
    page_icon="🪄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling section
# Defines styles for:
# - Main background gradient
# - Input fields with rounded corners and shadows
# - Button animations and hover effects
# - Title gradient effects
# - Sidebar appearance
# - Checkbox and spinner customization
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

# Sidebar Configuration
# - API key input with password protection
# - Technique selection with tooltips
# - Each technique has a description shown on hover
with st.sidebar:
    api_key = st.text_input("Enter your Gemini API key:", type="password")
    st.markdown("### Select Prompt Engineering Skills")
    
    # Dictionary of available techniques with their descriptions
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
    
    # Create checkboxes for technique selection
    selected_techniques = []
    for technique, description in techniques.items():
        if st.checkbox(f"{technique}", help=description):
            selected_techniques.append(technique)

# Main Content Section
# Text area for user to input their prompt
st.text_area("Enter your prompt:", height=150, key="prompt_input")

# Buttons Layout
col1, col2 = st.columns([3, 1])  # Adjust ratio as needed

with col1:
    enhance_clicked = st.button(
        "✨ Enhance Prompt",
        disabled=not (api_key and st.session_state.prompt_input and selected_techniques),
        use_container_width=True
    )
with col2:
    if st.button("🧹 Clear Fields", use_container_width=True):
        st.session_state.prompt_input = ""
        st.session_state.enhanced_prompt_content = ""
        st.experimental_rerun()

# Enhancement Button Processing
if enhance_clicked:
    # Rate Limiting Logic
    # Prevents excessive API calls by:
    # - Enforcing 2-second delay between requests
    # - Limiting to 60 requests per minute
    current_time = datetime.now()
    time_diff = current_time - st.session_state.last_request_time
    
    if time_diff.total_seconds() < 2:
        st.warning("🪄 Magic needs a moment to recharge! Please wait a few seconds...")
    elif st.session_state.request_count >= 60:
        wait_time = 60 - time_diff.total_seconds()
        st.warning(f"✨ Magic quota reached! Please wait {int(wait_time)} seconds...")
    else:
        try:
            # API Interaction
            # - Configures Gemini AI with user's API key
            # - Constructs prompt with selected techniques
            # - Handles response and displays enhanced prompt
            with st.spinner("✨ Weaving magical enhancements..."):
                configure(api_key=api_key)
                model = GenerativeModel(model_name="gemini-1.0-pro")
                
                # Construct context for the AI model
                prompt_context = f"""
                As an AI prompt engineer, enhance the following prompt to be more effective and clear.
                Apply these specific techniques: {', '.join(selected_techniques)}.
                
                Original prompt: "{st.session_state.prompt_input}"
                
                Please provide an enhanced version that incorporates all selected techniques while maintaining the core intent of the original prompt.
                Just give only the enhanced prompt no explanation.
                """
                
                # Get and display enhanced prompt
                response = model.generate_content(prompt_context)
                st.session_state.enhanced_prompt_content = response.text
                
                # Update rate limiting trackers
                st.session_state.last_request_time = current_time
                st.session_state.request_count += 1
                
                # Reset counter after one minute
                if time_diff.total_seconds() >= 60:
                    st.session_state.request_count = 0

        except errors.PermissionDeniedError as e:
            st.error(f"🪄 Magic Words Mispronounced! It seems there's an issue with your API key or permissions. Please double-check it. Details: {e}")
        except errors.ResourceExhaustedError as e:
            st.error(f"✨ Magic Overload! You've exceeded your Gemini API quota. Please check your usage and limits. Details: {e}")
        except errors.InvalidArgumentError as e:
            st.error(f"🤔 Hmm, that's an odd request! The input seems invalid. Please check the prompt and try again. Details: {e}")
        except Exception as e:
            # General error handling for API issues
            st.error("🎭 Oops! The magic encountered an unknown hiccup. Please try again. If the problem persists, check the console for more details.")
            st.exception(e) # Keep this for detailed logs in the console

# Displaying the enhanced prompt (outside the enhance_clicked block, so it persists)
if st.session_state.enhanced_prompt_content: # Only display if there's content
    st.markdown("### ✨ Enhanced Prompt:")
    st.text_area("", value=st.session_state.enhanced_prompt_content, height=150, disabled=True, key="enhanced_prompt_display_area")
    stx.copy_button(
        text_to_copy=st.session_state.enhanced_prompt_content,
        label="📋 Copy Enhanced Prompt",
        success_message="Prompt copied to clipboard!"
    )

# Footer section with credits
st.markdown("---")
st.markdown("<div style='text-align: center; padding: 20px;'>✨ Crafted with 🪄 Magic and 🥺 🤗 Love by Karthik ✨</div>", unsafe_allow_html=True)
