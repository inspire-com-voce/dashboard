import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pandas as pd
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

#Functions
from functions2 import validate_user

#Pages
from functions2 import login_page, main, descritiva_page




st.set_page_config(
    page_title="Dashboard Inspire",
    layout="wide",
    initial_sidebar_state="expanded"
)





if __name__ == "__main__":
    main()

        




        








