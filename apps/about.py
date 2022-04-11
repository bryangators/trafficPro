import streamlit as st
from hydralit import HydraHeadApp
from db import db_conn as oracle_db
from PIL import Image
import textwrap
traffic = Image.open('images/traffic1.jpg')


class About(HydraHeadApp):

    def run(self):
        st.image(Image.open('images/logo_banner.png'), use_column_width = True)
        st.title("About")
        
        s = ("TrafficPro is a traffic accident data visualization tool designed for "
                "professionals in many fields from public safety to civil engineering. "
                "TrafficPro allows users to analyze trends about traffic accidents "
                "occurring in the United States from 2016-2019. "
        
                "TrafficPro integrates this accident data along with state demographic "
                "data to allow users to visualize trends in areas of interest. ")
        st.text(textwrap.fill(s, 60))
        st.image(traffic, width = 512)
