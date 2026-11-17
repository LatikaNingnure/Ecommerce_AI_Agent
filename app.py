
import streamlit as st
from customer_agent import customer_support

# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(
    page_title="Customer Support AI",
    page_icon="🤖",
    layout="centered"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 35px;
        font-weight: bold;
        color: #4F46E5;
    }

    .sub-title {
        text-align: center;
        color: gray;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.markdown(
    '<div class="main-title">🤖 Customer Support AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Ask about your order status or cancel an order.</div>',
    unsafe_allow_html=True
)

st.divider()

# =========================
# SESSION STATE
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# DISPLAY CHAT HISTORY
# =========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# CHAT INPUT
# =========================

question = st.chat_input("Ask your question here...")

if question:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # AI RESPONSE
    with st.chat_message("assistant"):

        with st.spinner("🤖 AI is processing your request..."):

            try:
                response = customer_support(question)

                # Extract response content
                answer = (
                    response.content
                    if hasattr(response, "content")
                    else str(response)
                )

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:

                st.error(f"Something went wrong: {str(e)}")
