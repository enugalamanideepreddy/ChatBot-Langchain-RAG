import streamlit as st
from streamlit_chat import message
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from menu import menu

menu()
if 'api' not in st.session_state:
    st.stop()
api_key = st.session_state.api

if 'chain' not in st.session_state:
    prompt = ChatPromptTemplate.from_messages(
    [
        ('system','You are helpful assistant. Please respond to the queries'),
        ('user','Question : {question}')
    ]
    )
    # prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
    st.session_state.chain = prompt | ChatOpenAI(api_key=api_key) | StrOutputParser()

st.session_state.option = st.selectbox(
   "What chatbox type you want to use?",
   options=("Type 1", "Type 2"),
   index=None,
   placeholder="ChatBot type",
   label_visibility = 'collapsed'
)

st.title("ChatBot")

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.session_state.option == 'Type 1':

    if st.session_state['messages']:
    	for i in range(len(st.session_state['messages'])):
            if st.session_state['messages'][i]['role'] == 'user':
                message(st.session_state['messages'][i]['content'], 
    				avatar_style="miniavs",is_user=True,
    				key=str(i) + 'data_by_user')
            else:
                message(st.session_state['messages'][i]['content'], 
                        key=str(i),avatar_style="icons")

    instr = 'Hi there! Enter what you want to let me know here.'

    with st.form('chat_input_form'):
        col1, col2 = st.columns([9,1]) 
        with col1:
            user_input = st.text_input(
                instr,
                placeholder=instr,
                label_visibility='collapsed'
            )
        with col2:
            submit = st.form_submit_button('🤖')

    if user_input and submit:
        output = st.session_state.chain.invoke({'question':user_input})
        output = output.lstrip("\n")

        # Store the output
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": output})
        st.rerun()

else:

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = st.session_state.chain.stream({'question': st.session_state.messages[-1]['content']},)
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})