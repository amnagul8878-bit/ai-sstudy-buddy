import streamlit as st
import os

from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Page config
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="centered"
)

# Custom CSS for chat bubbles
st.markdown("""
    <style>
    .user-msg {
        background-color: #DCF8C6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: right;
    }
    .ai-msg {
        background-color: #F1F0F0;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📚 AI Study Buddy")
st.caption("Ask anything. Learn faster.")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.session_state.memory = ConversationBufferMemory()
        st.success("Chat cleared!")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7
)

# Conversation chain
conversation = ConversationChain(
    llm=llm,
    memory=st.session_state.memory
)

# Chat input
user_input = st.chat_input("Type your question...")

if user_input:
    try:
        # Save user message
        st.session_state.chat_history.append(("user", user_input))

        # Get AI response
        response = conversation.predict(input=user_input)

        # Save AI response
        st.session_state.chat_history.append(("ai", response))

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")

# Display chat history
for role, message in st.session_state.chat_history:
    if role == "user":
        st.markdown(f'<div class="user-msg">{message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-msg">{message}</div>', unsafe_allow_html=True)
