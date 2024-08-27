from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from streamlit_chat import message
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from menu import menu
from utils import extract_data

if 'api' not in st.session_state:
    st.switch_page("main.py")

# Builds Menu 
menu()

api_key = st.session_state.api

def create_vector_store(pdfs):
    splitter = RecursiveCharacterTextSplitter(chunk_size = 500,chunk_overlap = 50)
    docs = extract_data(pdfs,splitter)
    vector_db = FAISS.from_documents(docs,OpenAIEmbeddings(api_key=api_key))

    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on provided context.<context>{context}</context>/n/nQuestion : {input}""")
    llm = ChatOpenAI(api_key=api_key)
    doc_chain = create_stuff_documents_chain(llm,prompt,output_parser=StrOutputParser())

    retriever = vector_db.as_retriever()
    st.session_state.retrieval_chain = create_retrieval_chain(retriever,doc_chain,)

## Streamlit framework

st.title('RAG QnA')

if "rag_messages" not in st.session_state:
    st.session_state.rag_messages = []

# if st.session_state['rag_user_input']:
# 	for i in range(len(st.session_state['rag_user_input'])):
		
# 		# This function displays OpenAI response
# 		message(st.session_state['rag_openai_response'][i], 
# 				avatar_style="miniavs",is_user=True,
# 				key=str(i) + 'data_by_user')
		
#         # This function displays user input
# 		message(st.session_state["rag_user_input"][i], 
# 				key=str(i)+'data_from_llm',avatar_style="icons")
          
if st.session_state['rag_messages'] and len(st.session_state['rag_messages']) > 0:
    for i in range(len(st.session_state['rag_messages'])):
        if st.session_state['rag_messages'][i]['role'] == 'user':
            message(st.session_state['rag_messages'][i]['content'], 
                avatar_style="miniavs",is_user=True,
                key=str(i) + 'data_by_user')
        else:
            message(st.session_state['rag_messages'][i]['content'], 
                    key=str(i),avatar_style="icons")
            
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

        # Store the output
        st.session_state.rag_messages.append({"role": "user", "content": user_input})
        st.session_state.rag_messages.append({"role": "assistant", "content": output})
        st.rerun()
















