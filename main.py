import streamlit as st
from openai import OpenAI
import os
import time

# --- Configuration ---
API_KEY = os.getenv("OPENAI_API_KEY", "")
client = OpenAI(api_key=API_KEY)

# --- Session State ---
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- Custom CSS for Simple Stylish Design ---
page_style = """
<style>
/* Main styling */
body, .stApp {
    background: linear-gradient(135deg, #1a1c3d 0%, #2d3561 100%);
    color: #e0e6ed;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Container */
.main-container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 2rem;
    background: rgba(15, 23, 42, 0.85);
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

/* Header */
.header {
    text-align: center;
    margin-bottom: 2rem;
}

.title {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(90deg, #6366f1, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.subtitle {
    color: #94a3b8;
    font-size: 1.1rem;
}

/* Chat area */
.chat-container {
    background: rgba(30, 41, 59, 0.6);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    min-height: 400px;
    max-height: 500px;
    overflow-y: auto;
}

/* Messages */
.message {
    margin-bottom: 1.5rem;
    animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.user-message {
    text-align: right;
}

.message-bubble {
    display: inline-block;
    padding: 1rem 1.5rem;
    border-radius: 18px;
    max-width: 80%;
    text-align: left;
}

.user-message .message-bubble {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
}

.bot-message .message-bubble {
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid rgba(100, 116, 139, 0.3);
}

.message-header {
    display: flex;
    align-items: center;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
    color: #94a3b8;
}

.user-message .message-header {
    justify-content: flex-end;
}

.message-avatar {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin: 0 0.5rem;
}

.user-avatar {
    background: rgba(255, 255, 255, 0.2);
}

.bot-avatar {
    background: rgba(16, 185, 129, 0.2);
}

/* Input area */
.input-container {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.text-input {
    flex: 1;
    padding: 1rem 1.5rem;
    border-radius: 12px;
    border: 1px solid rgba(100, 116, 139, 0.3);
    background: rgba(30, 41, 59, 0.6);
    color: #e2e8f0;
    font-size: 1rem;
}

.text-input:focus {
    outline: none;
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.send-button {
    padding: 1rem 2rem;
    border-radius: 12px;
    border: none;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}

.send-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4);
}

/* Examples */
.examples {
    margin-bottom: 1.5rem;
}

.examples-title {
    font-size: 1.2rem;
    margin-bottom: 1rem;
    color: #cbd5e1;
}

.example-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
}

.example-button {
    padding: 0.75rem 1rem;
    border-radius: 8px;
    border: 1px solid rgba(100, 116, 139, 0.3);
    background: rgba(30, 41, 59, 0.6);
    color: #cbd5e1;
    cursor: pointer;
    transition: all 0.2s ease;
}

.example-button:hover {
    background: rgba(99, 102, 241, 0.2);
    border-color: #6366f1;
}

/* Controls */
.controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.clear-button {
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    border: 1px solid rgba(239, 68, 68, 0.3);
    background: rgba(239, 68, 68, 0.1);
    color: #fca5a5;
    cursor: pointer;
    transition: all 0.2s ease;
}

.clear-button:hover {
    background: rgba(239, 68, 68, 0.2);
}

/* Math styling */
.math-formula {
    background: rgba(16, 185, 129, 0.1);
    border-left: 3px solid #10b981;
    padding: 0.75rem 1rem;
    margin: 1rem 0;
    border-radius: 0 8px 8px 0;
    font-family: 'Courier New', monospace;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(30, 41, 59, 0.3);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: rgba(100, 116, 139, 0.5);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(100, 116, 139, 0.8);
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: #94a3b8;
}

.empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    opacity: 0.7;
}

/* Responsive */
@media (max-width: 768px) {
    .main-container {
        margin: 1rem;
        padding: 1.5rem;
    }
    
    .title {
        font-size: 2rem;
    }
    
    .example-buttons {
        justify-content: center;
    }
}
</style>
"""

st.markdown(page_style, unsafe_allow_html=True)

# --- Main Content ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1 class="title">Math Tutor</h1>
    <p class="subtitle">Ask any math question and get step-by-step explanations</p>
</div>
""", unsafe_allow_html=True)

# Examples
st.markdown('<div class="examples">', unsafe_allow_html=True)
st.markdown('<div class="examples-title">Try these examples:</div>', unsafe_allow_html=True)

examples = [
    "Solve for x: 3x + 5 = 17",
    "Derivative of x² + 3x - 7",
    "Pythagorean theorem",
    "Area of a circle",
    "Quadratic formula"
]

cols = st.columns(len(examples))
for i, example in enumerate(examples):
    if cols[i].button(example, key=f"ex_{i}"):
        st.session_state.example_question = example

st.markdown('</div>', unsafe_allow_html=True)

# Chat container
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display messages
    if not st.session_state.messages:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🧮</div>
            <p>Start a conversation by asking a math question</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="message user-message">
                    <div class="message-header">
                        You
                        <div class="message-avatar user-avatar">👤</div>
                    </div>
                    <div class="message-bubble">{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="message bot-message">
                    <div class="message-header">
                        <div class="message-avatar bot-avatar">🤖</div>
                        Math Tutor
                    </div>
                    <div class="message-bubble">{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Input area
with st.form("chat_form", clear_on_submit=True):
    # Get example question if selected
    if "example_question" in st.session_state:
        user_input = st.text_input("Ask your math question:", value=st.session_state.example_question, key="question_input")
        del st.session_state.example_question
    else:
        user_input = st.text_input("Ask your math question:", key="question_input")
    
    submitted = st.form_submit_button("Send", use_container_width=True)

    if submitted and user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get bot response
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful math tutor. Explain solutions clearly with step-by-step reasoning. Use markdown formatting and LaTeX for formulas."},
                        {"role": "user", "content": user_input}
                    ]
                )
                answer = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"Sorry, I encountered an error: {str(e)}"
                })
        
        st.rerun()

# Controls
st.markdown('<div class="controls">', unsafe_allow_html=True)
if st.button("Clear Conversation", key="clear_btn"):
    st.session_state.messages = []
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)








































