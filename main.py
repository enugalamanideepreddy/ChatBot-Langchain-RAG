# from st_pages import Page, show_pages
import streamlit as st
from utils import load_image,login
from menu import menu

if 'api' not in st.session_state:
    login()

# Image URLs
general_image_url = "https://t4.ftcdn.net/jpg/05/47/89/79/240_F_547897906_xOyy9X2M0VuInOpsnMOjcirgyoU9T8aJ.jpg"
rag_image_url = "https://t3.ftcdn.net/jpg/07/14/91/96/240_F_714919690_PED2joeQrOzZYEoi8OfCTmjKMxQ3cKf3.jpg"

# Load and resize images
image_size = (400, 400)  # Example size (width, height)
general_image = load_image(general_image_url, image_size)
rag_image = load_image(rag_image_url, image_size)

# Set the title of the page
st.title("Welcome to Our LLM Chatbot Website")

# # Introduction section
st.header("Explore Our Chatbots")
st.write("""
Welcome to our chatbot platform. We offer two distinct chatbots:
- **General Chatbot**: A helpful assistant that responds to a wide range of general queries.
- **RAG Chatbot**: A specialized chatbot that leverages Retrieval-Augmented Generation for more accurate responses based on your decouments.
""")

# Display images and create buttons to navigate to different chatbots
col1, col2 = st.columns(2)

with col1:
    st.image(general_image, use_column_width=True)

with col2:
    st.image(rag_image, use_column_width=True)