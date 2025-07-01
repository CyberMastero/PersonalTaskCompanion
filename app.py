import streamlit as st
import json
import os
from datetime import datetime, date
import time
from utils.task_manager import TaskManager
from utils.motivational_content import MotivationalContent
from utils.calendar_integration import CalendarIntegration
from utils.habit_tracker import HabitTracker
from utils.data_export import DataExportBackup
from utils.auth_manager import AuthManager
from components.task_display import TaskDisplay
from components.progress_tracker import ProgressTracker
from components.habit_display import HabitDisplay
from components.auth_display import AuthDisplay

# Page configuration
st.set_page_config(
    page_title="✨ Your Personal Task Companion",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for humanized design
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 30px;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .task-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 10px 0;
        border-left: 4px solid #FF6B6B;
        transition: transform 0.2s ease;
    }
    .task-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    .completed-task {
        opacity: 0.7;
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-left-color: #00b894;
    }
    .priority-high {
        border-left-color: #e17055;
    }
    .priority-medium {
        border-left-color: #fdcb6e;
    }
    .priority-low {
        border-left-color: #00b894;
    }
    .motivation-box {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .stats-container {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
    }
    .category-tag {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        margin: 2px;
    }
    .empty-state {
        text-align: center;
        padding: 40px;
        color: #636e72;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'auth_manager' not in st.session_state:
    st.session_state.auth_manager = AuthManager()
if 'auth_display' not in st.session_state:
    st.session_state.auth_display = AuthDisplay()
    st.session_state.auth_display.set_auth_manager(st.session_state.auth_manager)
if 'motivational_content' not in st.session_state:
    st.session_state.motivational_content = MotivationalContent()
if 'task_display' not in st.session_state:
    st.session_state.task_display = TaskDisplay()
if 'progress_tracker' not in st.session_state:
    st.session_state.progress_tracker = ProgressTracker()
if 'calendar_integration' not in st.session_state:
    st.session_state.calendar_integration = CalendarIntegration()
if 'habit_display' not in st.session_state:
    st.session_state.habit_display = HabitDisplay()
if 'data_export' not in st.session_state:
    st.session_state.data_export = DataExportBackup()
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "Tasks"
if 'calendar_date' not in st.session_state:
    st.session_state.calendar_date = date.today()

# Initialize user-specific managers after authentication
def initialize_user_managers():
    """Initialize user-specific data managers"""
    if st.session_state.auth_manager.is_logged_in():
        current_user = st.session_state.auth_manager.get_current_user()
        data_files = st.session_state.auth_manager.get_user_data_files(current_user)
        
        # Initialize user-specific task and habit managers
        if 'task_manager' not in st.session_state or getattr(st.session_state, 'current_user', None) != current_user:
            st.session_state.task_manager = TaskManager(data_files['tasks'])
            st.session_state.habit_tracker = HabitTracker(data_files['habits'])
            st.session_state.current_user = current_user

# Main function to control flow
def main():
    if not st.session_state.auth_manager.is_logged_in():
        st.session_state.auth_display.show_login_page()
        return

    initialize_user_managers()

    st.markdown("""
    <div class="main-header">
        <h1>✨ Your Personal Task Companion ✨</h1>
        <p>Let's make today amazing together! 🌟</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get('show_profile', False):
        st.session_state.auth_display.show_user_profile()
        if st.button("← Back to Dashboard"):
            st.session_state.show_profile = False
            st.rerun()
        return

    st.session_state.auth_display.show_header_user_info()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Tasks", "🎯 Habits", "📅 Calendar", "📊 Data", "⚙️ Settings"])

    with tab1:
        render_tasks_tab()

    with tab2:
        render_habits_tab()

    with tab3:
        render_calendar_tab()

    with tab4:
        render_data_tab()

    with tab5:
        render_settings_tab()

# ✅ RUN THE APP — THIS LINE FIXES THE BLANK SCREEN
if __name__ == "__main__":
    main()
