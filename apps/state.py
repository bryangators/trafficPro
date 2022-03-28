import streamlit as st
import re
from hydralit import HydraHeadApp
from db import db_conn as oracle_db
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import altair as alt

class State(HydraHeadApp):

    def run(self):

        # Dropdown selection
        state = 'State'
        st.sidebar.header(state, anchor=None)
        add_selectbox = st.sidebar.selectbox(
            "Select State",
            ('Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
            'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 
            'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 
            'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 
            'Missouri', 'MontanaNebraska', 'Nevada', 'NewHampshire', 'NewJersey', 
            'NewMexico', 'NewYork', 'NorthCarolina', 'NorthDakota', 'Ohio', 'Oklahoma', 
            'Oregon', 'PennsylvaniaRhodeIsland', 'SouthCarolina', 'SouthDakota', 
            'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 
            'WestVirginia', 'Wisconsin', 'Wyoming') 
        )

        # Date selection
        day = 'Accidents by Day'
        st.sidebar.header(day, anchor=None)
        add_calendar = st.sidebar.date_input(
            "Date:", datetime.date(2019, 4, 1)
        )

        # year slider
        year = 'Accidents by Year'
        st.sidebar.header(year, anchor=None)
        add_slider = st.sidebar.slider(
            'Select the range of years',
            2016, 2021, (2016, 2017)
        )

        # multiselect weather
        weather = 'Weather'
        st.sidebar.header(weather, anchor=None)
        add_multiselect = st.sidebar.multiselect(
            'Select Weather Condition',
            ['Rain', 'Snow', 'Partly Cloudy', 'Tornado']
        )

        # multiselect temperature
        temperature = 'Temperature'
        st.sidebar.header(temperature, anchor=None)
        add_multiselect = st.sidebar.multiselect(
            'Select Temperature',
            ['00 - 34 °F', '35 - 69 °F', '70 - 100 °F']
        )

        # multiselect time
        time = 'Time'
        st.sidebar.header(time, anchor=None)
        add_multiselect = st.sidebar.multiselect(
            'Select Time',
            ['12:00 AM - 05:59 AM', '06:00 AM - 11:59 AM', 
            '12:00 PM - 05:59 PM', '06:00 PM - 11:59 PM']
        )

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
        
        # updates and displays the city that matches the latitude and longitude
        df = pd.DataFrame({
            'City ' : [name], 
            'lat' : [l1],
            'lon' : [l2]
        })
        st.map(df, zoom = 10)

        #creating a sample dataframe
        #data_set = np.random.randint(1,10,(5,4))
        data_set = {
            'State': ['Florida', 'Michigan', 'Texas', 'Arizona', 'Nevada', 'NY', 'Georgia', 'Maryland', 'California', 'New Mexico'],
            'Accident Totals': [450000, 250000, 105345, 500450, 320032, 75345, 350450, 320032, 145345, 600450]
        }

        dframe = pd.DataFrame(data_set)

        #specifying the figure to plot
        chart_data = alt.Chart(dframe).mark_bar().encode(
            x = 'State', 
            y = 'Accident Totals'
        ).properties(height = 500, title = "Bar Graph")
        #plotting the figure
        st.altair_chart(chart_data, use_container_width = True)
        

    