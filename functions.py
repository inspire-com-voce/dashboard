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
import plotly.express as px

#Pages

def login_page():
    st.title("Dashboard Bem Estar Inspire")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        valid, access_level, user_data = validate_user(email, password)

        if valid:
            st.session_state.access_level = access_level
            st.session_state.logged_in = True
            st.session_state.user_data = user_data  # Store user-specific data
            st.success(f"Logged in as {email} with access level: {access_level}")
        else:
            st.error("Invalid credentials")

def main():
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    st.sidebar.image('/home/henrique/Desktop/Gaia/Dash-Mel/Prancheta 1inspire.png', width = 250)
    st.sidebar.title("Navegação")

    # Add options in the sidebar for navigation
    page = st.sidebar.selectbox("Escolha a página", ["Login", "Métricas"])
    
    if page == "Login":
        login_page()
    elif page == "Métricas":
        descritiva_page()

if __name__ == '__main__':
    main()


#Functions

def validate_user(email, password):
    users_df = pd.read_csv("users.csv")
    print(users_df)  # Print the DataFrame for debugging purposes
    user = users_df[(users_df['email'] == email) & (users_df['password'] == password)]
    
    if not user.empty:
        access_level = user.iloc[0]['access']
        user_data = user.iloc[0]  # Get the data for the logged-in user
        return True, access_level, user_data
    else:
        st.error("empty")
        return False, None, None  # Return None for user_data when no user is found


def preprocess_data_admin(df):
    df = df.dropna()
    columns_to_map = ['bocaseca', 'respiracao', 'tremor', 'panico', 'panoutros', 'coracao', 'mompos', 
                            'iniciativa', 'desejo', 'animo', 'entusiasmo', 'valor', 'sentido', 'acalmar', 
                            'exagero', 'nervoso', 'impedir', 'emotivo', 'agitado', 'relaxar']

    mapping_dict = {'Bastante': 3, 'Sim': 2, 'Um pouco': 1, 'Não': 0}
    for col in columns_to_map:
        df[col] = df[col].map(mapping_dict)
    df.set_index('Nome', inplace=True)
            # Step 4: Use get_dummies on the Setor column
    df = pd.get_dummies(df, columns=['Setor'])
    df = pd.get_dummies(df, columns=['Cargo'])
    df = pd.get_dummies(df, columns=['Gênero'])

            # Step 5: Calculate the Body Mass Index (BMI) and save it as a new column
    df['altura'] = df['altura'] / 100  
    df['BMI'] = df['peso'] / (df['altura'] ** 2)

            # Step 6: Map the medicamento column values to 0 and 1
    df['medicamento'] = df['medicamento'].astype(int) 
    df['Setor_Marketing'] = df['Setor_Marketing'].astype(int)
    df['Setor_IT'] = df['Setor_IT'].astype(int)
    df['Setor_HR'] = df['Setor_HR'].astype(int)
    df['Setor_Finance'] = df['Setor_Finance'].astype(int) 
    df['Setor_Sales'] = df['Setor_Sales'].astype(int)
    df.drop(columns=['imc'], inplace=True)
    df.drop(columns=['Email'], inplace=True)

            # Step 7: Create the new columns based on the specified columns
    depressao_cols = ['mompos', 'iniciativa', 'desejo', 'animo', 'entusiasmo', 'valor', 'sentido']
    estresse_cols = ['acalmar', 'exagero', 'nervoso', 'impedir', 'emotivo', 'agitado', 'relaxar']
    ansiedade_cols = ['bocaseca', 'respiracao', 'tremor', 'panico', 'panoutros', 'coracao', 'mompos']
            
    df['Depressao'] = df[depressao_cols].sum(axis=1)
    df['Estresse'] = df[estresse_cols].sum(axis=1)
    df['Ansiedade'] = df[ansiedade_cols].sum(axis=1)

    return df

def preprocess_data_mkt(df):
            df = df.dropna()
            columns_to_map = ['bocaseca', 'respiracao', 'tremor', 'panico', 'panoutros', 'coracao', 'mompos', 
                            'iniciativa', 'desejo', 'animo', 'entusiasmo', 'valor', 'sentido', 'acalmar', 
                            'exagero', 'nervoso', 'impedir', 'emotivo', 'agitado', 'relaxar']

            mapping_dict = {'Bastante': 3, 'Sim': 2, 'Um pouco': 1, 'Não': 0}
            for col in columns_to_map:
                df[col] = df[col].map(mapping_dict)
            df.set_index('Nome', inplace=True)
            # Step 4: Use get_dummies on the Setor column
            df = pd.get_dummies(df, columns=['Setor'])
            df = pd.get_dummies(df, columns=['Cargo'])
            df = pd.get_dummies(df, columns=['Gênero'])

            # Step 5: Calculate the Body Mass Index (BMI) and save it as a new column
            df['altura'] = df['altura'] / 100  
            df['BMI'] = df['peso'] / (df['altura'] ** 2)

            # Step 6: Map the medicamento column values to 0 and 1
            df['medicamento'] = df['medicamento'].astype(int) 
            df['Setor_Marketing'] = df['Setor_Marketing'].astype(int)
            df['Setor_IT'] = df['Setor_IT'].astype(int)
            df['Setor_HR'] = df['Setor_HR'].astype(int)
            df['Setor_Finance'] = df['Setor_Finance'].astype(int) 
            df['Setor_Sales'] = df['Setor_Sales'].astype(int)
            df.drop(columns=['imc'], inplace=True)
            df.drop(columns=['Email'], inplace=True)
            df = df[df['Setor_Marketing'] == 1]

            # Step 7: Create the new columns based on the specified columns
            depressao_cols = ['mompos', 'iniciativa', 'desejo', 'animo', 'entusiasmo', 'valor', 'sentido']
            estresse_cols = ['acalmar', 'exagero', 'nervoso', 'impedir', 'emotivo', 'agitado', 'relaxar']
            ansiedade_cols = ['bocaseca', 'respiracao', 'tremor', 'panico', 'panoutros', 'coracao', 'mompos']
            
            df['Depressao'] = df[depressao_cols].sum(axis=1)
            df['Estresse'] = df[estresse_cols].sum(axis=1)
            df['Ansiedade'] = df[ansiedade_cols].sum(axis=1)

            return df


def preprocess_data_fin(df):
            df = df.dropna()
            columns_to_map = ['bocaseca', 'respiracao', 'tremor', 'panico', 'panoutros', 'coracao', 'mompos', 
                            'iniciativa', 'desejo', 'animo', 'entusiasmo', 'valor', 'sentido', 'acalmar', 
                            'exagero', 'nervoso', 'impedir', 'emotivo', 'agitado', 'relaxar']

            mapping_dict = {'Bastante': 3, 'Sim': 2, 'Um pouco': 1, 'Não': 0}
            for col in columns_to_map:
                df[col] = df[col].map(mapping_dict)
            df.set_index('Nome', inplace=True)
            # Step 4: Use get_dummies on the Setor column
            df = pd.get_dummies(df, columns=['Setor'])
            df = pd.get_dummies(df, columns=['Cargo'])
            df = pd.get_dummies(df, columns=['Gênero'])

            # Step 5: Calculate the Body Mass Index (BMI) and save it as a new column
            df['altura'] = df['altura'] / 100  
            df['BMI'] = df['peso'] / (df['altura'] ** 2)

            # Step 6: Map the medicamento column values to 0 and 1
            df['medicamento'] = df['medicamento'].astype(int) 
            df['Setor_Marketing'] = df['Setor_Marketing'].astype(int)
            df['Setor_IT'] = df['Setor_IT'].astype(int)
            df['Setor_HR'] = df['Setor_HR'].astype(int)
            df['Setor_Finance'] = df['Setor_Finance'].astype(int) 
            df['Setor_Sales'] = df['Setor_Sales'].astype(int)
            df.drop(columns=['imc'], inplace=True)
            df.drop(columns=['Email'], inplace=True)
            df = df[df['Setor_Finance'] == 1]

            # Step 7: Create the new columns based on the specified columns
            depressao_cols = ['mompos', 'iniciativa', 'desejo', 'animo', 'entusiasmo', 'valor', 'sentido']
            estresse_cols = ['acalmar', 'exagero', 'nervoso', 'impedir', 'emotivo', 'agitado', 'relaxar']
            ansiedade_cols = ['bocaseca', 'respiracao', 'tremor', 'panico', 'panoutros', 'coracao', 'mompos']
            
            df['Depressao'] = df[depressao_cols].sum(axis=1)
            df['Estresse'] = df[estresse_cols].sum(axis=1)
            df['Ansiedade'] = df[ansiedade_cols].sum(axis=1)

            return df


def preprocess_data_it(df):
            df = df.dropna()
            columns_to_map = ['bocaseca', 'respiracao', 'tremor', 'panico', 'panoutros', 'coracao', 'mompos', 
                            'iniciativa', 'desejo', 'animo', 'entusiasmo', 'valor', 'sentido', 'acalmar', 
                            'exagero', 'nervoso', 'impedir', 'emotivo', 'agitado', 'relaxar']

            mapping_dict = {'Bastante': 3, 'Sim': 2, 'Um pouco': 1, 'Não': 0}
            for col in columns_to_map:
                df[col] = df[col].map(mapping_dict)
            df.set_index('Nome', inplace=True)
            # Step 4: Use get_dummies on the Setor column
            df = pd.get_dummies(df, columns=['Setor'])
            df = pd.get_dummies(df, columns=['Cargo'])
            df = pd.get_dummies(df, columns=['Gênero'])

            # Step 5: Calculate the Body Mass Index (BMI) and save it as a new column
            df['altura'] = df['altura'] / 100  
            df['BMI'] = df['peso'] / (df['altura'] ** 2)

            # Step 6: Map the medicamento column values to 0 and 1
            df['medicamento'] = df['medicamento'].astype(int) 
            df['Setor_Marketing'] = df['Setor_Marketing'].astype(int)
            df['Setor_IT'] = df['Setor_IT'].astype(int)
            df['Setor_HR'] = df['Setor_HR'].astype(int)
            df['Setor_Finance'] = df['Setor_Finance'].astype(int) 
            df['Setor_Sales'] = df['Setor_Sales'].astype(int)
            df.drop(columns=['imc'], inplace=True)
            df.drop(columns=['Email'], inplace=True)
            df = df[df['Setor_IT'] == 1]

            # Step 7: Create the new columns based on the specified columns
            depressao_cols = ['mompos', 'iniciativa', 'desejo', 'animo', 'entusiasmo', 'valor', 'sentido']
            estresse_cols = ['acalmar', 'exagero', 'nervoso', 'impedir', 'emotivo', 'agitado', 'relaxar']
            ansiedade_cols = ['bocaseca', 'respiracao', 'tremor', 'panico', 'panoutros', 'coracao', 'mompos']
            
            df['Depressao'] = df[depressao_cols].sum(axis=1)
            df['Estresse'] = df[estresse_cols].sum(axis=1)
            df['Ansiedade'] = df[ansiedade_cols].sum(axis=1)

            return df


def preprocess_data_sales(df):
            df = df.dropna()
            columns_to_map = ['bocaseca', 'respiracao', 'tremor', 'panico', 'panoutros', 'coracao', 'mompos', 
                            'iniciativa', 'desejo', 'animo', 'entusiasmo', 'valor', 'sentido', 'acalmar', 
                            'exagero', 'nervoso', 'impedir', 'emotivo', 'agitado', 'relaxar']

            mapping_dict = {'Bastante': 3, 'Sim': 2, 'Um pouco': 1, 'Não': 0}
            for col in columns_to_map:
                df[col] = df[col].map(mapping_dict)
            df.set_index('Nome', inplace=True)
            # Step 4: Use get_dummies on the Setor column
            df = pd.get_dummies(df, columns=['Setor'])
            df = pd.get_dummies(df, columns=['Cargo'])
            df = pd.get_dummies(df, columns=['Gênero'])

            # Step 5: Calculate the Body Mass Index (BMI) and save it as a new column
            df['altura'] = df['altura'] / 100  
            df['BMI'] = df['peso'] / (df['altura'] ** 2)

            # Step 6: Map the medicamento column values to 0 and 1
            df['medicamento'] = df['medicamento'].astype(int) 
            df['Setor_Marketing'] = df['Setor_Marketing'].astype(int)
            df['Setor_IT'] = df['Setor_IT'].astype(int)
            df['Setor_HR'] = df['Setor_HR'].astype(int)
            df['Setor_Finance'] = df['Setor_Finance'].astype(int) 
            df['Setor_Sales'] = df['Setor_Sales'].astype(int)
            df.drop(columns=['imc'], inplace=True)
            df.drop(columns=['Email'], inplace=True)
            df = df[df['Setor_Sales'] == 1]

            # Step 7: Create the new columns based on the specified columns
            depressao_cols = ['mompos', 'iniciativa', 'desejo', 'animo', 'entusiasmo', 'valor', 'sentido']
            estresse_cols = ['acalmar', 'exagero', 'nervoso', 'impedir', 'emotivo', 'agitado', 'relaxar']
            ansiedade_cols = ['bocaseca', 'respiracao', 'tremor', 'panico', 'panoutros', 'coracao', 'mompos']
            
            df['Depressao'] = df[depressao_cols].sum(axis=1)
            df['Estresse'] = df[estresse_cols].sum(axis=1)
            df['Ansiedade'] = df[ansiedade_cols].sum(axis=1)

            return df


def preprocess_data_rh(df):
                df = df.dropna()
                columns_to_map = ['bocaseca', 'respiracao', 'tremor', 'panico', 'panoutros', 'coracao', 'mompos', 
                                'iniciativa', 'desejo', 'animo', 'entusiasmo', 'valor', 'sentido', 'acalmar', 
                                'exagero', 'nervoso', 'impedir', 'emotivo', 'agitado', 'relaxar']

                mapping_dict = {'Bastante': 3, 'Sim': 2, 'Um pouco': 1, 'Não': 0}
                for col in columns_to_map:
                    df[col] = df[col].map(mapping_dict)
                df.set_index('Nome', inplace=True)
                # Step 4: Use get_dummies on the Setor column
                df = pd.get_dummies(df, columns=['Setor'])
                df = pd.get_dummies(df, columns=['Cargo'])
                df = pd.get_dummies(df, columns=['Gênero'])

                # Step 5: Calculate the Body Mass Index (BMI) and save it as a new column
                df['altura'] = df['altura'] / 100  
                df['BMI'] = df['peso'] / (df['altura'] ** 2)

                # Step 6: Map the medicamento column values to 0 and 1
                df['medicamento'] = df['medicamento'].astype(int) 
                df['Setor_Marketing'] = df['Setor_Marketing'].astype(int)
                df['Setor_IT'] = df['Setor_IT'].astype(int)
                df['Setor_HR'] = df['Setor_HR'].astype(int)
                df['Setor_Finance'] = df['Setor_Finance'].astype(int) 
                df['Setor_Sales'] = df['Setor_Sales'].astype(int)
                df.drop(columns=['imc'], inplace=True)
                df.drop(columns=['Email'], inplace=True)
                df = df[df['Setor_HR'] == 1]

                # Step 7: Create the new columns based on the specified columns
                depressao_cols = ['mompos', 'iniciativa', 'desejo', 'animo', 'entusiasmo', 'valor', 'sentido']
                estresse_cols = ['acalmar', 'exagero', 'nervoso', 'impedir', 'emotivo', 'agitado', 'relaxar']
                ansiedade_cols = ['bocaseca', 'respiracao', 'tremor', 'panico', 'panoutros', 'coracao', 'mompos']
                
                df['Depressao'] = df[depressao_cols].sum(axis=1)
                df['Estresse'] = df[estresse_cols].sum(axis=1)
                df['Ansiedade'] = df[ansiedade_cols].sum(axis=1)

                return df


# Define the main dashboard page
def descritiva_page():
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    import pandas as pd
    import requests
    st.title('Dashboard Inspire')


    #Notion credentials
    NOTION_TOKEN = "secret_BL3kRZyHDQKu0tHNn0lHiHdl7ExPYO3Rq3dOmwaKgS7"
    DATABASE_ID = "07866cdaf4884048ac3db6e357d1ecec"

    headers = {
        "Authorization": "Bearer " + NOTION_TOKEN,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }


    #Defining get info from Notion
    def get_pages(num_pages=None):
        """
        If num_pages is None, get all pages, otherwise just the defined number.
        """
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

        get_all = num_pages is None
        page_size = 100 if get_all else num_pages

        payload = {"page_size": page_size}
        response = requests.post(url, json=payload, headers=headers)

        data = response.json()

        # Comment this out to dump all data to a file
        # import json
        # with open('db.json', 'w', encoding='utf8') as f:
        #    json.dump(data, f, ensure_ascii=False, indent=4)

        results = data["results"]
        while data["has_more"] and get_all:
            payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
            url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            results.extend(data["results"])

        return results
    #Getting info
    pages = get_pages()

    # Initialize an empty list to store row data
    rows_data = []

    # Iterate through each page using the index
    for i in range(len(pages)):
        page = pages[i]
        row_data = {
            'Name': page['properties']['Name']['title'][0]['plain_text'] if 'Name' in page['properties'] and 'title' in page['properties']['Name'] and page['properties']['Name']['title'] else None,
            'Email': page['properties']['Email']['email'] if 'Email' in page['properties'] and 'email' in page['properties']['Email'] else None,
            'Gênero': page['properties']['Gênero']['rich_text'][0]['plain_text'] if 'Gênero' in page['properties'] and 'rich_text' in page['properties']['Gênero'] and page['properties']['Gênero']['rich_text'] else None,
            'Idade': page['properties']['Idade']['number'] if 'Idade' in page['properties'] and 'number' in page['properties']['Idade'] else None,
            'Burnout': page['properties']['Burnout']['rich_text'][0]['plain_text'] if 'Burnout' in page['properties'] and 'rich_text' in page['properties']['Burnout'] and page['properties']['Burnout']['rich_text'] else None,
            'Medicamento': page['properties']['Medicamento']['rich_text'][0]['plain_text'] if 'Medicamento' in page['properties'] and 'rich_text' in page['properties']['Medicamento'] and page['properties']['Medicamento']['rich_text'] else None,
            'Estresse': page['properties']['Estresse']['number'] if 'Estresse' in page['properties'] and 'number' in page['properties']['Estresse'] else None,
            'Ansiedade': page['properties']['Ansiedade']['number'] if 'Ansiedade' in page['properties'] and 'number' in page['properties']['Ansiedade'] else None,
            'Depressão': page['properties']['Depressão']['number'] if 'Depressão' in page['properties'] and 'number' in page['properties']['Depressão'] else None,
            'IMC': page['properties']['IMC']['number'] if 'IMC' in page['properties'] and 'number' in page['properties']['IMC'] else None,
            'Senha': page['properties']['Senha']['rich_text'][0]['plain_text'] if 'Senha' in page['properties'] and 'rich_text' in page['properties']['Senha'] and page['properties']['Senha']['rich_text'] else None,
            'Bem Estar': page['properties']['Bem Estar']['number'] if 'Bem Estar' in page['properties'] and 'number' in page['properties']['Bem Estar'] else None
        }
        rows_data.append(row_data)



    # Create a DataFrame from the fetched data
    df = pd.DataFrame(rows_data)
    # Check if the user is logged in
    if not st.session_state.get("logged_in"):
        st.warning("You need to login first.")
        return
    



    # Display content based on the access level
    if st.session_state.access_level == "admin":

      
        # Opção para upload do arquivo CSV
        uploaded_file = df

        if uploaded_file is not None:
            
            
            # Lendo o arquivo CSV
            df = uploaded_file
            
            # Realizando o pré-processamento dos dados
            df_processed = preprocess_data_admin(df)

            #Geral
            mean_values1 = df_processed[['Ansiedade', 'Depressao', 'Estresse']].mean()


            # Calcular o valor final conforme a fórmula fornecida
            final_value1 = (mean_values1.sum()) / (63)
            result1 = final_value1

            #Depressão
            mean_values2 = df_processed[['Depressao']].mean()

            # Calcular o valor final conforme a fórmula fornecida
            final_value2 = (mean_values2.sum()) / (21)
            result2 = 1 - final_value2

            #Estresse
            mean_values3 = df_processed[['Estresse']].mean()

            # Calcular o valor final conforme a fórmula fornecida
            final_value3 = (mean_values3.sum()) / (21)
            result3 = 1 - final_value3

            #Ansiedade
            mean_values4 = df_processed[['Ansiedade']].mean()

            # Calcular o valor final conforme a fórmula fornecida
            final_value4 = (mean_values4.sum()) / (21)
            result4 = 1 - final_value4

            y_scale = alt.Scale(domain=(0, 100))

            st.header("Métricas da equipe: ")
            #índices
            cola, colb, colc, cold = st.columns(4)
            
            with cola:
                st.subheader("Índice Bem Estar:")
                st.write(f"{result1*100:.2f}%")
              
            with colb:
                st.subheader("Nível de Depressão:")
                st.write(f"{result2*100:.2f}%")
                

            with colc:
                st.subheader("Nível de Estresse:")
                st.write(f"{result3*100:.2f}%")
               

            with cold:
                st.subheader("Nível de Ansiedade:")
                st.write(f"{result4*100:.2f}%")
        

            # Padronizando os dados
            scaler = StandardScaler()
            df_standardized = pd.DataFrame(scaler.fit_transform(df_processed), columns=df_processed.columns, index=df_processed.index)


            # Botão para realizar análise descritiva
            # Identifying the dummy columns in the DataFrame
            setor_dummies = [col for col in df_processed.columns if col.startswith('Setor_')]
            cargo_dummies = [col for col in df_processed.columns if col.startswith('Cargo_')]
            genero_dummies = [col for col in df_processed.columns if col.startswith('Gênero_')]

            # Creating a list of aggregation functions for each metric
            aggregation_functions = {
                'Ansiedade': ['mean', 'median', 'std'],
                'Depressao': ['mean', 'median', 'std'],
                'Estresse': ['mean', 'median', 'std']
            }

            # Creating the list of metrics to be plotted
            metrics = ['Ansiedade', 'Depressao', 'Estresse']

            # Aggregating data using dummy columns for setor
            metrics_by_sector = df_processed.groupby(setor_dummies).agg(aggregation_functions).reset_index()
            metrics_by_sector.columns = ['_'.join(col).strip() if col != ('', '') else 'Setor' for col in metrics_by_sector.columns]

            # Setor
            setor_filtered_df = df_processed[df_processed[setor_dummies].eq(1).any(axis=1)]
            setor_filtered_df.set_index(setor_filtered_df[setor_dummies].apply(lambda x: x[x == 1].index[0], axis=1), inplace=True)
            setor_filtered_df.drop(columns=setor_dummies, inplace=True)

            # Cargo
            cargo_filtered_df = df_processed[df_processed[cargo_dummies].eq(1).any(axis=1)]
            cargo_filtered_df.set_index(cargo_filtered_df[cargo_dummies].apply(lambda x: x[x == 1].index[0], axis=1), inplace=True)
            cargo_filtered_df.drop(columns=cargo_dummies, inplace=True)

            # Gênero
            genero_filtered_df = df_processed[df_processed[genero_dummies].eq(1).any(axis=1)]
            genero_filtered_df.set_index(genero_filtered_df[genero_dummies].apply(lambda x: x[x == 1].index[0], axis=1), inplace=True)
            genero_filtered_df.drop(columns=genero_dummies, inplace=True)

            # Sidebar selector
            selected_view = st.sidebar.radio("Selecione a visão:", ["Cargo", "Gênero", "Setor"])

            # Display charts based on the selected view
            if selected_view == "Cargo":
                filtered_df = cargo_filtered_df
                title_prefix = "Cargo"
            elif selected_view == "Gênero":
                filtered_df = genero_filtered_df
                title_prefix = "Gênero"
            else:
                filtered_df = setor_filtered_df
                title_prefix = "Setor"

            # Display the charts
            cola, colb, colc = st.columns(3)
            with cola:
                st.subheader(f"Distribuição por {title_prefix}:")
                for metric in metrics:
                    map_metric = {'Depressao':'Depressão','Ansiedade':'Ansiedade','Estresse':'Estresse'}
                    import plotly.express as px
                    fig = px.pie(
                        values=filtered_df[metric],
                        names=filtered_df.index,
                        title=f"{map_metric[metric]} por {title_prefix}",
                        width=520, height=520, hole=0.5
                    )
                    st.plotly_chart(fig)

    elif st.session_state.access_level == "mkt":

        # Título do Streamlit
        st.title('Mapeamento de perfil de funcionário - Setor de Marketing')

        # Opção para upload do arquivo CSV
        uploaded_file = df

        if uploaded_file is not None:
            # Lendo o arquivo CSV
            df = uploaded_file
            
            # Realizando o pré-processamento dos dados
            df_processed = preprocess_data_mkt(df)



            # Botão para realizar análise descritiva
            if st.button('Visualização'):
                

                # Agrupando por setor e calculando as métricas solicitadas
                # Identificando as colunas dummy de setor no DataFrame
                setor_dummies = [col for col in df_processed.columns if col.startswith('Cargo_')]

                # Criando a lista de funções de agregação para cada métrica
                aggregation_functions = {
                    'Ansiedade': ['mean', 'median', 'std'],
                    'Depressao': ['mean', 'median', 'std'],
                    'Estresse': ['mean', 'median', 'std']
                }

                # Agregando os dados usando as colunas dummy de setor
                metrics_by_sector = df_processed.groupby(setor_dummies).agg(aggregation_functions).reset_index()

                # Renomeando as colunas para melhor visualização
                metrics_by_sector.columns = ['_'.join(col).strip() if col != ('', '') else 'Setor' for col in metrics_by_sector.columns]

               


                # Filtrando o DataFrame para obter apenas as linhas onde as colunas Setor_ têm valor 1
                setor_filtered_df = df_processed[df_processed[setor_dummies].eq(1).any(axis=1)]

                # Definindo o índice do novo DataFrame com o nome da coluna Setor_ que tem valor 1
                setor_filtered_df.set_index(setor_filtered_df[setor_dummies].apply(lambda x: x[x == 1].index[0], axis=1), inplace=True)

                # Removendo as colunas Setor_ do novo DataFrame
                setor_filtered_df.drop(columns=setor_dummies, inplace=True)

               
          
                import plotly.express as px

                setor_filtered_df['Geral'] = setor_filtered_df['Ansiedade'] + setor_filtered_df['Depressao'] + setor_filtered_df['Estresse']
                metrics = ['Ansiedade', 'Depressao', 'Estresse','Geral']
                col1, col2, col3, col4 = st.columns(4)
                cols = [col1, col2, col3, col4]

                # Criando gráficos de pizza para cada métrica
                for col, metric in zip(cols, metrics):
                    with col:
                        fig = px.pie(
                                values=setor_filtered_df[metric],
                                names=setor_filtered_df.index,
                                title=f"{metric} por Cargo",
                                height=320,
                                width=320,
                                hole=0.5,
                            )

                            # Exibindo o gráfico no Streamlit
                        st.plotly_chart(fig)

    
    elif st.session_state.access_level == "finance":

        # Título do Streamlit
        st.title('Mapeamento de perfil de funcionário - Setor Financeiro')

        # Opção para upload do arquivo CSV
        uploaded_file = df

        if uploaded_file is not None:
            # Lendo o arquivo CSV
            df = uploaded_file
            
            # Realizando o pré-processamento dos dados
            df_processed = preprocess_data_fin(df)


            # Botão para realizar análise descritiva
            if st.button('Visualização'):

                # Agrupando por setor e calculando as métricas solicitadas
                # Identificando as colunas dummy de setor no DataFrame
                setor_dummies = [col for col in df_processed.columns if col.startswith('Cargo_')]

                # Criando a lista de funções de agregação para cada métrica
                aggregation_functions = {
                    'Ansiedade': ['mean', 'median', 'std'],
                    'Depressao': ['mean', 'median', 'std'],
                    'Estresse': ['mean', 'median', 'std']
                }

                # Agregando os dados usando as colunas dummy de setor
                metrics_by_sector = df_processed.groupby(setor_dummies).agg(aggregation_functions).reset_index()

                # Renomeando as colunas para melhor visualização
                metrics_by_sector.columns = ['_'.join(col).strip() if col != ('', '') else 'Setor' for col in metrics_by_sector.columns]


                # Filtrando o DataFrame para obter apenas as linhas onde as colunas Setor_ têm valor 1
                setor_filtered_df = df_processed[df_processed[setor_dummies].eq(1).any(axis=1)]

                # Definindo o índice do novo DataFrame com o nome da coluna Setor_ que tem valor 1
                setor_filtered_df.set_index(setor_filtered_df[setor_dummies].apply(lambda x: x[x == 1].index[0], axis=1), inplace=True)

                # Removendo as colunas Setor_ do novo DataFrame
                setor_filtered_df.drop(columns=setor_dummies, inplace=True)


                import plotly.express as px

                setor_filtered_df['Geral'] = setor_filtered_df['Ansiedade'] + setor_filtered_df['Depressao'] + setor_filtered_df['Estresse']
                metrics = ['Ansiedade', 'Depressao', 'Estresse','Geral']
                col1, col2, col3, col4 = st.columns(4)
                cols = [col1, col2, col3, col4]

                import plotly.express as px
                # Criando gráficos de pizza para cada métrica
                for col, metric in zip(cols, metrics):
                    with col:
                        fig = px.pie(
                                values=setor_filtered_df[metric],
                                names=setor_filtered_df.index,
                                title=f"{metric} por Cargo",
                                height=320,
                                width=320,
                                hole=0.5,
                            )

                            # Exibindo o gráfico no Streamlit
                        st.plotly_chart(fig)

    elif st.session_state.access_level == "it":
        # Display user content
        

        # Título do Streamlit
        st.title('Mapeamento de perfil de funcionário - Setor de TI')

        # Opção para upload do arquivo CSV
        uploaded_file = df

        if uploaded_file is not None:
            # Lendo o arquivo CSV
            df = uploaded_file
            
            # Realizando o pré-processamento dos dados
            df_processed = preprocess_data_it(df)


            # Botão para realizar análise descritiva
            if st.button('Visualização'):


                # Agrupando por setor e calculando as métricas solicitadas
                # Identificando as colunas dummy de setor no DataFrame
                setor_dummies = [col for col in df_processed.columns if col.startswith('Cargo_')]

                # Criando a lista de funções de agregação para cada métrica
                aggregation_functions = {
                    'Ansiedade': ['mean', 'median', 'std'],
                    'Depressao': ['mean', 'median', 'std'],
                    'Estresse': ['mean', 'median', 'std']
                }

                # Agregando os dados usando as colunas dummy de setor
                metrics_by_sector = df_processed.groupby(setor_dummies).agg(aggregation_functions).reset_index()

                # Renomeando as colunas para melhor visualização
                metrics_by_sector.columns = ['_'.join(col).strip() if col != ('', '') else 'Setor' for col in metrics_by_sector.columns]

                # Filtrando o DataFrame para obter apenas as linhas onde as colunas Setor_ têm valor 1
                setor_filtered_df = df_processed[df_processed[setor_dummies].eq(1).any(axis=1)]

                # Definindo o índice do novo DataFrame com o nome da coluna Setor_ que tem valor 1
                setor_filtered_df.set_index(setor_filtered_df[setor_dummies].apply(lambda x: x[x == 1].index[0], axis=1), inplace=True)

                # Removendo as colunas Setor_ do novo DataFrame
                setor_filtered_df.drop(columns=setor_dummies, inplace=True)


                import plotly.express as px

                # Lista de métricas a serem plotadas
                setor_filtered_df['Geral'] = setor_filtered_df['Ansiedade'] + setor_filtered_df['Depressao'] + setor_filtered_df['Estresse']
                metrics = ['Ansiedade', 'Depressao', 'Estresse','Geral']
                col1, col2, col3, col4 = st.columns(4)
                cols = [col1, col2, col3, col4]

                import plotly.express as px
                # Criando gráficos de pizza para cada métrica
                for col, metric in zip(cols, metrics):
                    with col:
                        fig = px.pie(
                                values=setor_filtered_df[metric],
                                names=setor_filtered_df.index,
                                title=f"{metric} por Cargo",
                                height=320,
                                width=320,
                                hole=0.5,
                            )

                            # Exibindo o gráfico no Streamlit
                        st.plotly_chart(fig)
                

    
    elif st.session_state.access_level == "sales":

        # Título do Streamlit
        st.title('Mapeamento de perfil de funcionário - Setor de Vendas')

        # Opção para upload do arquivo CSV
        uploaded_file = df

        if uploaded_file is not None:
            # Lendo o arquivo CSV
            df = uploaded_file
            
            # Realizando o pré-processamento dos dados
            df_processed = preprocess_data_sales(df)



            # Botão para realizar análise descritiva
            if st.button('Visualização'):

                # Agrupando por setor e calculando as métricas solicitadas
                # Identificando as colunas dummy de setor no DataFrame
                setor_dummies = [col for col in df_processed.columns if col.startswith('Cargo_')]

                # Criando a lista de funções de agregação para cada métrica
                aggregation_functions = {
                    'Ansiedade': ['mean', 'median', 'std'],
                    'Depressao': ['mean', 'median', 'std'],
                    'Estresse': ['mean', 'median', 'std']
                }

                # Agregando os dados usando as colunas dummy de setor
                metrics_by_sector = df_processed.groupby(setor_dummies).agg(aggregation_functions).reset_index()

                # Renomeando as colunas para melhor visualização
                metrics_by_sector.columns = ['_'.join(col).strip() if col != ('', '') else 'Setor' for col in metrics_by_sector.columns]

                # Filtrando o DataFrame para obter apenas as linhas onde as colunas Setor_ têm valor 1
                setor_filtered_df = df_processed[df_processed[setor_dummies].eq(1).any(axis=1)]

                # Definindo o índice do novo DataFrame com o nome da coluna Setor_ que tem valor 1
                setor_filtered_df.set_index(setor_filtered_df[setor_dummies].apply(lambda x: x[x == 1].index[0], axis=1), inplace=True)

                # Removendo as colunas Setor_ do novo DataFrame
                setor_filtered_df.drop(columns=setor_dummies, inplace=True)


                # Lista de métricas a serem plotadas
                setor_filtered_df['Geral'] = setor_filtered_df['Ansiedade'] + setor_filtered_df['Depressao'] + setor_filtered_df['Estresse']
                metrics = ['Ansiedade', 'Depressao', 'Estresse','Geral']
                col1, col2, col3, col4 = st.columns(4)
                cols = [col1, col2, col3, col4]

                import plotly.express as px
                # Criando gráficos de pizza para cada métrica
                for col, metric in zip(cols, metrics):
                    with col:
                        fig = px.pie(
                                values=setor_filtered_df[metric],
                                names=setor_filtered_df.index,
                                title=f"{metric} por Cargo",
                                height=320,
                                width=320,
                                hole=0.5,
                            )

                            # Exibindo o gráfico no Streamlit
                        st.plotly_chart(fig)
       
    elif st.session_state.access_level == "rh":
            # Display user content
            # Função para pré-processamento de dados
            



            # Título do Streamlit
            st.title('Mapeamento de perfil de funcionário - Setor de RH')

            # Opção para upload do arquivo CSV
            uploaded_file = df

            if uploaded_file is not None:
                # Lendo o arquivo CSV
                df = uploaded_file
                
                # Realizando o pré-processamento dos dados
                df_processed = preprocess_data_rh(df)


                # Botão para realizar análise descritiva
                if st.button('Visualização'):

                    # Agrupando por setor e calculando as métricas solicitadas
                    # Identificando as colunas dummy de setor no DataFrame
                    setor_dummies = [col for col in df_processed.columns if col.startswith('Cargo_')]

                    # Criando a lista de funções de agregação para cada métrica
                    aggregation_functions = {
                        'Ansiedade': ['mean', 'median', 'std'],
                        'Depressao': ['mean', 'median', 'std'],
                        'Estresse': ['mean', 'median', 'std']
                    }

                    # Agregando os dados usando as colunas dummy de setor
                    metrics_by_sector = df_processed.groupby(setor_dummies).agg(aggregation_functions).reset_index()

                    # Renomeando as colunas para melhor visualização
                    metrics_by_sector.columns = ['_'.join(col).strip() if col != ('', '') else 'Setor' for col in metrics_by_sector.columns]


                    # Filtrando o DataFrame para obter apenas as linhas onde as colunas Setor_ têm valor 1
                    setor_filtered_df = df_processed[df_processed[setor_dummies].eq(1).any(axis=1)]

                    # Definindo o índice do novo DataFrame com o nome da coluna Setor_ que tem valor 1
                    setor_filtered_df.set_index(setor_filtered_df[setor_dummies].apply(lambda x: x[x == 1].index[0], axis=1), inplace=True)

                    # Removendo as colunas Setor_ do novo DataFrame
                    setor_filtered_df.drop(columns=setor_dummies, inplace=True)


                    # Lista de métricas a serem plotadas
                    setor_filtered_df['Geral'] = setor_filtered_df['Ansiedade'] + setor_filtered_df['Depressao'] + setor_filtered_df['Estresse']
                    metrics = ['Ansiedade', 'Depressao', 'Estresse','Geral']
                    pretty_map = [{'Depressao' : 'Depressão'}]

                    col1, col2, col3, col4 = st.columns(4)
                    cols = [col1, col2, col3, col4]

                    import plotly.express as px

                    # Assuming you have DataFrame variable setor_filtered_df and metrics defined

                    for col, metric in zip(cols, metrics):
                        with col:
                            fig = px.pie(
                                values=setor_filtered_df[metric],
                                names=setor_filtered_df.index,
                                title=f"{metric} por Cargo",
                                height=320,
                                width=320,
                                hole=0.5,
                            )

                            # Exibindo o gráfico no Streamlit
                            st.plotly_chart(fig)


    elif st.session_state.access_level == "user":
            # Get user-specific data
            user_data = st.session_state.user_data

            # Display user-specific information
            st.subheader(f"Suas informações, {user_data['Nome']}")

           
            y_scale = alt.Scale(domain=(0, 100))

            # Create bar charts for each value
            cola1, colb1, colc1, cold1 = st.columns(4)

            with cola1:
                st.subheader("Índice Bem Estar:")
                st.write(user_data['bem_estar'])
                chart_bem_estar = alt.Chart(pd.DataFrame({'Bem Estar': [user_data['bem_estar']]})).mark_bar().encode(
                    x=alt.X('Bem Estar:Q', title='Bem Estar'),
                    y=alt.Y('Bem Estar:Q', scale=y_scale, axis=None)
                )
                st.altair_chart(chart_bem_estar, use_container_width=True)

            with colb1:
                st.subheader("Nível de Depressão:")
                st.write(user_data['depressao'])
                chart_depressao = alt.Chart(pd.DataFrame({'Depressão': [user_data['depressao']]})).mark_bar().encode(
                    x=alt.X('Depressão:Q', title='Depressão'),
                    y=alt.Y('Depressão:Q', scale=y_scale, axis=None)
                )
                st.altair_chart(chart_depressao, use_container_width=True)

            with colc1:
                st.subheader("Nível de Estresse:")
                st.write(user_data['estresse'])
                chart_estresse = alt.Chart(pd.DataFrame({'Estresse': [user_data['estresse']]})).mark_bar().encode(
                    x=alt.X('Estresse:Q', title='Estresse'),
                    y=alt.Y('Estresse:Q', scale=y_scale, axis=None)
                )
                st.altair_chart(chart_estresse, use_container_width=True)

            with cold1:
                st.subheader("Nível de Ansiedade:")
                st.write(user_data['ansiedade'])
                chart_ansiedade = alt.Chart(pd.DataFrame({'Ansiedade': [user_data['ansiedade']]})).mark_bar().encode(
                    x=alt.X('Ansiedade:Q', title='Ansiedade'),
                    y=alt.Y('Ansiedade:Q', scale=y_scale, axis=None)
                )
                st.altair_chart(chart_ansiedade, use_container_width=True)
            



if __name__ == '__main__':
    main()