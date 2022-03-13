import streamlit as st
from hydralit import HydraHeadApp
from db import db_conn as oracle_db
import pandas as pd
import matplotlib.pyplot as plt
#import plotly
from io import BytesIO


class Home(HydraHeadApp):

    def run(self):
        
        # Example code to get data from database using cursor and connection object

        query = """SELECT "Country Name", "Population Density", population / Total AS Percentage 
        FROM (SELECT SUM(Population) AS Total FROM Country), 
            (SELECT Country.Name AS "Country Name", Population, Area, Population / Area AS "Population Density" 
                FROM Country
                ORDER BY "Population Density" DESC)
        WHERE ROWNUM <= 10"""
        #plt.figure(figsize=(10, 6))
        plt.title('Top 10 Countries Population Density')
        plt.xlabel('Country', fontsize=12)
        plt.ylabel('Amount')
        plt.xticks(fontsize=6)
        plt.yticks(fontsize=8)
        df_oracle = pd.read_sql(query, con=oracle_db.connection)
        st.write(df_oracle)

        #plt.rcParams({'font.size': 6})

        # fig = plt.bar(df_oracle['Country Name'], df_oracle['Population Density'])
        # st.write(fig)
        fig = plt.bar(df_oracle['Country Name'], df_oracle['Population Density'])

        #buf = BytesIO()
        #fig.savefig(buf, format="png")
        #st.image(buf)
        #fig.update_layout(width=800)
        st.pyplot(fig=plt, figsize=(6, 4))



        #fig.update_layout(width=800)
        #st.write(fig)


        #cursor.execute(query)

        #st.title('Continent(s) From Encompasses table')
        #cursor = oracle_db.connection.cursor()

        #cursor.execute(query)

