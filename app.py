import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from streamlit_gsheets import GSheetsConnection
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

#Functions
from functions2 import validate_user, preprocess_data_admin, preprocess_data_fin, preprocess_data_it, preprocess_data_mkt, preprocess_data_rh, preprocess_data_sales

#Pages
from functions2 import login_page, main, descritiva_page










if __name__ == "__main__":
    main()

        




        








