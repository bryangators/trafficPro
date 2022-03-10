import streamlit as st
from hydralit import HydraHeadApp
from db import db_conn as oracle_db


class About(HydraHeadApp):

    def run(self):
        st.title("About")
        # this is where code for page will be