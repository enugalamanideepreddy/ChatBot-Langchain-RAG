from streamlit.testing.v1 import AppTest

# Currently Not Working
def test_AppRunning():
    """Writing Test Function. """
    at = AppTest.from_file("main.py").run()
    at.text_input[0].set_value("Testing").run()
    at.text_input[1].set_value("wrong_api").run()
    at.form_submit_button[0].click().run()
    assert at.error[0] == "Wrong Credentials"
