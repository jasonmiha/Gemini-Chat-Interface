import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

# Initialize the Vertex AI project
project = "gemini-explorer-424717"
vertexai.init(project = project)

# Set the generation configuration for the model
config = generative_models.GenerationConfig(
    temperature=0.4
)

# Load the generative model with the specified configuration
model = GenerativeModel(
    "gemini-pro",
    generation_config = config
)

# Create a new chat session
chat = model.start_chat()

# Helper function to send messages and display responses in Streamlit
def llm_function(chat: ChatSession, query):
    """
    Sends a query to the model and displays the response in Streamlit.

    Parameters:
    chat (ChatSession): The chat session object.
    query (str): The user's input query.

    Returns:
    None
    """

    # Send the message to the model and get the response
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    # Display the model's response in Streamlit chat message
    with st.chat_message("model"):
        st.markdown(output)

    # Append user query and model response to the session state
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )
    st.session_state.messages.append(
        {
            "role": "model",
            "content": output
        }
    )

    # Set the title of the Streamlit app
    st.title("Gemini Explorer")

# Initialize chat history in session state if not already done
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display and load the chat history
for index, message in enumerate(st.session_state.messages):
    content = Content(
        role = message["role"],
        parts = [ Part.from_text(message["content"])]
    )

    # Display previous messages except the first one
    if index != 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Append the message content to the chat history
    chat.history.append(content)

# For initial message startup, introduce the assistant
if len(st.session_state.messages) == 0:
    initial_prompt = "Introduce yourself as ReX, an assistant powered by Google Gemini. You use emojis to be interactive"
    llm_function(chat, initial_prompt)
    
# Capture user input from Streamlit chat input box
query = st.chat_input("Gemini Explorer")

# If there is a user query, display it and send it to the model
if query:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)