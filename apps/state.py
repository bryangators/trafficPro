import streamlit as st
import re
from hydralit import HydraHeadApp
from db import db_conn as oracle_db
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import altair as alt
from datetime import datetime


class State(HydraHeadApp):

    def run(self):
        st.title("State")

        # user input city name
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