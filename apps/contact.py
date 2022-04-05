import streamlit as st
from hydralit import HydraHeadApp
from db import db_conn as oracle_db
from PIL import Image
import textwrap
traffic = Image.open('images/banner.png')


class Contact(HydraHeadApp):
	def run(self):		
		st.title("Contact")
		st.image(traffic, width = 512)
		st.write("Contact us with any inquiries:  \n\n")			
		st.write("Jeremiah Brookes    -  j.brookes@ufl.edu ")
		st.write("Bryan Kristofferson -  bkristofferson@ufl.edu ")
		st.write("John Poulos         -  j.poulos@ufl.edu ")
		st.write("Clyde Slichter      -  cnslichter@ufl.edu ")