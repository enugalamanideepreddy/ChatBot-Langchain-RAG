import streamlit as st
from streamlit_chat import message
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

if 'chain' not in st.session_state:
    prompt = ChatPromptTemplate.from_messages(
    [
        ('system','You are helpful assistant. Please respond to the queries'),
        ('user','Question : {question}')
    ]
    )
    st.session_state.chain = prompt | ChatOpenAI(api_key=st.session_state.api) | StrOutputParser()

if 'user_input' not in st.session_state:
	st.session_state['user_input'] = []

if 'openai_response' not in st.session_state:
	st.session_state['openai_response'] = []

st.title("ChatBot")

if st.session_state['user_input']:
	for i in range(len(st.session_state['user_input'])):
		
		# This function displays OpenAI response
		message(st.session_state['openai_response'][i], 
				avatar_style="miniavs",is_user=True,
				key=str(i) + 'data_by_user')
		
        # This function displays user input
		message(st.session_state["user_input"][i], 
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
        submit = st.form_submit_button('Chat')

if user_input and submit:
	output = st.session_state.chain.invoke({'question':user_input})
	output = output.lstrip("\n\n")

	# Store the output
	st.session_state.openai_response.append(user_input)
	st.session_state.user_input.append(output)
	st.rerun()