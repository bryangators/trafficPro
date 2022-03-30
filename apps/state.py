import streamlit as st
import re
from hydralit import HydraHeadApp
from db import db_conn as oracle_db
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import altair as alt
import pydeck as pdk
from PIL import Image


class State(HydraHeadApp):

    # latitude longitude

    latitude = 0.0
    longitude = 0.0

    def state(self, name):
        match name:
            case "Alabama":
                self.latitude = 32.318230
                self.longitude = -86.902298

            case "Alaska":
                self.latitude = 66.160507
                self.longitude = -153.369141

            case "Arizona":
                self.latitude = 34.048927
                self.longitude = -111.093735

            case "Arkansas":
                self.latitude = 34.799999
                self.longitude = -92.199997

            case "California":
                self.latitude = 36.778259
                self.longitude = -119.417931

            case "Colorado":
                self.latitude = 39.113014
                self.longitude = -105.358887

            case "Connecticut":
                self.latitude = 41.599998
                self.longitude = -72.699997

            case "Delaware":
                self.latitude = 39.000000
                self.longitude = -75.500000

            case "Florida":
                self.latitude = 27.994402
                self.longitude = -81.760254

            case "Georgia":
                self.latitude = 33.247875
                self.longitude = -83.441162

            case "Idaho":
                self.latitude = 44.068203
                self.longitude = -114.742043

            case "Illinois":
                self.latitude = 40.000000
                self.longitude = -89.000000

            case "Indiana":
                self.latitude = 40.273502
                self.longitude = -86.126976

            case "Iowa":
                self.latitude = 42.032974
                self.longitude = -93.581543

            case "Kansas":
                self.latitude = 38.500000
                self.longitude = -98.000000

            case "Kentucky":
                self.latitude = 37.839333
                self.longitude = -84.270020

            case "Louisiana":
                self.latitude = 30.391830
                self.longitude = -92.329102

            case "Maine":
                self.latitude = 45.367584
                self.longitude = -68.972168

            case "Maryland":
                self.latitude = 39.045753
                self.longitude = -76.641273

            case "Massachusetts":
                self.latitude = 42.407211
                self.longitude = -71.382439

            case "Michigan":
                self.latitude = 44.182205
                self.longitude = -84.506836

            case "Minnesota":
                self.latitude = 46.392410
                self.longitude = -94.636230

            case "Mississippi":
                self.latitude = 33.000000
                self.longitude = -90.000000

            case "Missouri":
                self.latitude = 38.573936
                self.longitude = -92.603760

            case "Montana":
                self.latitude = 46.965260
                self.longitude = -109.533691

            case "Nebraska":
                self.latitude = 41.500000
                self.longitude = -100.000000

            case "Nevada":
                self.latitude = 39.876019
                self.longitude = -117.224121

            case "New Hampshire":
                self.latitude = 44.000000
                self.longitude = -71.500000

            case "New Jersey":
                self.latitude = 39.833851
                self.longitude = -74.871826

            case "New Mexico":
                self.latitude = 34.307144
                self.longitude = -106.018066

            case "New York":
                self.latitude = 43.000000
                self.longitude = -75.000000

            case "North Carolina":
                self.latitude = 35.782169
                self.longitude = -80.793457
            
            case "North Dakota":
                self.latitude = 47.650589
                self.longitude = -100.437012

            case "Ohio":
                self.latitude = 40.367474
                self.longitude = -82.996216

            case "Oklahoma":
                self.latitude = 36.084621
                self.longitude = -96.921387

            case "Oregon":
                self.latitude = 44.000000
                self.longitude = -120.500000

            case "Pennsylvania":
                self.latitude = 41.203323
                self.longitude = -77.194527

            case "Rhode Island":
                self.latitude = 41.742325
                self.longitude = -71.742332

            case "South Carolina":
                self.latitude = 33.836082
                self.longitude = -81.163727

            case "South Dakota":
                self.latitude = 44.500000
                self.longitude = -100.000000

            case "Tennessee":
                self.latitude = 35.860119
                self.longitude = -86.660156

            case "Texas":
                self.latitude = 31.000000
                self.longitude = -100.000000

            case "Utah":
                self.latitude = 39.419220
                self.longitude = -111.950684

            case "Vermont":
                self.latitude = 44.000000
                self.longitude = -72.699997

            case "Virginia":
                self.latitude = 37.926868
                self.longitude = -78.024902

            case "Washington":
                self.latitude = 47.751076
                self.longitude = -120.740135

            case "West Virginia":
                self.latitude = 39.000000
                self.longitude = -80.500000

            case "Wisconsin":
                self.latitude = 44.500000
                self.longitude = -89.500000

            case "Wyoming":
                self.latitude = 43.075970
                self.longitude = -107.290283   

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
        state_selectbox = st.sidebar.selectbox(
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

        # calls the state function. updates the map to the state selected.
        self.state(state_selectbox)

        # Date selection
        day = 'Accidents by Day'
        st.sidebar.header(day, anchor = None)
        add_calendar = st.sidebar.date_input(
            "Date:", datetime.date(2019, 4, 1)
        )

        # Year slider
        st.sidebar.header('Accidents by Year', anchor = None)
        year_slider = st.sidebar.slider(
            'Select the range of years',
            2016, 2021, (2016, 2017)
        )

        # multiselect weather
        st.sidebar.header('Weather', anchor = None)
        weather_multiselect = st.sidebar.multiselect(
            'Select Weather Condition',
            ['Rain', 'Snow', 'Partly Cloudy', 'Tornado']
        )

        # multiselect temperature
        st.sidebar.header('Temperature', anchor = None)
        temperature_multiselect = st.sidebar.multiselect(
            'Select Temperature',
            ['00 - 34 °F', '35 - 69 °F', '70 - 100 °F']
        )

        # multiselect time
        time = 'Time'
        st.sidebar.header(time, anchor = None)
        time_multiselect = st.sidebar.multiselect(
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
            city = """SELECT * FROM city WHERE name = :city_name"""
            cursor.execute(city, city_name = name)
            
            l1 = 0.0
            l2 = 0.0

            # get the latitude
            latitude = """SELECT latitude FROM city WHERE name = :city_name"""
            cursor.execute(latitude, city_name = name)
            for row in cursor:
                lat = row[0]
                self.latitude = float(lat)
            
            # get the longitude
            longitude = """SELECT longitude FROM city WHERE name = :city_name"""
            cursor.execute(longitude, city_name = name)
            for row in cursor:
                long = row[0]
                self.longitude = float(long) 

            # dataframe and map for the state.
            # this should grab the longitude and latitude and append it to
            # the dataframe. It should then update the pdk.Layer of the map 
            # with a scatterplot from the lat and long. It's not updating as expected.
            state_lat_long = """SELECT start_long, start_lat 
                                FROM "J.POULOS".Accident 
                                WHERE ROWNUM < 20 AND state_name = :state"""
            
            cursor.execute(state_lat_long, state = state_selectbox)
            df_state = pd.DataFrame(columns = ['lon', 'lat'])
            for row in cursor:
                lon = row[0]
                lat = row[1]
                temp1 = float(lon)
                temp2 = float(lat)
                df_state.append({'lon' : temp1, 'lat' : temp2}, ignore_index = True)   

            st.pydeck_chart(pdk.Deck(
                map_style = 'mapbox://styles/mapbox/light-v9',
                initial_view_state = pdk.ViewState(
                    latitude = self.latitude,
                    longitude = self.longitude,
                    zoom = 5,
                    pitch = 10,
                ),
                layers = [
                    pdk.Layer(
                        'ScatterplotLayer',
                        data = df_state,
                        get_position = '[lat, lon]',
                        radius = 200,
                        elevation_scale = 4,
                        elevation_range = [0, 1000],
                        pickable = True,
                        extruded = True,
                        get_color = '[200, 30, 0, 160]',
                        get_radius = 400,
                    ),
                ],
            ))

        # table output
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