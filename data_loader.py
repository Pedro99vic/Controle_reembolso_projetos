import pandas as pd
import streamlit as st

@st.cache_data
def load_data(caminho):
    raw_data = pd.read_excel(caminho)
    return(raw_data)
