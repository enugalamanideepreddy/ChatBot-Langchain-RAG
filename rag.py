from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from streamlit_chat import message
import streamlit as st

from utils import extract_data

## Streamlit framework

st.title('RAG QnA')

if 'rag_user_input' not in st.session_state:
	st.session_state['rag_user_input'] = []

if 'rag_openai_response' not in st.session_state:
	st.session_state['rag_openai_response'] = []


def create_vector_store(pdfs):
    splitter = RecursiveCharacterTextSplitter(chunk_size = 500,chunk_overlap = 50)
    docs = extract_data(pdfs,splitter)
    vector_db = Chroma.from_documents(docs,OpenAIEmbeddings())

    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on provided context.<context>{context}</context>/n/nQuestion : {input}""")
    llm = ChatOpenAI()
    doc_chain = create_stuff_documents_chain(llm,prompt)

    retriever = vector_db.as_retriever()
    st.session_state.retrieval_chain = create_retrieval_chain(retriever,doc_chain)

if st.session_state['rag_user_input']:
	for i in range(len(st.session_state['rag_user_input'])):
		
		# This function displays OpenAI response
		message(st.session_state['rag_openai_response'][i], 
				avatar_style="miniavs",is_user=True,
				key=str(i) + 'data_by_user')
		
        # This function displays user input
		message(st.session_state["rag_user_input"][i], 
				key=str(i)+'data_from_llm',avatar_style="icons")
            
if 'retrieval_chain' not in st.session_state:
    uploaded_files = st.file_uploader("Choose a file",type=['pdf','txt','csv'],accept_multiple_files=True)
    button = st.button('Load Embeddings')

    if button:
        if len(uploaded_files) == 0:
            st.write('Please Upload files')
        else:
            create_vector_store(uploaded_files)
            st.rerun()

else:  
    instr = 'Docs are locked and loaded'
    with st.form('chat_input_form'):
        col1, col2 = st.columns([9,1]) 
        with col1:
            user_input = st.text_input(
                instr,
                placeholder=instr,
                label_visibility='collapsed'
            )
        with col2:
            submit = st.form_submit_button('Chat')

    if user_input and submit:
        output = st.session_state.retrieval_chain.invoke({'input':user_input})['answer']
        output = output.lstrip("\n\n")

        # Store the output
        st.session_state.rag_openai_response.append(user_input)
        st.session_state.rag_user_input.append(output)
        st.rerun()
















