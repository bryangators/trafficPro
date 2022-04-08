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
        #state = st.text_input("Enter State: ")
        st.sidebar.header('State', anchor=None)
        state = st.sidebar.selectbox(
            "Select State",
            ('Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
             'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Idaho',
             'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
             'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
             'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
             'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma',
             'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
             'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
             'West Virginia', 'Wisconsin', 'Wyoming')
        )

        query = f"""WITH cte_funding AS(
                SELECT sname AS state_name, year, funding
                FROM "J.POULOS".state_fund),

                cte_accidents AS (
                SELECT COUNT(id) AS accidents, EXTRACT(year FROM start_time) AS year, state_name
                FROM "J.POULOS".accident
                GROUP BY state_name, EXTRACT(year FROM start_time))

                SELECT * FROM cte_funding NATURAL JOIN cte_accidents
                WHERE state_name = '{state}'
                ORDER BY year"""

        df_oracle2 = pd.read_sql(query, con=oracle_db.connection)
        st.write(df_oracle2)

        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
        ax1.set_title('Funding')
        ax1.set_ylabel('Dollar Amount')

        ax2.set_title('Amount of Accidents', fontsize=12)
        ax2.set_xlabel('Year', fontsize=12)
        ax2.set_ylabel('Accidents')
        ax2.plot(df_oracle2['YEAR'], df_oracle2['ACCIDENTS'])
        ax1.plot(df_oracle2['YEAR'], df_oracle2['FUNDING'])
        plt.subplots_adjust(bottom=0.000000000000000000001)

        for tick in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label, ax2.title,
                    ax2.xaxis.label, ax2.yaxis.label] + ax1.get_xticklabels() +
                    ax2.get_xticklabels() + ax1.get_yticklabels() + ax2.get_yticklabels()):
            tick.set_fontsize(6)
        ax2.set_xticks(df_oracle2['YEAR'])
        ax1.set_xticks(df_oracle2['YEAR'])
        st.pyplot(fig=plt)
