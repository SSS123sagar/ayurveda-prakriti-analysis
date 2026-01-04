import streamlit as st
from collections import Counter
import pandas as pd
from datetime import datetime, date, timedelta
import base64

# =============================
# PAGE CONFIG & ANCIENT THEME
# =============================
st.set_page_config(
    page_title="Vaidya: Prakriti Mastery",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Ancient Wisdom Theme with improved button colors and DARK MODE SUPPORT
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&family=Merriweather:wght@300;400;700&display=swap');
    
    /* CSS Variables for Light/Dark Mode */
    :root {
        /* Light Mode Colors */
        --light-bg: linear-gradient(135deg, #f5f1e8 0%, #f0e6d6 100%);
        --light-bg-radial: radial-gradient(circle at 10% 20%, rgba(142, 110, 99, 0.03) 0%, transparent 20%),
                           radial-gradient(circle at 90% 80%, rgba(78, 52, 46, 0.02) 0%, transparent 20%);
        --light-text: #1a1a1a;
        --light-card-bg: rgba(255, 255, 255, 0.95);
        --light-card-border: #d7ccc8;
        --light-metric-bg: white;
        
        /* Dark Mode Colors */
        --dark-bg: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        --dark-bg-radial: radial-gradient(circle at 10% 20%, rgba(142, 110, 99, 0.1) 0%, transparent 20%),
                          radial-gradient(circle at 90% 80%, rgba(78, 52, 46, 0.05) 0%, transparent 20%);
        --dark-text: #f0f0f0;
        --dark-card-bg: rgba(40, 40, 40, 0.95);
        --dark-card-border: #444;
        --dark-metric-bg: #2d2d2d;
        
        /* Common Colors */
        --primary-gold: #D4AF37;
        --primary-gold-dark: #B8860B;
        --secondary-green: #388e3c;
        --secondary-green-dark: #2e7d32;
        --vata-color: #8e6e63;
        --pitta-color: #d32f2f;
        --kapha-color: #388e3c;
        --h1-color: #4e342e;
        --h2-color: #5d4037;
        --subtitle-color: #795548;
    }
    
    /* Apply colors based on data-theme attribute */
    .main {
        background: var(--light-bg);
        background-image: var(--light-bg-radial);
        color: var(--light-text);
    }
    
    /* Dark Mode Detection and Overrides */
    @media (prefers-color-scheme: dark) {
        :root {
            --h1-color: #e0d6cc;
            --h2-color: #d7ccc8;
            --subtitle-color: #bcaaa4;
        }
        
        .main {
            background: var(--dark-bg);
            background-image: var(--dark-bg-radial);
            color: var(--dark-text);
        }
        
        /* Dark Mode Text Colors */
        h1, h2, h3 {
            color: var(--dark-text) !important;
        }
        
        .subtitle {
            color: var(--subtitle-color) !important;
        }
        
        p, span, label, .stSelectbox label, .stRadio label, div[data-testid="stMarkdownContainer"] p {
            color: var(--dark-text) !important;
        }
        
        /* Dark Mode Cards */
        .wisdom-card {
            background: var(--dark-card-bg);
            border-color: var(--dark-card-border);
            color: var(--dark-text);
        }
        
        /* Dark Mode Specific Card Backgrounds */
        .vata-card {
            background: linear-gradient(90deg, rgba(142, 110, 99, 0.1) 0%, var(--dark-card-bg) 10%) !important;
        }
        
        .pitta-card {
            background: linear-gradient(90deg, rgba(211, 47, 47, 0.1) 0%, var(--dark-card-bg) 10%) !important;
        }
        
        .kapha-card {
            background: linear-gradient(90deg, rgba(56, 142, 60, 0.1) 0%, var(--dark-card-bg) 10%) !important;
        }
        
        /* Dark Mode Metric Cards */
        .metric-card {
            background: var(--dark-metric-bg);
            border-color: var(--dark-card-border);
            color: var(--dark-text);
        }
        
        /* Dark Mode Fact Boxes */
        .fact-box {
            background: linear-gradient(135deg, #2a2a2a 0%, #333 100%);
            border-color: #555;
            color: var(--dark-text);
        }
        
        .nepali-date-box {
            background: linear-gradient(135deg, #1a2a3a 0%, #2a3a4a 100%);
            border-color: #3a5a7a;
            color: var(--dark-text);
        }
        
        /* Dark Mode Routine Items */
        .routine-item {
            background: rgba(40, 40, 40, 0.9);
            border-left-color: #8d6e63;
            color: var(--dark-text);
        }
        
        .routine-time {
            color: #e0d6cc;
        }
        
        /* Dark Mode Question Toggle */
        .question-toggle-container {
            background: linear-gradient(135deg, #2a2a2a 0%, #333 100%);
            border-color: #555;
            color: var(--dark-text);
        }
        
        .question-toggle-container:hover {
            background: linear-gradient(135deg, #333 0%, #3a3a3a 100%);
            border-color: var(--vata-color);
        }
        
        /* Dark Mode Footer */
        .footer {
            background: linear-gradient(135deg, rgba(40, 40, 40, 0.7) 0%, rgba(50, 50, 50, 0.7) 100%) !important;
            border-top-color: #555;
            color: #bcaaa4 !important;
        }
        
        .footer a {
            color: #d7a46e !important;
        }
        
        /* Dark Mode Expanders */
        .streamlit-expanderHeader {
            color: var(--dark-text) !important;
            background-color: var(--dark-card-bg) !important;
            border-color: var(--dark-card-border) !important;
        }
        
        .streamlit-expanderHeader:hover {
            background-color: rgba(50, 50, 50, 0.95) !important;
        }
        
        /* Dark Mode Info/Warning/Success/Error Boxes */
        .stAlert {
            background-color: rgba(40, 40, 40, 0.9) !important;
            border-color: #555 !important;
        }
        
        /* Dark Mode Radio Buttons */
        .stRadio > div > label {
            color: var(--dark-text) !important;
        }
        
        /* Dark Mode Select Box */
        .stSelectbox > div > div > div {
            color: var(--dark-text) !important;
        }
        
        /* Dark Mode Date Input */
        .stDateInput > div > div > input {
            background-color: var(--dark-metric-bg) !important;
            color: var(--dark-text) !important;
            border-color: #555 !important;
        }
        
        /* Dark Mode Number Input */
        .stNumberInput > div > div > input {
            background-color: var(--dark-metric-bg) !important;
            color: var(--dark-text) !important;
            border-color: #555 !important;
        }
        
        /* Dark Mode Text Input */
        .stTextInput > div > div > input {
            background-color: var(--dark-metric-bg) !important;
            color: var(--dark-text) !important;
            border-color: #555 !important;
        }
        
        /* Dark Mode Slider */
        .stSlider > div > div > div {
            background-color: #555 !important;
        }
        
        /* Dark Mode Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(60, 60, 60, 0.8) !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #444 !important;
            color: #ccc !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #8d6e63 0%, #6d4c41 100%) !important;
            color: white !important;
        }
        
        /* Dark Mode Progress Bar Background */
        .stProgress > div > div {
            background-color: #555 !important;
        }
        
        /* Welcome message container for dark mode */
        .welcome-container {
            background: rgba(255, 255, 255, 0.8) !important;
        }
        
        @media (prefers-color-scheme: dark) {
            .welcome-container {
                background: rgba(40, 40, 40, 0.9) !important;
                color: var(--dark-text) !important;
            }
            
            .welcome-container h3 {
                color: var(--dark-text) !important;
            }
            
            .welcome-container p {
                color: var(--dark-text) !important;
            }
            
            .welcome-container .quote {
                color: #d7a46e !important;
            }
        }
    }
    
    /* Typography Hierarchy */
    h1 {
        font-family: 'Crimson Text', serif;
        color: var(--h1-color) !important;
        text-align: center;
        font-weight: 700;
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        letter-spacing: -0.5px;
        animation: fadeInDown 1s ease;
    }
    
    h2, h3 {
        font-family: 'Crimson Text', serif;
        color: var(--h2-color) !important;
        font-weight: 600;
        border-bottom: 1px solid var(--light-card-border);
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        animation: fadeIn 1.2s ease;
    }
    
    .subtitle {
        font-family: 'Merriweather', serif;
        color: var(--subtitle-color) !important;
        text-align: center;
        font-size: 1.2rem;
        font-style: italic;
        margin-bottom: 2rem;
        animation: fadeIn 1.5s ease;
    }
    
    p, span, label, .stSelectbox label, .stRadio label {
        font-family: 'Inter', sans-serif;
        color: var(--light-text) !important;
        line-height: 1.6;
    }
    
    /* Enhanced Card Design */
    .wisdom-card {
        background: var(--light-card-bg);
        border: 1px solid var(--light-card-border);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 2px 4px 12px rgba(78, 52, 46, 0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
        animation: slideInUp 0.8s ease;
    }
    
    .wisdom-card:hover {
        transform: translateY(-2px);
        box-shadow: 4px 6px 16px rgba(78, 52, 46, 0.12);
    }
    
    .wisdom-card::before {
        content: "ॐ";
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 1.5rem;
        color: rgba(142, 110, 99, 0.1);
        font-family: 'Inter', sans-serif;
    }
    
    /* Dosha-specific cards */
    .vata-card {
        border-left: 6px solid var(--vata-color);
        background: linear-gradient(90deg, rgba(142, 110, 99, 0.05) 0%, var(--light-card-bg) 10%);
    }
    
    .pitta-card {
        border-left: 6px solid var(--pitta-color);
        background: linear-gradient(90deg, rgba(211, 47, 47, 0.05) 0%, var(--light-card-bg) 10%);
    }
    
    .kapha-card {
        border-left: 6px solid var(--kapha-color);
        background: linear-gradient(90deg, rgba(56, 142, 60, 0.05) 0%, var(--light-card-bg) 10%);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        background: rgba(239, 235, 233, 0.8);
        padding: 10px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #efebe9;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: #5d4037;
        padding: 0 20px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8d6e63 0%, #6d4c41 100%) !important;
        color: white !important;
        box-shadow: 0 4px 8px rgba(141, 110, 99, 0.3);
    }
    
    /* IMPROVED BUTTON STYLING */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary-gold) 0%, var(--primary-gold-dark) 100%) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        border: none !important;
        width: 100% !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 8px rgba(212, 175, 55, 0.3) !important;
        animation: pulse 2s infinite;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(212, 175, 55, 0.4) !important;
        background: linear-gradient(135deg, #E6C158 0%, #C19A20 100%) !important;
        animation: none;
    }
    
    /* Secondary Button */
    .stButton > button:not([kind="primary"]) {
        background: linear-gradient(135deg, var(--secondary-green) 0%, var(--secondary-green-dark) 100%) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        border: none !important;
        width: 100% !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 3px 6px rgba(56, 142, 60, 0.2) !important;
    }
    
    .stButton > button:not([kind="primary"]):hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 5px 10px rgba(56, 142, 60, 0.3) !important;
        background: linear-gradient(135deg, #43a047 0%, var(--secondary-green) 100%) !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #8d6e63, #d32f2f, #388e3c);
    }
    
    /* Custom Metrics */
    .metric-card {
        background: var(--light-metric-bg);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid var(--light-card-border);
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        animation: fadeIn 1s ease;
    }
    
    .dosha-pill {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 600;
        margin: 4px;
        font-size: 0.9rem;
    }
    
    .vata-pill { background-color: #efebe9; color: #5d4037; border: 1px solid #8d6e63; }
    .pitta-pill { background-color: #ffebee; color: #c62828; border: 1px solid #d32f2f; }
    .kapha-pill { background-color: #e8f5e9; color: #2e7d32; border: 1px solid #388e3c; }
    
    /* Date Input Styling */
    .stDateInput > div > div > input {
        font-family: 'Inter', sans-serif !important;
        color: var(--light-text) !important;
    }
    
    [data-testid="stDateInput"] svg {
        color: #8d6e63 !important;
    }
    
    /* Fact Boxes */
    .fact-box {
        background: linear-gradient(135deg, #fffaf0 0%, #fff5e6 100%);
        border: 1px solid #e0d6cc;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #8d6e63;
    }
    
    .nepali-date-box {
        background: linear-gradient(135deg, #f0f7ff 0%, #e6f0ff 100%);
        border: 1px solid #b8d4ff;
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
        text-align: center;
    }
    
    /* Daily Routine Styling */
    .routine-item {
        background: rgba(255, 255, 255, 0.9);
        border-left: 4px solid #8d6e63;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .routine-time {
        font-weight: 600;
        color: #5d4037;
        margin-bottom: 5px;
    }
    
    .routine-activity {
        color: var(--light-text);
        margin-bottom: 5px;
    }
    
    /* Download Button Special */
    .download-btn {
        background: linear-gradient(135deg, var(--primary-gold) 0%, var(--primary-gold-dark) 100%) !important;
        border: 2px solid #FFD700 !important;
    }
    
    /* Question Toggle Styling */
    .question-toggle-container {
        background: linear-gradient(135deg, #f5f1e8 0%, #efebe9 100%);
        border: 1px solid #d7ccc8;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        transition: all 0.3s ease;
        animation: fadeIn 1s ease;
    }
    
    .question-toggle-container:hover {
        background: linear-gradient(135deg, #efebe9 0%, #e8e4e1 100%);
        border-color: #8d6e63;
    }
    
    /* Footer Styling */
    .footer {
        text-align: center;
        padding: 20px 0;  /* Reduced from 30px to 20px */
        margin-top: 10px;  /* Reduced from 50px to 30px */
        border-top: 1px solid #d7ccc8;
        background: linear-gradient(135deg, rgba(245, 241, 232, 0.7) 0%, rgba(240, 230, 214, 0.7) 100%);
        font-family: 'Merriweather', serif;
        font-size: 0.85rem;  /* Reduced from 0.9rem */
        color: #795548;
        animation: fadeIn 2s ease;
    }
    
    .footer p {
    margin: 3px 0;  /* Reduced from 5px to 4px */
    font-family: 'Merriweather', serif;
    line-height: 1.4;  /* Added for better spacing */
}
    
    .footer a {
        color: #8d6e63;
        text-decoration: none;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    /* Image Container */
    .image-container {
        text-align: center;
        margin: 20px 0;
        animation: fadeIn 1.5s ease;
    }
    
    .ancient-symbol {
        font-size: 4rem;
        text-align: center;
        margin: 15px 0;
        animation: fadeIn 2s ease;
        color: #8d6e63;
    }
    
    /* Error Message Styling */
    .error-message {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border: 1px solid #f44336;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        color: #c62828;
        font-weight: 500;
        animation: shake 0.5s ease;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    /* Validation Styling */
    .validation-error {
        border-color: #f44336 !important;
        background: rgba(244, 67, 54, 0.05) !important;
    }
    
    /* Required field indicator */
    .required-field::after {
        content: " *";
        color: #f44336;
    }
    
    /* Custom slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #8d6e63, #d32f2f, #388e3c);
    }
    
    /* Question slider container */
    .question-slider-container {
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
        border: 1px solid #d7ccc8;
    }
    
    /* Results anchor for scrolling */
    .results-anchor {
        position: relative;
        top: -100px; /* Adjust based on your header height */
    }
    
    /* Dark Mode specific text color overrides */
    @media (prefers-color-scheme: dark) {
        /* Info boxes */
        div[data-testid="stAlert"] div[role="alert"] {
            color: var(--dark-text) !important;
        }
        
        /* Metric values */
        [data-testid="stMetricValue"] {
            color: var(--dark-text) !important;
            font-weight: bold !important;
            font-size: 1.8rem !important;
        }
        
        /* Metric labels */
        [data-testid="stMetricLabel"] {
            color: #ccc !important;
            font-weight: 600 !important;
        }
        
        /* Progress bar labels */
        .stProgress .st-emotion-cache-1e5tc9u {
            color: var(--dark-text) !important;
        }
        
        /* Divider */
        hr {
            border-color: #555 !important;
        }
        
        /* Success/Info/Warning/Error colors remain vibrant */
        .stAlert [data-testid="stMarkdownContainer"] {
            color: inherit !important;
        }
        
        /* Caption text */
        .stCaption {
            color: #ccc !important;
            font-weight: 500 !important;
        }
        
        /* Make sure expander content is readable */
        .streamlit-expanderContent {
            color: var(--dark-text) !important;
            background-color: var(--dark-card-bg) !important;
        }
        
        /* Ensure proper contrast in all alerts */
        .stAlert [data-baseweb="notification"] {
            color: inherit !important;
        }
        
        /* Dark mode for success/info/warning/error */
        /* Success */
        div[data-testid="stAlert"] div[role="alert"][style*="background-color: rgb(237, 247, 237)"] {
            background-color: rgba(46, 125, 50, 0.2) !important;
            border-color: #2e7d32 !important;
        }
        
        /* Info */
        div[data-testid="stAlert"] div[role="alert"][style*="background-color: rgb(229, 246, 253)"] {
            background-color: rgba(30, 136, 229, 0.2) !important;
            border-color: #1e88e5 !important;
        }
        
        /* Warning */
        div[data-testid="stAlert"] div[role="alert"][style*="background-color: rgb(255, 244, 229)"] {
            background-color: rgba(245, 124, 0, 0.2) !important;
            border-color: #f57c00 !important;
        }
        
        /* Error */
        div[data-testid="stAlert"] div[role="alert"][style*="background-color: rgb(253, 236, 234)"] {
            background-color: rgba(211, 47, 47, 0.2) !important;
            border-color: #d32f2f !important;
        }
        
        /* Expander headers - consistent styling */
        .streamlit-expanderHeader {
            color: #e0d6cc !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            background: linear-gradient(135deg, rgba(60, 60, 60, 0.9) 0%, rgba(70, 70, 70, 0.9) 100%) !important;
            border: 1px solid #555 !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            margin-bottom: 5px !important;
        }
        
        .streamlit-expanderHeader:hover {
            background: linear-gradient(135deg, rgba(70, 70, 70, 0.95) 0%, rgba(80, 80, 80, 0.95) 100%) !important;
            border-color: #8d6e63 !important;
        }
        
        .streamlit-expanderHeader:focus {
            outline: 2px solid #8d6e63 !important;
        }
        
        /* Expander icons */
        .streamlit-expanderHeader svg {
            color: #8d6e63 !important;
        }
        
        /* Progress bar track in dark mode */
        .stProgress > div > div {
            background-color: #555 !important;
        }
        
        /* Progress bar fill */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #8d6e63, #d32f2f, #388e3c) !important;
        }
    }
    
    /* Ensure all Streamlit text elements have proper contrast */
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: inherit !important;
    }
    
    /* Caption styling for dark mode */
    @media (prefers-color-scheme: dark) {
        .stCaption {
            color: #ccc !important;
        }
    }
    
    /* Make sure expander content is readable */
    .streamlit-expanderContent {
        color: inherit !important;
    }
    
    /* Ensure proper contrast in all alerts */
    .stAlert [data-baseweb="notification"] {
        color: inherit !important;
    }
    
    /* Welcome message styling */
    .welcome-message-container {
        text-align: center;
        padding: 40px;
        border-radius: 12px;
        margin: 20px 0;
        animation: fadeIn 2s ease;
        background: rgba(255, 255, 255, 0.8);
    }
    
    @media (prefers-color-scheme: dark) {
        .welcome-message-container {
            background: rgba(40, 40, 40, 0.9) !important;
        }
        
        .welcome-message-container h3 {
            color: #e0d6cc !important;
        }
        
        .welcome-message-container p {
            color: #f0f0f0 !important;
        }
        
        .welcome-message-container .dosha-label {
            color: #ccc !important;
        }
        
        .welcome-message-container .quote {
            color: #d7a46e !important;
            font-style: italic;
        }
        
        .welcome-message-container .symbol {
            color: #8d6e63 !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# =============================
# SIMPLIFIED DATE INPUT FOR DD/MM/YYYY
# =============================
def simplified_date_input(label, value=None):
    """Create a simplified date input that accepts DD/MM/YYYY format"""
    st.markdown(f"<span class='required-field'>{label}</span>", unsafe_allow_html=True)
    
    # Create three columns for day, month, year
    col1, col2, col3 = st.columns(3)
    
    with col1:
        day = st.number_input("Day", min_value=1, max_value=31, value=1, key=f"{label}_day", label_visibility="collapsed")
    
    with col2:
        month = st.selectbox("Month", 
                           ["01 - January", "02 - February", "03 - March", "04 - April", 
                            "05 - May", "06 - June", "07 - July", "08 - August", 
                            "09 - September", "10 - October", "11 - November", "12 - December"],
                           key=f"{label}_month", label_visibility="collapsed")
    
    with col3:
        current_year = date.today().year
        year = st.number_input("Year", 
                              min_value=current_year-100, 
                              max_value=current_year, 
                              value=1990,
                              key=f"{label}_year", label_visibility="collapsed")
    
    # Extract month number from selection
    month_num = int(month.split(" - ")[0])
    
    # Validate the date
    try:
        # Check for February and leap year
        if month_num == 2:
            if day > 29:
                day = 29
            elif day == 29 and not (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
                day = 28
        
        selected_date = date(year, month_num, day)
        return selected_date, f"{day:02d}/{month_num:02d}/{year}"
    except ValueError:
        # Fallback to first day of month if invalid
        return date(year, month_num, 1), f"01/{month_num:02d}/{year}"

# =============================
# DATE FORMATTING FUNCTION
# =============================
def format_date_ddmmyyyy(date_obj):
    """Format date as DD/MM/YYYY"""
    return date_obj.strftime("%d/%m/%Y")

# =============================
# ACCURATE NEPALI DATE CONVERSION SYSTEM
# =============================
class NepaliDateConverter:
    """Accurate English to Nepali date conversion (Bikram Sambat)"""
    
    # Nepali calendar data (month days for each year 1970-2090 BS)
    NEPALI_CALENDAR = {
        1970: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 1971: [31, 31, 32, 31, 32, 30, 30, 29, 30, 29, 30, 30],
        1972: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31], 1973: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        1974: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 1975: [31, 31, 32, 32, 30, 31, 30, 29, 30, 29, 30, 30],
        1976: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31], 1977: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        1978: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 1979: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        1980: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31], 1981: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
        1982: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 1983: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        1984: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31], 1985: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
        1986: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 1987: [31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        1988: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31], 1989: [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
        1990: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 1991: [31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        1992: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31], 1993: [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
        1994: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 1995: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
        1996: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31], 1997: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        1998: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 1999: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        2000: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31], 2001: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        2002: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2003: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        2004: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31], 2005: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        2006: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2007: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        2008: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31], 2009: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        2010: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2011: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        2012: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30], 2013: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        2014: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2015: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        2016: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30], 2017: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        2018: [31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2019: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        2020: [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30], 2021: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        2022: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30], 2023: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        2024: [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30], 2025: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        2026: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31], 2027: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        2028: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 2029: [31, 31, 32, 31, 32, 30, 30, 29, 30, 29, 30, 30],
        2030: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31], 2031: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        2032: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 2033: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        2034: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31], 2035: [30, 32, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31],
        2036: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 2037: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        2038: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31], 2039: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
        2040: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 2041: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        2042: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31], 2043: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30],
        2044: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 2045: [31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        2046: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31], 2047: [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
        2048: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 2049: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
        2050: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31], 2051: [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30],
        2052: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 2053: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
        2054: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31], 2055: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        2056: [31, 31, 32, 31, 32, 30, 30, 29, 30, 29, 30, 30], 2057: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        2058: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31], 2059: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        2060: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2061: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        2062: [30, 32, 31, 32, 31, 31, 29, 30, 29, 30, 29, 31], 2063: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        2064: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2065: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        2066: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 29, 31], 2067: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        2068: [31, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2069: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        2070: [31, 31, 31, 32, 31, 31, 29, 30, 30, 29, 30, 30], 2071: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        2072: [31, 32, 31, 32, 31, 30, 30, 29, 30, 29, 30, 30], 2073: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
        2074: [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30], 2075: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        2076: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30], 2077: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        2078: [31, 31, 31, 32, 31, 31, 30, 29, 30, 29, 30, 30], 2079: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30],
        2080: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30], 2081: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        2082: [31, 31, 32, 31, 31, 31, 30, 29, 30, 29, 30, 30], 2083: [31, 31, 32, 31, 31, 30, 30, 30, 29, 30, 30, 30],
        2084: [31, 31, 32, 31, 31, 30, 30, 30, 29, 30, 30, 30], 2085: [31, 32, 31, 32, 30, 31, 30, 30, 29, 30, 30, 30],
        2086: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30], 2087: [31, 31, 32, 31, 31, 31, 30, 30, 29, 30, 30, 30],
        2088: [30, 31, 32, 32, 30, 31, 30, 30, 29, 30, 30, 30], 2089: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30],
        2090: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30],
    }
    
    # Nepali month names (with Nepali script)
    NEPALI_MONTHS = [
        "बैशाख", "जेठ", "असार", "श्रावण", "भदौ", "असोज",
        "कार्तिक", "मंसिर", "पुष", "माघ", "फाल्गुन", "चैत्र"
    ]
    
    @staticmethod
    def english_to_nepali(english_date):
        """Convert English date to accurate Nepali date"""
        try:
            # Fixed Anchor: 14th April 1999 (English) = 1st Baisakh 2056 (Nepali)
            anchor_en = date(1999, 4, 14)
            bs_y, bs_m, bs_d = 2056, 1, 1
            
            # Calculate days difference
            delta_days = (english_date - anchor_en).days
            direction = 1 if delta_days >= 0 else -1
            delta_days = abs(delta_days)
            
            # Convert days to Nepali date
            while delta_days > 0:
                year_months = NepaliDateConverter.NEPALI_CALENDAR.get(bs_y)
                if not year_months:
                    # If year not in data, use average month length
                    year_months = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
                
                if direction == 1:  # Forward in time
                    month_days = year_months[bs_m - 1]
                    days_left_in_month = month_days - bs_d + 1
                    
                    if delta_days < days_left_in_month:
                        bs_d += delta_days
                        delta_days = 0
                    else:
                        delta_days -= days_left_in_month
                        bs_d = 1
                        bs_m += 1
                        
                        if bs_m > 12:
                            bs_m = 1
                            bs_y += 1
                else:  # Backward in time
                    if delta_days < bs_d:
                        bs_d -= delta_days
                        delta_days = 0
                    else:
                        delta_days -= bs_d
                        bs_m -= 1
                        
                        if bs_m < 1:
                            bs_m = 12
                            bs_y -= 1
                            
                        year_months = NepaliDateConverter.NEPALI_CALENDAR.get(bs_y)
                        if not year_months:
                            year_months = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
                        
                        bs_d = year_months[bs_m - 1]
            
            # Format the result
            month_name = NepaliDateConverter.NEPALI_MONTHS[bs_m - 1]
            
            # Convert to Nepali numerals if needed
            def to_nepali_num(num):
                nepali_numerals = {
                    '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
                    '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
                }
                return ''.join(nepali_numerals.get(digit, digit) for digit in str(num))
            
            nepali_day = to_nepali_num(bs_d)
            nepali_year = to_nepali_num(bs_y)
            
            return {
                'year': bs_y,
                'month': month_name,
                'day': bs_d,
                'formatted': f"{nepali_year} {month_name} {nepali_day} गते",
                'formatted_english': f"{bs_d} {month_name} {bs_y}"
            }
            
        except Exception as e:
            # Fallback in case of error
            return {
                'year': 2080,
                'month': "मंसिर",
                'day': 22,
                'formatted': "२०८० मंसिर २२ गते",
                'formatted_english': "22 मंसिर 2080"
            }

# =============================
# ENHANCED KNOWLEDGE BASE WITH ALL FEATURES
# =============================
DOSHA_ARCHETYPES = {
    "Vata": {
        "title": "The Wind-Walker (Vayu)",
        "element": "Air + Ether",
        "qualities": "Light, Cold, Dry, Mobile, Subtle, Clear",
        "season": "Autumn to Early Winter",
        "time_of_day": "2-6 AM & PM (Vata Time)",
        "life_stage": "Old Age",
        "symbol": "🌀",
        "story": """
        You are the Wind-Walker, blessed with the essence of movement and creativity. 
        Like the autumn leaves carried by the breeze, your mind dances with ideas and inspiration. 
        Ancient sages called you 'Vayu-putra' - child of the wind, destined to bring change and innovation.
        Your journey is one of exploration and spiritual awakening, moving through life with the grace of a gentle breeze.
        """,
        "ancient_quote": "As the wind moves freely, so does the Vata soul. Embrace change, for it is your nature.",
        "sanskrit_name": "वात प्रकृति",
        "governing_planet": "Saturn & Mercury",
        
        # DAILY CARE SECTION
        "oil_massage": {
            "recommended_oil": "Sesame oil (warm) or almond oil. Add a few drops of lavender or sandalwood essential oil for grounding.",
            "technique": "Massage from extremities toward the heart using long, slow strokes. Pay special attention to joints and feet.",
            "duration": "10-15 minutes before warm bath",
            "benefits": "Calms nervous system, lubricates dry skin, improves circulation"
        },
        
        "pranayama": {
            "recommended_practices": "Nadi Shodhana (Alternate Nostril Breathing), Ujjayi (Victorious Breath), Bhramari (Bee Breath)",
            "best_time": "Early morning (5-7 AM) or evening (6-7 PM)",
            "duration": "10-15 minutes daily",
            "instructions": "Practice in a warm, comfortable space. Focus on slow, rhythmic breathing."
        },
        
        # BODY TYPE DESCRIPTION
        "body_description": {
            "frame": "Thin, bony, irregular frame with prominent joints and veins",
            "height": "Usually tall or very short, rarely average",
            "weight": "Difficulty gaining weight, tends to stay thin",
            "skin": "Dry, thin, cool to touch, tends to crack in winter",
            "hair": "Thin, dry, brittle, frizzy, prone to split ends",
            "eyes": "Small, sunken, darting, dry, often blink frequently",
            "nails": "Brittle, dry, ridges, break easily",
            "teeth": "Irregular, spaced, prone to sensitivity",
            "posture": "Often slouching or restless movement"
        },
        
        # PERSONALITY SECTION
        "personality": {
            "nature": "Creative, enthusiastic, quick-witted, adaptable, visionary",
            "communication": "Talks fast, changes topics frequently, expressive with hands",
            "learning": "Quick learner but quick forgetter, needs variety",
            "social": "Makes friends easily but relationships may be short-lived",
            "strengths": ["Creative", "Adaptable", "Quick-thinking", "Spiritual"],
            "weaknesses": ["Anxious", "Forgetful", "Inconsistent", "Prone to worry"]
        },
        
        # HOROSCOPE SECTION
        "horoscope": {
            "lucky_day": "Saturday",
            "lucky_color": "Golden Yellow / Royal Blue",
            "lucky_direction": "North-West",
            "lucky_numbers": [5, 14, 23, 32],
            "mantra": "Om Shanti Shanti Shanti",
            "prediction": "Your fate is tied to travel and communication. Wealth enters in rapid waves. Embrace change as your constant companion.",
            "career": ["Creative Director", "Pilot", "Journalist", "Spiritual Guide"],
            "love": "You need a partner who provides stability and routine",
            "health": "Prone to nervous disorders, joint pain, and insomnia"
        },
        
        "interesting_facts": [
            "Vatas have the most vivid dreams but often forget them",
            "They can learn a new language in months but forget it just as fast",
            "Ancient yogis observed Vatas are most creative between 2-6 AM",
            "Vata-dominant people are natural storytellers and entertainers",
            "They have sensitive nervous systems and feel emotions deeply"
        ],
        
        "marriage_compatibility": {
            "best_with": "Kapha (earth stabilizes wind)",
            "challenging_with": "Pitta (fire can overheat wind)",
            "advice": "Needs routine and stability from partner",
            "traits": "Romantic but inconsistent, needs space and freedom",
            "ideal_partner": "Someone calm, grounded, and patient"
        },
        
        "financial_tendencies": [
            "Impulsive spender - buys on emotion",
            "Money comes and goes quickly",
            "Great at starting businesses, needs help maintaining them",
            "Should avoid get-rich-quick schemes",
            "Best financial advice: Automatic savings"
        ],
        
        "yogi_observations": [
            "Vatas reach enlightenment fastest but also fall fastest",
            "They should practice grounding meditation daily",
            "Their spiritual gift is detachment (Vairagya)",
            "Most prone to spiritual experiences but also to confusion",
            "Ancient texts call them 'children of the gods'"
        ]
    },
    "Pitta": {
        "title": "The Fire-Keeper (Agni)",
        "element": "Fire + Water",
        "qualities": "Hot, Sharp, Light, Liquid, Oily, Spreading",
        "season": "Summer",
        "time_of_day": "10 AM-2 PM & 10 PM-2 AM (Pitta Time)",
        "life_stage": "Adulthood",
        "symbol": "🔥",
        "story": """
        You are the Fire-Keeper, guardian of transformation and wisdom. 
        Like the sacred fire of a yajna ceremony, you illuminate truth and burn away illusion. 
        Ancient warriors sought your counsel, for you carry the spark of Agni within - the divine fire of digestion and discernment.
        Your path is one of mastery and leadership, turning obstacles into opportunities through sheer will.
        """,
        "ancient_quote": "As fire transforms all it touches, so does Pitta transform challenges into victories.",
        "sanskrit_name": "पित्त प्रकृति",
        "governing_planet": "Sun & Mars",
        
        # DAILY CARE SECTION
        "oil_massage": {
            "recommended_oil": "Coconut oil (cool) or sunflower oil. Add a few drops of rose or jasmine essential oil for cooling.",
            "technique": "Gentle, circular motions. Avoid excessive rubbing which can generate heat.",
            "duration": "5-10 minutes before cool shower",
            "benefits": "Cools inflammation, soothes sensitive skin, reduces excess heat"
        },
        
        "pranayama": {
            "recommended_practices": "Sheetali (Cooling Breath), Sheetkari (Hissing Breath), Chandra Bhedana (Left Nostril Breathing)",
            "best_time": "Early morning (5-7 AM) or late evening (9-10 PM)",
            "duration": "10-15 minutes daily",
            "instructions": "Practice in a cool, well-ventilated space. Focus on cooling breaths."
        },
        
        # BODY TYPE DESCRIPTION
        "body_description": {
            "frame": "Medium, symmetrical, athletic build with good muscle tone",
            "height": "Average to tall, well-proportioned",
            "weight": "Maintains weight easily, gains and loses with effort",
            "skin": "Warm, reddish, sensitive, prone to rashes and moles",
            "hair": "Fine, straight or wavy, tends to grey early, may thin",
            "eyes": "Sharp, penetrating, light-colored (green/hazel), sensitive to light",
            "nails": "Strong, pink, flexible, well-formed",
            "teeth": "Medium, symmetrical, prone to sensitivity to hot/cold",
            "posture": "Upright, confident, commanding presence"
        },
        
        # PERSONALITY SECTION
        "personality": {
            "nature": "Ambitious, focused, intelligent, natural leader, perfectionist",
            "communication": "Direct, precise, can be sharp when angry",
            "learning": "Analytical, competitive, excellent memory for details",
            "social": "Selective with friends, values loyalty and competence",
            "strengths": ["Focused", "Brave", "Intelligent", "Natural leader"],
            "weaknesses": ["Angry", "Critical", "Impatient", "Perfectionist"]
        },
        
        # HOROSCOPE SECTION
        "horoscope": {
            "lucky_day": "Tuesday",
            "lucky_color": "Soft White / Sky Blue",
            "lucky_direction": "South",
            "lucky_numbers": [1, 10, 19, 28],
            "mantra": "Om Sharavana Bhavaya Namaha",
            "prediction": "Your fate is governed by Mars. You are destined for authority and recognition. Leadership comes naturally.",
            "career": ["CEO", "Surgeon", "Lawyer", "Engineer"],
            "love": "You need a partner who provides cooling balance and patience",
            "health": "Prone to inflammation, acidity, and skin disorders"
        },
        
        "interesting_facts": [
            "Pittas have the strongest digestive fire (Agni)",
            "They're natural born leaders but can be controlling",
            "Ancient texts say Pittas make the best surgeons and warriors",
            "Their body temperature is naturally higher than others",
            "Pittas are most productive during midday (10AM-2PM)"
        ],
        
        "marriage_compatibility": {
            "best_with": "Vata (wind fans the fire gently)",
            "challenging_with": "Pitta (fire with fire creates conflict)",
            "advice": "Needs cooling and patience in relationships",
            "traits": "Protective partner but can be jealous",
            "ideal_partner": "Someone calming, patient, and non-competitive"
        },
        
        "financial_tendencies": [
            "Strategic spender - plans purchases carefully",
            "Values quality over quantity",
            "Excellent at managing businesses and investments",
            "Tends to be wealthy but spends on luxury",
            "Ancient advice: Donate 10% to cool financial fire"
        ],
        
        "yogi_observations": [
            "Pittas achieve mastery in yoga but struggle with surrender",
            "Their spiritual challenge is releasing control",
            "Natural capacity for concentration (Dharana)",
            "Should practice moon-gazing meditation",
            "Ancient texts call them 'warriors of light'"
        ]
    },
    "Kapha": {
        "title": "The Earth-Anchor (Prithvi)",
        "element": "Earth + Water",
        "qualities": "Heavy, Cold, Dull, Oily, Smooth, Dense, Soft, Stable",
        "season": "Spring",
        "time_of_day": "6-10 AM & PM (Kapha Time)",
        "life_stage": "Childhood",
        "symbol": "🌊",
        "story": """
        You are the Earth-Anchor, foundation of stability and compassion. 
        Like the mighty Himalayas standing firm through ages, you provide shelter and nourishment to all. 
        Ancient healers revered your nature, for you embody the union of earth and water - the essence of creation itself.
        Your journey is one of nurturing growth and building lasting legacies.
        """,
        "ancient_quote": "As the earth supports all life, so does Kapha support all beings with unwavering strength.",
        "sanskrit_name": "कफ प्रकृति",
        "governing_planet": "Moon & Venus",
        
        # DAILY CARE SECTION
        "oil_massage": {
            "recommended_oil": "Mustard oil (warm) or corn oil. Add a few drops of eucalyptus or cinnamon essential oil for stimulation.",
            "technique": "Vigorous, dry brushing followed by light oil massage. Use upward strokes toward the heart.",
            "duration": "5-10 minutes before warm shower",
            "benefits": "Stimulates circulation, reduces congestion, energizes the body"
        },
        
        "pranayama": {
            "recommended_practices": "Kapalabhati (Skull Shining Breath), Bhastrika (Bellows Breath), Surya Bhedana (Right Nostril Breathing)",
            "best_time": "Early morning (5-7 AM) on empty stomach",
            "duration": "10-15 minutes daily",
            "instructions": "Practice in a well-ventilated space. Focus on vigorous, energizing breaths."
        },
        
        # BODY TYPE DESCRIPTION
        "body_description": {
            "frame": "Large, broad, solid frame with tendency to gain weight",
            "height": "Short to medium, sturdy build",
            "weight": "Gains weight easily, difficult to lose",
            "skin": "Thick, smooth, oily, cool, pale, few wrinkles",
            "hair": "Thick, wavy/curly, oily, lustrous, strong",
            "eyes": "Large, doe-like, thick lashes, calm compassionate gaze",
            "nails": "Strong, thick, smooth, grow slowly",
            "teeth": "Large, well-spaced, strong enamel",
            "posture": "Solid, grounded, moves slowly but surely"
        },
        
        # PERSONALITY SECTION
        "personality": {
            "nature": "Calm, patient, loyal, nurturing, methodical, stable",
            "communication": "Slow, thoughtful, melodious voice, good listener",
            "learning": "Slow but steady, excellent long-term memory",
            "social": "Few but lifelong friends, family-oriented",
            "strengths": ["Calm", "Loyal", "Strong immunity", "Steady"],
            "weaknesses": ["Lethargic", "Possessive", "Resistant to change", "Slow metabolism"]
        },
        
        # HOROSCOPE SECTION
        "horoscope": {
            "lucky_day": "Monday",
            "lucky_color": "Royal Blue / Sea Green",
            "lucky_direction": "North",
            "lucky_numbers": [2, 11, 20, 29],
            "mantra": "Om Namah Shivaya",
            "prediction": "Your fate is stable and protected. Wealth accumulates through land and loyalty. Patience is your greatest virtue.",
            "career": ["Teacher", "Real Estate Mogul", "Chef", "HR Director"],
            "love": "You need a partner who provides stimulation and adventure",
            "health": "Prone to congestion, weight gain, and respiratory issues"
        },
        
        "interesting_facts": [
            "Kaphas have the strongest immune systems",
            "They can fast the longest without discomfort",
            "Ancient yogis said Kaphas have the sweetest sleep",
            "They're naturally strong and have great endurance",
            "Kaphas are most stable during morning (6-10AM)"
        ],
        
        "marriage_compatibility": {
            "best_with": "Pitta (fire warms earth)",
            "challenging_with": "Kapha (too much stability becomes stagnant)",
            "advice": "Needs stimulation and novelty in relationships",
            "traits": "Devoted, reliable partner but can be possessive",
            "ideal_partner": "Someone energetic, adventurous, and motivating"
        },
        
        "financial_tendencies": [
            "Conservative spender - saves for security",
            "Money accumulates slowly but steadily",
            "Excellent at long-term investments and real estate",
            "May miss opportunities due to caution",
            "Ancient advice: Take calculated risks for growth"
        ],
        
        "yogi_observations": [
            "Kaphas have natural devotion (Bhakti) but struggle with effort",
            "Their spiritual challenge is overcoming inertia",
            "Should practice vigorous morning yoga",
            "Natural capacity for meditation but falls asleep easily",
            "Ancient texts call them 'pillars of dharma'"
        ]
    }
}

# =============================
# 10 QUESTION ASSESSMENT
# =============================
AYURVEDIC_QUESTIONS = [
    ("1. What is your natural body frame?", 
     ["A) Thin, bony, irregular with prominent joints",
      "B) Medium, symmetrical, athletic build", 
      "C) Large, broad, solid frame"]),
    
    ("2. How would you describe your weight pattern?",
     ["A) Difficulty gaining weight, tends to stay thin",
      "B) Maintains weight easily, gains and loses with effort", 
      "C) Gains weight easily, difficult to lose"]),
    
    ("3. What is your skin texture like?",
     ["A) Dry, thin, cool to touch", 
      "B) Warm, reddish, sensitive", 
      "C) Thick, smooth, oily, cool"]),
    
    ("4. What is your typical energy pattern?",
     ["A) Bursts of energy followed by fatigue",
      "B) Consistent, focused energy", 
      "C) Steady, enduring energy"]),
    
    ("5. How is your appetite and digestion?",
     ["A) Irregular appetite, prone to bloating",
      "B) Strong appetite, quick digestion", 
      "C) Steady appetite, slow digestion"]),
    
    ("6. What is your sleep pattern like?",
     ["A) Light, restless, difficulty falling asleep",
      "B) Sound sleep, vivid dreams", 
      "C) Deep, heavy sleep, difficult to wake"]),
    
    ("7. How is your mind typically?",
     ["A) Creative, restless, full of ideas", 
      "B) Focused, ambitious, analytical", 
      "C) Calm, steady, patient"]),
    
    ("8. How do you handle stress?",
     ["A) Anxiety, worry, nervous energy",
      "B) Anger, frustration, need to solve immediately", 
      "C) Avoidance, lethargy, emotional eating"]),
    
    ("9. What climate suits you best?",
     ["A) Warm, humid, calm weather", 
      "B) Cool, dry, well-ventilated", 
      "C) Warm, dry, stimulating"]),
    
    ("10. What is your learning style?",
     ["A) Quick to grasp, quick to forget", 
      "B) Sharp, analytical, competitive", 
      "C) Slow, steady, excellent long-term memory"])
]

# =============================
# STREAMLIT COMPONENTS
# =============================
def display_daily_routine_visual(routine_data, dosha_type):
    """Display daily routine in a beautiful format with specific oil massage and pranayama"""
    st.markdown("### 🌅 Your Sacred Daily Rhythm")
    
    # Get dosha-specific recommendations
    dosha_data = DOSHA_ARCHETYPES[dosha_type]
    oil_info = dosha_data.get('oil_massage', {})
    pranayama_info = dosha_data.get('pranayama', {})
    
    routines = [
        {"time": "5-6 AM", "activity": "Wake with first light (Brahma Muhurta)"},
        {"time": "6-7 AM", "activity": f"Oil massage (Abhyanga) with {oil_info.get('recommended_oil', 'warm sesame oil')}"},
        {"time": "7-8 AM", "activity": f"30 minutes of {pranayama_info.get('recommended_practices', 'Nadi Shodhana')} and gentle yoga"},
        {"time": "8 AM", "activity": "Warm, cooked breakfast with appropriate spices"},
        {"time": "10 AM-2 PM", "activity": "Creative/productive work hours"},
        {"time": "12-1 PM", "activity": "Main meal of the day (largest meal)"},
        {"time": "4-6 PM", "activity": "Gentle walk or light exercise"},
        {"time": "6 PM", "activity": "Light, warm dinner"},
        {"time": "8-9 PM", "activity": "Wind down, gentle reading or meditation"},
        {"time": "9-10 PM", "activity": "Bedtime with warm milk and calming spices"}
    ]
    
    for routine in routines:
        color = "#8d6e63" if dosha_type == "Vata" else "#d32f2f" if dosha_type == "Pitta" else "#388e3c"
        st.markdown(f"""
        <div style="border-left: 4px solid {color}; padding-left: 15px; margin: 10px 0; background: rgba(255,255,255,0.9); padding: 15px; border-radius: 8px; animation: slideInUp 0.5s ease;">
            <div style="font-weight: 600; color: #5d4037; font-size: 1.1rem;">{routine['time']}</div>
            <div style="color: #2d2d2d; margin-top: 5px;">{routine['activity']}</div>
        </div>
        """, unsafe_allow_html=True)

def create_dosha_chart_streamlit(scores):
    """Create a simple dosha chart with improved dark mode visibility"""
    st.markdown("### 📊 Your Dosha Balance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        vata_percent = scores['Vata']
        # Custom HTML for Vata metric with dark mode support
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; border-radius: 10px; border-left: 4px solid #8d6e63; 
                    background: rgba(142, 110, 99, 0.1); margin-bottom: 10px;">
            <div style="font-size: 1rem; color: #5d4037; font-weight: 600; margin-bottom: 5px;">VATA</div>
            <div style="font-size: 2.5rem; color: #8d6e63; font-weight: 700; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">
                {vata_percent:.0f}%
            </div>
            <div style="font-size: 0.9rem; color: #795548; margin-top: 5px;">Light, Cold, Dry, Mobile</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar
        st.progress(vata_percent/100)
    
    with col2:
        pitta_percent = scores['Pitta']
        # Custom HTML for Pitta metric with dark mode support
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; border-radius: 10px; border-left: 4px solid #d32f2f; 
                    background: rgba(211, 47, 47, 0.1); margin-bottom: 10px;">
            <div style="font-size: 1rem; color: #c62828; font-weight: 600; margin-bottom: 5px;">PITTA</div>
            <div style="font-size: 2.5rem; color: #d32f2f; font-weight: 700; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">
                {pitta_percent:.0f}%
            </div>
            <div style="font-size: 0.9rem; color: #795548; margin-top: 5px;">Hot, Sharp, Light, Liquid</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar
        st.progress(pitta_percent/100)
    
    with col3:
        kapha_percent = scores['Kapha']
        # Custom HTML for Kapha metric with dark mode support
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; border-radius: 10px; border-left: 4px solid #388e3c; 
                    background: rgba(56, 142, 60, 0.1); margin-bottom: 10px;">
            <div style="font-size: 1rem; color: #2e7d32; font-weight: 600; margin-bottom: 5px;">KAPHA</div>
            <div style="font-size: 2.5rem; color: #388e3c; font-weight: 700; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">
                {kapha_percent:.0f}%
            </div>
            <div style="font-size: 0.9rem; color: #795548; margin-top: 5px;">Heavy, Cold, Oily, Stable</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar
        st.progress(kapha_percent/100)
    
    # Add dark mode CSS overrides
    st.markdown("""
    <style>
    @media (prefers-color-scheme: dark) {
        /* Vata metric dark mode */
        div[style*="border-left: 4px solid #8d6e63"] {
            background: rgba(142, 110, 99, 0.15) !important;
        }
        div[style*="border-left: 4px solid #8d6e63"] div:nth-child(1) {
            color: #e0d6cc !important;
        }
        div[style*="border-left: 4px solid #8d6e63"] div:nth-child(2) {
            color: #d7ccc8 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
        }
        div[style*="border-left: 4px solid #8d6e63"] div:nth-child(3) {
            color: #bcaaa4 !important;
        }
        
        /* Pitta metric dark mode */
        div[style*="border-left: 4px solid #d32f2f"] {
            background: rgba(211, 47, 47, 0.15) !important;
        }
        div[style*="border-left: 4px solid #d32f2f"] div:nth-child(1) {
            color: #ffcdd2 !important;
        }
        div[style*="border-left: 4px solid #d32f2f"] div:nth-child(2) {
            color: #ff8a80 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
        }
        div[style*="border-left: 4px solid #d32f2f"] div:nth-child(3) {
            color: #ffab91 !important;
        }
        
        /* Kapha metric dark mode */
        div[style*="border-left: 4px solid #388e3c"] {
            background: rgba(56, 142, 60, 0.15) !important;
        }
        div[style*="border-left: 4px solid #388e3c"] div:nth-child(1) {
            color: #c8e6c9 !important;
        }
        div[style*="border-left: 4px solid #388e3c"] div:nth-child(2) {
            color: #a5d6a7 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
        }
        div[style*="border-left: 4px solid #388e3c"] div:nth-child(3) {
            color: #c5e1a5 !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def display_body_description(dosha_data):
    """Display detailed body type description"""
    with st.expander("👁️ **Physical Characteristics**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Frame & Build:**")
            st.info(dosha_data["body_description"]["frame"])
            
            st.markdown("**Height & Weight:**")
            st.info(f"{dosha_data['body_description']['height']}. {dosha_data['body_description']['weight']}")
            
            st.markdown("**Skin:**")
            st.info(dosha_data["body_description"]["skin"])
            
            st.markdown("**Hair:**")
            st.info(dosha_data["body_description"]["hair"])
        
        with col2:
            st.markdown("**Eyes:**")
            st.info(dosha_data["body_description"]["eyes"])
            
            st.markdown("**Nails:**")
            st.info(dosha_data["body_description"]["nails"])
            
            st.markdown("**Teeth:**")
            st.info(dosha_data["body_description"]["teeth"])
            
            st.markdown("**Posture:**")
            st.info(dosha_data["body_description"]["posture"])

def display_horoscope(dosha_data):
    """Display horoscope section"""
    with st.expander("🌟 **Vedic Horoscope**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Lucky Elements:**")
            st.success(f"**Day:** {dosha_data['horoscope']['lucky_day']}")
            st.success(f"**Color:** {dosha_data['horoscope']['lucky_color']}")
            st.success(f"**Direction:** {dosha_data['horoscope']['lucky_direction']}")
            st.success(f"**Numbers:** {', '.join(map(str, dosha_data['horoscope']['lucky_numbers']))}")
            
            st.markdown("**Career Paths:**")
            for career in dosha_data['horoscope']['career']:
                st.markdown(f"• {career}")
        
        with col2:
            st.markdown("**Life Prediction:**")
            st.info(dosha_data['horoscope']['prediction'])
            
            st.markdown("**Love & Relationships:**")
            st.warning(dosha_data['horoscope']['love'])
            
            st.markdown("**Health Watch:**")
            st.error(dosha_data['horoscope']['health'])
            
            st.markdown("**Sacred Mantra:**")
            st.markdown(f"*{dosha_data['horoscope']['mantra']}*")

def display_personality_section(dosha_data):
    """Display personality, facts, and marriage sections"""
    
    # Personality Traits
    with st.expander("🧠 **Personality & Nature**", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Core Nature:**")
            st.info(dosha_data["personality"]["nature"])
            
            st.markdown("**Communication Style:**")
            st.info(dosha_data["personality"]["communication"])
            
            st.markdown("**Strengths:**")
            for strength in dosha_data["personality"]["strengths"]:
                st.success(f"• {strength}")
            
        with col2:
            st.markdown("**Learning Style:**")
            st.info(dosha_data["personality"]["learning"])
            
            st.markdown("**Social Tendencies:**")
            st.info(dosha_data["personality"]["social"])
            
            st.markdown("**Weaknesses:**")
            for weakness in dosha_data["personality"]["weaknesses"]:
                st.error(f"• {weakness}")
    
    # Interesting Facts
    with st.expander("🌟 **5 Interesting Facts**", expanded=False):
        for i, fact in enumerate(dosha_data["interesting_facts"], 1):
            st.markdown(f"**{i}.** {fact}")
    
    # Marriage & Relationships
    with st.expander("💑 **Marriage & Compatibility**", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"**Best Match:** {dosha_data['marriage_compatibility']['best_with']}")
            st.warning(f"**Challenging Match:** {dosha_data['marriage_compatibility']['challenging_with']}")
            st.info(f"**Ideal Partner:** {dosha_data['marriage_compatibility']['ideal_partner']}")
            
        with col2:
            st.info(f"**Relationship Advice:** {dosha_data['marriage_compatibility']['advice']}")
            st.markdown(f"**Partner Traits:** {dosha_data['marriage_compatibility']['traits']}")
    
    # Financial Tendencies
    with st.expander("💰 **Financial Patterns**", expanded=False):
        for tendency in dosha_data["financial_tendencies"]:
            st.markdown(f"• {tendency}")
    
    # Yogi Observations
    with st.expander("🕉️ **Ancient Yogi Observations**", expanded=False):
        for observation in dosha_data["yogi_observations"]:
            st.markdown(f"• {observation}")

# =============================
# QUESTION TOGGLE COMPONENT
# =============================
def display_questions_with_toggle():
    """Display questions with horizontal minimize option"""
    
    # Initialize session state for toggle
    if 'questions_visible' not in st.session_state:
        st.session_state.questions_visible = True
    
    # Horizontal toggle layout
    st.markdown('<div class="question-toggle-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.questions_visible:
            if st.button("🔽 Hide Assessment Questions", use_container_width=True):
                st.session_state.questions_visible = False
                st.rerun()
        else:
            if st.button("▶️ Show Assessment Questions", use_container_width=True):
                st.session_state.questions_visible = True
                st.rerun()
    
    responses = []
    
    if st.session_state.questions_visible:
        st.markdown("### 📝 The Great Assessment of Self")
        st.info("Answer these 10 questions based on your lifelong natural tendencies. Be honest, not ideal.")
        
        for i, (q_text, options) in enumerate(AYURVEDIC_QUESTIONS):
            response = st.radio(
                q_text,
                options,
                key=f"q_{i}",
                index=None
            )
            if response:
                responses.append(response[0])
            st.markdown("---")
    
    st.markdown('</div>', unsafe_allow_html=True)
    return responses

# =============================
# FOOTER COMPONENT
# =============================
def display_footer():
    """Display compact footer with ancient wisdom"""
    st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <div style="font-size: 2rem; color: #8d6e63; opacity: 0.8; margin-bottom: 5px;">ॐ</div>
            <div class="footer-row">
                <span><strong>VAIDYA: PRAKRITI MASTERY</strong></span>
                <span>•</span>
                <span>Ancient Wisdom for Modern Living</span>
            </div>
            <div class="footer-row">
                <span>"सर्वे भवन्तु सुखिनः"</span>
                <span>•</span>
                <span>May all be happy</span>
            </div>
            <div class="footer-row" style="font-size: 0.7rem; color: #8d6e63; margin-top: 8px;">
                <span>© 2026</span>
                <span>•</span>
                <span>5,000 years of Ayurvedic Tradition (Yogendra Timilsina)</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =============================
# VALIDATION FUNCTIONS
# =============================
def validate_required_fields(name, birth_date_obj, formatted_date):
    """Validate required fields and return error messages"""
    errors = []
    
    if not name or name.strip() == "":
        errors.append("Name is required")
    
    if not birth_date_obj:
        errors.append("Date of birth is required")
    else:
        # Additional date validation
        if birth_date_obj > date.today():
            errors.append("Date of birth cannot be in the future")
        if birth_date_obj.year < date.today().year - 100:
            errors.append("Please enter a valid date (within last 100 years)")
    
    return errors

# =============================
# MAIN APP
# =============================
def main():
    # Header with ancient symbol
    st.markdown('<div class="ancient-symbol">ॐ</div>', unsafe_allow_html=True)
    st.markdown("<h1>🕉️ VAIDYA: PRAKRITI MASTERY</h1>", unsafe_allow_html=True)
    st.markdown('<p class="subtitle">"Discover your eternal blueprint through 5,000 years of Ayurvedic wisdom"</p>', 
                unsafe_allow_html=True)
    
    # Sidebar with simplified content
    with st.sidebar:
        st.markdown("### 📜 Ancient Wisdom")
        st.info("""
        **The Three Doshas:**
        1. **Vata** - Movement & Creativity
        2. **Pitta** - Transformation & Leadership  
        3. **Kapha** - Structure & Nurturing
        
        **Golden Rule:**
        Know your nature,
        Live by its rhythm,
        Find eternal balance.
        """)
        
        st.markdown("---")
        st.markdown("### 🔮 Quick Tips")
        st.caption("• Answer honestly, not ideally")
        st.caption("• Choose what feels most natural")
        st.caption("• Consider your lifelong tendencies")
        st.caption("• The assessment reveals your true nature")
    
    # Initialize session state
    if 'assessment_complete' not in st.session_state:
        st.session_state.assessment_complete = False
    if 'validation_errors' not in st.session_state:
        st.session_state.validation_errors = []
    
    # User Introduction
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if not st.session_state.assessment_complete:
            with st.form("user_intro"):
                user_name = st.text_input(
                    "🌿 What is your sacred name, seeker of wisdom?",
                    placeholder="Enter your name...",
                    key="user_name_input"
                )
                
                # Simplified date input
                birth_date_obj, formatted_date = simplified_date_input("📅 Date of Birth (DD/MM/YYYY)")
                
                submitted = st.form_submit_button("🚀 Begin My Ayurvedic Journey", type="primary")
                
                if submitted:
                    # Validate required fields
                    errors = validate_required_fields(user_name, birth_date_obj, formatted_date)
                    
                    if errors:
                        st.session_state.validation_errors = errors
                        for error in errors:
                            st.markdown(f'<div class="error-message">{error}</div>', unsafe_allow_html=True)
                    else:
                        st.session_state.validation_errors = []
                        # Convert to Nepali date
                        nepali_date = NepaliDateConverter.english_to_nepali(birth_date_obj)
                        
                        st.session_state.user_name = user_name.strip()
                        st.session_state.birth_date = birth_date_obj
                        st.session_state.formatted_date = formatted_date
                        st.session_state.nepali_date = nepali_date
    
    with col2:
        if 'user_name' in st.session_state and st.session_state.user_name:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem; color: #8d6e63;">🌱</div>
                <div style="font-weight: 600; margin-top: 10px;">{st.session_state.user_name}</div>
                <div style="color: #795548; font-size: 0.9rem;">
                    English: {st.session_state.formatted_date}<br>
                    Nepali: {st.session_state.nepali_date['formatted']}<br>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Assessment Questions
    if 'user_name' in st.session_state and st.session_state.user_name and not st.session_state.validation_errors:
        if not st.session_state.assessment_complete:
            st.divider()
            
            # Display questions with toggle
            responses = display_questions_with_toggle()
            
            if len(responses) == 10:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🌀 Reveal My Sacred Blueprint", type="primary", use_container_width=True):
                        # Calculate scores
                        mapping = {"A": "Vata", "B": "Pitta", "C": "Kapha"}
                        results = [mapping[r] for r in responses]
                        counter = Counter(results)
                        main_dosha = counter.most_common(1)[0][0]
                        
                        # Calculate percentages
                        scores = {
                            "Vata": (results.count("Vata") / len(results)) * 100,
                            "Pitta": (results.count("Pitta") / len(results)) * 100,
                            "Kapha": (results.count("Kapha") / len(results)) * 100
                        }
                        
                        st.session_state.scores = scores
                        st.session_state.main_dosha = main_dosha
                        st.session_state.assessment_complete = True
                        
                        # Use Streamlit's native scrolling to results
                        st.rerun()
            else:
                if st.session_state.questions_visible:
                    st.warning("Please answer all 10 questions to reveal your blueprint.")
        
        # Display Results - Add an anchor for scrolling
        if st.session_state.assessment_complete:
            # Add an invisible anchor at the top of results
            st.markdown('<div class="results-anchor" id="results-top"></div>', unsafe_allow_html=True)
            
            # Add a script to scroll to results on page load
            st.markdown("""
            <script>
            // Scroll to results when page loads
            window.onload = function() {
                // Small delay to ensure content is rendered
                setTimeout(function() {
                    const resultsAnchor = document.querySelector('.results-anchor');
                    if (resultsAnchor) {
                        resultsAnchor.scrollIntoView({behavior: 'smooth'});
                    }
                }, 100);
            };
            </script>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            dosha_data = DOSHA_ARCHETYPES[st.session_state.main_dosha]
            
            # Header Result with animation
            st.markdown(f"## ✨ {st.session_state.user_name}, You Are:")
            st.markdown(f"# {dosha_data['symbol']} **{st.session_state.main_dosha}**")
            st.markdown(f"### _{dosha_data['title']}_")
            
            # Dosha Chart
            create_dosha_chart_streamlit(st.session_state.scores)
            
            # Tabs for different sections
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "📖 Story", "👁️ Body", "🧠 Personality", "🌟 Horoscope", "🧘 Daily Life", "🥗 Nutrition"
            ])
            
            with tab1:
                st.markdown(f"""
                <div class="wisdom-card">
                    <h3>Your Archetype Story</h3>
                    <p>{dosha_data['story']}</p>
                    <hr>
                    <p><b>Ancient Wisdom:</b> <i>"{dosha_data['ancient_quote']}"</i></p>
                    <p><b>Sanskrit Name:</b> {dosha_data['sanskrit_name']}</p>
                    <p><b>Element:</b> {dosha_data['element']}</p>
                    <p><b>Governing Planets:</b> {dosha_data['governing_planet']}</p>
                    <p><b>Season:</b> {dosha_data['season']}</p>
                    <p><b>Peak Time:</b> {dosha_data['time_of_day']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with tab2:
                # Body Type Description
                display_body_description(dosha_data)
            
            with tab3:
                # Personality Section
                display_personality_section(dosha_data)
            
            with tab4:
                # Horoscope Section
                display_horoscope(dosha_data)
            
            with tab5:
                # Daily Routine with specific oil massage and pranayama
                display_daily_routine_visual(dosha_data, st.session_state.main_dosha)
                
                # Seasonal Living
                with st.expander("🌿 **Seasonal Wisdom**", expanded=False):
                    seasons_data = {
                        "Spring": "Light detox, gentle exercise, reduce dairy",
                        "Summer": "Stay cool, eat cooling foods, avoid midday sun",
                        "Autumn": "Establish routine, eat warm foods, practice grounding",
                        "Winter": "Rest more, eat warm oily foods, oil massage"
                    }
                    for season, advice in seasons_data.items():
                        st.markdown(f"**{season}:** {advice}")
            
            with tab6:
                # Nutrition Section
                col1, col2 = st.columns(2)
                with col1:
                    st.success("**Foods to Embrace:**")
                    if st.session_state.main_dosha == "Vata":
                        foods = ["Warm cooked grains", "Root vegetables", "Ghee", "Nuts (soaked)", "Spiced milk", "Sweet fruits"]
                    elif st.session_state.main_dosha == "Pitta":
                        foods = ["Sweet fruits", "Coconut", "Cucumber", "Mint", "Fennel", "Rice", "Dairy"]
                    else:  # Kapha
                        foods = ["Light grains", "Steamed greens", "Legumes", "Honey", "Spices", "Apples", "Pomegranate"]
                    
                    for food in foods:
                        st.markdown(f"• {food}")
                    
                    st.info("**Eating Schedule:**")
                    st.markdown("• Breakfast: 7-8 AM (Light)")
                    st.markdown("• Lunch: 12-1 PM (Main meal)")
                    st.markdown("• Dinner: 6-7 PM (Very light)")
                
                with col2:
                    st.warning("**Foods to Minimize:**")
                    if st.session_state.main_dosha == "Vata":
                        avoids = ["Cold foods", "Raw salads", "Dry crackers", "Beans", "Leftovers", "Caffeine"]
                    elif st.session_state.main_dosha == "Pitta":
                        avoids = ["Spicy foods", "Sour fruits", "Fermented foods", "Alcohol", "Excessive salt"]
                    else:  # Kapha
                        avoids = ["Heavy desserts", "Dairy", "Fried foods", "Cold drinks", "Excessive nuts", "Bananas"]
                    
                    for avoid in avoids:
                        st.markdown(f"• {avoid}")
                    
                    st.info("**Eating Wisdom:**")
                    st.markdown("• Eat when hungry, not by clock")
                    st.markdown("• Chew each bite 32 times")
                    st.markdown("• Sit down to eat mindfully")
                    st.markdown("• Stop when 3/4 full")
            
            # Reset Button
            st.markdown("---")

            # Add scroll indicator text
            st.markdown("""
            <div style="text-align: center; margin-bottom: 20px;">
                <p style="color: #666; font-size: 14px;">
                    ⬆️ <em>Scroll up to see your full Prakriti analysis results</em> ⬆️
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Reset button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 Take Assessment Again", type="secondary", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
    
    else:
        # Welcome Message with ancient experience - UPDATED FOR DARK MODE
        if not st.session_state.validation_errors:
            st.markdown("""
            <div class="welcome-message-container">
                <div class="symbol" style="font-size: 4rem; color: #8d6e63;">🌿</div>
                <h3>Welcome, Seeker of Balance</h3>
                <p style="max-width: 600px; margin: 20px auto; color: #2d2d2d;">
                Discover your unique constitution through 5,000 years of Ayurvedic wisdom. 
                Enter your name and birth date to begin your journey to self-knowledge.
                </p>
                <div style="margin: 30px 0;">
                    <div style="display: inline-block; margin: 0 20px; animation: fadeIn 2.5s ease;">
                        <div style="font-size: 2.5rem; color: #8d6e63;">🌀</div>
                        <div class="dosha-label" style="color: #5d4037; font-weight: 500;">Vata</div>
                    </div>
                    <div style="display: inline-block; margin: 0 20px; animation: fadeIn 3s ease;">
                        <div style="font-size: 2.5rem; color: #d32f2f;">🔥</div>
                        <div class="dosha-label" style="color: #5d4037; font-weight: 500;">Pitta</div>
                    </div>
                    <div style="display: inline-block; margin: 0 20px; animation: fadeIn 3.5s ease;">
                        <div style="font-size: 2.5rem; color: #388e3c;">🌊</div>
                        <div class="dosha-label" style="color: #5d4037; font-weight: 500;">Kapha</div>
                    </div>
                </div>
                <p class="quote" style="font-style: italic; color: #795548;">
                "Health is the greatest gift, contentment the greatest wealth, 
                faithfulness the best relationship."<br>
                — Buddha
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Display Footer
    display_footer()

if __name__ == "__main__":
    main()
