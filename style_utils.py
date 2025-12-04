import streamlit as st

def load_global_css():
    """
    Injects the global CSS to customize the app's appearance.
    """
    st.markdown("""
<style>
    /* --- 1. IMPORT A CUSTOM FONT --- */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    /* --- 2. CSS KEYFRAME ANIMATIONS --- */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0px); opacity: 1; }
    }

    /* --- 3. RESET ALL FONTS --- */
    /* Limit the global font reset to avoid overriding Streamlit internal layout classes
       which can cause layout issues (overlapping text). Avoid targeting [class*="st-"]
       as it is too broad. */
    html, body, .st-emotion-cache-1jicfl2, h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
    }

    /* --- 4. HIDE STREAMLIT DEFAULTS --- */
    /* Keep the header visible so the sidebar toggle and page navigation remain accessible.
       Only hide the toolbar and footer which are safe to remove. */
    footer, [data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* --- 5. STYLE THE MAIN PAGE & BODY --- */
    body {
        background-color: #000000;
        background-image: radial-gradient(circle at 20% 20%, #0a0a0f 0%, #1a1a24 50%, #000000 100%);
        background-attachment: fixed;
    }
    [data-testid="block-container"] {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
        background-color: rgba(14, 17, 23, 0.8);
        border-radius: 15px;
        backdrop-filter: blur(5px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        /* Apply entry animation to the main container */
        animation: fadeIn 1s ease-out;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(26, 26, 36, 0.8) !important;
        backdrop-filter: blur(5px);
    }

    /* --- 6. CUSTOM "BACK TO HOME" BUTTON --- */
    .back-button {
        display: inline-block;
        padding: 8px 16px;
        background-color: #f63366;
        color: #FFFFFF !important;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        animation: fadeIn 1s ease-out 0.5s; /* Delayed fade in */
        animation-fill-mode: backwards;
    }
    .back-button:hover {
        background-color: #d62254;
        color: #FFFFFF !important;
        text-decoration: none;
        transform: scale(1.05);
    }
    
    /* --- 7. LOTTIE / SPINNER STYLES --- */
    /* This centers the Lottie spinner */
    .stSpinner {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }

    /* --- 8. HOME PAGE CARD STYLES --- */
    .card-link {
        display: block;
        text-decoration: none;
        /* Apply slide-up animation to cards */
        animation: slideUp 0.8s ease-out;
    }
    /* Add staggered animation delay */
    .card-col-1 { animation-delay: 0.2s; animation-fill-mode: backwards; }
    .card-col-2 { animation-delay: 0.4s; animation-fill-mode: backwards; }

    .card {
        border: 2px solid #262730;
        border-radius: 15px;
        padding: 25px;
        background-color: #0E1117;
        box-shadow: 0 4px 10px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        height: 380px;
        color: #FAFAFA;
    }
    .card:hover {
        transform: translateY(-10px);
        box-shadow: 0 12px 24px 0 rgba(246, 51, 102, 0.2);
        border-color: #f63366;
    }
    .card-header { 
        font-size: 28px;
        font-weight: 600;
        color: #f63366;
        margin-bottom: 20px;
    }
    .card-text {
        font-size: 16px;
        line-height: 1.7;
    }
    .card-text ul { padding-left: 20px; }
    
    /* --- 9. GLOBAL TITLE STYLES (WITH ANIMATION) --- */
    h1 {
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        padding-bottom: 0.5rem;
        animation: slideUp 0.6s ease-out;
    }
    h3 {
        font-size: 1.5rem !important;
        font-weight: 400 !important;
        color: #FAFAFA !important;
        animation: slideUp 0.7s ease-out;
    }
    hr {
        background-color: #f63366;
        height: 2px;
        border: none;
        animation: fadeIn 1s ease-out;
    }
    
    /* --- 10. METRIC & TAB STYLES (FOR SUB-PAGES) --- */
    [data-testid="stMetric"] {
        background-color: #0E1117;
        border: 2px solid #262730;
        border-radius: 10px;
        padding: 15px;
        animation: slideUp 0.5s ease-out;
        animation-fill-mode: backwards;
    }
    [data-testid="stMetric"] label {
        font-weight: 600;
        color: #FAFAFA;
    }
    [data-testid="stMetric"] p {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #f63366;
    }
    
    /* Style for tabs */
    [data-testid="stTabs"] {
        animation: fadeIn 1s ease-out;
        animation-fill-mode: backwards;
    }
    /* --- 11. HEADING & TABLE FIXES TO PREVENT OVERLAP --- */
    /* Ensure headings keep normal margins/line-height so they don't overlap nearby widgets */
    h1, h2, h3 {
        margin-top: 0.5rem !important;
        margin-bottom: 0.75rem !important;
        line-height: 1.25 !important;
    }

    /* Streamlit DataFrame/Table specific fixes: keep adequate line-height and prevent
       header labels from overlapping. Use data-testid where available to scope safely. */
    [data-testid="stDataFrame"] table th, [data-testid="stDataFrame"] table td,
    .stDataFrame table th, .stDataFrame table td {
        line-height: 1.4 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        padding: 0.5rem 0.75rem !important;
    }
    
</style>
    """, unsafe_allow_html=True)