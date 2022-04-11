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

    latitude = 0.0
    longitude = 0.0
    state1 = ""
    state2 = ""
    state3 = ""
    condition = ""
    df_city = pd.DataFrame(columns = ['lon', 'lat'])
    cursor = oracle_db.connection.cursor()
    state_name = ('Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
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

    def load_graphs(self):
        # where = "WHERE state_name = "
        col1, col2 = st.columns(2)
        
        with col1:
            # global where
            # print(where)
            where = "WHERE state_name IN ("
            states = []
            modified_states = []
            
            # Example code to get data from database using cursor and connection object
            #state = st.text_input("Enter State: ")
            #states = []
            #st.sidebar.header('State', anchor = None)
            #state = st.sidebar.selectbox(
            #    "Select State", self.state_names
            #)
            if self.state1 not in states:
                states.append(self.state1)

            for val in states:
                mod = "\'" + val + "\'"
                if mod not in modified_states:
                    modified_states.append(mod)

            print(states)
            print(modified_states)

            for index, val in enumerate(modified_states):
                if len(modified_states) > 1:
                    where = where[:len(where) - 2]
                    print(where)
                    where += ", "
                where += modified_states[index] + ", "
                if index == len(modified_states) - 1:
                    where = where[:len(where) - 2] + ")"


            #print(where)
            query = f"""WITH cte_funding AS(
                    SELECT sname AS state_name, year, funding
                    FROM "J.POULOS".state_fund),

                    cte_accidents AS (
                    SELECT COUNT(id) AS accidents, EXTRACT(year FROM start_time) AS year, state_name
                    FROM "J.POULOS".accident
                    GROUP BY state_name, EXTRACT(year FROM start_time))

                    SELECT * FROM cte_funding NATURAL JOIN cte_accidents
                    {where}
                    ORDER BY year"""

            #{where}
            #print(query)

            df_oracle2 = pd.read_sql(query, con=oracle_db.connection)
            st.write(df_oracle2)
            
            fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize = (5, 3))
        

            ax1.set_title('Funding')
            ax1.set_ylabel('Dollar Amount')
        
            ax2.set_title('Amount of Accidents', fontsize=12)
            ax2.set_xlabel('Year', fontsize=12)
            ax2.set_ylabel('Accidents')
            
            ax2.plot(df_oracle2['YEAR'], df_oracle2['ACCIDENTS'])
            ax1.plot(df_oracle2['YEAR'], df_oracle2['FUNDING'])
           

            for tick in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label, ax2.title,
                        ax2.xaxis.label, ax2.yaxis.label] + ax1.get_xticklabels() +
                        ax2.get_xticklabels() + ax1.get_yticklabels() + ax2.get_yticklabels()):
                tick.set_fontsize(6)
            ax2.set_xticks(df_oracle2['YEAR'])
            ax1.set_xticks(df_oracle2['YEAR'])
            st.pyplot(fig=plt)

            if "load_state" not in st.session_state:
                st.session_state.load_state = False

            if st.button("Compare this state with another?") or st.session_state.load_state:
                st.session_state.load_state = True
                #st.write('Why? One state should be good enough for you')
                
                if self.state2 not in states:
                    states.append(self.state2)

                for val in states:
                    mod = "\'" + val + "\'"
                    if mod not in modified_states:
                        modified_states.append(mod)

                # print(states)
                # print(modified_states)

                for index, val in enumerate(modified_states):
                    if len(modified_states) == 1:
                        break
                    if len(modified_states) > 1:
                        where = where[:len(where) - 1]
                        #print(where)
                        #where += ", "
                    where += modified_states[index] + ", "
                    if index == len(modified_states) - 1:
                        where = where[:len(where) - 2] + ")"
            with col2:
                # print(where)
                query = f"""WITH cte_funding AS(
                        SELECT sname AS state_name, year, funding
                        FROM "J.POULOS".state_fund),

                        cte_accidents AS (
                        SELECT COUNT(id) AS accidents, EXTRACT(year FROM start_time) AS year, state_name
                        FROM "J.POULOS".accident
                        GROUP BY state_name, EXTRACT(year FROM start_time))

                        SELECT * FROM cte_funding NATURAL JOIN cte_accidents
                        {where}
                        ORDER BY year"""

                #for debugging purposes. A previous sate shows up but that doesn't screw up the sql code.
                # ie if state1 was Alabama and state2 is arkansas you'll get ('Alabama', 'Alabama', 'Arkansas')
                # Too tired to fix. But really, it doesn't matter.
                #print(query)
                #print(where)

                #print(df_oracle2)
                #wtf? Why aren't isn't the previ
                df_oracle3 = pd.read_sql(query, con=oracle_db.connection)

                # Wtf? The dataframe printed completely ignores the previous state/funding values that were selected.
                # I don't see how thats possible when the query that prints has the 2 different states?!?
                st.write(df_oracle3)
                # print(df_oracle3)
                # for col in df_oracle3:
                #     print(col)
                #
                # for val in df_oracle3['STATE_NAME']:
                #     print(val)
                #frames = [df_oracle2, df_oracle3]
                #result = pd.concat(frames)
                #st.write(result)

                # df_oracle2['Key'] = 'trail1'
                # df_oracle3['Key'] = 'trail2'

                fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
                ax1.set_title('Funding')
                ax1.set_ylabel('Dollar Amount')

                ax2.set_title('Amount of Accidents', fontsize=12)
                ax2.set_xlabel('Year', fontsize=12)
                ax2.set_ylabel('Accidents')
                # ax2.plot(df_oracle2['YEAR'], df_oracle3['YEAR'], df_oracle2['ACCIDENTS'], df_oracle3['ACCIDENTS'])
                # ax1.plot(df_oracle2['FUNDING'], df_oracle3['FUNDING'])

                for frame in [df_oracle2, df_oracle3]:
                    ax1.plot(frame['YEAR'], frame['FUNDING'], label=frame['STATE_NAME'].loc[0])
                    ax2.plot(frame['YEAR'], frame['ACCIDENTS'], label=frame['STATE_NAME'].loc[0])

                ax1.legend()
                ax2.legend()

                # df = pd.concat([df_oracle2, df_oracle3], keys=['trail1', 'trail2'])
                # dfgroup = df.groupby(['YEAR', 'Key'])
                # plt = dfgroup.sum().unstack('Key').plot()

                #plt.subplots_adjust(bottom=0.000000000000000000001)
               
                
                for tick in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label, ax2.title,
                            ax2.xaxis.label, ax2.yaxis.label] + ax1.get_xticklabels() +
                            ax2.get_xticklabels() + ax1.get_yticklabels() + ax2.get_yticklabels()):
                    tick.set_fontsize(6)
                ax2.set_xticks(df_oracle2['YEAR'])
                ax1.set_xticks(df_oracle2['YEAR'])
                #print(states)

                st.pyplot(fig=plt)

                if "another_state" not in st.session_state:
                    st.session_state.another_state = False

                if st.button("Compare previous two with another state?") or st.session_state.another_state:
                    st.session_state.another_state = True
                    #st.write('Why? Hot shot over here comparing 3 states smh')
                    
                    if self.state3 not in states:
                        states.append(self.state3)

                    for val in states:
                        mod = "\'" + val + "\'"
                        if mod not in modified_states:
                            modified_states.append(mod)

                    # print(states)
                    # print(modified_states)

                    for index, val in enumerate(modified_states):
                        if len(modified_states) == 1:
                            break
                        if len(modified_states) > 1:
                            where = where[:len(where) - 1]
                            # print(where)
                            # where += ", "
                        where += modified_states[index] + ", "
                        if index == len(modified_states) - 1:
                            where = where[:len(where) - 2] + ")"

                    # print(where)
                    query = f"""WITH cte_funding AS(
                            SELECT sname AS state_name, year, funding
                            FROM "J.POULOS".state_fund),

                            cte_accidents AS (
                            SELECT COUNT(id) AS accidents, EXTRACT(year FROM start_time) AS year, state_name
                            FROM "J.POULOS".accident
                            GROUP BY state_name, EXTRACT(year FROM start_time))

                            SELECT * FROM cte_funding NATURAL JOIN cte_accidents
                            {where}
                            ORDER BY year"""

                    # for debugging purposes. A previous sate shows up but that doesn't screw up the sql code.
                    # ie if state1 was Alabama and state2 is arkansas you'll get ('Alabama', 'Alabama', 'Arkansas')
                    # Too tired to fix. But really, it doesn't matter.
                    # print(query)
                    #print(where)

                    # print(df_oracle2)
                    # wtf? Why aren't isn't the previ
                    df_oracle4 = pd.read_sql(query, con=oracle_db.connection)
                    df_oracle4 = df_oracle4[df_oracle4['STATE_NAME'] == states[len(states)-1]]

                    # Wtf? The dataframe printed completely ignores the previous state/funding values that were selected.
                    # I don't see how thats possible when the query that prints has the 2 different states?!?
                    st.write(df_oracle4)
                    # print(df_oracle4)
                    # for col in df_oracle4:
                    #     print(col)
                    #
                    # for val in df_oracle4['STATE_NAME']:
                    #     print(val)
                    # frames = [df_oracle2, df_oracle3]
                    # result = pd.concat(frames)
                    # st.write(result)

                    # df_oracle2['Key'] = 'trail1'
                    # df_oracle3['Key'] = 'trail2'

                    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
                    ax1.set_title('Funding')
                    ax1.set_ylabel('Dollar Amount')

                    ax2.set_title('Amount of Accidents', fontsize=12)
                    ax2.set_xlabel('Year', fontsize=12)
                    ax2.set_ylabel('Accidents')
                    # ax2.plot(df_oracle2['YEAR'], df_oracle3['YEAR'], df_oracle2['ACCIDENTS'], df_oracle3['ACCIDENTS'])
                    # ax1.plot(df_oracle2['FUNDING'], df_oracle3['FUNDING'])

                   ##This dataframe index sometimes gets screwed up dependin
                    df_oracle4 = df_oracle4.reset_index()
                    #st.write(df_oracle4)

                    for frame in [df_oracle2, df_oracle3, df_oracle4]:
                        ax1.plot(frame['YEAR'], frame['FUNDING'], label=frame['STATE_NAME'].loc[0])
                        ax2.plot(frame['YEAR'], frame['ACCIDENTS'], label=frame['STATE_NAME'].loc[0])

                    ax1.legend()
                    ax2.legend()


                    # df = pd.concat([df_oracle2, df_oracle3], keys=['trail1', 'trail2'])
                    # dfgroup = df.groupby(['YEAR', 'Key'])
                    # plt = dfgroup.sum().unstack('Key').plot()

                    # plt.subplots_adjust(bottom=0.000000000000000000001)
                    

                    for tick in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label, ax2.title,
                                ax2.xaxis.label, ax2.yaxis.label] + ax1.get_xticklabels() +
                                ax2.get_xticklabels() + ax1.get_yticklabels() + ax2.get_yticklabels()):
                        tick.set_fontsize(6)
                    ax2.set_xticks(df_oracle2['YEAR'])
                    ax1.set_xticks(df_oracle2['YEAR'])
                    #print(states)
                    #plt.legend(ax1.get_legend_handle_labels(), ax2.get_legend_handle_labels())

                    st.pyplot(fig=plt)

    def load_sidebar(self):
        l2 = Image.open('images/logo2.png')
        st.sidebar.image(l2, width = 250)

        """
        This section is for the elements in the sidebar
        """
        # State selection
        st.sidebar.header('State', anchor = None)
        self.state1 = st.sidebar.selectbox(
            "Select State", self.state_name    
        )

        self.state2 = st.sidebar.selectbox(
            "Select State 2", self.state_name    
        )

        self.state3 = st.sidebar.selectbox(
            "Select State 3", self.state_name    
        )

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

        # multiselect weather. passes the condition to the weather function
        st.sidebar.header('Weather', anchor = None)
        weather_multiselect = st.sidebar.multiselect(
            'Select Weather Condition',
            ['Rain', 'Snow', 'Partly Cloudy', 'Tornado', 'Clear', 'Scattered Clouds']
        )
        self.weather_condition(weather_multiselect)

        # multiselect temperature
        st.sidebar.header('Temperature', anchor = None)
        temperature_multiselect = st.sidebar.multiselect(
            'Select Temperature',
            ['00 - 34 °F', '35 - 69 °F', '70 - 100 °F']
        )
        self.temperature_condition(temperature_multiselect)

        # multiselect time
        time = 'Time'
        st.sidebar.header(time, anchor = None)
        time_multiselect = st.sidebar.multiselect(
            'Select Time',
            ['12:00 AM - 05:59 AM', '06:00 AM - 11:59 AM', 
            '12:00 PM - 05:59 PM', '06:00 PM - 11:59 PM']
        )
        self.time_condition(time_multiselect)

    def load_map(self, current_state):
       

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
        df_state = pd.DataFrame(columns = ['lon', 'lat'])

        # adds the state accident lon and lat to the state dataframe
        i = 0
        for row in self.cursor:
            lon = row[0]
            lat = row[1]
            temp1 = float(lon)
            temp2 = float(lat)
            df_state.loc[i] = [temp1, temp2]
            i += 1

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
                    get_position = '[lon, lat]',
                    radius = 200,
                    elevation_scale = 4,
                    elevation_range = [0, 1000],
                    pickable = True,
                    extruded = True,
                    get_color = '[200, 30, 0, 160]',
                    get_radius = 2000,
                ), pdk.Layer(
                    'ScatterplotLayer',
                    data = self.df_city,
                    get_position = '[lon, lat]',
                    radius = 200,
                    elevation_scale = 4,
                    elevation_range = [0, 1000],
                    pickable = True,
                    extruded = True,
                    get_color = '[400, 30, 0, 160]',
                    get_radius = 200,
                )
            ],
        ))
    
    def city(self, city_num):
        # user input
        str = "Enter city " + city_num
        name = st.text_input(str)

        # query the city input by user
        city = """SELECT * FROM city WHERE name = :city_name"""
        self.cursor.execute(city, city_name = name)

        # get the city latitude and longitude. This is to zoom the
        # the map to the location of the city
        city_coordinates = """SELECT c.latitude, c.longitude 
                              FROM "J.POULOS".city c
                              WHERE c.name = :city_name"""
        
        self.cursor.execute(city_coordinates, city_name = name)
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

        self.cursor.execute(city_accident_coordinates, city_name =  name)
        
        # adds the city lon and lat to the city dataframe
        i = 0
        for row in self.cursor:
            lon = row[0]
            lat = row[1]
            temp1 = float(lon)
            temp2 = float(lat)
            self.df_city.loc[i] = [temp1, temp2]
            i += 1

    def weather_condition(self, condition):
        # Gets all of the conditions from the weather selction box 
        # to pass to the query below. creates a comma separted string
        # of the conditions.
        for i in range(0, len(condition)):
            self.condition = self.condition + str(condition[i])
            if not i == len(condition) - 1:
                 self.condition = self.condition + ", "

        # Needs to be fixed.
        # query for getting accidents based on weather condition
        # currently only allows for a single selection from the checkbox.
        # additional conditions in the string are ignored. 
        if not len(condition) == 0:
            weather = """SELECT *
                        FROM "J.POULOS".Accident 
                        WHERE ROWNUM < 20 AND condition IN :wthr"""
            self.cursor.execute(weather, wthr =  self.condition)      

    def temperature_condition(self, temperature):
        # add queries and functionality
        # for temperature in the sidebar
        for i in range(0, len(temperature)):
            st.write(temperature)

    def time_condition(self, time):
        # add queries and functionality
        # for time in the sidebar
        for i in range(0, len(time)):
            st.write(time)

    def load_table(self):
        st.header('State Data', anchor = None)
        with st.expander("See details"):
            st.write('Add some additional text here')
            
        df_table = pd.DataFrame(
            np.random.randn(10, 5),
            columns=('col %d' % i for i in range(5))
        )
        st.table(df_table)

    def run(self):

        st.image(Image.open('images/logo.png'))
        self.load_sidebar()

        # creates a two column layout.
        col1, col2 = st.columns(2)
        
        with col1:
            # calls the state function. 
            # updates the left map to the state selected.
            self.update_state(self.state1)
            self.city("1")
            self.load_map(self.state1)

        with col2:
            # calls the state function. 
            # updates the right map to the state selected.
            self.update_state(self.state2)
            self.city("2")
            self.load_map(self.state2)

        self.load_graphs()
        self.load_table()
        
       