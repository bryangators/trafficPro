import streamlit as st
from hydralit import HydraHeadApp


class State(HydraHeadApp):

    def run(self):
        st.title("State")
        # this is where code for page will be