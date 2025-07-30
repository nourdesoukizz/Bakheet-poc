import streamlit as st
import sys
import os
import base64

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Page configuration
st.set_page_config(
    page_title="Demand Forecast Planner - SEELOZ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Function to load and encode SVG
def load_svg(file_path):
    """Load SVG file and return as base64 encoded string"""
    try:
        with open(file_path, "r") as f:
            svg_content = f.read()
        return svg_content
    except:
        return None

# Initialize session state variables
def initialize_session_state():
    """Initialize all session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'auth'
    
    if 'username' not in st.session_state:
        st.session_state.username = ''
    
    if 'forecast_data' not in st.session_state:
        st.session_state.forecast_data = None

# Authentication credentials (hardcoded for demo)
VALID_USERNAME = "admin"
VALID_PASSWORD = "demo123"

def authenticate(username: str, password: str) -> bool:
    """Authenticate user with hardcoded credentials"""
    return username == VALID_USERNAME and password == VALID_PASSWORD

def show_authentication_page():
    """Display the beautiful authentication/login page"""
    
    # Load SEELOZ logo
    logo_svg = load_svg("assets/seeloz.svg")
    
    # Custom CSS for the login page
    st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Full screen background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Neural network animation CSS */
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        33% { transform: translateY(-10px) rotate(2deg); }
        66% { transform: translateY(5px) rotate(-1deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }
    
    @keyframes pulse {
        0% { opacity: 0.4; }
        50% { opacity: 0.8; }
        100% { opacity: 0.4; }
    }
    
    .neural-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        overflow: hidden;
    }
    
    .neural-node {
        position: absolute;
        width: 8px;
        height: 8px;
        background: rgba(255, 255, 255, 0.6);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite, pulse 3s ease-in-out infinite;
    }
    
    .neural-connection {
        position: absolute;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: pulse 4s ease-in-out infinite;
    }
    
    /* Login container */
    .login-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 3rem;
        margin: 2rem auto;
        max-width: 500px;
        position: relative;
        z-index: 1;
    }
    
    .logo-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .logo-container svg {
        width: 200px;
        height: auto;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
    }
    
    .title-text {
        background: linear-gradient(135deg, #4460ef, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
    }
    
    .subtitle-text {
        color: #666;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Form styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e1e5e9;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4460ef;
        box-shadow: 0 0 0 3px rgba(68, 96, 239, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4460ef, #764ba2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(68, 96, 239, 0.3);
    }
    
    .demo-credentials {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1.5rem;
        border-left: 4px solid #4460ef;
    }
    
    .ai-badge {
        display: inline-block;
        background: linear-gradient(135deg, #4460ef, #764ba2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Neural network background
    st.markdown("""
    <div class="neural-bg">
        <div class="neural-node" style="top: 10%; left: 15%; animation-delay: 0s;"></div>
        <div class="neural-node" style="top: 20%; left: 80%; animation-delay: 1s;"></div>
        <div class="neural-node" style="top: 30%; left: 25%; animation-delay: 2s;"></div>
        <div class="neural-node" style="top: 45%; left: 70%; animation-delay: 0.5s;"></div>
        <div class="neural-node" style="top: 60%; left: 30%; animation-delay: 1.5s;"></div>
        <div class="neural-node" style="top: 75%; left: 85%; animation-delay: 3s;"></div>
        <div class="neural-node" style="top: 80%; left: 20%; animation-delay: 2.5s;"></div>
        
        <div class="neural-connection" style="top: 15%; left: 20%; width: 200px; transform: rotate(45deg); animation-delay: 1s;"></div>
        <div class="neural-connection" style="top: 35%; left: 30%; width: 150px; transform: rotate(-30deg); animation-delay: 2s;"></div>
        <div class="neural-connection" style="top: 50%; left: 40%; width: 180px; transform: rotate(60deg); animation-delay: 0s;"></div>
        <div class="neural-connection" style="top: 65%; left: 25%; width: 220px; transform: rotate(-45deg); animation-delay: 1.5s;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the login container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Logo
        if logo_svg:
            st.markdown(f'<div class="logo-container">{logo_svg}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="logo-container"><h1 style="color: #4460ef;">SEELOZ</h1></div>', unsafe_allow_html=True)
        
        # AI Badge
        st.markdown('<div style="text-align: center;"><span class="ai-badge">🧠 AI-Powered Demand Forecasting</span></div>', unsafe_allow_html=True)
        
        # Title and subtitle
        st.markdown('<h1 class="title-text">Demand Forecast Planner</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle-text">Advanced Machine Learning Analytics Platform</p>', unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form"):
            st.markdown("### 🔐 Secure Access")
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            login_button = st.form_submit_button("🚀 Login to Platform")
            
            if login_button:
                if authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.current_page = 'dashboard'
                    st.success("✅ Authentication successful! Redirecting to dashboard...")
                    st.rerun()
                else:
                    st.error("❌ Access denied. Please check your credentials.")
        
        # Demo credentials
        st.markdown("""
        <div class="demo-credentials">
            <strong>🎯 Demo Access Credentials:</strong><br>
            <strong>Username:</strong> admin<br>
            <strong>Password:</strong> demo123<br>
            <small>🔒 Secure demo environment for testing</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard_page():
    """Display the main dashboard with 3 boxes and RUN button"""
    # Header
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
        <h1 style="color: #1f77b4; margin: 0;">📊 Demand Forecast Planner</h1>
        <div style="text-align: right;">
            <p style="margin: 0; color: #666;">Welcome, {}</p>
            <small style="color: #888;">SEELOZ Forecasting System</small>
        </div>
    </div>
    """.format(st.session_state.username), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main content area
    st.markdown("### Configuration")
    
    # Three information boxes in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="padding: 1.5rem; border: 2px solid #1f77b4; border-radius: 10px; text-align: center; background-color: #f8f9fa;">
            <h3 style="color: #1f77b4; margin: 0 0 0.5rem 0;">Client</h3>
            <h2 style="color: #333; margin: 0;">Bakheet</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="padding: 1.5rem; border: 2px solid #1f77b4; border-radius: 10px; text-align: center; background-color: #f8f9fa;">
            <h3 style="color: #1f77b4; margin: 0 0 0.5rem 0;">Train on Past Period</h3>
            <h2 style="color: #333; margin: 0;">5 Years</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="padding: 1.5rem; border: 2px solid #1f77b4; border-radius: 10px; text-align: center; background-color: #f8f9fa;">
            <h3 style="color: #1f77b4; margin: 0 0 0.5rem 0;">Forecast Period</h3>
            <h2 style="color: #333; margin: 0;">12 Months</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # RUN button centered below the boxes
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🚀 RUN", use_container_width=True, type="primary"):
            st.session_state.current_page = 'forecast_details'
            st.success("✅ Running forecasting algorithms...")
            st.rerun()
    
    # Logout button at the bottom
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚪 Logout", type="secondary"):
        # Clear session state
        st.session_state.authenticated = False
        st.session_state.current_page = 'auth'
        st.session_state.username = ''
        st.session_state.forecast_data = None
        st.rerun()

def show_forecast_details_page():
    """Display the detailed forecast view (placeholder for now)"""
    # Header with back button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("⬅️ Back to Dashboard"):
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    with col2:
        st.markdown("# 📈 Forecast & Model Details")
    
    st.markdown("---")
    
    # Placeholder content for now
    st.markdown("""
    <div style="padding: 2rem; border: 2px dashed #ccc; border-radius: 10px; text-align: center;">
        <h3>🚧 Forecast Details Coming Soon</h3>
        <p>This section will display:</p>
        <ul style="text-align: left; max-width: 400px; margin: 0 auto;">
            <li>Historical vs Predicted Charts</li>
            <li>Algorithm Comparison</li>
            <li>Model Analysis & Reasoning</li>
            <li>12-Month Forecast Details</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Logout button
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚪 Logout", type="secondary", key="logout_forecast"):
        st.session_state.authenticated = False
        st.session_state.current_page = 'auth'
        st.session_state.username = ''
        st.session_state.forecast_data = None
        st.rerun()

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Route to appropriate page based on authentication and current page
    if not st.session_state.authenticated:
        show_authentication_page()
    else:
        if st.session_state.current_page == 'dashboard':
            show_dashboard_page()
        elif st.session_state.current_page == 'forecast_details':
            show_forecast_details_page()
        else:
            # Default to dashboard if unknown page
            st.session_state.current_page = 'dashboard'
            st.rerun()

if __name__ == "__main__":
    main()