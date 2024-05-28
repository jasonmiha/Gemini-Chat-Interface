import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

project = "gemini-explorer-424717"
vertexai.init(project = project)

config = generative_models.GenerationConfig(
    temperature=0.4
)

# Load model with Config
model = GenerativeModel(
    "gemini-pro",
    generation_config = config
)

# Create chat session
chat = model.start_chat()