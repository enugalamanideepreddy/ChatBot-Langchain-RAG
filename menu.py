import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    if st.session_state.api:
        st.sidebar.page_link("main.py", label="Home")
        st.sidebar.page_link("pages/chat.py", label="General Chatbot")
        st.sidebar.page_link("pages/rag.py", label="RAG Chatbot")
        # st.sidebar.page_link(
        #     "pages/super-admin.py",
        #     label="Manage admin access",
        #     disabled=st.session_state.role != "super-admin",
        # )


# def unauthenticated_menu():
#     # Show a navigation menu for unauthenticated users
#     st.sidebar.page_link("main.py", label="Log in")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "api" not in st.session_state or st.session_state.api is None:
        # unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "api" not in st.session_state or st.session_state.api is None:
        st.switch_page("main.py")
    menu()