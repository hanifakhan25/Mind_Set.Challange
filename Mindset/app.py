import streamlit as st
import random
import datetime
import pandas as pd
import json
import os

# Motivational Quotes
QUOTES = [
    "Failure is simply the opportunity to begin again, this time more intelligently. – Henry Ford",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. – Winston Churchill",
    "Hardships often prepare ordinary people for an extraordinary destiny. – C.S. Lewis",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "Your limitation—it's only your imagination."
]

# File paths
REFLECTIONS_FILE = "reflections.csv"
PROGRESS_FILE = "progress.json"

# Function to get a daily quote
def get_daily_quote():
    """Get a new quote only once per day."""
    today = datetime.date.today().isoformat()
    if "quote" not in st.session_state or st.session_state.get("quote_date") != today:
        st.session_state["quote"] = random.choice(QUOTES)
        st.session_state["quote_date"] = today
    return st.session_state["quote"]

# Function to save user reflection
def save_reflection(reflection):
    """Save the user's reflection to a CSV file."""
    new_entry = pd.DataFrame([[datetime.datetime.now().isoformat(), reflection]], columns=["timestamp", "reflection"])
    if os.path.exists(REFLECTIONS_FILE):
        df = pd.read_csv(REFLECTIONS_FILE)
        df = pd.concat([df, new_entry], ignore_index=True)
    else:
        df = new_entry
    df.to_csv(REFLECTIONS_FILE, index=False)

# Function to save progress
def save_progress(progress):
    """Save progress data to a JSON file."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as file:
            data = json.load(file)
    else:
        data = []
    data.append({"date": datetime.date.today().isoformat(), "progress": progress})
    with open(PROGRESS_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Function to load progress history
def load_past_progress():
    """Load progress history from the JSON file."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as file:
            return json.load(file)
    return []

# Main function
def main():
    # Set page config
    st.set_page_config(
        page_title="Growth Mindset Challenge",
        page_icon="🚀",
        layout="centered"
    )

    # Apply custom CSS
    st.markdown("""
        <style>
            /* General Styling */
            body {
                font-family: 'Arial', sans-serif;
                background-color: #121212;
                color: #ffffff;
            }
            .header {
                text-align: center;
                padding: 20px;
                background: linear-gradient(135deg, #6a11cb, #2575fc);
                color: white;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            .header h1 {
                font-size: 2.5rem;
                margin: 0;
            }
            .header p {
                font-size: 1.2rem;
                margin: 0;
            }
            .quote-card {
                background: #1e1e1e;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                margin-bottom: 20px;
            }
            .quote-card p {
                font-style: italic;
                color: #ffffff;
                margin: 0;
            }
            .progress-bar {
                width: 100%;
                background-color: #333333;
                border-radius: 10px;
                overflow: hidden;
                margin-bottom: 10px;
            }
            .progress-fill {
                height: 10px;
                background: linear-gradient(135deg, #6a11cb, #2575fc);
                border-radius: 10px;
            }
            .progress-text {
                text-align: center;
                font-size: 1.1rem;
                color: #ffffff;
            }
            .time-card {
                background: #1e1e1e;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                text-align: center;
                margin-bottom: 20px;
            }
            .time-card p {
                font-size: 1.2rem;
                color: #ffffff;
                margin: 0;
            }
            .footer {
                text-align: center;
                padding: 20px;
                background: linear-gradient(135deg, #6a11cb, #2575fc);
                color: white;
                border-radius: 10px;
                margin-top: 20px;
            }
            .footer p {
                font-size: 1.1rem;
                margin: 0;
            }
            .stButton button {
                background: linear-gradient(135deg, #6a11cb, #2575fc);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 1rem;
            }
            .stButton button:hover {
                background: linear-gradient(135deg, #2575fc, #6a11cb);
            }
        </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown(
        """
        <div class="header">
            <h1> ThriveHub 🌱"</h1>
            <p>Develop a mindset that thrives on challenges and effort!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Display Random Motivational Quote
    st.markdown("### Fuel for Your Soul ✨🔥")
    quote = get_daily_quote()
    st.markdown(
        f"""
        <div class="quote-card">
            <p>{quote}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # User Reflection Input
    st.markdown("### 📝Unfold Your Growth Story ✨")
    user_reflection = st.text_area(
        "What challenges did you overcome recently and what did you learn from them?",
        placeholder="Write your thoughts here..."
    )

    if st.button("Submit Reflection", key="submit_button"):
        if user_reflection:
            save_reflection(user_reflection)
            st.success("Thank you for sharing! Keep growing! 🌱")
        else:
            st.warning("Please write something before submitting.")

    # Progress Tracking
    st.markdown("### 📈 Chart Your Growth Journey")
    progress = st.slider(
        "How much do you feel you've grown this week?",
        0, 100, 50,
        key="progress_slider"
    )
    st.markdown(
        f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress}%;"></div>
        </div>
        <p class="progress-text">Your growth mindset progress: {progress}%</p>
        """,
        unsafe_allow_html=True
    )

    if st.button("Save Progress", key="save_progress_button"):
        save_progress(progress)
        st.success("Your progress has been saved! 📈")

    # Show Progress History
    st.markdown("### 📜 Your Growth Timeline")
    past_progress = load_past_progress()
    if past_progress:
        df_progress = pd.DataFrame(past_progress)
        st.line_chart(df_progress.set_index("date"))
    else:
        st.write("No progress data available yet.")

    # Show Current Date & Time
    st.markdown("### ⏳ Today's Date & Time")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(
        f"""
        <div class="time-card">
            <p>{current_time}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div class="footer">
            <p>🚀 Keep pushing forward and embrace the power of a Growth Mindset!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()