import streamlit as st
from hydralit import HydraHeadApp
import matplotlib.pyplot as plt
import pandas as pd
from db import db_conn as oracle_db
import ads

from io import BytesIO


class State(HydraHeadApp):

    def run(self):
        st.title("State")
        # this is where code for page will be

        cat = ["bored", "happy", "bored", "bored", "happy", "bored"]
        dog = ["happy", "happy", "happy", "happy", "bored", "bored"]
        activity = ["combing", "drinking", "feeding", "napping", "playing", "washing"]

        #st.button("button")
        # width = st.sidebar.slider("plot width", 2016, 2020, key="fred")
        # year = width
        # #width = st.sidebar.slider("year", 2016, 2020, key='interval')
        #print(width)
        #
        #height = st.sidebar.slider("plot height", 2016, 2020, key="jeff")
        # height = 1
        # #
        # fig, ax = plt.subplots(figsize=(width - (width-1), height-(height - 1)))
        # ax.plot(activity, dog, label="dog")
        # ax.plot(activity, cat, label="cat")
        # ax.legend()
        # #
        # buf = BytesIO()
        # fig.savefig(buf, format="png")
        # st.image(buf)

        year = st.sidebar.slider("year", 2016, 2020)  # 👈 this is a widget

        # count = 0
        #
        # year = st.slider('Choose a year', 2016, 2020, key=count)
        # st.write('You chose', year)
        # st.write("Will this show?")
        #
        query = f"""SELECT COUNT(ID) AS total, state_name
                    FROM "J.POULOS".accident
                    WHERE start_time IN (
                        SELECT start_time FROM "J.POULOS".accident
                        WHERE EXTRACT(year FROM start_time) = {year})
                        GROUP BY state_name
                    ORDER BY total DESC
                    FETCH FIRST 8 ROWS ONLY"""
        # st.write(query)
        # # plt.figure(figsize=(10, 6))
        plt.title('Top 8 states with most accidents')
        plt.xlabel('State', fontsize=12)
        plt.ylabel('Amount')
        plt.xticks(fontsize=6)
        plt.yticks(fontsize=8)
        #count += 1
        df = pd.read_sql(query, con=oracle_db.connection)
        #st.write(df)

        fig = plt.bar(df['STATE_NAME'], df['TOTAL'])
        st.pyplot(fig=plt)

        st.write(df)
