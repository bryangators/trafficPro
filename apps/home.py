import streamlit as st
from hydralit import HydraHeadApp
from db import db_conn as oracle_db

class Home(HydraHeadApp):

    def run(self):
        
        # Example code to get data from database using cursor and connection object

        st.title('Continent(s) From Encompasses table')
        cursor = oracle_db.connection.cursor()

        cursor.execute("""SELECT DISTINCT continent
                    FROM encompasses""")
        for row in cursor:
            st.text(row[0])