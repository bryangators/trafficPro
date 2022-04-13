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

    def __init(self):
        self.formatted_query = f""""""
        self.day = None
        self.year = None
        self.weather = None
        self.time = None
        

    def run(self):
        l2 = Image.open('images/logo2.png')
        st.image(Image.open('images/logo_banner.png'), use_column_width = True)

        """
        This section is for the elements in the sidebar
        """
        with st.sidebar:
            
            st.image(l2, width = 250)
            date_choice = st.radio(
                "Query by Date or Year Range",
                ("Date", "Year")
            )
            
            with st.form(key='form1'):

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
                    self.year = st.slider(
                        'Select the range of years',
                        2016, 2020, (2017, 2019)
                    )
                
                # Weather options
                # multiselect weather. passes the condition to the weather function
                st.header('Weather', anchor = None)
                self.weather = st.multiselect(
                    'Select Weather Condition',
                    ['Rain', 'Snow', 'Partly Cloudy', 'Tornado', 'Clear', 'Cloudy', 'Thunderstorm', 'Hail', 'Windy', 
                    'Mostly Cloudy', 'Fair', 'Overcast', 'Scattered Clouds', 'Fog', 'Haze']
                )

                st.header('Temperature', anchor = None)
                self.temp = st.multiselect(
                    'Select Temperature',
                    ['Temp < 00 °F', '00 - 19 °F', '20 - 39 °F', '40 - 59 °F', '60 - 79 °F', 'Temp > 80 °F']
                )

                # Time selection
                st.header('Time', anchor = None)
                self.time = st.multiselect(
                    'Select Time',
                    ['12:00 AM - 02:59 AM', '03:00 AM - 05:59 AM',
                    '06:00 AM - 08:59 AM', '09:00 AM - 11:59 AM',
                    '12:00 PM - 02:59 PM', '03:00 PM - 05:59 PM',
                    '06:00 PM - 08:59 PM', '09:00 PM - 11:59 PM']
                )

                submitted = st.form_submit_button(label='Run Query')

            self.dbstats()

        """
        This section is for the main page elements
        """
        self.formatted_query = self.generate_query(date_choice)
        print(self.formatted_query)

        # Data frame and map
        df = pd.DataFrame(
            np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
            columns = ['lat', 'lon']
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

        # preview table of query results
        st.write(pd.read_sql(self.formatted_query + " FETCH FIRST 20 ROWS ONLY", con = oracle_db.connection))
        
    
    def generate_query(self, date_choice):
        result = f"""SELECT * 
                     FROM "J.POULOS".ACCIDENT
                     WHERE
                     """

        # add date conditions
        if date_choice == 'Date':
            result += f""" trunc(start_time) = to_date('{self.day}', 'YYYY-MM-DD') """
        else:
            result += f""" EXTRACT(year FROM start_time) >= {self.year[0]}
                           AND EXTRACT(year FROM start_time) <= {self.year[1]} """
        
        # add weather conditions
        result += self.generate_weather_list()

        # add temperature conditions
        result += self.generate_temp_list()

        # add time conditions
        result += self.generate_time_list()
        
        return result
    
    # helper function to format list of weather conditions chosen
    def generate_weather_list(self):
        result = f""" """

        if self.weather:
            first = True
            for cond in self.weather: 
                if first:
                    result += f""" AND (condition LIKE '%{cond}%' """
                    first = False
                else: 
                    result += f""" OR condition LIKE '%{cond}%' """ 
            result += """) """     
        return result

    # helper function to format list of temp conditions chosen
    def generate_temp_list(self):
        
        result = f""" """

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
            first = True
            for t in tempRange:
                if first:
                    result += f""" AND (temperature BETWEEN {t[0]} AND {t[1]} """
                    first = False
                else:
                    result += f""" OR temperature BETWEEN {t[0]} AND {t[1]} """
            result += f""") """       
        return result

    # helper function to format list of time conditions chosen
    def generate_time_list(self):
        result = f""" """
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
            first = True
            for t in timeRange:
                if first:
                    result += f""" AND (to_char(start_time, 'hh24:mi:ss') BETWEEN '{t[0]}' AND '{t[1]}' """
                    first = False
                else:
                    result += f""" OR to_char(start_time, 'hh24:mi:ss') BETWEEN '{t[0]}' AND '{t[1]}' """
            result += f""") """

        return result

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
            str7 = "Tuples in County table: " + str(q7t) + "\n"
            str8 = "Tuples in County_pop table: " + str(q8t) + "\n"
            str9 = "Tuples in City table: " + str(q9t) + "\n"
            str10 = "Tuples in City_pop table: " + str(q10t) + "\n"
        
            sum = q1t + q2t + q3t + q4t + q5t + q6t + q7t + q8t + q9t + q10t
            str11 = "\nTotal Tuples: " + str(sum) + "\n"

            st.sidebar.text_area('About', 
                str1 + str2 + str3 + str4 + str5 + 
                str6 + str7 + str8 + str9 + str10 + str11,
                height = 350
            )