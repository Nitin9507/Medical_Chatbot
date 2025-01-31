import streamlit as st
import requests

# Chatbot API URL
chat_url = "http://localhost:8080/chat/completion"

# Sidebar for Title, Description, and Input Form
st.sidebar.title("Medical Chat Bot")
st.sidebar.markdown("""
### 🌟 **About the Medical Chat Bot** 🌟

Welcome to the **Medical Chat Bot**, your personal assistant for **medical-related queries**!  
This chatbot leverages cutting-edge **AI technology** to provide:

- 🩺 **Quick medical insights**  
- 💊 **Helpful tips and advice**  
- 📚 **Answers to common health questions**  

🤖 *Ask your questions below and let the bot assist you!*  
""")

st.title("Welcome to the Medical Chat Bot")
# User Input Section in Sidebar
st.subheader("Ask a Question")
user_query = st.text_input("Enter your medical question below:")

# Main Content Area


# Processing the Query
if user_query:
    # Payload for API
    payload = {"prompt": user_query}
    # Sending request to the backend
    response = requests.post(chat_url, json=payload)
    
    # Displaying Response
    if response.status_code == 200:
        answer = response.json().get("response")
        st.write(f"### 🤖 **Chat Bot Answer:**")
        st.write(answer)
    else:
        st.error(f"Error: {response.json().get('error')}")
