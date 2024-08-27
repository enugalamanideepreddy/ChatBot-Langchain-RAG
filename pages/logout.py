import streamlit as st


if 'api' in st.session_state:
    del st.session_state.api

st.switch_page('main.py')