
import json
import streamlit as st

from orchestrator import route_request, generate_natural_response
from tools.banking_api import get_customer, get_balance

st.set_page_config(
    page_title="Wrench Wise Banking AI",
    page_icon="🏦",
    layout="wide",
)

st.title("🏦 Banking AI Assistant")
st.subheader("Multi-Agent Banking System")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Specialized Agents", "3")
col2.metric("Banking API", "Simulated")
col3.metric("Database", "SQLite")
col4.metric("AI Model", "Gemini")
st.caption("Wrench Wise | Multi-Agent Banking Architecture")
st.info(
    "Demo environment only. All customer and transaction data is fictional."
)

# Sidebar
with st.sidebar:
    st.header("Demo Controls")

    customer_id = st.selectbox(
        "Select demo customer",
        ["C1001", "C1002", "C1003"],
    )

    customer = get_customer(customer_id)

    st.divider()
    st.subheader("Customer Profile")

    if customer:
        st.write(f"**Name:** {customer['name']}")
        st.write(f"**Customer ID:** {customer['customer_id']}")
        st.metric(
            "Account Balance",
            f"₹{customer['balance']:,.2f}",
        )
        st.metric("Credit Score", customer["credit_score"])
    else:
        st.error("Customer not found.")

    st.divider()
    st.subheader("Available Agents")
    st.write("🏦 Banking Agent")
    st.write("🛡️ Risk/Fraud Agent")
    st.write("💳 Credit/Loan Agent")

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("result"):
            with st.expander("View agent execution details"):
                st.json(message["result"])

# Chat input
user_input = st.chat_input(
    "Ask about balances, transactions, fraud or loans..."
)

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Supervisor is routing your request..."):
            try:
                result = route_request(
                    user_input,
                    default_customer_id=customer_id,
                )
                answer = generate_natural_response(user_input, result) 
                agent_name = result.get("agent", "Supervisor")
                st.caption(f"🤖 Agent selected: {agent_name}") 

                st.markdown(answer)
                with st.expander("View agent execution details"):
                    st.json(result)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "result": result,
                })

                st.markdown(answer)

                with st.expander("View agent execution details"):
                    st.json(result)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "result": result,
                })

            except Exception as error:
                answer = (
                    "Something went wrong while processing your request. "
                    "Please check the application logs."
                )
                st.error(answer)
                print("Application error:", error)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                })
