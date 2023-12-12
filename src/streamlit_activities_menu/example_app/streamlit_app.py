import os
import streamlit as st
from streamlit_activities_menu import build_activities_menu, get_available_activities

st.set_page_config(
    layout='wide',
    page_title='SSTC',
    page_icon='https://github.com/SITES-spectral/sstc-assets/blob/main/src/sstc_assets/favicons/SITES_favicon.png?raw=true',
    initial_sidebar_state='expanded',
    )


def run():
    working_directory = os.path.dirname(os.path.abspath(__file__))    

    LOGO_SIDEBAR_URL = "https://github.com/SITES-spectral/sstc-assets/blob/main/src/sstc_assets/logos/SITES_spectral_LOGO.png?raw=true"

    if LOGO_SIDEBAR_URL: st.sidebar.image(
            LOGO_SIDEBAR_URL,             
            caption= 'Swedish Infrastructure for Ecosystem Science (SITES) Spectral'
            )
        
 
        
    # Load the available services
    ACTIVITIES_FILEPATH = os.path.join(working_directory, "app_activities.yaml")
    ACTIVITIES_DIRPATH =  os.path.join(working_directory, "activities/" )

    # Load the yaml with core services as activities    
    core_activities =  get_available_activities(
        activities_filepath=os.path.abspath(ACTIVITIES_FILEPATH)        
    )
       
    build_activities_menu(
            activities_dict=core_activities, 
            label='**Activities:**', 
            key='activitiesMenu', 
            activities_dirpath=os.path.abspath(ACTIVITIES_DIRPATH),
            disabled=False
            )


if __name__ == '__main__':
    run()
else:
    st.error('The app failed initialization. Report issue to mantainers in github')