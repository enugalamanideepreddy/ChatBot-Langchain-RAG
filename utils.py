from io import BytesIO, StringIO
from langchain.schema.document import Document
import pandas as pd
from langchain_openai import OpenAI
from PIL import Image
from PyPDF2 import PdfReader
import requests
from menu import menu


def load_image(url, size=(300, 200)):
    response = requests.get(url, timeout=10)
    img = Image.open(BytesIO(response.content))
    return img.resize(size)


def check_openai_api_key(api_key):
    try:
        x = OpenAI(api_key=api_key)
        x.invoke(["hello"])
    except Exception:
        return False
    return True


def extract_data(uploaded_files, splitter):
    # List to hold the document objects
    documents = []
    # Process each uploaded file
    for uploaded_file in uploaded_files:

        if uploaded_file.type == "application/pdf":
            # Read the file bytes
            bytes_data = uploaded_file.read()

            # Initialize a PdfFileReader object with the BytesIO object
            pdf_file = BytesIO(bytes_data)
            pdf_reader = PdfReader(pdf_file)

            # Extract information from the PDF
            number_of_pages = len(pdf_reader.pages)

            # Read all the pages and extract text
            pdf_text = ""
            for page_num in range(number_of_pages):
                page = pdf_reader.pages[page_num]
                pdf_text += page.extract_text()

            pdf_text = pdf_text.replace("\n", " ")

            # Create a LangChain Document object
            document = Document(
                page_content=pdf_text,
                metadata={
                    "file_name": uploaded_file.name,
                    "num_pages": number_of_pages,
                },
            )
            doc = splitter.split_documents([document])

            # Add the document to the list
            documents += doc

        elif uploaded_file.type == "text/plain":
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            string_data = stringio.read()

            # Create a LangChain Document object
            document = Document(
                page_content=string_data, metadata={"file_name": uploaded_file.name}
            )
            doc = splitter.split_documents([document])

            # Add the document to the list
            documents += doc

        elif uploaded_file.type == "text/csv":
            dataframe = pd.read_csv(uploaded_file)
            # Convert the DataFrame to a string
            csv_text = dataframe.to_string(index=False, na_rep="Missing")

            # Create a LangChain Document object
            document = Document(
                page_content=csv_text, metadata={"file_name": uploaded_file.name}
            )
            doc = splitter.split_documents([document])

            # Add the document to the list
            documents += doc
    return documents


def login():
    import streamlit as st

    # Set up the Streamlit app
    st.title("Login")

    # Create the login form
    with st.form(key="login_form"):
        name = st.text_input("Name")
        api_key = st.text_input("OpenAI API Key")
        submit_button = st.form_submit_button(label="Login")

    # Process the login
    if submit_button:
        if name and api_key:
            if len(api_key) > 12:
                is_valid = check_openai_api_key(api_key)
                if is_valid:
                    st.success(f"Welcome, {name}!")
                    st.write("Your API Key is securely stored.")
                    # Here you can use the API key to authenticate with OpenAI
                    # For example, you can save the API key in session state
                    st.session_state.api = api_key

                    # Builds Menu
                    menu()
            else:
                st.error("Wrong Credentials")
        else:
            st.error("Please Enter Name and API key to Enjoy Our ChatBot Services")
