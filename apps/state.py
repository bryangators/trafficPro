from sqlite3 import Cursor
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
import matplotlib.pyplot as plt
plt.style.use('default')


class State(HydraHeadApp):

    def __init__(self):
        self.years = ()
        self.day = None
        self.latitude = 29.6516
        self.longitude = -82.3248
        self.condition = ""
        self.temperature = ""
        self.location1 = ""
        self.location2 = ""
        self.state_selection = True
        self.date_selection = False
        self.time_query = pd.DataFrame()
        self.wthr_query = pd.DataFrame()
        self.temp_query = pd.DataFrame()
        self.df_location = pd.DataFrame(columns = ['lon', 'lat'])
        self.cursor = oracle_db.connection.cursor()
        self.state_name = ('Alabama', 'Arizona', 'Arkansas', 'California', 'Colorado', 
                'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Idaho', 
                'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 
                'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 
                'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 
                'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 
                'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 
                'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 
                'West Virginia', 'Wisconsin', 'Wyoming') 

    def update_state(self, name):
        match name:
            case "Alabama":
                self.latitude = 32.318230
                self.longitude = -86.902298

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
        
    def load_graph(self, location1, location2):
        # this is temporary. Put here to make sure it doesn't break when
        # when location passed in is a city. Fix later.
        if self.state_selection == True and self.date_selection == False:
            
            st.header("State Funding")
            year_where = "WHERE EXTRACT(year FROM start_time) IN ("
            loc1 = "\'" + location1 + "\'"
            loc2 = "\'" + location2 + "\'"
            
            # builds string for year query
            value = self.years[0]
            while value != self.years[1]:
                year_where += str(value) + ", "
                value += 1
            year_where += str(value) + ")"

            query1 = f"""WITH cte_funding AS(
                    SELECT sname AS state_name, year, funding
                    FROM "J.POULOS".state_fund),

                    cte_accidents AS (
                    SELECT COUNT(id) AS accidents, EXTRACT(year FROM start_time) AS year, state_name
                    FROM "J.POULOS".accident
                    {year_where}
                    GROUP BY state_name, EXTRACT(year FROM start_time))

                    SELECT * FROM cte_funding NATURAL JOIN cte_accidents
                    WHERE state_name IN ({loc1})
                    ORDER BY year"""

            query2 = f"""WITH cte_funding AS(
                    SELECT sname AS state_name, year, funding
                    FROM "J.POULOS".state_fund),

                    cte_accidents AS (
                    SELECT COUNT(id) AS accidents, EXTRACT(year FROM start_time) AS year, state_name
                    FROM "J.POULOS".accident
                    {year_where}
                    GROUP BY state_name, EXTRACT(year FROM start_time))

                    SELECT * FROM cte_funding NATURAL JOIN cte_accidents
                    WHERE state_name IN ({loc2})
                    ORDER BY year"""

            df_oracle1 = pd.read_sql(query1, con=oracle_db.connection)
            df_oracle2 = pd.read_sql(query2, con=oracle_db.connection)
            
            fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize = (5, 3))
        
            ax1.set_title('Funding')
            ax1.set_ylabel('Dollar Amount')
        
            ax2.set_title('Amount of Accidents', fontsize=12)
            ax2.set_xlabel('Year', fontsize=12)
            ax2.set_ylabel('Accidents')
            
            ax1.plot(df_oracle1['YEAR'], df_oracle1['FUNDING'])
            ax2.plot(df_oracle1['YEAR'], df_oracle1['ACCIDENTS'])
        
            for frame in [df_oracle1, df_oracle2]:
                ax1.plot(frame['YEAR'], frame['FUNDING'], label=frame['STATE_NAME'].loc[0])
                ax2.plot(frame['YEAR'], frame['ACCIDENTS'], label=frame['STATE_NAME'].loc[0])
            ax1.legend(bbox_to_anchor = (1,1), loc = "upper left")
            ax2.legend(bbox_to_anchor = (1,1), loc = "upper left")
        
            for tick in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label, ax2.title,
                        ax2.xaxis.label, ax2.yaxis.label] + ax1.get_xticklabels() +
                        ax2.get_xticklabels() + ax1.get_yticklabels() + ax2.get_yticklabels()):
                tick.set_fontsize(6)
            
            ax1.set_xticks(df_oracle1['YEAR'])
            ax2.set_xticks(df_oracle1['YEAR'])
            st.pyplot(fig=plt)
            st.write(df_oracle1)
            st.write(df_oracle2)
                
    def load_sidebar(self):
        with st.sidebar:
            st.image(Image.open('images/logo2.png'), width = 250)
            date_choice = st.radio(
                "Query by Date or Year Range",
                ("Date", "Year")
            )

            location_choice = st.radio(
                "Query by City or State",
                ("State", "City")
            )
            
            with st.form(key = 'form1'):
                if (date_choice == 'Date'):
                    # Date selection by day
                    st.header('Accidents by Day', anchor = None)
                   
                    # date selector for queries. Has correct min and max dates
                    self.day = st.date_input(
                        "Date:", datetime.datetime(2020, 12, 30), min_value=datetime.datetime(2016, 2, 8), max_value=datetime.datetime(2020, 12, 30)
                    )
                else:
                    # Year slider
                    st.header('Accidents by Year', anchor = None)
                    year_slider = st.slider(
                        'Select the range of years',
                        2016, 2021, (2016, 2017)
                    )
                    self.years = year_slider

                if (location_choice == "City"):
                    self.state_selection = False
                    st.header('City', anchor = None)
                    self.location1 = st.text_input("Enter city name 1")
                    self.location2 = st.text_input("Enter city name 2")
                   
                else:
                    # State selection
                    self.state_selection = True
                    st.header('State', anchor = None)
                    self.location1 = st.selectbox(
                        "Select State 1", self.state_name    
                    )

                    self.location2 = st.selectbox(
                        "Select State 2", self.state_name    
                    )
                    
                # multiselect weather. passes the condition to the weather function
                st.header('Weather', anchor = None)
                weather_multiselect = st.multiselect(
                    'Select Weather Condition',
                    ['Clear', 'Cloudy', 'Drizzle', 'Fair', 'Fog', 'Hail', 'Haze', 'Heavy Rain', 
                    'Light Drizzle', 'Light Freezing Drizzle', 'Light Rain', 'Light Snow', 
                    'Mostly Cloudy', 'Overcast', 'Partly Cloudy', 'Patched of Fog', 'Rain', 
                    'Scattered Clouds', 'Snow', 'Thunderstorm', 'Thunderstorms and Rain', 'Tornado']
                )
                self.weather_condition(weather_multiselect)

                # multiselect temperature
                st.header('Temperature', anchor = None)
                temperature_multiselect = st.multiselect(
                    'Select Temperature',
                    ['Temp < 00 °F', '00 - 19 °F', '20 - 39 °F', '40 - 59 °F', '60 - 79 °F', 'Temp > 80 °F']
                )
                self.temperature_condition(temperature_multiselect)

                # multiselect time
                time = 'Time'
                st.header(time, anchor = None)
                time_multiselect = st.multiselect(
                    'Select Time',
                    ['12:00 AM - 02:59 AM', '03:00 AM - 05:59 AM',
                    '06:00 AM - 08:59 AM', '09:00 AM - 11:59 AM',
                    '12:00 PM - 02:59 PM', '03:00 PM - 05:59 PM',
                    '06:00 PM - 08:59 PM', '09:00 PM - 11:59 PM']
                )
                self.time_condition(time_multiselect)
                submitted = st.form_submit_button(label='Run Query')

    def load_map(self, location):
        temp_df = pd.DataFrame()

        if(self.state_selection == True):
            temp_df = self.state_location(location)
        else:
            temp_df = self.city_location(location)
        
        st.pydeck_chart(pdk.Deck(
            map_style = 'mapbox://styles/mapbox/light-v9',
            initial_view_state = pdk.ViewState(
                latitude = self.latitude,
                longitude = self.longitude,
                height = 440,
                zoom = 5,
                pitch = 10,
            ),
            layers = [
                pdk.Layer(
                    'ScatterplotLayer',
                    data = temp_df,
                    get_position = '[lon, lat]',
                    radius = 200,
                    elevation_scale = 4,
                    elevation_range = [0, 1000],
                    pickable = True,
                    extruded = True,
                    get_color = '[200, 30, 0, 160]',
                    get_radius = 2000,
                )
            ],
        ))
    
    def city_location(self, current_city):
        temp_df = pd.DataFrame(columns = ['lon', 'lat'])
        
        # query the city input by user
        city = """SELECT * FROM city WHERE name = :city_name"""
        self.cursor.execute(city, city_name = current_city)
       
        # get the city latitude and longitude. This is to zoom the
        # the map to the location of the city
        city_coordinates = """SELECT c.latitude, c.longitude 
                              FROM "J.POULOS".city c
                              WHERE c.name = :city_name"""
        self.cursor.execute(city_coordinates, city_name = current_city)
        for row in self.cursor:
            lat = row[0]
            long = row[1]
            self.latitude = float(lat)
            self.longitude = float(long) 
        
        # get the accident latitude and longitude for the specific city. 
        # This is to update the map with a scatterplot
        city_accident_coordinates = """SELECT start_long, start_lat
                                        FROM "J.POULOS".accident a
                                        JOIN "J.POULOS".city c ON c.name = a.city_name
                                        WHERE ROWNUM < 500 AND a.city_name = :city_name"""
        
        self.cursor.execute(city_accident_coordinates, city_name = current_city)
        
        # adds the city lon and lat to the location dataframe
        i = 0
        for row in self.cursor:
            lon = row[0]
            lat = row[1]
            temp1 = float(lon)
            temp2 = float(lat)
            
            temp_df.loc[i] = [temp1, temp2]
            i += 1
     
        return temp_df

    def state_location(self, current_state):
        # updates the map location to the selected state.
        temp_df = pd.DataFrame(columns = ['lon', 'lat'])
        self.update_state(current_state)
        # dataframe and map for the state.
        # grabs the longitude and latitude and appends it to
        # the dataframe. The dataframe is passed to the scatterplot
        # layer of pydeck_chart to update the map 
        # with a scatterplot based on long and lat. This is expensive.
        # doing the entire state of Florida takes 5 minutes.
        # currently limited to 500 rows for a state for faster loading.
        state_accident_coordinates = """SELECT start_long, start_lat 
                                        FROM "J.POULOS".Accident 
                                        WHERE ROWNUM < 500 AND state_name = :state"""
        
        self.cursor.execute(state_accident_coordinates, state = current_state)
       
        # adds the state accident lon and lat to the dataframe
        i = 0
        for row in self.cursor:
            lon = row[0]
            lat = row[1]
            temp1 = float(lon)
            temp2 = float(lat)
            temp_df.loc[i] = [temp1, temp2]
            i += 1
        return temp_df

    def weather_condition(self, wthr_condition):
        # Takes all of the conditions in the wthr_condition 
        # parameter and builds a comma separted string of 
        # the conditions for the query below.
        # wthr_condition is passed in from the multiselect 
        # dropdown in the sidebar function.
        self.condition = "("
        for i in range(0, len(wthr_condition)):
            self.condition = self.condition + "\'" + str(wthr_condition[i]) + "\'"
            if not i == len(wthr_condition) - 1:
                self.condition = self.condition + ", "
        self.condition += ")"
        
        # Query for weather condition. 
        if not len(wthr_condition) == 0:
            weather = f"""SELECT city_name, condition
                        FROM "J.POULOS".Accident
                        WHERE ROWNUM < 1000 AND condition IN {self.condition} 
                        ORDER by condition ASC"""
            self.wthr_query = pd.read_sql(weather, con = oracle_db.connection)                
        
    def temperature_condition(self, temp_condition):
        # list to store the range of temperatures selected.
        # adds every selected value to the list.
        tempRange = []
        
        for i in range(0, len(temp_condition)):
            match temp_condition[i]:
                case "Temp < 00 °F":
                    tempRange.append(-100)
                    tempRange.append(-0.1)
                case "00 - 19.9 °F":
                    tempRange.append(0)
                    tempRange.append(19.9)    
                case "20 - 39.9 °F":
                    tempRange.append(20)
                    tempRange.append(39.9)
                case "40 - 59.9 °F":
                    tempRange.append(40)
                    tempRange.append(59.9) 
                case "60 - 79.9 °F":
                    tempRange.append(60)
                    tempRange.append(79.9)
                case "Temp > 80 °F":
                    tempRange.append(80) 
                    tempRange.append(200)   

        # Query for temp range condition. sorts the tempRange list
        # and grabs the lowest and highest temperature (index 0, index len - 1),
        # i.e. the temperature range we want to query
        if not len(tempRange) == 0:
            tempRange.sort()
            low = tempRange[0]
            high = tempRange[len(tempRange) - 1]
            temperature = f"""SELECT state_name, temperature
                        FROM "J.POULOS".Accident
                        WHERE ROWNUM < 1000 AND temperature >= {low} AND temperature <= {high}
                        ORDER BY temperature DESC"""       
            self.temp_query = pd.read_sql(temperature, con = oracle_db.connection)

    def time_condition(self, time_condition):
        timeRange = []
        
        # adds the selected time conditions to
        # the timeRange list.
        for i in range(0, len(time_condition)):
            match time_condition[i]:
                case "12:00 AM - 02:59 AM":
                    timeRange.append("00:00:00")
                    timeRange.append("02:59:59")
                
                case "03:00 AM - 05:59 AM":
                    timeRange.append("03:00:00")
                    timeRange.append("05:59:59") 
                
                case "06:00 AM - 08:59 AM":
                    timeRange.append("06:00:00")
                    timeRange.append("08:59:59")
               
                case "09:00 AM - 11:59 AM":
                    timeRange.append("09:00:00")
                    timeRange.append("11:59:59") 
                
                case "12:00 PM - 02:59 PM":
                    timeRange.append("12:00:00")
                    timeRange.append("14:59:59")              
                
                case "03:00 PM - 05:59 PM":
                    timeRange.append("15:00:00")
                    timeRange.append("17:59:59")    
                
                case "06:00 PM - 08:59 PM":
                    timeRange.append("18:00:00")
                    timeRange.append("20:59:59")
                
                case "09:00 PM - 11:59 PM":
                    timeRange.append("21:00:00")
                    timeRange.append("23:59:59") 
        
        # sorts the timeRange list. 
        # grabs the 0 index and last index,
        # i.e. the range of time we want
        if not len(timeRange) == 0:     
            timeRange.sort()
            start = "\'" + timeRange[0] + "\'"
            end = "\'" + timeRange[len(timeRange) - 1] + "\'" 
            
            time = f"""SELECT city_name, start_time 
                       FROM "J.POULOS".Accident
                       WHERE ROWNUM < 1000 
                       AND to_char(start_time, 'hh24:mi:ss') BETWEEN {start} AND {end}"""
            self.time_query = pd.read_sql(time, con = oracle_db.connection)

    def load_table(self):
        st.header('State Data', anchor = None)
        df_table = pd.DataFrame(
            np.random.randn(10, 5),
            columns=('col %d' % i for i in range(5))
        )
        st.table(df_table)

    def run(self):

        st.image(Image.open('images/logo_banner.png'), use_column_width = True)
        st.header("Accidents by Location")
        self.load_sidebar()

        # creates a two column layout.
        col1, col2, col3 = st.columns(3)
        with col1:
            # updates the left map to the state selected.
            self.load_map(self.location1)

        with col2:
            # updates the right map to the state selected.
            self.load_map(self.location2)
        
        with col3:
            st.text_area("Query Info", 
                         "Weather Query: \n" + str(self.wthr_query) + "\n\n"
                         "Temperature Query: \n" + str(self.temp_query) + "\n\n" + 
                         "Time Query: \n" + str(self.time_query), height = 405)  

        col4, col5 = st.columns(2) 
        with col4:                 
            self.load_graph(self.location1, self.location2)

        with col5:    
            self.load_table() 