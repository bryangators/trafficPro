import streamlit as st
import re
from hydralit import HydraHeadApp
from db import db_conn as oracle_db
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import altair as alt
from PIL import Image


class State(HydraHeadApp):

    def run(self):

        # logos
        l1 = Image.open('images/logo.png')
        l2 = Image.open('images/logo2.png')
        st.image(l1)
        st.sidebar.image(l2, width = 250)
        
        """
        This section is for the elements in the sidebar
        """
        # State selection
        st.sidebar.header('State', anchor=None)
        add_selectbox = st.sidebar.selectbox(
            "Select State",
            ('Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
            'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 
            'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 
            'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 
            'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'NewJersey', 
            'NewMexico', 'NewYork', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 
            'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 
            'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 
            'West Virginia', 'Wisconsin', 'Wyoming') 
        )

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

        # multiselect weather
        st.sidebar.header('Weather', anchor = None)
        add_multiselect = st.sidebar.multiselect(
            'Select Weather Condition',
            ['Rain', 'Snow', 'Partly Cloudy', 'Tornado']
        )

        # multiselect temperature
        st.sidebar.header('Temperature', anchor = None)
        add_multiselect = st.sidebar.multiselect(
            'Select Temperature',
            ['00 - 34 °F', '35 - 69 °F', '70 - 100 °F']
        )

        # multiselect time
        time = 'Time'
        st.sidebar.header(time, anchor = None)
        add_multiselect = st.sidebar.multiselect(
            'Select Time',
            ['12:00 AM - 05:59 AM', '06:00 AM - 11:59 AM', 
            '12:00 PM - 05:59 PM', '06:00 PM - 11:59 PM']
        )

        """
        This section is for the main page elements
        """
        # creates a two column layout. col1 holds the map
        # col2 holds the table
        col1, col2 = st.columns(2)
        
        with col1:
             # user input
            name = st.text_input("Enter a city name")

            # query the city input by user
            cursor = oracle_db.connection.cursor()
            sql = """SELECT * FROM city WHERE name = :city_name"""
            cursor.execute(sql, city_name = name)
            for row in cursor:
                st.text(row)
            
            l1 = 0.0
            l2 = 0.0

            # get the latitude
            latitude = """SELECT latitude FROM city WHERE name = :city_name"""
            cursor.execute(latitude, city_name = name)
            for row in cursor:
                lat = row[0]
                l1 = float(lat)
            
            # get the longitude
            longitude = """SELECT longitude FROM city WHERE name = :city_name"""
            cursor.execute(longitude, city_name = name)
            for row in cursor:
                long = row[0]
                l2 = float(long)    

            # data frame and map
            df_map = pd.DataFrame({
                'City ' : [name], 
                'lat' : [l1],
                'lon' : [l2]
            })
            st.map(df_map, zoom = 10)

        with col2:
            st.header('State Data', anchor = None)
            with st.expander("See details"):
                st.write('Add some additional text here')
                
            df_table = pd.DataFrame(
                np.random.randn(10, 5),
                columns=('col %d' % i for i in range(5))
            )
            st.table(df_table)

        # data frame and bar graph
        df_graph = pd.DataFrame({
            'State': ['Florida', 'Michigan', 'Texas', 'Arizona', 'Nevada', 
                    'NY', 'Georgia', 'Maryland', 'California', 'New Mexico'],
            'Accident Totals': [450000, 250000, 105345, 500450, 320032, 
                                75345, 350450, 320032, 145345, 600450]
        })
        chart_data = alt.Chart(df_graph).mark_bar().encode(
            x = 'State', 
            y = 'Accident Totals'
        ).properties(height = 500, title = "Bar Graph")
        st.altair_chart(chart_data, use_container_width = True)