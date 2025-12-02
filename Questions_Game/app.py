import streamlit as st
import pandas as pd
import random as rn
import time

# Load CSV and clean column names
here = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(here, "questions.csv"))
df.columns = df.columns.str.strip()

# App title
st.markdown("<h1 style='text-align: center; color: #4B0082;'>🎲 Questions Game 🎲</h1>", unsafe_allow_html=True)
st.write("---")

# Category selection
category_selection = st.selectbox("Select Category 🎯", df["Category"].unique())

# Filter dataframe
df_filtered = df.query("Category == @category_selection")

# Initialize session state for non-repeating questions
if "remaining_questions" not in st.session_state or st.session_state.category != category_selection:
    st.session_state.category = category_selection
    st.session_state.remaining_questions = df_filtered["Question"].tolist()

# Buttons in columns
col1, col2 = st.columns(2)

with col1:
    pick_question_clicked = st.button("🎯 Pick Question")

with col2:
    reset_questions_clicked = st.button("🔄 Reset Questions")

# Reset logic
if reset_questions_clicked:
    st.session_state.remaining_questions = df_filtered["Question"].tolist()
    st.success("✅ Questions reset for this category!")

# Pick question logic
if pick_question_clicked:
    if st.session_state.remaining_questions:
        with st.spinner("Picking a great question..."):
            time.sleep(1.2)
        question = rn.choice(st.session_state.remaining_questions)
        st.session_state.remaining_questions.remove(question)

        # Display question in a full-width container below the buttons
        st.markdown(
            f"""
            <div style='
                display: flex;
                justify-content: center;
                margin-top: 20px;
            '>
                <div style='
                    width: 80%;
                    padding: 40px;
                    border-radius: 20px;
                    background-color: #E0F7FA;
                    border-left: 8px solid #00796B;
                    font-size: 26px;
                    font-weight: bold;
                    text-align: center;
                    color: black;
                    box-shadow: 2px 2px 15px rgba(0,0,0,0.2);
                '>
                    🎉 {question}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ No more questions in this category!")

# Footer
st.write("---")
st.markdown("<p style='text-align: center; color: gray;'>Made with ❤️ using Streamlit</p>", unsafe_allow_html=True)
