import streamlit as st
from hydralit import HydraHeadApp


class Contact(HydraHeadApp):

    def run(self):
        st.title("Contact")
        # this is where code for page will be