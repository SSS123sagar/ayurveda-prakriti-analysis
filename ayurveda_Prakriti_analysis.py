import streamlit as st
from collections import Counter
import pandas as pd
from datetime import datetime, date, timedelta
import base64
from fpdf import FPDF, HTMLMixin 
import tempfile
import os

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
            /* background: var(--dark-card-bg)*/
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
            color: #ffffff !important;  /* CHANGED: White text for better visibility */
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
            box-shadow: 0 4px 8px rgba(141, 110, 99, 0.3);
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
# PDF GENERATION CLASS - SIMPLIFIED VERSION
# =============================
class AyurvedicPDFReport(FPDF):
    def __init__(self):
        super().__init__()
        # Use standard fonts only
        self.set_auto_page_break(auto=True, margin=15)
        
    def header(self):
        # Simple header without Unicode
        self.set_font('Arial', 'B', 20)
        self.set_text_color(142, 110, 99)
        self.cell(0, 10, 'VAIDYA: PRAKRITI MASTERY', 0, 1, 'C')
        
        self.set_font('Arial', 'I', 12)
        self.set_text_color(121, 85, 72)
        self.cell(0, 8, 'Ancient Wisdom for Modern Living - Personal Prakriti Analysis', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title, symbol="*"):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(142, 110, 99)
        self.cell(0, 10, f'{symbol} {title}', 0, 1, 'L')
        self.ln(2)
    
    def dosha_section_title(self, title, dosha_color):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(*dosha_color)
        self.cell(0, 8, title, 0, 1, 'L')
        self.ln(1)
    
    def add_body_text(self, text):
        self.set_font('Arial', '', 11)
        self.set_text_color(50, 50, 50)
        # Clean text by removing Unicode characters
        cleaned_text = self._clean_text(text)
        self.multi_cell(0, 6, cleaned_text)
        self.ln(2)
    
    def add_bullet_point(self, text, indent=10):
        self.set_font('Arial', '', 11)
        self.set_text_color(50, 50, 50)
        self.cell(indent)
        # Clean text by removing Unicode characters
        cleaned_text = self._clean_text(text)
        self.cell(0, 6, f'* {cleaned_text}', 0, 1)
    
    def add_table_row(self, col1, col2, col_width=80):
        self.set_font('Arial', 'B', 11)
        self.set_text_color(93, 64, 55)
        self.cell(col_width, 8, col1, 'B', 0)
        self.set_font('Arial', '', 10)
        self.set_text_color(50, 50, 50)
        # Clean text by removing Unicode characters
        cleaned_col2 = self._clean_text(col2)
        self.cell(0, 8, cleaned_col2, 'B', 1)
    
    def add_dosha_chart(self, scores, user_name):
        # Chart header
        self.set_font('Arial', 'B', 14)
        self.set_text_color(93, 64, 55)
        self.cell(0, 10, f'Dosha Analysis for {user_name}', 0, 1, 'C')
        self.ln(2)
        
        # Create a simple bar chart representation
        chart_width = 180
        bar_height = 15
        
        # Vata bar
        vata_percent = scores['Vata']
        vata_width = (vata_percent / 100) * chart_width
        self.set_fill_color(142, 110, 99)
        self.rect(10, self.get_y(), vata_width, bar_height, 'F')
        self.set_font('Arial', 'B', 10)
        self.set_text_color(255, 255, 255)
        self.set_xy(10 + vata_width + 5, self.get_y())
        self.cell(0, bar_height, f'Vata: {vata_percent:.0f}%', 0, 1)
        self.ln(3)
        
        # Pitta bar
        pitta_percent = scores['Pitta']
        pitta_width = (pitta_percent / 100) * chart_width
        self.set_fill_color(211, 47, 47)
        self.rect(10, self.get_y(), pitta_width, bar_height, 'F')
        self.set_text_color(255, 255, 255)
        self.set_xy(10 + pitta_width + 5, self.get_y())
        self.cell(0, bar_height, f'Pitta: {pitta_percent:.0f}%', 0, 1)
        self.ln(3)
        
        # Kapha bar
        kapha_percent = scores['Kapha']
        kapha_width = (kapha_percent / 100) * chart_width
        self.set_fill_color(56, 142, 60)
        self.rect(10, self.get_y(), kapha_width, bar_height, 'F')
        self.set_text_color(255, 255, 255)
        self.set_xy(10 + kapha_width + 5, self.get_y())
        self.cell(0, bar_height, f'Kapha: {kapha_percent:.0f}%', 0, 1)
        self.ln(10)
    
    def add_wisdom_quote(self, quote):
        self.set_font('Arial', 'I', 10)
        self.set_text_color(121, 85, 72)
        self.set_x(10)
        # Clean quote by removing Unicode characters
        cleaned_quote = self._clean_text(quote)
        self.multi_cell(0, 6, f'"{cleaned_quote}"')
        self.ln(3)
    
    def _clean_text(self, text):
        """Remove Unicode characters from text for PDF compatibility"""
        if not text:
            return ""
        # Replace common Unicode characters with ASCII equivalents
        replacements = {
            'ॐ': 'OM',
            '—': '-',
            '–': '-',
            '•': '*',
            '“': '"',
            '”': '"',
            '‘': "'",
            '’': "'",
            '…': '...',
            '₹': 'Rs',
            '℃': 'C',
            '°': ' deg '
        }
        
        cleaned_text = text
        for unicode_char, ascii_char in replacements.items():
            cleaned_text = cleaned_text.replace(unicode_char, ascii_char)
        
        # Remove any other non-ASCII characters
        cleaned_text = ''.join(char for char in cleaned_text if ord(char) < 128)
        return cleaned_text

# =============================
# PDF GENERATION FUNCTION
# =============================
# =============================
# PDF GENERATION FUNCTION
# =============================
def generate_pdf_report(user_data, dosha_data, scores, main_dosha):
    pdf = AyurvedicPDFReport()
    
    # Add first page
    pdf.add_page()
    
    # Personal Information Section
    pdf.chapter_title("Personal Information")
    pdf.add_table_row("Name:", user_data['name'])
    pdf.add_table_row("Date of Birth:", user_data['birth_date'])
    pdf.add_table_row("Nepali Date:", user_data['nepali_date'])
    pdf.add_table_row("Analysis Date:", datetime.now().strftime("%d/%m/%Y %H:%M"))
    pdf.ln(5)
    
    # Dosha Analysis Section
    pdf.chapter_title("Dosha Analysis Results")
    pdf.add_dosha_chart(scores, user_data['name'])
    
    # Main Dosha Information
    dosha_colors = {
        "Vata": (142, 110, 99),
        "Pitta": (211, 47, 47),
        "Kapha": (56, 142, 60)
    }
    
    pdf.dosha_section_title(f"Primary Dosha: {main_dosha}", dosha_colors[main_dosha])
    pdf.add_body_text(f"Archetype: {dosha_data['title']}")
    pdf.add_body_text(f"Elements: {dosha_data['element']}")
    pdf.add_body_text(f"Governing Planets: {dosha_data['governing_planet']}")
    pdf.add_body_text(f"Sanskrit Name: {dosha_data['sanskrit_name']}")
    pdf.ln(5)
    
    # Personal Story
    pdf.chapter_title("Your Archetype Story")
    story_text = pdf._clean_text(dosha_data['story'])
    pdf.add_body_text(story_text)
    quote_text = pdf._clean_text(dosha_data['ancient_quote'])
    pdf.add_wisdom_quote(quote_text)
    pdf.ln(5)
    
    # Physical Characteristics
    pdf.chapter_title("Physical Characteristics")
    if "body_description" in dosha_data:
        body = dosha_data["body_description"]
        pdf.add_table_row("Frame & Build:", body["frame"])
        pdf.add_table_row("Height Pattern:", body["height"])
        pdf.add_table_row("Weight Pattern:", body["weight"])
        pdf.add_table_row("Skin Type:", body["skin"])
        pdf.add_table_row("Hair Type:", body["hair"])
        pdf.add_table_row("Eye Characteristics:", body["eyes"])
    pdf.ln(5)
    
    # Personality Traits
    pdf.chapter_title("Personality Profile")
    if "personality" in dosha_data:
        personality = dosha_data["personality"]
        pdf.add_body_text(f"Core Nature: {personality['nature']}")
        pdf.add_body_text(f"Communication Style: {personality['communication']}")
        pdf.ln(2)
        
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(142, 110, 99)
        pdf.cell(0, 8, "Strengths:", 0, 1)
        pdf.set_font('Arial', '', 11)
        pdf.set_text_color(50, 50, 50)
        for strength in personality['strengths']:
            pdf.add_bullet_point(strength)
        
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(211, 47, 47)
        pdf.cell(0, 8, "Areas for Balance:", 0, 1)
        pdf.set_font('Arial', '', 11)
        pdf.set_text_color(50, 50, 50)
        for weakness in personality['weaknesses']:
            pdf.add_bullet_point(weakness)
    pdf.ln(5)
    
    # Add new page for detailed recommendations
    pdf.add_page()
    
    # Daily Routine
    pdf.chapter_title("Daily Rituals & Routine")
    pdf.add_body_text("According to Ayurveda, following a daily routine (Dinacharya) aligned with your dosha is key to balance.")
    pdf.ln(2)
    
    routine_items = [
        ("5-6 AM", "Wake with first light (Brahma Muhurta)"),
        ("6-7 AM", f"Oil massage with warm sesame oil"),
        ("7-8 AM", f"30 minutes of pranayama and gentle yoga"),
        ("8 AM", "Warm, cooked breakfast with spices"),
        ("12-1 PM", "Main meal of the day"),
        ("4-6 PM", "Gentle walk or light exercise"),
        ("6 PM", "Light, warm dinner"),
        ("9 PM", "Bedtime with warm milk and calming spices")
    ]
    
    for time, activity in routine_items:
        pdf.add_table_row(f"{time}:", activity)
    pdf.ln(5)
    
    # Diet & Nutrition
    pdf.chapter_title("Diet & Nutrition Guidelines")
    
    if main_dosha == "Vata":
        foods_to_embrace = ["Warm cooked grains", "Root vegetables", "Ghee", "Nuts (soaked)", "Spiced milk", "Sweet fruits"]
        foods_to_minimize = ["Cold foods", "Raw salads", "Dry crackers", "Beans", "Leftovers", "Caffeine"]
    elif main_dosha == "Pitta":
        foods_to_embrace = ["Sweet fruits", "Coconut", "Cucumber", "Mint", "Fennel", "Rice", "Dairy"]
        foods_to_minimize = ["Spicy foods", "Sour fruits", "Fermented foods", "Alcohol", "Excessive salt"]
    else:  # Kapha
        foods_to_embrace = ["Light grains", "Steamed greens", "Legumes", "Honey", "Spices", "Apples", "Pomegranate"]
        foods_to_minimize = ["Heavy desserts", "Dairy", "Fried foods", "Cold drinks", "Excessive nuts", "Bananas"]
    
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(56, 142, 60)
    pdf.cell(0, 8, "Foods to Embrace:", 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(50, 50, 50)
    for food in foods_to_embrace[:6]:
        pdf.add_bullet_point(food)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(211, 47, 47)
    pdf.cell(0, 8, "Foods to Minimize:", 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(50, 50, 50)
    for food in foods_to_minimize[:6]:
        pdf.add_bullet_point(food)
    pdf.ln(5)
    
    # Herbs & Supplements
    pdf.chapter_title("Ayurvedic Herbs & Supplements")
    if "herbs_supplements" in dosha_data:
        herbs = dosha_data["herbs_supplements"]
        if "general_herbs" in herbs:
            pdf.set_font('Arial', 'B', 12)
            pdf.set_text_color(93, 64, 55)
            pdf.cell(0, 8, "Recommended Herbs:", 0, 1)
            pdf.set_font('Arial', '', 11)
            pdf.set_text_color(50, 50, 50)
            for herb in herbs["general_herbs"][:5]:
                pdf.add_bullet_point(herb)
    
    pdf.ln(3)
    pdf.add_body_text("Always consult with an Ayurvedic practitioner before starting any herbal regimen.")
    pdf.ln(5)
    
    # Perfume & Aromatherapy
    pdf.chapter_title("Sacred Scents & Aromatherapy")
    if "perfume_recommendations" in dosha_data:
        perfume = dosha_data["perfume_recommendations"]
        if "top_scents" in perfume:
            pdf.set_font('Arial', 'B', 12)
            pdf.set_text_color(142, 110, 99)
            pdf.cell(0, 8, "Balancing Scents:", 0, 1)
            pdf.set_font('Arial', '', 11)
            pdf.set_text_color(50, 50, 50)
            for scent in perfume["top_scents"][:5]:
                pdf.add_bullet_point(scent)
    pdf.ln(5)
    
    # Health Guidance
    pdf.chapter_title("Health & Wellness Guidance")
    pdf.add_body_text(f"As a {main_dosha} predominant type, pay attention to:")
    pdf.ln(2)
    
    health_guidance = {
        "Vata": ["Nervous system balance", "Joint health", "Digestive regularity", "Warmth and grounding"],
        "Pitta": ["Inflammation management", "Liver health", "Skin care", "Cooling practices"],
        "Kapha": ["Metabolic stimulation", "Respiratory health", "Weight management", "Lymphatic drainage"]
    }
    
    for guidance in health_guidance[main_dosha]:
        pdf.add_bullet_point(guidance)
    pdf.ln(5)
    
    # Exercise & Lifestyle
    pdf.chapter_title("Exercise & Lifestyle")
    exercise_tips = {
        "Vata": "Gentle, grounding exercises like yoga, tai chi, and walking in nature. Avoid excessive cardio.",
        "Pitta": "Moderate, cooling exercises like swimming and moon salutations. Avoid competitive sports.",
        "Kapha": "Vigorous, stimulating exercises like running and strength training. Avoid sedentary lifestyle."
    }
    
    pdf.add_body_text(f"Recommended: {exercise_tips[main_dosha]}")
    pdf.ln(2)
    
    # Final Wisdom
    pdf.add_page()
    pdf.chapter_title("Ancient Wisdom for Your Journey")
    
    wisdom_quotes = [
        "Health is the greatest gift, contentment the greatest wealth.",
        "When diet is wrong, medicine is of no use. When diet is correct, medicine is of no need.",
        "The secret of health for both mind and body is not to mourn for the past, nor to worry about the future, but to live the present moment wisely.",
        "Balance is not something you find, it's something you create."
    ]
    
    for quote in wisdom_quotes:
        pdf.add_wisdom_quote(quote)
        pdf.ln(2)
    
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(93, 64, 55)
    pdf.cell(0, 10, 'SARVE BHAVANTU SUKHINAH', 0, 1, 'C')
    pdf.set_font('Arial', 'I', 10)
    pdf.set_text_color(121, 85, 72)
    pdf.cell(0, 8, '"May all be happy, may all be free from illness"', 0, 1, 'C')
    pdf.ln(5)
    
    # Final note
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, 'Generated with Vaidya: Prakriti Mastery - www.ayurveda-prakriti-analysis.streamlit', 0, 1, 'C')
    
    # Generate PDF - FIXED VERSION
    try:
        # Method 1: Try to get bytes directly
        pdf_output = pdf.output(dest='S')
        
        # Check if it's already bytes
        if isinstance(pdf_output, bytes):
            return pdf_output
        elif isinstance(pdf_output, str):
            # If it's a string, encode it
            return pdf_output.encode('latin-1')
        elif isinstance(pdf_output, bytearray):
            # If it's a bytearray, convert to bytes
            return bytes(pdf_output)
        else:
            # Fallback: use to_bytes method
            return pdf.output()
    except:
        # Ultimate fallback
        return pdf.output()

# =============================
# CREATE DOWNLOAD LINK FOR PDF
# =============================
def create_download_link(pdf_output, filename):
    """Create a download link for the PDF file with proper encoding"""
    b64 = base64.b64encode(pdf_output).decode()
    href = f'''
    <div style="text-align: center; margin: 20px 0;">
        <a href="data:application/pdf;base64,{b64}" download="{filename}" 
           style="background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%); 
                  color: white; padding: 14px 28px; text-decoration: none; 
                  border-radius: 10px; font-weight: 600; display: inline-block; 
                  font-family: Inter, sans-serif; font-size: 1.1rem;
                  box-shadow: 0 4px 8px rgba(212, 175, 55, 0.3);
                  transition: all 0.3s ease;">
           📥 Download Complete Analysis PDF
        </a>
    </div>
    '''
    return href

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
# ENHANCED KNOWLEDGE BASE WITH ALL FEATURES (INCLUDING HERBS & BEAUTY)
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
        
        # PERFUME & SCENTS SECTION - ADDED
        "perfume_recommendations": {
            "top_scents": ["Sandalwood", "Vanilla", "Cinnamon", "Orange", "Bergamot", "Frankincense", "Myrrh"],
            "notes_to_embrace": ["Warm", "Sweet", "Grounding", "Woody", "Comforting"],
            "notes_to_avoid": ["Minty", "Cooling", "Light", "Airy", "Eucalyptus"],
            "best_perfume_types": ["Oriental", "Woody", "Gourmand", "Amber", "Spicy"],
            "application_tips": "Apply to pulse points (wrists, neck) after warm oil massage for better absorption",
            "ayurvedic_blend": "Sandalwood (3 drops) + Vanilla (2 drops) + Orange (1 drop) in 10ml carrier oil",
            "famous_perfumes": ["Shalimar by Guerlain", "Santal 33 by Le Labo", "Vanilla by Dior", "Cinnamon by Jo Malone"],
            "seasonal_scents": {
                "Spring": "Light citrus with warm base notes",
                "Summer": "Milder versions of warm scents",
                "Autumn": "Full-bodied spicy and woody scents",
                "Winter": "Rich, deep, warming oriental blends"
            }
        },
        
        # NEW: HERBS & SUPPLEMENTS SECTION
        "herbs_supplements": {
            "general_herbs": ["Ashwagandha (Winter Cherry)", "Shatavari (Asparagus)", "Brahmi (Gotu Kola)", "Triphala", "Ginger", "Licorice", "Cinnamon"],
            "male_specific": [
                "Ashwagandha for strength and vitality",
                "Gokshura for male reproductive health",
                "Shilajit for energy and stamina",
                "Safed Musli for testosterone balance"
            ],
            "female_specific": [
                "Shatavari for hormonal balance",
                "Ashoka for menstrual health",
                "Lodhra for feminine wellness",
                "Manjistha for skin and detox"
            ],
            "daily_supplements": ["Ashwagandha powder (1 tsp)", "Triphala (500mg)", "Sesame oil capsules", "Warm milk with turmeric"],
            "avoid_herbs": ["Bitter melon", "Neem", "Aloe vera juice (cold)", "Strong laxatives"],
            "best_form": "Powders in warm milk or ghee",
            "timing": "Take with warm meals, avoid on empty stomach",
            "ayurvedic_formulas": ["Ashwagandharishta", "Chyawanprash", "Dashamoola", "Bala Taila"]
        },
        
        # NEW: BEAUTY & SKINCARE SECTION
        "beauty_skincare": {
            "skin_type": "Dry, thin, cool, prone to wrinkles and cracking",
            "male_specific": [
                "Use rich, creamy shaving creams",
                "Warm oil beard conditioning daily",
                "Avoid alcohol-based aftershaves",
                "Moisturize immediately after shower"
            ],
            "female_specific": [
                "Oil-based makeup removers",
                "Cream-based foundations",
                "Avoid powder-based products",
                "Night creams with almond oil"
            ],
            "cleansing": "Oil cleansing method with warm sesame oil",
            "moisturizing": "Heavy creams with shea butter, avocado oil",
            "face_masks": ["Avocado + honey", "Banana + almond oil", "Sandalwood + rose water"],
            "hair_care": ["Warm oil scalp massage", "Avoid blow drying", "Deep conditioning weekly"],
            "problem_areas": ["Dry patches", "Early wrinkles", "Cold hands/feet", "Cracked heels"],
            "ayurvedic_treatments": ["Abhyanga (oil massage)", "Shirodhara", "Nasya (nasal oils)", "Padabhyanga (foot massage)"]
        },
        
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
        
        # PERFUME & SCENTS SECTION - ADDED
        "perfume_recommendations": {
            "top_scents": ["Rose", "Jasmine", "Sandalwood", "Lavender", "Mint", "Chamomile", "Vetiver"],
            "notes_to_embrace": ["Cooling", "Floral", "Sweet", "Fresh", "Calming"],
            "notes_to_avoid": ["Spicy", "Warm", "Citrus", "Pepper", "Cinnamon"],
            "best_perfume_types": ["Floral", "Aquatic", "Green", "Fresh", "Light Oriental"],
            "application_tips": "Apply to cooler areas (inner elbows, behind knees) to avoid overheating",
            "ayurvedic_blend": "Rose (3 drops) + Sandalwood (2 drops) + Lavender (1 drop) in 10ml coconut oil",
            "famous_perfumes": ["Chanel No. 5", "Miss Dior", "Light Blue by Dolce & Gabbana", "J'adore by Dior"],
            "seasonal_scents": {
                "Spring": "Light floral and green scents",
                "Summer": "Cool aquatic and fresh citrus",
                "Autumn": "Mild woody with floral notes",
                "Winter": "Gentle sweet florals with cool base"
            }
        },
        
        # NEW: HERBS & SUPPLEMENTS SECTION
        "herbs_supplements": {
            "general_herbs": ["Amla (Indian Gooseberry)", "Shatavari", "Coriander", "Fennel", "Rose", "Sandalwood", "Aloe Vera"],
            "male_specific": [
                "Shatavari for cooling and stress",
                "Amalaki for antioxidant protection",
                "Guduchi for liver health",
                "Bhringaraj for hair and cooling"
            ],
            "female_specific": [
                "Shatavari for hormonal balance",
                "Manjistha for clear skin",
                "Kumari (Aloe) for digestion",
                "Chandana (Sandalwood) for cooling"
            ],
            "daily_supplements": ["Amla powder (1 tsp)", "Shatavari (500mg)", "Coconut water", "Rose water"],
            "avoid_herbs": ["Ginger (excess)", "Black pepper", "Garlic", "Cayenne"],
            "best_form": "Cool infusions, powders in cool water",
            "timing": "Take between meals, avoid in midday heat",
            "ayurvedic_formulas": ["Chandraprabha Vati", "Amla Murabba", "Shatavari Ghrita", "Kumaryasava"]
        },
        
        # NEW: BEAUTY & SKINCARE SECTION
        "beauty_skincare": {
            "skin_type": "Sensitive, warm, reddish, prone to rashes and acne",
            "male_specific": [
                "Alcohol-free aftershaves",
                "Cooling pre-shave oils",
                "Avoid hot water shaving",
                "SPF 30+ daily"
            ],
            "female_specific": [
                "Mineral-based makeup",
                "Cooling sheet masks",
                "Rose water toner",
                "Avoid heavy foundations"
            ],
            "cleansing": "Gentle milk cleansers, rose water",
            "moisturizing": "Light gels with aloe vera, cucumber",
            "face_masks": ["Cucumber + mint", "Sandlwood + rose", "Aloe vera gel"],
            "hair_care": ["Coconut oil cooling", "Avoid heat styling", "Herbal rinses"],
            "problem_areas": ["Acne", "Rosacea", "Sun sensitivity", "Premature greying"],
            "ayurvedic_treatments": ["Takradhara", "Chandana Lepa", "Ubtan with sandalwood", "Kashaya Dhara"]
        },
        
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
        
        # PERFUME & SCENTS SECTION - ADDED
        "perfume_recommendations": {
            "top_scents": ["Eucalyptus", "Rosemary", "Ginger", "Juniper", "Peppermint", "Lemon", "Cypress"],
            "notes_to_embrace": ["Stimulating", "Fresh", "Citrus", "Herbal", "Uplifting"],
            "notes_to_avoid": ["Sweet", "Heavy", "Musk", "Vanilla", "Floral"],
            "best_perfume_types": ["Citrus", "Fresh", "Green", "Herbal", "Aromatic"],
            "application_tips": "Apply to active areas (wrists, neck) after dry brushing for better absorption",
            "ayurvedic_blend": "Eucalyptus (3 drops) + Lemon (2 drops) + Rosemary (1 drop) in 10ml jojoba oil",
            "famous_perfumes": ["Acqua di Gio by Giorgio Armani", "Eau Sauvage by Dior", "Un Jardin en Méditerranée by Hermès", "Green Tea by Elizabeth Arden"],
            "seasonal_scents": {
                "Spring": "Light citrus and herbal blends",
                "Summer": "Fresh green and aquatic notes",
                "Autumn": "Warm herbal with light spice",
                "Winter": "Stimulating citrus with pine notes"
            }
        },
        
        # NEW: HERBS & SUPPLEMENTS SECTION
        "herbs_supplements": {
            "general_herbs": ["Ginger", "Turmeric", "Black Pepper", "Pippali (Long Pepper)", "Guggul", "Triphala", "Bitter Melon"],
            "male_specific": [
                "Guggul for cholesterol and weight",
                "Shilajit for energy (small doses)",
                "Punarnava for fluid balance",
                "Musta for digestion"
            ],
            "female_specific": [
                "Turmeric for inflammation",
                "Ginger for circulation",
                "Fenugreek for metabolism",
                "Cinnamon for blood sugar"
            ],
            "daily_supplements": ["Triphala (750mg)", "Ginger tea", "Honey + lemon", "Warm water with spices"],
            "avoid_herbs": ["Licorice", "Shatavari", "Heavy tonics", "Dairy-based formulas"],
            "best_form": "Powders in honey, decoctions",
            "timing": "Take on empty stomach, early morning",
            "ayurvedic_formulas": ["Triphala Guggulu", "Medohar Guggulu", "Arogyavardhini", "Chitrakadi Vati"]
        },
        
        # NEW: BEAUTY & SKINCARE SECTION
        "beauty_skincare": {
            "skin_type": "Oily, thick, cool, prone to congestion and large pores",
            "male_specific": [
                "Clay-based shaving creams",
                "Exfoliate before shaving",
                "Alcohol-free toners",
                "Light, oil-free moisturizers"
            ],
            "female_specific": [
                "Water-based foundations",
                "Mineral powder makeup",
                "Clay masks weekly",
                "Avoid cream blushes"
            ],
            "cleansing": "Foaming cleansers, clay masks",
            "moisturizing": "Light gels, oil-free lotions",
            "face_masks": ["Clay + rose water", "Oatmeal + honey", "Turmeric + chickpea flour"],
            "hair_care": ["Dry shampoo as needed", "Clarifying shampoos", "Avoid heavy conditioners"],
            "problem_areas": ["Oily T-zone", "Blackheads", "Cellulite", "Water retention"],
            "ayurvedic_treatments": ["Udvartana (dry massage)", "Swedana (herbal steam)", "Lepa (herbal pastes)", "Nasya with stimulating oils"]
        },
        
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
     ["A) Naturally lean or light-framed, often appearing slender even without effort",
      "B) Naturally well-proportioned with a balanced, athletic-looking structure", 
      "C) Naturally broad or solid, with a sturdy or fuller physical presence"]),
    
    ("2. How would you describe your weight pattern?",
     ["A) Tends to remain thin or lose weight easily, even when eating well",
      "B) Weight usually stays stable and changes gradually with conscious effort", 
      "C) Tends to gain weight easily and finds weight loss slower"]),
    
    ("3. What is your skin texture like?",
     ["A) Often feels dry, rough, or lacking moisture",
      "B) Often feels warm, sensitive, or prone to redness", 
      "C) Generally smooth, soft, or slightly oily"]),
    
    ("4. What is your typical energy pattern?",
     ["A) Energy rises and falls throughout the day, with moments of enthusiasm followed by rest",
      "B) Energy feels strong, focused, and goal-driven for extended periods", 
      "C) Energy is steady, calm, and long-lasting without sharp peaks"]),
    
    ("5. How is your appetite and digestion?",
     ["A) Appetite can be unpredictable, sometimes strong and sometimes low",
      "B) Appetite is usually strong with quick digestion", 
      "C) Appetite is moderate and digestion feels slower but consistent"]),
    
    ("6. What is your sleep pattern like?",
     ["A) Sleep tends to be light, easily interrupted, or irregular",
      "B) Sleep is generally restful and refreshing", 
      "C) Sleep is deep, heavy, and long, sometimes making waking up difficult"]),
    
    ("7. How is your mind typically?",
     ["A) Mind is active, imaginative, and often jumping between ideas",
      "B) Mind is sharp, focused, and oriented toward goals or problem-solving", 
      "C) Mind is calm, patient, and steady"]),
    
    ("8. How do you handle stress?",
     ["A) Stress shows up as worry, overthinking, or nervous energy",
      "B) Stress triggers intensity, frustration, or a strong urge to take control", 
      "C) Stress leads to withdrawal, slowing down, or seeking comfort"]),
    
    ("9. What climate suits you best?",
     ["A) Feels best in warm, calm, or slightly humid environments",
      "B) Feels best in cooler or well-ventilated environments", 
      "C) Feels best in warm, dry, or stable environments"]),
    
    ("10. What is your learning style?",
     ["A) Learns quickly and intuitively but may forget details over time",
      "B) Learns best through focus, challenge, and analysis", 
      "C) Learns gradually but retains information for a long time"])
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
# NEW: HERBS & SUPPLEMENTS SECTION
# =============================
def display_herbs_supplements_section(dosha_data):
    """Display herbs and supplements recommendations"""
    
    herbs_data = dosha_data.get("herbs_supplements", {})
    
    if not herbs_data:
        st.warning("Herbs and supplements recommendations not available.")
        return
    
    st.markdown("### 🌿 **Ayurvedic Herbs & Supplements**")
    st.info("Ancient Ayurvedic wisdom for natural healing and balance.")
    
    # Gender selection for specific recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌱 **General Herbs for All**")
        for herb in herbs_data.get("general_herbs", []):
            st.markdown(f"• **{herb}**")
    
    with col2:
        st.markdown("#### 💊 **Daily Supplements**")
        for supplement in herbs_data.get("daily_supplements", []):
            st.success(f"• {supplement}")
    
    # Gender-specific recommendations
    st.markdown("---")
    st.markdown("#### 👨‍⚕️ **Gender-Specific Recommendations**")
    
    gender_col1, gender_col2 = st.columns(2)
    
    with gender_col1:
        st.markdown("##### 👨 **For Men**")
        for item in herbs_data.get("male_specific", []):
            st.markdown(f"• {item}")
    
    with gender_col2:
        st.markdown("##### 👩 **For Women**")
        for item in herbs_data.get("female_specific", []):
            st.markdown(f"• {item}")
    
    # Additional Information
    with st.expander("📋 **Usage Guidelines & Ayurvedic Formulas**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Best Form & Timing:**")
            st.info(f"**Form:** {herbs_data.get('best_form', '')}")
            st.info(f"**Timing:** {herbs_data.get('timing', '')}")
            
            st.markdown("**Herbs to Avoid:**")
            for herb in herbs_data.get("avoid_herbs", []):
                st.warning(f"• {herb}")
        
        with col2:
            st.markdown("**Classic Ayurvedic Formulas:**")
            for formula in herbs_data.get("ayurvedic_formulas", []):
                st.success(f"• {formula}")
            
            st.markdown("**Ancient Wisdom:**")
            st.info("""
            - Take herbs according to seasons
            - Always consult an Ayurvedic practitioner
            - Combine with proper diet and lifestyle
            - Start with small doses and observe effects
            """)

# =============================
# NEW: BEAUTY & SKINCARE SECTION
# =============================
def display_beauty_skincare_section(dosha_data):
    """Display beauty and skincare recommendations"""
    
    beauty_data = dosha_data.get("beauty_skincare", {})
    
    if not beauty_data:
        st.warning("Beauty and skincare recommendations not available.")
        return
    
    st.markdown("### 💄 **Ayurvedic Beauty & Skincare**")
    st.info("Natural beauty rituals for your unique prakriti.")
    
    # Skin Type
    st.markdown(f"#### 🎯 **Your Skin Type:** {beauty_data.get('skin_type', '')}")
    
    # Gender-specific routines
    st.markdown("---")
    st.markdown("#### 🛁 **Gender-Specific Routines**")
    
    gender_col1, gender_col2 = st.columns(2)
    
    with gender_col1:
        st.markdown("##### 👨 **Men's Grooming**")
        for tip in beauty_data.get("male_specific", []):
            st.markdown(f"• {tip}")
    
    with gender_col2:
        st.markdown("##### 👩 **Women's Beauty**")
        for tip in beauty_data.get("female_specific", []):
            st.markdown(f"• {tip}")
    
    # Skincare Routine
    st.markdown("---")
    st.markdown("#### 🌸 **Daily Skincare Ritual**")
    
    routine_col1, routine_col2 = st.columns(2)
    
    with routine_col1:
        st.markdown("**Cleansing:**")
        st.info(beauty_data.get("cleansing", ""))
        
        st.markdown("**Moisturizing:**")
        st.info(beauty_data.get("moisturizing", ""))
    
    with routine_col2:
        st.markdown("**Weekly Face Masks:**")
        for mask in beauty_data.get("face_masks", []):
            st.success(f"• {mask}")
        
        st.markdown("**Hair Care:**")
        for tip in beauty_data.get("hair_care", []):
            st.info(f"• {tip}")
    
    # Problem Areas & Treatments
    with st.expander("🔍 **Problem Areas & Ayurvedic Treatments**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Common Problem Areas:**")
            for problem in beauty_data.get("problem_areas", []):
                st.warning(f"• {problem}")
            
            st.markdown("**Seasonal Care:**")
            st.info("""
            - **Spring:** Focus on detox and cleansing
            - **Summer:** Emphasize sun protection and cooling
            - **Autumn:** Prepare skin for dryness
            - **Winter:** Intensive moisturizing and protection
            """)
        
        with col2:
            st.markdown("**Ayurvedic Treatments:**")
            for treatment in beauty_data.get("ayurvedic_treatments", []):
                st.success(f"• {treatment}")
            
            st.markdown("**Ancient Beauty Secrets:**")
            st.info("""
            - Beauty starts from within (Ahara)
            - Seasonal detox (Panchakarma)
            - Daily self-massage (Abhyanga)
            - Proper sleep (Nidra) for skin renewal
            """)

# =============================
# PERFUME & SCENTS SECTION
# =============================
def display_perfume_section(dosha_data):
    """Display perfume and aromatherapy recommendations"""
    
    perfume_data = dosha_data.get("perfume_recommendations", {})
    
    if not perfume_data:
        st.warning("Perfume recommendations not available for this dosha.")
        return
    
    # Main Perfume Section
    st.markdown("### 🌸 **Sacred Scents & Perfume Wisdom**")
    st.info("According to Ayurveda, scents directly influence your mind and energy. Choose perfumes that balance your dosha.")
    
    # Top Scents
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 **Top Scents for You**")
        for scent in perfume_data.get("top_scents", []):
            st.markdown(f"• **{scent}**")
        
        st.markdown("#### ✅ **Notes to Embrace**")
        for note in perfume_data.get("notes_to_embrace", []):
            st.success(f"• {note}")
    
    with col2:
        st.markdown("#### ⚠️ **Notes to Avoid**")
        for note in perfume_data.get("notes_to_avoid", []):
            st.warning(f"• {note}")
        
        st.markdown("#### 🎭 **Best Perfume Types**")
        for perfume_type in perfume_data.get("best_perfume_types", []):
            st.info(f"• {perfume_type}")
    
    # Application Tips
    with st.expander("💡 **Application & Ayurvedic Wisdom**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Application Tips:**")
            st.info(perfume_data.get("application_tips", ""))
            
            st.markdown("**Ayurvedic Blend:**")
            st.success(perfume_data.get("ayurvedic_blend", ""))
        
        with col2:
            st.markdown("**Famous Perfume Examples:**")
            for perfume in perfume_data.get("famous_perfumes", []):
                st.markdown(f"• {perfume}")
    
    # Seasonal Scents
    with st.expander("🍂 **Seasonal Scents Guide**", expanded=False):
        seasonal_data = perfume_data.get("seasonal_scents", {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Spring:**")
            st.info(seasonal_data.get("Spring", ""))
            
            st.markdown("**Summer:**")
            st.info(seasonal_data.get("Summer", ""))
        
        with col2:
            st.markdown("**Autumn:**")
            st.info(seasonal_data.get("Autumn", ""))
            
            st.markdown("**Winter:**")
            st.info(seasonal_data.get("Winter", ""))
    
    # Ancient Perfume Rituals
    with st.expander("🕯️ **Ancient Perfume Rituals**", expanded=False):
        st.markdown("""
        **Vedic Gandha (Perfume) Traditions:**
        - Apply perfume after morning bath during Brahma Muhurta (5-6 AM)
        - Use natural attars (essential oil perfumes) over synthetic fragrances
        - Apply to pulse points to enhance scent diffusion
        - Match your perfume to the season and time of day
        - Practice scent fasting (no perfume) one day a week
        """)

# =============================
# NEW: EXERCISE, FASTING & DIET SECTION
# =============================
def display_exercise_fasting_diet_section(dosha_data, main_dosha):
    """Display comprehensive exercise, fasting, and diet recommendations"""
    
    st.markdown("### 💪 **Exercise, Fasting & Diet Mastery**")
    st.info("Complete lifestyle guidance tailored to your dosha for optimal health and balance.")
    
    # Dosha-specific recommendations
    dosha_recommendations = {
        "Vata": {
            "exercise": {
                "type": "Gentle, grounding, calming",
                "recommended": [
                    "Yoga (Hatha, Restorative, Yin)",
                    "Tai Chi & Qigong",
                    "Gentle walking in nature",
                    "Swimming (warm water)",
                    "Pilates (gentle)",
                    "Light cycling",
                    "Dancing (slow, fluid movements)"
                ],
                "intensity": "Low to moderate (40-60% max effort)",
                "duration": "20-45 minutes maximum",
                "best_time": "10 AM - 12 PM or 6-7 PM",
                "frequency": "4-5 times per week, with rest days",
                "avoid": [
                    "High-impact exercises",
                    "Long-distance running",
                    "Extreme cardio",
                    "Competitive sports",
                    "Exercising when tired or stressed"
                ],
                "benefits": "Grounds energy, calms nervous system, improves circulation gently",
                "caution": "Never exercise to exhaustion. Stop at first sign of fatigue."
            },
            "fasting": {
                "recommended": "Mild, intermittent fasting only",
                "schedule": "12-14 hour overnight fast (7 PM - 7 AM)",
                "duration": "Maximum 14 hours",
                "best_type": [
                    "Warm liquid fasting (herbal teas, warm water)",
                    "Fruit fasting (sweet fruits only)",
                    "Kitchari mono-diet"
                ],
                "frequency": "1-2 times per month, not during Vata season",
                "avoid": [
                    "Dry fasting",
                    "Water-only fasting beyond 16 hours",
                    "Fasting during autumn/winter",
                    "Fasting when anxious or stressed"
                ],
                "benefits": "Gentle detox, improves digestion, resets appetite",
                "warning": "Vatas should never do prolonged fasting. Always break fast with warm, oily food."
            },
            "diet_philosophy": {
                "primary": "Warm, moist, grounding, nourishing",
                "meals": "Regular, consistent meal times",
                "quantity": "Moderate portions, never skip meals",
                "temperature": "Always warm or hot, never cold",
                "texture": "Soft, moist, well-cooked"
            },
            "keto_compatibility": {
                "status": "NOT RECOMMENDED",
                "reason": "Keto is too drying, light, and cold for Vata",
                "if_attempting": [
                    "Use generous amounts of ghee and oils",
                    "Include root vegetables",
                    "Drink warm herbal teas",
                    "Avoid raw vegetables",
                    "Supplement with warming spices"
                ],
                "better_alternative": "Ayurvedic balancing diet with whole grains, healthy fats, and cooked vegetables"
            },
            "veg_nonveg": {
                "vegetarian": "HIGHLY RECOMMENDED",
                "recommended_veg": [
                    "Ghee (clarified butter)",
                    "Soaked nuts and seeds",
                    "Whole milk (warm)",
                    "Paneer (fresh cheese)",
                    "Eggs (soft boiled or scrambled)"
                ],
                "non_vegetarian": "Minimal, if at all",
                "if_nonveg": [
                    "Chicken soup (well-cooked)",
                    "Fish (oily, warm water fish)",
                    "Bone broth",
                    "Avoid: Beef, pork, lamb"
                ],
                "protein_timing": "Lunch time only, never at dinner"
            },
            "meal_timing": {
                "breakfast": "7-8 AM: Warm cooked cereal with ghee and spices",
                "lunch": "12-1 PM: Main meal - grains, vegetables, protein",
                "dinner": "6-7 PM: Light soup or kitchari",
                "snacks": "10 AM & 4 PM: Warm milk, soaked nuts, sweet fruit"
            }
        },
        "Pitta": {
            "exercise": {
                "type": "Moderate, cooling, non-competitive",
                "recommended": [
                    "Swimming (cool water)",
                    "Yoga (Moon salutations, cooling poses)",
                    "Cycling (early morning or evening)",
                    "Hiking in nature",
                    "Dancing (fluid, non-competitive)",
                    "Strength training (moderate)",
                    "Team sports (non-competitive)"
                ],
                "intensity": "Moderate (60-70% max effort)",
                "duration": "30-60 minutes",
                "best_time": "6-10 AM or 6-8 PM (avoid midday heat)",
                "frequency": "5-6 times per week",
                "avoid": [
                    "Hot yoga/Bikram yoga",
                    "Exercising in direct sun",
                    "Competitive sports",
                    "Anger-driven workouts",
                    "Exercising during Pitta time (10 AM-2 PM)"
                ],
                "benefits": "Cools the system, reduces inflammation, releases tension",
                "caution": "Stop before sweating profusely. Stay hydrated with cool water."
            },
            "fasting": {
                "recommended": "YES, very beneficial",
                "schedule": "14-16 hour overnight fast",
                "duration": "16 hours maximum, 1-2 days per week",
                "best_type": [
                    "Fruit fasting (sweet fruits)",
                    "Juice fasting (sweet vegetable juices)",
                    "Monodiet (rice or kitchari)"
                ],
                "frequency": "Once per week, especially in summer",
                "avoid": [
                    "Dry fasting",
                    "Spicy food breaking fast",
                    "Fasting when angry or irritated"
                ],
                "benefits": "Reduces acidity, cools digestion, improves mental clarity",
                "warning": "Break fast gently with cooling foods. Never overeat after fasting."
            },
            "diet_philosophy": {
                "primary": "Cooling, sweet, bitter, astringent",
                "meals": "Regular but lighter than other doshas",
                "quantity": "Moderate, stop at 75% full",
                "temperature": "Cool or room temperature",
                "texture": "Moist but not oily"
            },
            "keto_compatibility": {
                "status": "MODERATELY COMPATIBLE with modifications",
                "reason": "Keto can increase heat and acidity if not balanced",
                "if_attempting": [
                    "Focus on cooling fats (coconut, ghee)",
                    "Include plenty of leafy greens",
                    "Avoid spicy keto foods",
                    "Drink cooling herbal teas",
                    "Monitor for increased acidity"
                ],
                "better_alternative": "Ayurvedic cooling diet with balanced macronutrients"
            },
            "veg_nonveg": {
                "vegetarian": "STRONGLY RECOMMENDED",
                "recommended_veg": [
                    "Coconut products",
                    "Ghee (moderate)",
                    "Milk and dairy (cool)",
                    "Moong dal",
                    "Fresh paneer"
                ],
                "non_vegetarian": "Minimal, cooling types only",
                "if_nonveg": [
                    "White meat chicken (boiled)",
                    "Freshwater fish",
                    "Avoid: Red meat, seafood, eggs"
                ],
                "protein_timing": "Lunch only, never at dinner"
            },
            "meal_timing": {
                "breakfast": "7-8 AM: Sweet fruits or cool cereal",
                "lunch": "12-1 PM: Main meal - grains, vegetables, light protein",
                "dinner": "6-7 PM: Very light - soup or vegetables",
                "snacks": "10 AM & 4 PM: Coconut water, sweet fruits, cucumber"
            }
        },
        "Kapha": {
            "exercise": {
                "type": "Vigorous, stimulating, energizing",
                "recommended": [
                    "Running/jogging",
                    "High-intensity interval training (HIIT)",
                    "Strength training",
                    "Vinyasa yoga",
                    "Dancing (energetic)",
                    "Cycling (uphill)",
                    "Team sports",
                    "Jumping rope",
                    "Swimming (vigorous)"
                ],
                "intensity": "High (70-85% max effort)",
                "duration": "45-90 minutes",
                "best_time": "6-10 AM (Kapha time for maximum benefit)",
                "frequency": "6-7 times per week",
                "avoid": [
                    "Sedentary lifestyle",
                    "Exercising after eating",
                    "Slow, gentle exercise only",
                    "Skipping workouts"
                ],
                "benefits": "Stimulates metabolism, reduces congestion, increases energy",
                "caution": "Push yourself but listen to your body. Variety is key to avoid boredom."
            },
            "fasting": {
                "recommended": "YES, highly beneficial",
                "schedule": "16-18 hour intermittent fasting",
                "duration": "Up to 24 hours, 1-2 times per week",
                "best_type": [
                    "Water fasting (short duration)",
                    "Juice fasting (bitter vegetable juices)",
                    "Dry fasting (experienced only)",
                    "Monodiet (light grains)"
                ],
                "frequency": "2-3 times per week, especially in spring",
                "avoid": [
                    "Breaking fast with heavy foods",
                    "Fasting when already lethargic",
                    "Skipping warm water during fast"
                ],
                "benefits": "Reduces congestion, stimulates digestion, promotes weight loss",
                "warning": "Kapha can handle longer fasts but should break fast with light, warm food."
            },
            "diet_philosophy": {
                "primary": "Light, dry, warm, stimulating",
                "meals": "Smaller, more frequent meals",
                "quantity": "Less than other doshas, stop at 50-75% full",
                "temperature": "Hot or warm",
                "texture": "Light, dry, well-spiced"
            },
            "keto_compatibility": {
                "status": "HIGHLY COMPATIBLE",
                "reason": "Keto diet aligns with Kapha's need for light, warm, stimulating food",
                "if_attempting": [
                    "Emphasize lean proteins",
                    "Include plenty of vegetables",
                    "Use spices generously",
                    "Maintain intermittent fasting",
                    "Stay hydrated with warm water"
                ],
                "better_alternative": "Ayurvedic Kapha-reducing diet with keto principles"
            },
            "veg_nonveg": {
                "vegetarian": "Recommended with caution",
                "recommended_veg": [
                    "Legumes and beans",
                    "Light dairy (goat milk)",
                    "Small amounts of ghee",
                    "Bitter vegetables"
                ],
                "non_vegetarian": "Acceptable in moderation",
                "if_nonveg": [
                    "Lean chicken",
                    "Fish",
                    "Egg whites",
                    "Avoid: Red meat, pork, heavy meats"
                ],
                "protein_timing": "Lunch and occasionally breakfast"
            },
            "meal_timing": {
                "breakfast": "6-7 AM: Light protein or skipped (if fasting)",
                "lunch": "12-1 PM: Main meal - light grains, vegetables, protein",
                "dinner": "5-6 PM: Very light - soup or steamed vegetables",
                "snacks": "Minimal, only if truly hungry"
            }
        }
    }
    
    rec = dosha_recommendations[main_dosha]
    
    # Create tabs for Exercise, Fasting, and Diet
    tab1, tab2, tab3, tab4 = st.tabs(["💪 Exercise", "⏳ Fasting", "🥗 Diet Philosophy", "📊 Detailed Guidelines"])
    
    with tab1:
        st.markdown("#### 🏃 **Exercise Recommendations**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Type & Intensity:**")
            st.success(f"**Type:** {rec['exercise']['type']}")
            st.info(f"**Intensity:** {rec['exercise']['intensity']}")
            st.info(f"**Duration:** {rec['exercise']['duration']}")
            st.info(f"**Frequency:** {rec['exercise']['frequency']}")
            st.success(f"**Best Time:** {rec['exercise']['best_time']}")
            
            st.markdown("**Benefits:**")
            st.info(rec['exercise']['benefits'])
        
        with col2:
            st.markdown("**Recommended Activities:**")
            for activity in rec['exercise']['recommended']:
                st.markdown(f"• {activity}")
            
            st.markdown("**Activities to Avoid:**")
            for activity in rec['exercise']['avoid']:
                st.warning(f"• {activity}")
            
            st.markdown("**Caution:**")
            st.error(rec['exercise']['caution'])
    
    with tab2:
        st.markdown("#### ⏳ **Fasting Guidelines**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Fasting Compatibility:**")
            if main_dosha == "Vata":
                st.error(f"**{rec['fasting']['recommended']}**")
            elif main_dosha == "Pitta":
                st.success(f"**{rec['fasting']['recommended']}**")
            else:  # Kapha
                st.success(f"**{rec['fasting']['recommended']}**")
            
            st.info(f"**Schedule:** {rec['fasting']['schedule']}")
            st.info(f"**Duration:** {rec['fasting']['duration']}")
            st.info(f"**Frequency:** {rec['fasting']['frequency']}")
            
            st.markdown("**Best Fasting Types:**")
            for ft in rec['fasting']['best_type']:
                st.success(f"• {ft}")
            
            st.markdown("**Benefits:**")
            st.info(rec['fasting']['benefits'])
        
        with col2:
            st.markdown("**Fasting Methods to Avoid:**")
            for avoid in rec['fasting']['avoid']:
                st.warning(f"• {avoid}")
            
            st.markdown("**Important Warning:**")
            st.error(rec['fasting']['warning'])
            
            # Seasonal Fasting Guidance
            st.markdown("**Seasonal Considerations:**")
            if main_dosha == "Vata":
                st.info("""
                - **Spring:** Mild fasting okay
                - **Summer:** Minimal fasting
                - **Autumn:** NO fasting (Vata season)
                - **Winter:** NO fasting (Vata aggravating)
                """)
            elif main_dosha == "Pitta":
                st.info("""
                - **Spring:** Good for cleansing
                - **Summer:** EXCELLENT for cooling
                - **Autumn:** Moderate fasting
                - **Winter:** Minimal fasting
                """)
            else:  # Kapha
                st.info("""
                - **Spring:** EXCELLENT for detox
                - **Summer:** Good, but stay hydrated
                - **Autumn:** Moderate fasting
                - **Winter:** Minimal fasting
                """)
    
    with tab3:
        st.markdown("#### 🥗 **Diet Philosophy & Special Diets**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Core Diet Philosophy:**")
            for key, value in rec['diet_philosophy'].items():
                st.info(f"**{key.replace('_', ' ').title()}:** {value}")
            
            st.markdown("**Keto Diet Compatibility:**")
            if rec['keto_compatibility']['status'] == "NOT RECOMMENDED":
                st.error(f"**{rec['keto_compatibility']['status']}**")
            elif rec['keto_compatibility']['status'] == "MODERATELY COMPATIBLE":
                st.warning(f"**{rec['keto_compatibility']['status']}**")
            else:
                st.success(f"**{rec['keto_compatibility']['status']}**")
            
            st.markdown(f"**Reason:** {rec['keto_compatibility']['reason']}")
            
            if rec['keto_compatibility']['status'] != "NOT RECOMMENDED":
                st.markdown("**If Attempting Keto:**")
                for tip in rec['keto_compatibility']['if_attempting']:
                    st.info(f"• {tip}")
        
        with col2:
            st.markdown("**Vegetarian vs Non-Vegetarian:**")
            if rec['veg_nonveg']['vegetarian'] == "HIGHLY RECOMMENDED":
                st.success(f"**Vegetarian:** {rec['veg_nonveg']['vegetarian']}")
            elif rec['veg_nonveg']['vegetarian'] == "STRONGLY RECOMMENDED":
                st.success(f"**Vegetarian:** {rec['veg_nonveg']['vegetarian']}")
            else:
                st.warning(f"**Vegetarian:** {rec['veg_nonveg']['vegetarian']}")
            
            st.markdown("**Recommended Vegetarian Foods:**")
            for food in rec['veg_nonveg']['recommended_veg']:
                st.success(f"• {food}")
            
            st.markdown(f"**Non-Vegetarian:** {rec['veg_nonveg']['non_vegetarian']}")
            if rec['veg_nonveg']['non_vegetarian'] != "Avoid completely":
                st.markdown("**If Consuming Non-Veg:**")
                for item in rec['veg_nonveg']['if_nonveg']:
                    st.info(f"• {item}")
            
            st.info(f"**Protein Timing:** {rec['veg_nonveg']['protein_timing']}")
    
    with tab4:
        st.markdown("#### 📊 **Detailed Daily Guidelines**")
        
        # Meal Timing
        st.markdown("**🍽️ Ideal Meal Timing:**")
        meal_col1, meal_col2 = st.columns(2)
        
        with meal_col1:
            st.success(f"**Breakfast:** {rec['meal_timing']['breakfast']}")
            st.info(f"**Lunch:** {rec['meal_timing']['lunch']}")
        
        with meal_col2:
            st.warning(f"**Dinner:** {rec['meal_timing']['dinner']}")
            st.info(f"**Snacks:** {rec['meal_timing']['snacks']}")
        
        st.divider()
        
        # Seasonal Adjustments
        st.markdown("**🍂 Seasonal Adjustments:**")
        
        seasonal_col1, seasonal_col2, seasonal_col3 = st.columns(3)
        
        with seasonal_col1:
            st.markdown("**Spring:**")
            if main_dosha == "Kapha":
                st.error("**Kapha Aggravation Season**")
                st.info("""
                - Increase exercise
                - More fasting
                - Light, dry foods
                - Avoid dairy
                """)
            else:
                st.info("Gentle detox, lighter foods")
        
        with seasonal_col2:
            st.markdown("**Summer:**")
            if main_dosha == "Pitta":
                st.error("**Pitta Aggravation Season**")
                st.info("""
                - Cooling foods
                - Moderate exercise
                - Stay hydrated
                - Avoid sun exposure
                """)
            else:
                st.info("Stay cool, hydrated")
        
        with seasonal_col3:
            st.markdown("**Autumn/Winter:**")
            if main_dosha == "Vata":
                st.error("**Vata Aggravation Season**")
                st.info("""
                - Warm, oily foods
                - Gentle exercise
                - No fasting
                - Regular routine
                """)
            else:
                st.info("Warming foods, moderate exercise")
        
        st.divider()
        
        # Additional Tips
        st.markdown("**💡 Additional Ayurvedic Wisdom:**")
        
        tips_col1, tips_col2 = st.columns(2)
        
        with tips_col1:
            st.markdown("**For Optimal Digestion:**")
            st.info("""
            • Eat in calm environment
            • Chew food thoroughly
            • Sit for 5 minutes after meals
            • Drink warm water with meals
            • Follow food combining rules
            """)
        
        with tips_col2:
            st.markdown("**For Exercise Success:**")
            st.info("""
            • Listen to your body
            • Respect your energy levels
            • Align with natural rhythms
            • Include variety
            • Rest when needed
            """)
        
        # Warning Section
        st.markdown("**⚠️ Important Warnings:**")
        if main_dosha == "Vata":
            st.error("""
            **VATA-SPECIFIC WARNINGS:**
            1. NEVER exercise to exhaustion
            2. NEVER skip meals
            3. NEVER do prolonged fasting
            4. ALWAYS eat warm, cooked foods
            5. ALWAYS maintain regular routine
            """)
        elif main_dosha == "Pitta":
            st.error("""
            **PITTA-SPECIFIC WARNINGS:**
            1. NEVER exercise in midday heat
            2. AVOID competitive exercise
            3. DON'T overdo spicy foods
            4. BREAK fasts gently
            5. MANAGE anger during workouts
            """)
        else:  # Kapha
            st.error("""
            **KAPHA-SPECIFIC WARNINGS:**
            1. DON'T skip exercise
            2. AVOID sedentary lifestyle
            3. DON'T overeat
            4. BREAK fasts with light food
            5. AVOID cold, heavy foods
            """)

# =============================
# NEW: COMPREHENSIVE HEALTH ISSUES SECTION
# =============================
def display_health_issues_section(dosha_data, main_dosha):
    """Display comprehensive health issues from Ayurvedic perspective"""
    
    st.markdown("### 🏥 **Ayurvedic Health & Disease Prevention**")
    st.info("Understanding health vulnerabilities from the Ayurvedic perspective helps prevent imbalances before they manifest as disease.")
    
    # Comprehensive health data for each dosha
    health_data = {
        "Vata": {
            "ayurvedic_principles": {
                "root_cause": "Imbalance of Air & Ether elements leading to dryness, coldness, and irregularity",
                "primary_dhatus_affected": ["Rasa (plasma)", "Majja (bone marrow)", "Shukra/Artava (reproductive tissue)"],
                "primary_srotas_affected": ["Prana Vaha (respiratory)", "Anna Vaha (digestive)", "Purisha Vaha (elimination)"],
                "agni_state": "Variable (Vishamagni) - irregular digestive fire",
                "ama_formation": "Tends to form dry, hard ama that settles in joints and colon",
                "immunity_type": "Variable immunity, strong when balanced but weak when stressed"
            },
            "common_health_issues": {
                "nervous_system": [
                    "Anxiety, panic attacks, restlessness",
                    "Insomnia, sleep disturbances",
                    "Nervous tics, tremors, muscle spasms",
                    "Memory problems, brain fog",
                    "Sensitivity to noise and light"
                ],
                "digestive_system": [
                    "Irritable Bowel Syndrome (IBS)",
                    "Constipation, bloating, gas",
                    "Irregular appetite, malabsorption",
                    "Dry stools, fissures, hemorrhoids",
                    "Weight loss despite eating"
                ],
                "musculoskeletal": [
                    "Arthritis (especially osteoarthritis)",
                    "Joint pain, cracking joints",
                    "Dryness in joints, reduced synovial fluid",
                    "Muscle wasting, weakness",
                    "Osteoporosis, brittle bones"
                ],
                "reproductive_health": [
                    "Menstrual irregularities, scanty flow",
                    "Infertility, low sperm count",
                    "Vaginal dryness, painful intercourse",
                    "Premature ejaculation",
                    "Low libido when imbalanced"
                ],
                "other_systems": [
                    "Dry skin, eczema, psoriasis",
                    "Constipation, fissures, hemorrhoids",
                    "Tinnitus, hearing issues",
                    "Cold intolerance, poor circulation",
                    "Premature aging, wrinkles"
                ]
            },
            "prevention_strategies": {
                "daily_routine": "Strict Dinacharya (daily routine), regular meal times, early bedtime",
                "diet": "Warm, moist, oily foods; regular meals; avoid fasting",
                "lifestyle": "Minimize stress, avoid excessive travel, maintain routine",
                "seasonal_care": "Extra care in autumn and winter; oil massage daily",
                "mental_health": "Meditation, pranayama, avoid overthinking"
            },
            "ayurvedic_treatments": {
                "panchakarma": ["Basti (medicated enema)", "Nasya (nasal administration)", "Shirodhara"],
                "external_therapies": ["Abhyanga (oil massage)", "Pinda Sweda (herbal bolus)", "Padabhyanga (foot massage)"],
                "internal_medicines": ["Ashwagandha", "Bala", "Shatavari", "Dashamoola"],
                "home_remedies": ["Warm milk with ghee", "Sesame oil massage", "Ginger tea"]
            },
            "warning_signs": [
                "Weight loss without trying",
                "Chronic constipation",
                "Persistent anxiety or insomnia",
                "Joint pain worsening with cold",
                "Dry skin and hair getting worse"
            ],
            "modern_correlations": [
                "Neurodegenerative diseases (early stages)",
                "Autoimmune conditions when combined with Pitta",
                "Anxiety disorders, panic attacks",
                "Irritable Bowel Syndrome",
                "Osteoarthritis, osteoporosis"
            ]
        },
        "Pitta": {
            "ayurvedic_principles": {
                "root_cause": "Excess Fire element leading to heat, inflammation, and acidity",
                "primary_dhatus_affected": ["Rakta (blood)", "Mamsa (muscle)", "Meda (fat)"],
                "primary_srotas_affected": ["Rakta Vaha (circulatory)", "Pitta Vaha (metabolic)", "Sweda Vaha (sweat)"],
                "agni_state": "Sharp (Tikshagni) - strong but potentially excessive digestive fire",
                "ama_formation": "Forms hot, sharp ama that causes inflammation and acidity",
                "immunity_type": "Strong immunity but prone to inflammatory and autoimmune conditions"
            },
            "common_health_issues": {
                "inflammatory_conditions": [
                    "Acid reflux, GERD, ulcers",
                    "Inflammatory bowel disease",
                    "Skin inflammations (acne, rosacea, eczema)",
                    "Autoimmune disorders",
                    "Tendinitis, bursitis"
                ],
                "digestive_system": [
                    "Hyperacidity, heartburn",
                    "Inflammatory bowel conditions",
                    "Hemorrhoids (bleeding type)",
                    "Excessive hunger, rapid digestion",
                    "Food sensitivities"
                ],
                "skin_conditions": [
                    "Acne, rosacea, rashes",
                    "Hives, allergic reactions",
                    "Excessive sweating, body odor",
                    "Premature greying, hair loss",
                    "Skin cancer risk (with sun exposure)"
                ],
                "metabolic_issues": [
                    "Hypertension, high blood pressure",
                    "High cholesterol (inflammatory type)",
                    "Diabetes (inflammatory component)",
                    "Gallstones, liver issues",
                    "Metabolic syndrome"
                ],
                "other_systems": [
                    "Migraines, tension headaches",
                    "Eye inflammation, conjunctivitis",
                    "Bleeding disorders, anemia",
                    "Fever, infections (acute)",
                    "Anger issues, irritability"
                ]
            },
            "prevention_strategies": {
                "daily_routine": "Avoid midday sun, regular cooling practices",
                "diet": "Cooling foods, avoid spicy/fermented foods, eat at regular times",
                "lifestyle": "Manage stress, avoid excessive competition, practice cooling activities",
                "seasonal_care": "Extra care in summer; cooling therapies",
                "mental_health": "Meditation, forgiveness practices, anger management"
            },
            "ayurvedic_treatments": {
                "panchakarma": ["Virechana (therapeutic purgation)", "Raktamokshana (bloodletting in some cases)"],
                "external_therapies": ["Takradhara (buttermilk flow)", "Chandana Lepa (sandalwood paste)", "Sheetali baths"],
                "internal_medicines": ["Guduchi", "Amla", "Manjistha", "Shatavari"],
                "home_remedies": ["Coconut water", "Aloe vera juice", "Coriander water", "Rose water"]
            },
            "warning_signs": [
                "Persistent heartburn or acidity",
                "Skin rashes or inflammation",
                "Excessive anger or irritability",
                "Bleeding disorders",
                "Feverish feelings without infection"
            ],
            "modern_correlations": [
                "Autoimmune diseases (Lupus, Rheumatoid Arthritis)",
                "Inflammatory bowel disease",
                "Hypertension, cardiovascular disease",
                "Acne, rosacea, psoriasis",
                "GERD, peptic ulcers"
            ]
        },
        "Kapha": {
            "ayurvedic_principles": {
                "root_cause": "Excess Earth & Water elements leading to heaviness, congestion, and stagnation",
                "primary_dhatus_affected": ["Meda (fat)", "Mamsa (muscle)", "Shleshma (mucous)"],
                "primary_srotas_affected": ["Kapha Vaha (respiratory mucus)", "Meda Vaha (fat metabolism)", "Mootra Vaha (urinary)"],
                "agni_state": "Slow (Mandagni) - sluggish digestive fire",
                "ama_formation": "Forms heavy, sticky ama that causes congestion and stagnation",
                "immunity_type": "Strong immunity but prone to congestive and metabolic disorders"
            },
            "common_health_issues": {
                "respiratory_system": [
                    "Asthma, bronchitis",
                    "Sinusitis, nasal congestion",
                    "Allergies, hay fever",
                    "Sleep apnea, snoring",
                    "Excessive mucus production"
                ],
                "metabolic_disorders": [
                    "Obesity, weight gain",
                    "Diabetes mellitus type 2",
                    "High cholesterol, triglycerides",
                    "Metabolic syndrome",
                    "Hypothyroidism"
                ],
                "digestive_system": [
                    "Slow digestion, lethargy after meals",
                    "Water retention, edema",
                    "Nausea, sluggish bowels",
                    "Food sensitivities (dairy, wheat)",
                    "Gallstones (cholesterol type)"
                ],
                "joint_issues": [
                    "Osteoarthritis (with stiffness)",
                    "Joint swelling, edema",
                    "Gout (in combination with Pitta)",
                    "Reduced mobility, stiffness",
                    "Water retention in joints"
                ],
                "other_systems": [
                    "Depression, seasonal affective disorder",
                    "Lethargy, excessive sleep",
                    "Cysts, benign tumors",
                    "Swollen lymph nodes",
                    "Water retention, cellulite"
                ]
            },
            "prevention_strategies": {
                "daily_routine": "Early rising, vigorous exercise, regular fasting",
                "diet": "Light, dry, warm foods; avoid heavy meals; regular fasting",
                "lifestyle": "Active lifestyle, avoid sedentary habits, regular detox",
                "seasonal_care": "Extra care in spring; regular detoxification",
                "mental_health": "Stimulation, new experiences, avoid stagnation"
            },
            "ayurvedic_treatments": {
                "panchakarma": ["Vamana (therapeutic emesis)", "Nasya (with stimulating herbs)"],
                "external_therapies": ["Udvartana (dry powder massage)", "Swedana (herbal steam)", "Lepa (herbal pastes)"],
                "internal_medicines": ["Triphala", "Guggulu", "Punarnava", "Chitrak"],
                "home_remedies": ["Ginger tea", "Honey water", "Dry brushing", "Hot water with spices"]
            },
            "warning_signs": [
                "Unexplained weight gain",
                "Persistent congestion or mucus",
                "Excessive sleep or lethargy",
                "Water retention, swelling",
                "Depression or lack of motivation"
            ],
            "modern_correlations": [
                "Metabolic syndrome, obesity",
                "Type 2 diabetes",
                "Hypothyroidism",
                "Depression (melancholic type)",
                "Asthma, COPD, sleep apnea"
            ]
        }
    }
    
    health_rec = health_data[main_dosha]
    
    # Create tabs for different aspects of health
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧬 Ayurvedic Principles", "🩺 Common Issues", "🛡️ Prevention", "🌿 Treatments", "⚠️ Warning Signs"])
    
    with tab1:
        st.markdown("#### 🧬 **Ayurvedic Understanding of Health**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Root Cause of Imbalance:**")
            st.error(health_rec["ayurvedic_principles"]["root_cause"])
            
            st.markdown("**Primary Tissues Affected (Dhatus):**")
            for dhatu in health_rec["ayurvedic_principles"]["primary_dhatus_affected"]:
                st.info(f"• {dhatu}")
            
            st.markdown("**Digestive Fire State (Agni):**")
            st.warning(health_rec["ayurvedic_principles"]["agni_state"])
        
        with col2:
            st.markdown("**Primary Channels Affected (Srotas):**")
            for srota in health_rec["ayurvedic_principles"]["primary_srotas_affected"]:
                st.success(f"• {srota}")
            
            st.markdown("**Toxin Formation (Ama):**")
            st.error(health_rec["ayurvedic_principles"]["ama_formation"])
            
            st.markdown("**Immunity Type:**")
            st.info(health_rec["ayurvedic_principles"]["immunity_type"])
    
    with tab2:
        st.markdown("#### 🩺 **Common Health Issues by System**")
        
        # Create expanders for each system
        systems = [
            ("Nervous System" if main_dosha == "Vata" else "Inflammatory Conditions" if main_dosha == "Pitta" else "Respiratory System", 
             "nervous_system" if main_dosha == "Vata" else "inflammatory_conditions" if main_dosha == "Pitta" else "respiratory_system"),
            ("Digestive System", "digestive_system"),
            ("Musculoskeletal" if main_dosha == "Vata" else "Skin Conditions" if main_dosha == "Pitta" else "Metabolic Disorders", 
             "musculoskeletal" if main_dosha == "Vata" else "skin_conditions" if main_dosha == "Pitta" else "metabolic_disorders"),
            ("Reproductive Health" if main_dosha == "Vata" else "Metabolic Issues" if main_dosha == "Pitta" else "Joint Issues", 
             "reproductive_health" if main_dosha == "Vata" else "metabolic_issues" if main_dosha == "Pitta" else "joint_issues"),
            ("Other Systems", "other_systems")
        ]
        
        for system_name, system_key in systems:
            with st.expander(f"**{system_name}**", expanded=True):
                if system_key in health_rec["common_health_issues"]:
                    for issue in health_rec["common_health_issues"][system_key]:
                        st.markdown(f"• {issue}")
                
                # Add Ayurvedic explanation
                if system_name == "Nervous System" and main_dosha == "Vata":
                    st.caption("*Ayurvedic Insight: Vata governs the nervous system. Imbalance leads to dryness and irregularity in nerve conduction.*")
                elif system_name == "Inflammatory Conditions" and main_dosha == "Pitta":
                    st.caption("*Ayurvedic Insight: Pitta's heat and sharpness cause inflammation and tissue damage when imbalanced.*")
                elif system_name == "Respiratory System" and main_dosha == "Kapha":
                    st.caption("*Ayurvedic Insight: Kapha's heaviness and moisture accumulate in respiratory channels causing congestion.*")
    
    with tab3:
        st.markdown("#### 🛡️ **Prevention Strategies**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Daily Routine (Dinacharya):**")
            st.success(health_rec["prevention_strategies"]["daily_routine"])
            
            st.markdown("**Dietary Guidelines:**")
            st.info(health_rec["prevention_strategies"]["diet"])
            
            st.markdown("**Lifestyle Recommendations:**")
            for item in health_rec["prevention_strategies"]["lifestyle"].split("; "):
                st.markdown(f"• {item}")
        
        with col2:
            st.markdown("**Seasonal Care (Ritucharya):**")
            st.warning(health_rec["prevention_strategies"]["seasonal_care"])
            
            st.markdown("**Mental & Emotional Health:**")
            st.info(health_rec["prevention_strategies"]["mental_health"])
            
            st.markdown("**Key Prevention Principles:**")
            prevention_principles = {
                "Vata": "Maintain routine, stay warm, avoid excess stimulation",
                "Pitta": "Stay cool, avoid excessive competition, practice moderation",
                "Kapha": "Stay active, avoid stagnation, regular detox"
            }
            st.success(prevention_principles[main_dosha])
    
    with tab4:
        st.markdown("#### 🌿 **Ayurvedic Treatments & Remedies**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Panchakarma Therapies:**")
            for therapy in health_rec["ayurvedic_treatments"]["panchakarma"]:
                st.success(f"• {therapy}")
            
            st.markdown("**External Therapies:**")
            for therapy in health_rec["ayurvedic_treatments"]["external_therapies"]:
                st.info(f"• {therapy}")
            
            st.markdown("**Classic Ayurvedic Principles:**")
            st.info("""
            • Treat the root cause, not symptoms
            • Balance doshas through opposites
            • Strengthen digestive fire (Agni)
            • Eliminate toxins (Ama)
            • Nourish tissues (Dhatus)
            """)
        
        with col2:
            st.markdown("**Internal Medicines:**")
            for medicine in health_rec["ayurvedic_treatments"]["internal_medicines"]:
                st.warning(f"• {medicine}")
            
            st.markdown("**Simple Home Remedies:**")
            for remedy in health_rec["ayurvedic_treatments"]["home_remedies"]:
                st.success(f"• {remedy}")
            
            st.markdown("**When to Seek Professional Help:**")
            st.error("""
            • Symptoms persist despite home care
            • Acute pain or severe symptoms
            • Sudden weight changes
            • Persistent digestive issues
            • Chronic fatigue or depression
            """)
    
    with tab5:
        st.markdown("#### ⚠️ **Early Warning Signs & Modern Correlations**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Early Warning Signs:**")
            for sign in health_rec["warning_signs"]:
                st.error(f"• {sign}")
            
            st.markdown("**Seasonal Vulnerabilities:**")
            seasonal_vuln = {
                "Vata": "**Autumn & Winter:** Increased dryness, anxiety, joint pain",
                "Pitta": "**Summer:** Increased inflammation, acidity, skin issues",
                "Kapha": "**Spring:** Increased congestion, lethargy, weight gain"
            }
            st.warning(seasonal_vuln[main_dosha])
            
            st.markdown("**Life Stage Vulnerabilities:**")
            life_stage = {
                "Vata": "**Old Age:** Natural Vata increase - extra care needed",
                "Pitta": "**Adulthood:** Peak Pitta years - maintain balance",
                "Kapha": "**Childhood:** Natural Kapha - establish healthy habits early"
            }
            st.info(life_stage[main_dosha])
        
        with col2:
            st.markdown("**Modern Medical Correlations:**")
            for correlation in health_rec["modern_correlations"]:
                st.info(f"• {correlation}")
            
            st.markdown("**Preventive Screening Recommended:**")
            screenings = {
                "Vata": ["Bone density scans", "Neurological exams", "Colon cancer screening"],
                "Pitta": ["Skin cancer checks", "Cardiac screening", "Liver function tests"],
                "Kapha": ["Metabolic panel", "Thyroid function", "Sleep apnea evaluation"]
            }
            for screening in screenings[main_dosha]:
                st.success(f"• {screening}")
            
            st.markdown("**Ayurvedic Wisdom:**")
            wisdom = {
                "Vata": "*""Prevention is maintaining your grounding when the winds of change blow.""*",
                "Pitta": "*""Balance your inner fire - enough to transform, not enough to burn.""*",
                "Kapha": "*""Keep the waters moving, for stagnant water breeds disease.""*"
            }
            st.markdown(wisdom[main_dosha])

# =============================
# QUESTION TOGGLE COMPONENT
# =============================
def display_questions_with_toggle():
    """Display questions with horizontal minimize option and improved dark mode visibility"""
    
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
            # Wrap question in custom div for better dark mode visibility
            st.markdown(f"""
            <div class="question-container" style="margin-bottom: 20px; padding: 15px; 
                    background: rgba(255, 255, 255, 0.05); border-radius: 8px; 
                    border-left: 3px solid #8d6e63;">
                <div style="font-weight: 600; font-size: 1.1rem; color: #5d4037; 
                        margin-bottom: 10px;">{q_text}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Create custom radio buttons with better styling
            response = st.radio(
                "",  # Empty label since we already displayed it above
                options,
                key=f"q_{i}",
                index=None,
                label_visibility="collapsed"
            )
            
            if response:
                responses.append(response[0])
            st.markdown("---")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add CSS for question styling in dark mode - CLEAN VERSION
    st.markdown("""
    <style>
    /* Question container styling */
    .question-container {
        transition: all 0.3s ease;
        animation: fadeIn 0.8s ease;
    }
    
    /* Radio button styling for better visibility */
    div[data-testid="stRadio"] > div {
        background: rgba(255, 255, 255, 0.03);
        padding: 12px;
        border-radius: 8px;
        margin: 8px 0;
        transition: all 0.3s ease;
        border: 1px solid rgba(221, 221, 221, 0.2);
    }
    
    div[data-testid="stRadio"] > div:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: #4a90e2 !important;
        transform: translateX(3px);
    }
    
    /* Radio button labels - CLEAN WHITE */
    div[data-testid="stRadio"] label {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
        color: #2d2d2d !important;
        padding-left: 8px !important;
    }
    
    /* Selected radio button */
    div[data-testid="stRadio"] > div[data-testid="stRadio"] {
        border-color: #2e7d32 !important;
        background: rgba(46, 125, 50, 0.1) !important;
        box-shadow: 0 2px 8px rgba(46, 125, 50, 0.2);
    }
    
    /* Radio button circle - BRIGHT BLUE FOR VISIBILITY */
    div[data-testid="stRadio"] div[role="radiogroup"] > div:first-child {
        border-color: #4a90e2 !important;
        border-width: 2px !important;
    }
    
    div[data-testid="stRadio"] div[role="radiogroup"] > div:first-child > div:first-child {
        background-color: #4a90e2 !important;
    }
    
    /* Dark mode overrides - CLEAN HIGH-CONTRAST VERSION */
    @media (prefers-color-scheme: dark) {
        .question-container {
            background: rgba(255, 255, 255, 0.05) !important;
            border-left: 3px solid #64b5f6 !important;
        }
        
        .question-container:hover {
            background: rgba(255, 255, 255, 0.08) !important;
            border-left-color: #4fc3f7 !important;
        }
        
        .question-container div {
            color: #ffffff !important;
            font-weight: 600 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        
        /* Radio button containers in dark mode - CLEAN DARK BACKGROUND */
        div[data-testid="stRadio"] > div {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
        }
        
        div[data-testid="stRadio"] > div:hover {
            background: rgba(255, 255, 255, 0.1) !important;
            border-color: #64b5f6 !important;
            box-shadow: 0 4px 12px rgba(100, 181, 246, 0.2);
        }
        
        /* Radio button labels in dark mode - BRIGHT WHITE */
        div[data-testid="stRadio"] label {
            color: #ffffff !important;
            font-weight: 400 !important;
            text-shadow: 0 1px 2px rgba(0,0,0,0.5);
        }
        
        /* Selected option in dark mode - CLEAN GREEN */
        div[data-testid="stRadio"] > div[data-testid="stRadio"] {
            border-color: #4caf50 !important;
            background: rgba(76, 175, 80, 0.15) !important;
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.25);
        }
        
        div[data-testid="stRadio"] > div[data-testid="stRadio"] label {
            color: #ffffff !important;
            font-weight: 500 !important;
        }
        
        /* Radio button indicators - BRIGHT BLUE */
        div[data-testid="stRadio"] div[role="radiogroup"] > div:first-child {
            border-color: #64b5f6 !important;
            border-width: 2px !important;
        }
        
        div[data-testid="stRadio"] div[role="radiogroup"] > div:first-child > div:first-child {
            background-color: #64b5f6 !important;
            transform: scale(0.8);
        }
        
        /* Make the divider more visible in dark mode */
        hr {
            border-color: rgba(255, 255, 255, 0.1) !important;
            margin: 20px 0 !important;
        }
    }
    
    /* Animation for question appearance */
    @keyframes fadeInQuestion {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .question-container {
        animation: fadeInQuestion 0.5s ease;
    }
    
    /* Make sure all text has good contrast */
    .stRadio, .stMarkdown {
        color-scheme: dark light;
    }
    </style>
    """, unsafe_allow_html=True)
    
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
                <span>"Sarve Bhavantu Sukhinah"</span>
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
        
        # PDF Export Info
        st.markdown("---")
        st.markdown("### 📄 Report Export")
        st.info("""
        After completing your assessment,
        download your personalized
        Ayurvedic Prakriti Analysis
        as a beautifully formatted PDF report.
        """)
    
    # Initialize session state
    if 'assessment_complete' not in st.session_state:
        st.session_state.assessment_complete = False
    if 'validation_errors' not in st.session_state:
        st.session_state.validation_errors = []
    if 'pdf_generated' not in st.session_state:
        st.session_state.pdf_generated = False
    if 'pdf_data' not in st.session_state:
        st.session_state.pdf_data = None
    
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
            
            st.markdown("---")
            dosha_data = DOSHA_ARCHETYPES[st.session_state.main_dosha]
            
            # Header Result with animation
            st.markdown(f"## ✨ {st.session_state.user_name}, You Are:")
            st.markdown(f"# {dosha_data['symbol']} **{st.session_state.main_dosha}**")
            st.markdown(f"### _{dosha_data['title']}_")
            
            # Dosha Chart
            create_dosha_chart_streamlit(st.session_state.scores)
            
            # PDF Export Section
            st.markdown("---")
            st.markdown("### 📄 Download Your Complete Analysis")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🖨️ Generate PDF Report", type="primary", use_container_width=True):
                    with st.spinner("Creating your beautiful Ayurvedic report..."):
                        # Prepare user data for PDF
                        user_data = {
                            'name': st.session_state.user_name,
                            'birth_date': st.session_state.formatted_date,
                            'nepali_date': st.session_state.nepali_date['formatted_english']
                        }
        
                        # Generate PDF
                        pdf_output = generate_pdf_report(
                            user_data, 
                            dosha_data, 
                            st.session_state.scores, 
                            st.session_state.main_dosha
                        )
                        
                        st.session_state.pdf_data = pdf_output
                        st.session_state.pdf_generated = True
                        st.rerun()
                
            # Display PDF download link if generated
            if st.session_state.pdf_generated and st.session_state.pdf_data:
                filename = f"Ayurvedic_Prakriti_Analysis_{st.session_state.user_name.replace(' ', '_')}.pdf"
                st.markdown(create_download_link(st.session_state.pdf_data, filename), unsafe_allow_html=True)
                
                st.info("""
                **Your PDF Report Includes:**
                • Personal information and dosha analysis
                • Archetype story and personality profile
                • Physical characteristics
                • Daily rituals and routines
                • Diet and nutrition guidelines
                • Herbs and supplements recommendations
                • Sacred scents and aromatherapy
                • Health and wellness guidance
                • Ancient wisdom for your journey
                """)
            
            # Tabs for different sections - UPDATED TO INCLUDE NEW HEALTH TAB
            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([
                "📖 Story", "👁️ Body", "🧠 Personality", "🌟 Horoscope", "🧘 Daily Life", 
                "🥗 Nutrition", "🌸 Perfume", "🌿 Herbs", "💄 Beauty", "💪 Exercise & Fasting", "🏥 Health Issues"
            ])
            
            with tab1:
                # FIXED: Use dark mode compatible colors for wisdom card
                st.markdown(f"""
                <div class="wisdom-card">
                    <h3 style="color: {st.session_state.main_dosha == 'Vata' and '#8d6e63' or st.session_state.main_dosha == 'Pitta' and '#d32f2f' or '#388e3c'};">
                        Your Archetype Story
                    </h3>
                    <p style="color: #6b3e26;">{dosha_data['story']}</p>
                    <hr>
                    <p style="color: #6b3e26;"><b>Ancient Wisdom:</b> <i>"{dosha_data['ancient_quote']}"</i></p>
                    <p style="color: #6b3e26;"><b>Sanskrit Name:</b> {dosha_data['sanskrit_name']}</p>
                    <p style="color: #6b3e26;"><b>Element:</b> {dosha_data['element']}</p>
                    <p style="color: #6b3e26;"><b>Governing Planets:</b> {dosha_data['governing_planet']}</p>
                    <p style="color: #6b3e26;"><b>Season:</b> {dosha_data['season']}</p>
                    <p style="color: #6b3e26;"><b>Peak Time:</b> {dosha_data['time_of_day']}</p>
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
            
            with tab7:
                # Perfume & Scents Section
                display_perfume_section(dosha_data)
            
            with tab8:
                # NEW: Herbs & Supplements Section
                display_herbs_supplements_section(dosha_data)
            
            with tab9:
                # NEW: Beauty & Skincare Section
                display_beauty_skincare_section(dosha_data)
            
            with tab10:
                # NEW: Exercise, Fasting & Diet Section
                display_exercise_fasting_diet_section(dosha_data, st.session_state.main_dosha)
            
            with tab11:
                # NEW: Comprehensive Health Issues Section
                display_health_issues_section(dosha_data, st.session_state.main_dosha)
            
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
