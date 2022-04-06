from itertools import count
import streamlit as st
from hydralit import HydraHeadApp
from db import db_conn as oracle_db
import numpy as np
import pandas as pd
from PIL import Image
import pydeck as pdk
import datetime
import altair as alt


class Home(HydraHeadApp):

    # button for tuples in the database
    def dbstats(self):

        cursor = oracle_db.connection.cursor()
        st.sidebar.header('Traffic Pro Database Information', anchor = None)
        
        if st.sidebar.button('Click For Totals'):
            q1 = """SELECT COUNT(*) 
                    FROM "J.POULOS".Accident"""
            cursor.execute(q1)
            for row in cursor:
                q1t= row[0]
            
            q2 = """SELECT COUNT(*) 
                    FROM "J.POULOS".State"""
            cursor.execute(q2)
            for row in cursor:
                q2t= row[0]

            q3 = """SELECT COUNT(*) 
                    FROM "J.POULOS".State_pop"""
            cursor.execute(q3)
            for row in cursor:
                q3t= row[0]

            q4 = """SELECT COUNT(*) 
                    FROM "J.POULOS".State_fund"""
            cursor.execute(q4)
            for row in cursor:
                q4t= row[0]    

            q5 = """SELECT COUNT(*) 
                    FROM "J.POULOS".State_veh"""
            cursor.execute(q5)
            for row in cursor:
                q5t= row[0]

            q6 = """SELECT COUNT(*) 
                    FROM "J.POULOS".State_lic_drivers"""
            cursor.execute(q6)
            for row in cursor:
                q6t= row[0]    

            q7 = """SELECT COUNT(*) 
                    FROM "J.POULOS".County"""
            cursor.execute(q7)
            for row in cursor:
                q7t= row[0]   

            q8 = """SELECT COUNT(*) 
                    FROM "J.POULOS".County_pop"""
            cursor.execute(q8)
            for row in cursor:
                q8t= row[0]   

            q9 = """SELECT COUNT(*) 
                    FROM "J.POULOS".City"""
            cursor.execute(q9)
            for row in cursor:
                q9t= row[0]   

            q10 = """SELECT COUNT(*) 
                    FROM "J.POULOS".City_pop"""
            cursor.execute(q10)
            for row in cursor:
                q10t= row[0]       
            
            str1 = "Tuples in Accident table: " + str(q1t) + "\n"
            str2 = "Tuples in State table: " + str(q2t) + "\n"
            str3 = "Tuples in State_pop table: " + str(q3t) + "\n"
            str4 = "Tuples in State_fund table: " + str(q4t) + "\n"
            str5 = "Tuples in State_veh table: " + str(q5t) + "\n"
            str6 = "Tuples in State_lic_drivers table: " + str(q6t) + "\n"
            str7 = "Tuples in County: " + str(q7t) + "\n"
            str8 = "Tuples in County_pop: " + str(q8t) + "\n"
            str9 = "Tuples in City table: " + str(q9t) + "\n"
            str10 = "Tuples in City_pop table: " + str(q10t) + "\n"
        
            sum = q1t + q2t + q3t + q4t + q5t + q6t + q7t + q8t + q9t + q10t
            str11 = "\nTotal Tuples: " + str(sum) + "\n"

            st.sidebar.text_area('About', 
                str1 + str2 + str3 + str4 + str5 + 
                str6 + str7 + str8 + str9 + str10 + str11,
                height = 350
            )

    def run(self):
        cursor = oracle_db.connection.cursor()
        l1 = Image.open('images/logo.png')
        l2 = Image.open('images/logo2.png')
        st.image(l1)

        """
        This section is for the elements in the sidebar
        """
        st.sidebar.image(l2, width = 250)

        # Date selection
        day = 'Accidents by Day'
        st.sidebar.header(day, anchor = None)
        add_calendar = st.sidebar.date_input(
            "Date:", datetime.date(2019, 4, 1)
        )

        # Year slider
        st.sidebar.header('Accidents by Year', anchor = None)
        add_slider = st.sidebar.slider(
            'Select the range of years',
            2016, 2021, (2016, 2017)
        )
        
        # Weather options
        st.sidebar.header('Select Weather Conditions', anchor = None)
        w_clear = st.sidebar.checkbox('Clear')
        w_rain = st.sidebar.checkbox('Rain')
        w_snow = st.sidebar.checkbox('Snow')
        w_tornado = st.sidebar.checkbox('Tornado')

        # Temperature options
        st.sidebar.header('Select Temperature', anchor = None)
        temp1 = st.sidebar.checkbox('00 - 34 °F')
        temp2 = st.sidebar.checkbox('35 - 69 °F')
        temp3 = st.sidebar.checkbox('70 - 100 °F')

        # Time selection
        st.sidebar.header('Select Time', anchor = None)
        st.sidebar.time_input('Select Time', datetime.time(8, 45))

        self.dbstats()

        """
        This section is for the main page elements
        """
        # Data frame and map
        df = pd.DataFrame(
            np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
            columns=['lat', 'lon']
        )

        st.pydeck_chart(pdk.Deck(
            map_style = 'mapbox://styles/mapbox/light-v9',
            initial_view_state = pdk.ViewState(
                latitude = 37.0,
                longitude = -98.0,
                zoom = 3,
                pitch = 10,
            ),
            layers = [
                pdk.Layer(
                    'ScatterplotLayer',
                    data = df,
                    get_position = '[lon, lat]',
                    get_color = '[200, 30, 0, 160]',
                    get_radius = 75,
                ),
            ],
        ))

        # Data frame and bar graph
        df_graph = pd.DataFrame({
            'State': ['Florida', 'Michigan', 'Texas', 'Arizona', 'Nevada', 
                    'NY', 'Georgia', 'Maryland', 'California', 'New Mexico'],
            'Accident Totals': [450000, 250000, 105345, 500450, 320032, 
                                75345, 350450, 320032, 145345, 600450]
        })
        chart_data = alt.Chart(df_graph).mark_bar().encode(
            x = 'State', 
            y = 'Accident Totals',
            color = 'Origin:N'
        ).properties(height = 500, title = "Bar Graph").configure_range(
            category={'scheme': 'yelloworangered'}
        )
        st.altair_chart(chart_data, use_container_width = True)
        st.text_area('About', 'place holder', 
                height = 350
        )
        
        # this uses the slider variable declared at the top
        # to get the left side year of the date slider
        # it should then pass it to cursor.execute for the query.
        # currently not working as intended
        start_year = datetime.date(add_slider[0], 1, 1)
        st.write(start_year)

        year = """SELECT * 
                  FROM "J.POULOS".Accident 
                  WHERE ROWNUM < 10 AND TRUNC(start_time) >= DATE :start"""
        cursor.execute(year, start = start_year)

        #temp = """SELECT * 
                 # FROM "J.POULOS".Accident 
                  #WHERE ROWNUM < 10 AND TRUNC(start_time) >= DATE '2016-01-01'"""
        #cursor.execute(temp)
        #for row in cursor:
            #str1 = row
            #st.write(str1)