import streamlit as st
from gbqAccess import dfPortPolygons, dfAisMessages, dfShipTypes
from home import Home
from port import PortsMap
from messages import Messages
from relativeGeo import relativeGeo
import time
from analyseProcess import Analyse

st.set_page_config(page_title="Spire Maritime Data Analysis", page_icon=":ship:", layout="wide")

progressBar = st.progress(0)
for i in range (100):
    time.sleep(0.01)
    progressBar.progress(i+1)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

st.sidebar.header("Welcome to...")
st.sidebar.image(r"images/spire_maritime.png")
st.sidebar.markdown("___")

dashboard = st.sidebar.radio(
    "Please select the view that best fit your need:",
    ["Ports", "Vessels", 'Relative Geolocation'],
    index=None
)
st.sidebar.markdown("___")

process = st.sidebar.button("ANALYSE PROCESS SUMMARY", type="primary")
if process == True:
    Analyse()
    dashboard = None

luiz = st.sidebar.button("Luiz Francisco Dos Santos", type="secondary")
st.sidebar.markdown("___")
if luiz == True:
    dashboard = None
    Home()
    
    
if dashboard == "Ports":
   PortsMap(dfPortPolygons) 
elif dashboard == "Vessels":
   Messages(dfAisMessages, dfShipTypes, dfPortPolygons)
elif dashboard == "Relative Geolocation":
   relativeGeo(dfPortPolygons, dfAisMessages, dfShipTypes)
else:
    Home()
# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            stSidebarContent = padding-top: {padding_top: 0;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)