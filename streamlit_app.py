import os
import streamlit as st
import subprocess

from autogen import ConversableAgent, UserProxyAgent, config_list_from_json

# Ensure the OpenAI API key is set as an environment variable
#os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"  # Replace with your API key
# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Initialize the agent configuration
    llm_config = {
        "config_list": [{"model": "gpt-4", "api_key": openai_api_key}]
    }

    # Create the Conversable Agent and User Proxy Agent
    assistant = ConversableAgent("agent", llm_config=llm_config)
    user_proxy = UserProxyAgent("user", code_execution_config=False)

    # Streamlit interface
    st.title("Autogen Interactive Chat")

    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # User input
    user_input = st.text_input("You:", "")

    # Process user input and get agent's response
    if user_input:
        # Add user input to chat history
        st.session_state.chat_history.append(("You", user_input))

        # Generate response from assistant
        assistant_response = assistant.initiate_chat(user_proxy, message=user_input)
        
        # Add assistant's response to chat history
        st.session_state.chat_history.append(("Agent", assistant_response))

    # Display chat history
    for speaker, message in st.session_state.chat_history:
        if speaker == "You":
            st.write(f"**You:** {message}")
        else:
            st.write(f"**Agent:** {message}")
