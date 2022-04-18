from logging import PlaceHolder
from sqlite3 import Cursor
import streamlit as st
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
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers
import plotly.express as px
import random

class State(HydraHeadApp):

    def __init__(self):
        self.year = ()
        self.day = None
        self.day2 = None
        self.year = None
        self.weather = None
        self.time = None
        self.temp = None
        self.location_choice = None
        self.latitude = 32.3792
        self.longitude = -86.3077
        self.date_choice = ""
        self.condition = ""
        self.temperature = ""
        self.state1 = ""
        self.state2 = ""
        self.city1 = ""
        self.city2 = ""
        self.sum1 = None
        self.sum2 = None
        self.add_queries = ""
        self.state_selection = False
        self.df_location1 = pd.DataFrame()
        self.df_location1 = pd.DataFrame()
        self.time_query = pd.DataFrame()
        self.wthr_query = pd.DataFrame()
        self.temp_query = pd.DataFrame()
        self.formState1 = False
        self.formState2 = False
        self.form = False
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
        self.sql_choice = 'Hide'

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
                
    def load_sidebar(self):
        with st.sidebar:
            st.image(Image.open('images/logo2.png'), width = 250)
            self.date_choice = st.radio(
                "Query by Year or Date Range",
                ("Year", "Date")
            )

            self.location_choice = st.radio(
                "Query by State or City",
                ("State", "City")
            )
            
            with st.form(key = 'form1'):
                if (self.date_choice == "Date"):
                    st.header('Accidents by Date', anchor = None)
                    self.day = st.date_input(
                        "Date 1:", datetime.datetime(2016, 2, 8), 
                        min_value = datetime.datetime(2016, 2, 8), 
                        max_value = datetime.datetime(2020, 12, 30)
                    )

                    self.day2 = st.date_input(
                        "Date 2:", datetime.datetime(2016, 2, 8), 
                        min_value = datetime.datetime(2016, 2, 8),
                        max_value = datetime.datetime(2020, 12, 30)
                    )
                else:
                    st.header('Accidents by Year', anchor = None)
                    self.year = st.slider(
                        'Select the range of years',
                        2016, 2020, (2016, 2017)
                    )
                   
                if (self.location_choice == "City"):
                    st.header('City', anchor = None)
                    self.state_selection = True

                    self.state1 = st.selectbox("Select State 1", self.state_name)
                    self.city1 = "Montgomery"
                    self.city1 = st.text_input("Enter city name 1")
                    
                    self.state2 = st.selectbox("Select State 2", self.state_name)
                    self.city2 = "Montgomery"
                    self.city2 = st.text_input("Enter city name 2")
                   
                else:
                    # State selection
                    self.state_selection = True
                    st.header('State', anchor = None)
                    self.state1 = st.selectbox(
                        "Select State 1", self.state_name    
                    )

                    self.state2 = st.selectbox(
                        "Select State 2", self.state_name    
                    )
                    
                # multiselect weather. passes the condition to the weather function
                st.header('Weather', anchor = None)
                self.weather = st.multiselect(
                    'Select Weather Condition',
                    ['Rain', 'Snow', 'Partly Cloudy', 'Tornado', 'Clear', 'Cloudy', 'Thunderstorm', 'Hail', 'Windy', 
                    'Mostly Cloudy', 'Fair', 'Overcast', 'Scattered Clouds', 'Fog', 'Haze']
                )

                # multiselect temperature
                st.header('Temperature', anchor = None)
                self.temp = st.multiselect(
                    'Select Temperature',
                    ['Temp < 00 °F', '00 - 19 °F', '20 - 39 °F', '40 - 59 °F', '60 - 79 °F', 'Temp > 80 °F']
                )

                # multiselect time
                time = 'Time'
                st.header(time, anchor = None)
                self.time = st.multiselect(
                    'Select Time',
                    ['12:00 AM - 02:59 AM', '03:00 AM - 05:59 AM',
                    '06:00 AM - 08:59 AM', '09:00 AM - 11:59 AM',
                    '12:00 PM - 02:59 PM', '03:00 PM - 05:59 PM',
                    '06:00 PM - 08:59 PM', '09:00 PM - 11:59 PM']
                )

                st.header('State Funding', anchor = None)
                self.add_queries = st.selectbox("Select a Query", ["", "State Funding"])
                self.form = st.form_submit_button(label = 'Run Query')
        
            self.sql_choice = st.radio(
                    "Show SQL Code for Queries",
                    ("Hide", "Show")
                )

    def load_map(self, state, city):

        coordinates = pd.DataFrame()
        defaultRadius = 0
        defaultZoom = 5
        
        if(self.location_choice == "City"):
            coordinates = self.coordinates(state, city)
            defaultZoom = 8
            defaultRadius = 400
        else:
            coordinates = self.coordinates(state, "")
            defaultZoom = 5.5
            defaultRadius = 2000
        
        st.pydeck_chart(pdk.Deck(
            map_style = 'mapbox://styles/mapbox/light-v9',
            initial_view_state = pdk.ViewState(
                latitude = self.latitude,
                longitude = self.longitude,
                height = 530,
                width = 450,
                zoom = defaultZoom,
                pitch = 10,
            ),
            layers = [
                pdk.Layer(
                    'ScatterplotLayer',
                    data = coordinates[:5000],
                    get_position = '[LON, LAT]',
                    radius = 200,
                    elevation_scale = 4,
                    elevation_range = [0, 1000],
                    pickable = True,
                    extruded = True,
                    get_color = '[200, 30, 0, 160]',
                    get_radius = defaultRadius,
                )
            ],
        ))

    def map_location(self, state, city):
        result = f"""SELECT  start_long AS lon, start_lat AS lat\nFROM "J.POULOS".ACCIDENT a\nWHERE """

        if self.location_choice == "City":
            result += f"a.STATE_NAME = '{state}' AND\n"
            result += f"a.CITY_NAME = '{city}' AND\n"
        else:
            result += f"a.STATE_NAME = '{state}' AND\n"

    def city_location(self, state, city):

        temp = f"""SELECT c.latitude, c.longitude
                FROM "J.POULOS".city c
                WHERE c.name = '{city}' AND c.province = '{state}'"""

        coord_Query = pd.read_sql(temp, con = oracle_db.connection)
        
        if not len(coord_Query) == 0:
            self.latitude = coord_Query.iloc[0,0]
            self.longitude = coord_Query.iloc[0,1]
        
    def coordinates(self, state, city):
        result = f"""SELECT  start_long AS lon, start_lat AS lat\nFROM "J.POULOS".ACCIDENT a\nWHERE """

        if self.location_choice == "City":
            result += f"a.STATE_NAME = '{state}' AND\n"
            result += f"a.CITY_NAME = '{city}' AND\n"
        else:
            result += f"a.STATE_NAME = '{state}' AND\n"
        
        # add date conditions based on a range of days selected
        if self.date_choice == 'Date':
            dates = [self.day, self.day2]
            dates.sort()
            result += f"trunc(start_time) BETWEEN to_date('{dates[0]}', 'YYYY-MM-DD') AND to_date('{dates[1]}', 'YYYY-MM-DD')\n"
        else:
            result += f"EXTRACT(year FROM start_time) BETWEEN {self.year[0]} AND {self.year[1]} \n"
        
        # add weather conditions
        result += self.generate_weather_list()

        # add temperature conditions
        result += self.generate_temp_list()

        # add time conditions
        result += self.generate_time_list()
        coord_Query = pd.read_sql(result, con = oracle_db.connection)
        return coord_Query

    def location_query(self, state, city):

        # check if date or year
        if self.date_choice == 'Date':
            result = f"""SELECT trunc(start_time) AS time,\nCOUNT(*) AS Total_Accidents \nFROM "J.POULOS".ACCIDENT a\nWHERE """
        
        else:
            result = f"""SELECT EXTRACT(year FROM start_time) AS Year,\nCOUNT(*) AS Total_Accidents \nFROM "J.POULOS".ACCIDENT a\nWHERE """  

        # check if city or state
        if self.location_choice == "City":
            result += f"a.STATE_NAME = '{state}' AND a.CITY_NAME = '{city}' \n\tAND "           
        else:
            result += f"a.STATE_NAME = '{state}' \nAND "
        
        # add date conditions based on a range of days selected
        if self.date_choice == 'Date':
            dates = [self.day, self.day2]
            dates.sort()
            result += f"trunc(start_time) BETWEEN \n\tto_date('{dates[0]}', 'YYYY-MM-DD') AND \n\tto_date('{dates[1]}', 'YYYY-MM-DD')\n"
        else:
            result += f"EXTRACT(year FROM start_time) BETWEEN {self.year[0]} AND {self.year[1]} \n"
        
        # add weather conditions
        result += self.generate_weather_list()

        # add temperature conditions
        result += self.generate_temp_list()

        # add time conditions
        result += self.generate_time_list()
        
        if self.date_choice == 'Date':
            result += f"GROUP BY trunc(start_time) \nORDER BY time"
            
        else:
            result += f"GROUP BY EXTRACT(year FROM start_time)\nORDER BY YEAR"
        return result    

    # helper function to format list of weather conditions chosen
    def generate_weather_list(self):
        result = f""""""
       
        if self.weather:
            for i, cond in enumerate(self.weather): 
                if i == 0:
                    if len(self.weather) == 1:
                        result += f"""AND (condition LIKE '%{cond}%'"""
                    else:
                        result += f"""AND (condition LIKE '%{cond}%'\n"""
                elif i != len(self.weather) - 1:
                    result += f"""     OR condition LIKE '%{cond}%'\n"""
                else: 
                    result += f"""     OR condition LIKE '%{cond}%'""" 
            result += """)\n"""     
        return result

    # helper function to format list of temp conditions chosen
    def generate_temp_list(self):
        
        result = f""""""
        
        tempRange = []
        
        for i in range(0, len(self.temp)):
            match self.temp[i]:
                case "Temp < 00 °F":
                    tempRange.append((-100, -0.1))
                case "00 - 19 °F":
                    tempRange.append((0, 19.9))   
                case "20 - 39 °F":
                    tempRange.append((20,39.9))
                case "40 - 59 °F":
                    tempRange.append((40, 59.9))
                case "60 - 79 °F":
                    tempRange.append((60, 79.9))
                case "Temp > 80 °F":
                    tempRange.append((80, 200))
       
        if tempRange:
            tempRange.sort()
            for i, t in enumerate(tempRange):
                if i == 0:
                    if len(tempRange) == 1:
                        result += f"""AND (temperature BETWEEN {t[0]} AND {t[1]}"""
                    else:
                        result += f"""AND (temperature BETWEEN {t[0]} AND {t[1]}\n"""
                elif i != len(tempRange) - 1:
                    result += f"""     OR temperature BETWEEN {t[0]} AND {t[1]}\n"""
                else:
                    result += f"""     OR temperature BETWEEN {t[0]} AND {t[1]}"""
            result += f""")\n""" 
        
        return result
    
    # helper function to format list of time conditions chosen
    def generate_time_list(self):
        result = f""""""
        timeRange = []
        
        # adds the selected time conditions to
        # the timeRange list.
        for i in range(0, len(self.time)):
            match self.time[i]:
                case "12:00 AM - 02:59 AM":
                    timeRange.append(("00:00:00", "02:59:59"))
                case "03:00 AM - 05:59 AM":
                    timeRange.append(("03:00:00", "05:59:59")) 
                case "06:00 AM - 08:59 AM":
                    timeRange.append(("06:00:00", "08:59:59"))
                case "09:00 AM - 11:59 AM":
                    timeRange.append(("09:00:00", "11:59:59")) 
                case "12:00 PM - 02:59 PM":
                    timeRange.append(("12:00:00", "14:59:59"))              
                case "03:00 PM - 05:59 PM":
                    timeRange.append(("15:00:00", "17:59:59"))    
                case "06:00 PM - 08:59 PM":
                    timeRange.append(("18:00:00", "20:59:59"))
                case "09:00 PM - 11:59 PM":
                    timeRange.append(("21:00:00", "23:59:59"))  
        
        if timeRange:
            timeRange.sort()
            for i, t in enumerate(timeRange):
                if i == 0:
                    if len(timeRange) == 1:
                        result += f"""AND (to_char(start_time, 'hh24:mi:ss')\n\tBETWEEN '{t[0]}' AND '{t[1]}'"""
                    else:
                        result += f"""AND (to_char(start_time, 'hh24:mi:ss')\n\tBETWEEN '{t[0]}' AND '{t[1]}'\n"""
                elif i != len(timeRange) - 1:
                    result += f"""     OR to_char(start_time, 'hh24:mi:ss')\n\tBETWEEN '{t[0]}' AND '{t[1]}'\n"""
                else:
                    result += f"""     OR to_char(start_time, 'hh24:mi:ss')\n\tBETWEEN '{t[0]}' AND '{t[1]}'"""

            result += f""")\n"""

        return result
    
    def totals_query(self, df1, df2):
    
        st.subheader("Data")
        
        with st.container():
            
            temp = self.avg_query()
            average = pd.read_sql(temp, con=oracle_db.connection)
            natl_average = average['AVERAGE'].sum()
            
            if self.form and self.location_choice == "City" and not self.city1 == "" and not self.city2 == "": 
                sum_accidents1 = df1['TOTAL_ACCIDENTS'].sum()
                sum_accidents2 = df2['TOTAL_ACCIDENTS'].sum()
                
                st.text_area("",
                        self.city1 + ", " + self.state1 +  ":\n"
                        "\tTotal Accidents: " + str(sum_accidents1) + "\n\n" +
                        self.city2 + ", " + self.state2 + ":\n"
                        "\tTotal Accidents: " + str(sum_accidents2) + "\n\n"
                        "Average number of accidents in the US for the selected time period: " + "\n\t" +
                        str(round(natl_average, 2)), height = 300)
            
            elif self.form and self.location_choice == "State":
                sum_accidents1 = df1['TOTAL_ACCIDENTS'].sum()
                sum_accidents2 = df2['TOTAL_ACCIDENTS'].sum()
                st.text_area("",
                        self.state1 + ":\n"
                        "\tTotal Accidents: " + str(sum_accidents1) + "\n\n" +
                        self.state2 + ":\n"
                        "\tTotal Accidents: " + str(sum_accidents2) + "\n\n"
                        "Average number of accidents in the US for the selected time period: " + "\n\t" +
                        str(round(natl_average, 2)), height = 300)
            if self.sql_choice == 'Show':
                st.subheader("Query for Averages: ")            
                st.code(temp + ";", language ='sql')

    def avg_query(self):
        
        result = f"""SELECT AVG(totals) AS Average FROM (\nSELECT UNIQUE(state_name) AS name, COUNT(*) AS totals\nFROM "J.POULOS".ACCIDENT a\nWHERE """
        
        # add date conditions based on a range of days selected
        if self.date_choice == 'Date':
            dates = [self.day, self.day2]
            dates.sort()
            result += f"trunc(start_time) BETWEEN \n\tto_date('{dates[0]}', 'YYYY-MM-DD') AND \n\tto_date('{dates[1]}', 'YYYY-MM-DD')\n"
        else:
            result += f"EXTRACT(year FROM start_time) BETWEEN {self.year[0]} AND {self.year[1]} \n"
        
        # add weather conditions
        result += self.generate_weather_list()

        # add temperature conditions
        result += self.generate_temp_list()

        # add time conditions
        result += self.generate_time_list()
        result += f"GROUP BY state_name)"
        return result
            
    def load_bar_graph(self, dframe, dframe2):
       
        date1 = None
        date2 = None
        total1 = None
        total2 = None
        xLabel = ""
        location1 = ""
        location2 = ""
        
        if dframe.empty or dframe2.empty:
            xLabel = "Accident Data"
            date1 = pd.DataFrame()
            date2 = pd.DataFrame()
            total1 = pd.DataFrame()
            total2 = pd.DataFrame()

        elif self.date_choice == 'Date':
            xLabel = "Accidents for the specified date range"
            date1 = dframe['TIME']
            date2 = dframe2['TIME']
            total1 = dframe['TOTAL_ACCIDENTS']
            total2 = dframe2['TOTAL_ACCIDENTS']
            self.sum1 = dframe['TOTAL_ACCIDENTS'].sum()
            self.sum2 = dframe2['TOTAL_ACCIDENTS'].sum()
        
        else:
            xLabel = "Years"
            date1 = dframe['YEAR']
            date2 = dframe2['YEAR']
            total1 = dframe['TOTAL_ACCIDENTS']
            total2 = dframe2['TOTAL_ACCIDENTS']
            self.sum1 = dframe['TOTAL_ACCIDENTS'].sum()
            self.sum2 = dframe2['TOTAL_ACCIDENTS'].sum()
        
        if self.location_choice == "City":
            location1 = self.city1 + ", " + self.state1
            location2 = self.city2 + ", " + self.state2

        else:
            location1 = self.state1
            location2 = self.state2
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x = date1,
            y = total1,
            name = location1,
            marker_color = '#ED8C31',
            opacity = 0.90
        ))

        fig.add_trace(go.Bar(
            x = date2,
            y = total2,
            name = location2,
            marker_color = '#3184ED',
            opacity = 0.90
        ))
        
        fig.update_layout(
            legend = dict(
                font = dict(family = "Arial", size = 18),
                yanchor = "top", y = 1.2, xanchor="left", x = 0
            ),
            xaxis_title_text = xLabel, # xaxis label
            yaxis_title_text = 'Total Accidents', # yaxis label
            bargap = 0.2, # gap between bars of adjacent location coordinates
            bargroupgap = 0.1, # gap between bars of the same location coordinates,
            height = 600,
        )
        
        fig.update_yaxes(title_font = dict(size = 18), tickfont_size = 18)
        fig.update_xaxes(title_font = dict(size = 18), tickfont_size = 18)
        st.plotly_chart(fig, use_container_width = True)
    
    def load_line_graph(self, location1, location2):

        if self.location_choice == "State" and self.date_choice == "Year":
            st.header(f"State Funding 2016 - 2019")
            col1, col2, col3 = st.columns([1.2, 1.2, 1])
            
            where = "WHERE state_name \nIN ("
            states = []
            modified_states = []
            
            if location1 not in states:
                states.append(location1)

            for val in states:
                mod = "\'" + val + "\'"
                if mod not in modified_states:
                    modified_states.append(mod)

            for index, val in enumerate(modified_states):
                if len(modified_states) > 1:
                    where = where[:len(where) - 2]
                    where += ", "
                where += modified_states[index] + ", "
                if index == len(modified_states) - 1:
                    where = where[:len(where) - 2] + ")"
            
            query1 = f"""\rWITH cte_funding AS(
                    SELECT sname AS state_name, year, funding FROM "J.POULOS".state_fund),

                    cte_accidents AS (
                    SELECT COUNT(id) AS accidents, EXTRACT(year FROM start_time) AS year, state_name
                    FROM "J.POULOS".accident
                    GROUP BY state_name, EXTRACT(year FROM start_time))

                    SELECT * FROM cte_funding NATURAL JOIN cte_accidents
                    {where}
                    ORDER BY year"""

            df_oracle2 = pd.read_sql(query1, con=oracle_db.connection)
            
            fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize = (5.5, 4.5))
            fig.tight_layout()
            
            ax1.set_title('Funding')
            ax1.set_ylabel('Dollar Amount')
        
            ax2.set_title('Amount of Accidents', fontsize = 8)
            ax2.set_xlabel('Year', fontsize = 8)
            ax2.set_ylabel('Accidents', fontsize = 8)
            
            ax2.plot(df_oracle2['YEAR'], df_oracle2['ACCIDENTS'], label = location1)
            ax1.plot(df_oracle2['YEAR'], df_oracle2['FUNDING'], label = location1)
        
            for tick in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label, ax2.title,
                        ax2.xaxis.label, ax2.yaxis.label] + ax1.get_xticklabels() +
                        ax2.get_xticklabels() + ax1.get_yticklabels() + ax2.get_yticklabels()):
                tick.set_fontsize(6)
            ax2.set_xticks(df_oracle2['YEAR'])
            ax1.set_xticks(df_oracle2['YEAR'])
            ax2.legend(bbox_to_anchor = (0., 2.4, 1., .102), 
                        fontsize = 7,
                        loc = 'lower left',
                        ncol = 2, mode = "expand", 
                        borderaxespad = 0)

            with col1: 
                st.subheader(f"\n {location1} vs {location2}")  
                if location2 not in states:
                    states.append(location2)

                for val in states:
                    mod = "\'" + val + "\'"
                    if mod not in modified_states:
                        modified_states.append(mod)

                for index, val in enumerate(modified_states):
                    if len(modified_states) == 1:
                        break
                    if len(modified_states) > 1:
                        where = where[:len(where) - 1]
                        
                    where += modified_states[index] + ", "
                    if index == len(modified_states) - 1:
                        where = where[:len(where) - 2] + ")"
        
                query2 = f"""WITH cte_funding AS(
                        SELECT sname AS state_name, year, funding
                        FROM "J.POULOS".state_fund),

                        cte_accidents AS (
                        SELECT COUNT(id) AS accidents, \nEXTRACT(year FROM start_time) AS year, state_name
                        FROM "J.POULOS".accident
                        GROUP BY state_name, EXTRACT(year FROM start_time))

                        SELECT * FROM cte_funding NATURAL JOIN cte_accidents
                        {where}
                        ORDER BY year"""

                df_oracle3 = pd.read_sql(query2, con=oracle_db.connection)

                ax1.set_title('Funding')
                ax1.set_ylabel('Dollar Amount')

                ax2.set_title('Amount of Accidents', fontsize=12)
                ax2.set_xlabel('Year', fontsize=12)
                ax2.set_ylabel('Accidents')

                for frame in [df_oracle3]:
                    ax1.plot(frame['YEAR'], frame['FUNDING'], label=frame['STATE_NAME'].loc[0])
                    ax2.plot(frame['YEAR'], frame['ACCIDENTS'], label=frame['STATE_NAME'].loc[0])
                ax2.legend(bbox_to_anchor = (0., 2.4, 1., .102), 
                        fontsize = 7,
                        loc = 'lower left',
                        ncol = 2, mode = "expand", 
                        borderaxespad = 0)

                for tick in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label, ax2.title,
                            ax2.xaxis.label, ax2.yaxis.label] + ax1.get_xticklabels() +
                            ax2.get_xticklabels() + ax1.get_yticklabels() + ax2.get_yticklabels()):
                    tick.set_fontsize(6)
                ax2.set_xticks(df_oracle2['YEAR'])
                ax1.set_xticks(df_oracle2['YEAR'])

                st.pyplot(fig = plt)
                
                with col2:
                    # randomly chooses a third state
                    random_state = random.choice(self.state_name)
                    while random_state == location1 or random_state == location2:
                        random_state = random.choice(self.state_name)
                        
                    st.subheader(f"\n{location1} vs {location2} vs random state {random_state}")
                    
                    if random_state not in states:
                        states.append(random_state)

                    for val in states:
                        mod = "\'" + val + "\'"
                        if mod not in modified_states:
                            modified_states.append(mod)

                    for index, val in enumerate(modified_states):
                        if len(modified_states) == 1:
                            break
                        
                        if len(modified_states) > 1:
                            where = where[:len(where) - 1]
            
                        where += modified_states[index] + ", "
                        if index == len(modified_states) - 1:
                            where = where[:len(where) - 2] + ")"

                    query3 = f"""WITH cte_funding AS(\nSELECT sname AS state_name, year, funding\nFROM "J.POULOS".state_fund), cte_accidents AS (
                            \nSELECT COUNT(id) AS accidents, \nEXTRACT(year FROM start_time) AS year, state_name
                            \nFROM "J.POULOS".accident\nGROUP BY state_name, EXTRACT(year FROM start_time))\nSELECT * FROM cte_funding NATURAL JOIN cte_accidents
                            \n{where}\nORDER BY year"""

                    df_oracle4 = pd.read_sql(query3, con=oracle_db.connection)
                    df_oracle4 = df_oracle4[df_oracle4['STATE_NAME'] == states[len(states)-1]]

                    ax1.set_title('Funding')
                    ax1.set_ylabel('Dollar Amount')
                    ax2.set_title('Amount of Accidents', fontsize = 8)
                    ax2.set_xlabel('Year', fontsize = 8)
                    ax2.set_ylabel('Accidents')

                    for frame in [df_oracle4]:
                        ax1.plot(frame['YEAR'], frame['FUNDING'], label = random_state)
                        ax2.plot(frame['YEAR'], frame['ACCIDENTS'], label = random_state)
                    
                    ax2.legend(
                        fontsize = 7, 
                        bbox_to_anchor = (0., 2.4, 1., .102), 
                        loc = 'lower left',
                        ncol = 3, mode = "expand", 
                        borderaxespad = 0.)
                    
                    for tick in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label, ax2.title,
                                ax2.xaxis.label, ax2.yaxis.label] + ax1.get_xticklabels() +
                                ax2.get_xticklabels() + ax1.get_yticklabels() + ax2.get_yticklabels()):
                        tick.set_fontsize(6)
                    ax2.set_xticks(df_oracle2['YEAR'])
                    ax1.set_xticks(df_oracle2['YEAR'])
                    st.pyplot(fig=plt)

                avg = f"""SELECT AVG(funding) AS avg
                        FROM "J.POULOS".state_fund"""

                df_oracle5 = pd.read_sql(avg, con=oracle_db.connection)
                
                sum_accidents1 = df_oracle2['ACCIDENTS'].sum()
                sum_accidents2 = df_oracle3['ACCIDENTS'].sum()
                sum_accidents3  = df_oracle3['ACCIDENTS'].sum()
                sum_funding1 = df_oracle2['FUNDING'].sum()
                sum_funding2 = df_oracle3['FUNDING'].sum()
                sum_funding3 = df_oracle3['FUNDING'].sum()
                natl_funding = df_oracle5['AVG'].sum()
                
                with col3: 
                    st.subheader("Data")
                    with st.container():
                        st.text_area("Total Funding years 2016 - 2019",
                                self.state1 + ":\n"
                                "\tTotal Accidents: " + str(sum_accidents1) + "\n"
                                "\tState Funding: " + str(sum_funding1) + "\n" +
                                self.state2 + ":\n"
                                "\tTotal Accidents: " + str(sum_accidents2) + "\n" 
                                "\tState Funding: " + str(sum_funding2) + "\n" +
                                random_state + ":\n"
                                "\tTotal Accidents: " + str(sum_accidents3) + "\n" 
                                "\tState Funding: " + str(sum_funding3) + "\n"
                                "National Average For State Funding:\n\t" + str(round(natl_funding, 2)), height = 300)
                        if self.sql_choice == 'Show':
                            st.subheader(f"Query for {self.state1}, {self.state2}, and {random_state}:")     
                            st.code(query3 + ";", language ='sql')
                                                                               
    def run(self):

        st.image(Image.open('images/logo_banner.png'), use_column_width = True)
        
        self.load_sidebar()
        data1 = ""
        data2 = ""
        
        if self.form:
        # calls query builder
            if self.location_choice == "City":
                data1 = self.location_query(self.state1, self.city1)
                data2 = self.location_query(self.state2, self.city2)
            else:
                data1 = self.location_query(self.state1, "")
                data2 = self.location_query(self.state2, "")

            # query dataframes
            self.df_location1 = pd.read_sql(data1, con = oracle_db.connection)
            self.df_location2 = pd.read_sql(data2, con = oracle_db.connection)
            
        # creates a two column layout.
        col1, col2, col3 = st.columns([1.25, 1.25, 1])
        
        with col1:
            
            if self.form and self.location_choice == "City" and not self.city1 == "":
                st.header(f"Accident locations for {self.city1}, {self.state1}")
                self.update_state(self.state1)
                self.city_location(self.state1, self.city1)
                self.load_map(self.state1, self.city1)
            
            elif self.form == False and self.location_choice == "State":
                st.header(f"Accident locations")
                self.load_map("", "")
            
            elif self.form and self.location_choice == "State":
                st.header(f"Accident locations for {self.state1}")
                self.update_state(self.state1)
                self.load_map(self.state1, "")

            else:
                st.header(f"Accident locations")
                self.load_map("", "")
                
        with col2:
           
            if self.form and self.location_choice == "City" and not self.city2 == "":
                st.header(f"Accident locations for {self.city2}, {self.state2}")
                self.update_state(self.state1)
                self.city_location(self.state2, self.city2)
                self.load_map(self.state2, self.city2)
            
            elif self.form == False and self.location_choice == "State":
                st.header(f"Accident locations")
                self.load_map("", "")

            elif self.form and self.location_choice == "State":
                st.header(f"Accident locations for {self.state2}")
                self.update_state(self.state2)
                self.load_map(self.state2, "")
            
            else:
                st.header(f"Accident locations")
                self.load_map("", "")

        with col3:
            if self.form and self.location_choice == "City" and not self.city1 == "" and not self.city2 == "": 
                self.totals_query(self.df_location1, self.df_location2)
            
            elif self.form and self.location_choice == "State":
                self.totals_query(self.df_location1, self.df_location2)
       
        # page separator
        st.markdown("""***""") 
        
        col4, col5 = st.columns([2,1])
        with col4:
            if self.form and self.location_choice == "City" and not self.city1 == "" and not self.city2 == "":
                st.header(f"Accident data for {self.city1}, {self.state1} and {self.city2}, {self.state2}")
                self.load_bar_graph(self.df_location1, self.df_location2)
            
            elif self.form and self.location_choice == "State":
                st.header(f"Accident data for {self.state1} and {self.state2}")
                self.load_bar_graph(self.df_location1, self.df_location2)
            
            else:
                st.header(f"Accident data")
                self.load_bar_graph(pd.DataFrame(), pd.DataFrame())
           
        with col5:
            if self.form and self.location_choice == "City" and not self.city1 == "" and not self.city2 == "":
                with st.container():
                    if self.sql_choice == 'Show':
                        st.subheader(f"Query for {self.city1}, {self.state1} :")
                        st.code(data1 + ";", language ='sql')
                        st.subheader(f"Query for for {self.city2}, {self.state2} :")        
                        st.code(data2 + ";", language ='sql')

            elif self.form and self.location_choice == "State":
                with st.container():
                    if self.sql_choice == 'Show':
                        st.subheader(f"Query for {self.state1} :")
                        st.code(data1 + ";", language ='sql')
                        st.subheader(f"Query for {self.state2} :")       
                        st.code(data2 + ";", language ='sql')

        st.markdown("""***""")
        if self.add_queries == "State Funding":
            self.load_line_graph(self.state1, self.state2)             