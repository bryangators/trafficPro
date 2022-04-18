from itertools import count
from re import U
from matplotlib.axis import YAxis
import streamlit as st
from hydralit import HydraHeadApp
from db import db_conn as oracle_db
import numpy as np
import pandas as pd
from PIL import Image
import pydeck as pdk
import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import altair as alt


class Home(HydraHeadApp):

    def __init(self):
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
                        2016, 2020, (2016, 2020)
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
        col1, col2 = st.columns(2)

        with col1:

            st.header("United States Accidents by State")
            if (date_choice == 'Date'):
                st.caption(f"Total on {self.day}")
            else:
                st.caption(f"Total between {self.year[0]} and {self.year[1]}")

            map_query = self.generate_map_query(date_choice)
            map_df = pd.read_sql(map_query, con = oracle_db.connection)

            map_fig = go.Figure(data=go.Choropleth(
                locations=map_df['CODE'], # Spatial coordinates
                z = map_df['TOTAL'].astype(float), # Data to be color-coded
                locationmode = 'USA-states', # set of locations match entries in `locations`
                colorscale = 'Oranges',
                text=map_df['STATE'],
                colorbar_title = "No. of Accidents",
            ))

            map_fig.update_layout(
                geo = dict(
                scope='usa',
                projection=go.layout.geo.Projection(type = 'albers usa'),
                showlakes=True, # lakes
                lakecolor='rgb(255, 255, 255)'),
            )
            map_fig.update_layout(height=300, margin={"r":20,"t":60,"l":0,"b":0})
            st.plotly_chart(map_fig, use_container_width=True)

            st.text("SQL for Above Query:")
            st.code(map_query + ";", language='sql')

            

        with col2:
            st.header("Top 10 States by Accident Query")
            if (date_choice == 'Date'):
                st.caption(f"Total on {self.day}")
            else:
                st.caption(f"Total between {self.year[0]} and {self.year[1]}")

            #Creates queries dynamically and stores the query code in USData
            USData = self.generate_query1(date_choice)
            top10_df = pd.read_sql_query(USData, con = oracle_db.connection)
            top10_df.sort_values('ACCIDENTS')

            top10_fig = go.Figure()
            top10_fig.add_trace(go.Bar(
                y=top10_df['STATE'],
                x=top10_df['ACCIDENTS'],
                orientation='h',
                 marker=dict(
                        color='rgba(50, 171, 96, 0.6)',
                        line=dict(
                            color='rgba(50, 171, 96, 1.0)',
                            width=1),
            )))
            top10_fig.update_layout(height=300, margin={"r":20,"t":60,"l":0,"b":0})
            top10_fig.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
            st.write(top10_fig, use_container_width=True)
            # st.bar_chart(USData4graph['ACCIDENTS'])
            st.text("SQL for Above Query:")
            st.code(USData + ";", language='sql')

        
        
        # query to get list of states for select box
        state_query = """select sname as state
                        FROM "J.POULOS".STATE
                        WHERE sname != 'Alaska' and sname != 'Hawaii'
                        ORDER BY sname ASC"""
        state_list = pd.read_sql(state_query, con = oracle_db.connection)
        #print("here")
        state = st.selectbox(
                'Choose a State',
                state_list['STATE'])

        #Weekly Graph
        if (date_choice == 'Year'):
            st.header(f"{state} Weekly Accidents")
            wk_query = self.generate_wk_query(date_choice,state)            
            wk_df = pd.read_sql(wk_query, con = oracle_db.connection)            
            wk_fig = px.line(wk_df, x="Weeks", y="Accidents")
            st.plotly_chart(wk_fig, use_container_width=True)
            st.code(wk_query + ";", language='sql')



        # FUNDING GRAPH
        st.header(f"{state} Funding vs Accidents")
        fund_query = self.generate_funding_query(state)
        fund_df = pd.read_sql(fund_query, con = oracle_db.connection)
        # Create figure with secondary y-axis
        fund_fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fund_fig.add_trace(
            go.Scatter(x=fund_df['YEAR'], y=fund_df['FUNDING'], name="Funding"),
            secondary_y=False,
        )

        fund_fig.add_trace(
            go.Scatter(x=fund_df['YEAR'], y=fund_df['ACCIDENTS'], name="Accidents"),
            secondary_y=True,
        )

        # Add figure title
        fund_fig.update_layout(
            title_text=f"Accidents vs Funding Trends for {state}"
        )

        # Set x-axis title
        fund_fig.update_xaxes(title_text="Year", dtick=1)

        # Set y-axes titles
        fund_fig.update_yaxes(title_text="Total Funding - US Dollars", secondary_y=False)
        fund_fig.update_yaxes(title_text="Total Accidents", secondary_y=True)

        st.plotly_chart(fund_fig, use_container_width=True)

        #POPULATION GRAPH
        st.header(f"{state} Population vs Accidents")
        pop_query = self.generate_pop_query(state)
        
        pop_df = pd.read_sql(pop_query, con = oracle_db.connection)
        # Create figure with secondary y-axis
        pop_fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        pop_fig.add_trace(
            go.Scatter(x=pop_df['YEAR'], y=pop_df['POPULATION'], name="Population"),
            secondary_y=False,
        )

        pop_fig.add_trace(
            go.Scatter(x=pop_df['YEAR'], y=pop_df['ACCIDENTS'], name="Accidents"),
            secondary_y=True,
        )

        # Add pop_figure title
        pop_fig.update_layout(
            title_text=f"Accidents vs Population Trends for {state}"
        )

        # Set x-axis title
        pop_fig.update_xaxes(title_text="Year", dtick=1)

        # Set y-axes titles
        pop_fig.update_yaxes(title_text="Total Population", secondary_y=False)
        pop_fig.update_yaxes(title_text="Total Accidents", secondary_y=True)

        st.plotly_chart(pop_fig, use_container_width=True)

            
    def generate_query(self, date_choice):
        result = f"""SELECT * 
                     FROM "J.POULOS".ACCIDENT
                     WHERE
                     """

        # add date conditions
        result += self.generate_date_list(date_choice)
        
        # add weather conditions
        result += self.generate_weather_list()

        # add temperature conditions
        result += self.generate_temp_list()

        # add time conditions
        result += self.generate_time_list()
        
        return result
    
    #Bar Chart Data Query Builder
    def generate_query1(self, date_choice):
        result = f"""SELECT COUNT(*) AS Accidents, STATE_NAME AS State\nFROM "J.POULOS".ACCIDENT\nWHERE """
        
        # add date conditions
        result += self.generate_date_list(date_choice)
        
        # add weather conditions
        result += self.generate_weather_list()

        # add temperature conditions
        result += self.generate_temp_list()

        # add time conditions
        result += self.generate_time_list()
      
        # group by STATE, show only top 10
        result += f"""GROUP BY STATE_NAME\nORDER BY COUNT(*) DESC\nFETCH FIRST 10 ROWS ONLY"""
       
        return result

    #Weekly
    def generate_wk_query(self,date_choice,state):
        result = f"""SELECT COUNT(*) AS "Accidents", TRUNC(Start_Time, 'IW') AS "Weeks"\nFROM "J.POULOS".ACCIDENT\nWHERE STATE_NAME = '{state}' AND\n"""    

         # add date conditions
        result += self.generate_date_list(date_choice)
        
        # add weather conditions
        result += self.generate_weather_list()

        # add temperature conditions
        result += self.generate_temp_list()

        # add time conditions
        result += self.generate_time_list()

        # group by week
        result += f"""GROUP BY TRUNC(Start_Time, 'IW') ORDER BY "Weeks" ASC"""

        return result
      

    def generate_map_query(self, date_choice):
        result = f"""SELECT s.ABBREVIATION AS code, count(a.ID) AS total, s.SNAME AS state\nFROM "J.POULOS".ACCIDENT a, "J.POULOS".STATE s\nWHERE a.STATE_NAME = s.SNAME AND\n"""

        # add date conditions
        result += self.generate_date_list(date_choice)
        
        # add weather conditions
        result += self.generate_weather_list()

        # add temperature conditions
        result += self.generate_temp_list()

        # add time conditions
        result += self.generate_time_list()

        result += f"GROUP BY s.ABBREVIATION, s.SNAME"

        return result
    
    def generate_funding_query(self, state):
        result = f"""with totals (state_name, accidents, year) as (
                    SELECT state_name, COUNT(ID) as Accidents, EXTRACT(year FROM start_time) as Year
                    FROM "J.POULOS".Accident
                    GROUP BY state_name, EXTRACT(year FROM start_time)
                    HAVING state_name = '{state}' AND EXTRACT(year FROM start_time) != 2020)

                    SELECT t.state_name as state, t.year as year, t.accidents as accidents, f.funding as funding
                    FROM totals t, "J.POULOS".STATE_FUND f
                    WHERE t.year = f.year and t.state_name = f.sname
                    ORDER BY year ASC"""

        return result
    
    def generate_pop_query(self, state):
        result = f"""with totals (state_name, accidents, year) as (
                    SELECT state_name, COUNT(ID) as Accidents, EXTRACT(year FROM start_time) as Year
                    FROM "J.POULOS".Accident
                    GROUP BY state_name, EXTRACT(year FROM start_time)
                    HAVING state_name = '{state}')

                    SELECT t.state_name as state, t.year as year, t.accidents as accidents, p.population
                    FROM totals t, "J.POULOS".STATE_POP p
                    WHERE t.year = p.year and t.state_name = p.sname
                    ORDER BY year ASC"""

        return result

    def generate_date_list(self, date_choice):
        result = """"""
        if date_choice == 'Date':
            result += f"""trunc(start_time) = to_date('{self.day}', 'YYYY-MM-DD')\n"""
        else:
            result += f"""EXTRACT(year FROM start_time) >= {self.year[0]}\nAND EXTRACT(year FROM start_time) <= {self.year[1]}\n"""
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
                        result += f"""AND (to_char(start_time, 'hh24:mi:ss') BETWEEN '{t[0]}' AND '{t[1]}'"""
                    else:
                        result += f"""AND (to_char(start_time, 'hh24:mi:ss') BETWEEN '{t[0]}' AND '{t[1]}'\n"""
                elif i != len(timeRange) - 1:
                    result += f"""     OR to_char(start_time, 'hh24:mi:ss') BETWEEN '{t[0]}' AND '{t[1]}'\n"""
                else:
                    result += f"""     OR to_char(start_time, 'hh24:mi:ss') BETWEEN '{t[0]}' AND '{t[1]}'"""

            result += f""")\n"""

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