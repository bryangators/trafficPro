import apps
import streamlit as st
from style.styles import page_style, over_theme
from hydralit import HydraApp

st.set_page_config(layout='wide', page_title='TrafficPro')


app = HydraApp(title='TrafficPro', 
               hide_streamlit_markers=True, 
               navbar_sticky=True, 
               use_navbar=True,
               navbar_animation=True,
               navbar_theme = over_theme)

app.add_app('Home', apps.Home(), is_home=True)
app.add_app('About', apps.About())
app.add_app('State', apps.State())
app.add_app('Contact', apps.Contact())
app.add_app("Logout", apps.LoginApp(title='Login'),is_login=True)
app.add_app("Signup", app=apps.SignUpApp(title='Signup'), is_unsecure=True)

# need this to get rid of hydralit default loader that is buggy
app.add_loader_app(apps.MyLoadingApp(delay=0))
user_access_level, username = app.check_access()

# menu setup for logged in and not logged in states
if user_access_level == 1:
    complex_nav = {
        'Home': ['Homes'],
        'State': ['State'],
        'About': ['About'],
        'Contact': ['Contact']
    }
else:
    complex_nav = {
        'Home': ['Home'],
        'About': ['About'],
        'Contact': ['Contact']
    }

app.run(complex_nav)
st.markdown(page_style, unsafe_allow_html=True)

    





