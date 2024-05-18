import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pandas as pd
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import date, datetime

#Pages

def login_page():
    st.title("Dashboard Bem Estar")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        valid, access_level, user_data = validate_user(email, password)

        if valid:
            st.session_state.access_level = access_level
            st.session_state.logged_in = True
            st.session_state.user_data = user_data  # Store user-specific data
            st.success(f"Logado com sucesso. Selecione a página de métricas à esquerda.")
        else:
            st.error("Credenciais inválidas.")

avaliados = []





def main():
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    st.sidebar.title("Navegação")

    # Add options in the sidebar for navigation
    page = st.sidebar.selectbox("Escolha a página", ["Login", "Métricas","Clima Organizacional"])
    
    if page == "Login":
        login_page()
    elif page == "Métricas":
        descritiva_page()
    elif page == "Clima Organizacional":
        clima_org()

if __name__ == '__main__':
    main()


#Functions

def validate_user(email, password):

    import pandas as pd
    import requests
    import streamlit as st

    #Notion credentials
    NOTION_TOKEN = "secret_BL3kRZyHDQKu0tHNn0lHiHdl7ExPYO3Rq3dOmwaKgS7"
    DATABASE_ID = "07866cdaf4884048ac3db6e357d1ecec"
    DATABASE_ID2 = "dd433aff401546aba3776b353e9391cb"

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
    
    def get_pages2(num_pages=None):
            """
            If num_pages is None, get all pages, otherwise just the defined number.
            """
            url = f"https://api.notion.com/v1/databases/{DATABASE_ID2}/query"

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

    pages2 = get_pages2()

        # Initialize an empty list to store row data
    rows_data = []

        # Iterate through each page using the index
    for i in range(len(pages)):
            page = pages[i]
            row_data = {
                'Nome': page['properties']['Name']['title'][0]['plain_text'] if 'Name' in page['properties'] and 'title' in page['properties']['Name'] and page['properties']['Name']['title'] else None,
                'email': page['properties']['Email']['email'] if 'Email' in page['properties'] and 'email' in page['properties']['Email'] else None,
                'Burnout': page['properties']['Burnout']['rich_text'][0]['plain_text'] if 'Burnout' in page['properties'] and 'rich_text' in page['properties']['Burnout'] and page['properties']['Burnout']['rich_text'] else None,
                'estresse': page['properties']['Estresse']['number'] if 'Estresse' in page['properties'] and 'number' in page['properties']['Estresse'] else None,
                'ansiedade': page['properties']['Ansiedade']['number'] if 'Ansiedade' in page['properties'] and 'number' in page['properties']['Ansiedade'] else None,
                'depressao': page['properties']['Depressão']['number'] if 'Depressão' in page['properties'] and 'number' in page['properties']['Depressão'] else None,
                'IMC': page['properties']['IMC']['number'] if 'IMC' in page['properties'] and 'number' in page['properties']['IMC'] else None,
                'access': page['properties']['access']['rich_text'][0]['plain_text'] if 'access' in page['properties'] and 'rich_text' in page['properties']['access'] else None,
                'password': page['properties']['Senha']['rich_text'][0]['plain_text'] if 'Senha' in page['properties'] and 'rich_text' in page['properties']['Senha'] and page['properties']['Senha']['rich_text'] else None,
                'bem_estar': page['properties']['Bem Estar']['number'] if 'Bem Estar' in page['properties'] and 'number' in page['properties']['Bem Estar'] else None
            }
            rows_data.append(row_data)

    users_df = pd.DataFrame(rows_data)

    rows_data2 = []

    for i in range(len(pages2)):
            page2 = pages2[i]
            row_data2 = {
                'Nome': page['properties']['Name']['title'][0]['plain_text'] if 'Name' in page['properties'] and 'title' in page['properties']['Name'] and page['properties']['Name']['title'] else None,
                'email': page['properties']['Email']['email'] if 'Email' in page['properties'] and 'email' in page['properties']['Email'] else None,
                'Desempenho': page['properties']['Desempenho']['number'] if 'Desempenho' in page['properties'] and 'number' in page['properties']['Desempenho'] else None,
                'bem_estar': page['properties']['Bem Estar']['number'] if 'Bem Estar' in page['properties'] and 'number' in page['properties']['Bem Estar'] else None
            }
            rows_data2.append(row_data2)

    users2_df = pd.DataFrame(rows_data2)







    user = users_df[(users_df['email'] == email) & (users_df['password'] == password)]
    
    if not user.empty:
        access_level = user.iloc[0]['access']
        user_data = user.iloc[0]  # Get the data for the logged-in user
        return True, access_level, user_data
    else:
        return False, None, None  # Return None for user_data when no user is found





# Define the main dashboard page
def descritiva_page():
    import pandas as pd
    import requests
    import streamlit as st
    st.title('Dashboard Inspire')

    #Notion credentials
    NOTION_TOKEN = "secret_BL3kRZyHDQKu0tHNn0lHiHdl7ExPYO3Rq3dOmwaKgS7"
    DATABASE_ID = "07866cdaf4884048ac3db6e357d1ecec"
    DATABASE_ID2 = "dd433aff401546aba3776b353e9391cb"

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

    # Supondo que você já tenha o DataFrame df e a coluna 'Date' no formato fornecido
    data = {'Date': {'id': '%3EXob',
                    'type': 'date',
                    'date': {'start': '2024-02-04', 'end': None, 'time_zone': None}}}

    # Extraindo a data do formato fornecido
    start_date = data['Date']['date']['start']
    # Initialize an empty list to store row data
    rows_data = []

    # Iterate through each page using the index
    for i in range(len(pages)):
        page = pages[i]
        row_data = {
            'Name': page['properties']['Name']['title'][0]['plain_text'] if 'Name' in page['properties'] and 'title' in page['properties']['Name'] and page['properties']['Name']['title'] else None,
            'Email': page['properties']['Email']['email'] if 'Email' in page['properties'] and 'email' in page['properties']['Email'] else None,
            'Gênero': page['properties']['Gênero']['rich_text'][0]['plain_text'] if 'Gênero' in page['properties'] and 'rich_text' in page['properties']['Gênero'] and page['properties']['Gênero']['rich_text'] else None,
            'Setor': page['properties']['Setor']['rich_text'][0]['plain_text'] if 'Setor' in page['properties'] and 'rich_text' in page['properties']['Setor'] and page['properties']['Setor']['rich_text'] else None,
            'Cargo': page['properties']['Cargo']['rich_text'][0]['plain_text'] if 'Cargo' in page['properties'] and 'rich_text' in page['properties']['Cargo'] and page['properties']['Cargo']['rich_text'] else None,
            'DISC': page['properties']['DISC']['rich_text'][0]['plain_text'] if 'DISC' in page['properties'] and 'rich_text' in page['properties']['DISC'] and page['properties']['DISC']['rich_text'] else None,
            'Idade': page['properties']['Idade']['number'] if 'Idade' in page['properties'] and 'number' in page['properties']['Idade'] else None,
            'Burnout': page['properties']['Burnout']['rich_text'][0]['plain_text'] if 'Burnout' in page['properties'] and 'rich_text' in page['properties']['Burnout'] and page['properties']['Burnout']['rich_text'] else None,
            'Medicamento': page['properties']['Medicamento']['rich_text'][0]['plain_text'] if 'Medicamento' in page['properties'] and 'rich_text' in page['properties']['Medicamento'] and page['properties']['Medicamento']['rich_text'] else None,
            'Estresse': page['properties']['Estresse']['number'] if 'Estresse' in page['properties'] and 'number' in page['properties']['Estresse'] else None,
            'Ansiedade': page['properties']['Ansiedade']['number'] if 'Ansiedade' in page['properties'] and 'number' in page['properties']['Ansiedade'] else None,
            'Depressão': page['properties']['Depressão']['number'] if 'Depressão' in page['properties'] and 'number' in page['properties']['Depressão'] else None,
            'IMC': page['properties']['IMC']['number'] if 'IMC' in page['properties'] and 'number' in page['properties']['IMC'] else None,
            'Date': start_date,
            'Engajamento': page['properties']['Engajamento']['number'] if 'Engajamento' in page['properties'] and 'number' in page['properties']['Engajamento'] else None,
            'Senha': page['properties']['Senha']['rich_text'][0]['plain_text'] if 'Senha' in page['properties'] and 'rich_text' in page['properties']['Senha'] and page['properties']['Senha']['rich_text'] else None,
            'Bem Estar': page['properties']['Bem Estar']['number'] if 'Bem Estar' in page['properties'] and 'number' in page['properties']['Bem Estar'] else None,
            'QualiVida': page['properties']['QualiVida']['number'] if 'QualiVida' in page['properties'] and 'number' in page['properties']['QualiVida'] else None
            
        }
        rows_data.append(row_data)

    df = pd.DataFrame(rows_data)
    df.dropna(inplace=True)
    


    # Criar a nova coluna 'Nine Box' e classificar de acordo com as condições
    df['Nine Box'] = 'N/A'  # Inicializa a coluna com 'N/A'

    # Aplicar as condições para classificar as categorias
    df.loc[(df['Bem Estar'] > 80) & (df['Engajamento'] > 8), 'Nine Box'] = 'Diamante'
    df.loc[(df['Bem Estar'] >= 50) & (df['Bem Estar'] <= 80) & (df['Engajamento'] > 8), 'Nine Box'] = 'Eficaz'
    df.loc[(df['Bem Estar'] > 80) & (df['Engajamento'] >= 5) & (df['Engajamento'] <= 8), 'Nine Box'] = 'Capaz'
    df.loc[(df['Bem Estar'] >= 50) & (df['Bem Estar'] <= 80) & (df['Engajamento'] >= 5) & (df['Engajamento'] <= 8), 'Nine Box'] = 'Médio'
    df.loc[(df['Bem Estar'] > 80) & (df['Engajamento'] < 5), 'Nine Box'] = 'Enigma'
    df.loc[(df['Bem Estar'] >= 50) & (df['Bem Estar'] <= 80) & (df['Engajamento'] < 5), 'Nine Box'] = 'Alerta Amarelo'
    df.loc[(df['Engajamento'] > 8) & (df['Bem Estar'] < 50), 'Nine Box'] = 'Enigma Persistente'
    df.loc[(df['Engajamento'] >= 5) & (df['Engajamento'] <= 8) & (df['Bem Estar'] < 50), 'Nine Box'] = 'Alerta Amarelo'
    df.loc[(df['Engajamento'] < 5) & (df['Bem Estar'] < 50), 'Nine Box'] = 'Alerta Vermelho'


    # Check if the user is logged in
    if not st.session_state.get("logged_in"):
        st.warning("You need to login first.")
        return
    



    # Display content based on the access level
    if st.session_state.access_level == "admin":

      
        # Opção para upload do arquivo CSV


        if df is not None:

            
            # Realizando o pré-processamento dos dados
            df_processed = df

            #Geral
            # Calculate averages
            avg_bem_estar = df['Bem Estar'].mean()
            avg_depressao = df['Depressão'].mean()
            avg_estresse = df['Estresse'].mean()
            avg_ansiedade = df['Ansiedade'].mean()
            avg_engaj = df['Engajamento'].mean()*10
            avg_QualiVida = df['QualiVida'].mean()

            std_bem_estar = df['Bem Estar'].std()
            std_depressao = df['Depressão'].std()
            std_estresse = df['Estresse'].std()
            std_ansiedade = df['Ansiedade'].std()
            std_engaj = df['Engajamento'].std()
            std_QualiVida = df['QualiVida'].std()





            disc_value_counts = df['DISC'].value_counts()





            # Streamlit App
            import streamlit as st

            st.header("Métricas globais da equipe:")

            # Índices
            cola, colb, colc, cold, cole, colg = st.columns(6)

            # Estilização com cores e destaque
            with cola:
                st.write("**Bem Estar Emocional:**")
                st.write(f"Média: **{avg_bem_estar:.2f}**")

            with colb:
                st.write("**Engajamento:**")
                st.write(f"Média: **{avg_engaj:.2f}**")

            with colc:
                st.write("**Estresse:**")
                st.write(f"Média: **{avg_estresse:.2f}**")

            with cold:
                st.write("**Ansiedade:**")
                st.write(f"Média: **{avg_ansiedade:.2f}**")

            with cole:
                st.write("**Depressão:**")
                st.write(f"Média: **{avg_depressao:.2f}**")

            with colg:
                st.write("**Qualidade de Vida:**")
                st.write(f"Média: **{avg_QualiVida:.2f}**")

            st.markdown(
            """
            <style>
                .css-1t42ko5 {
                    text-align: center;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
            
        
            
            # Opção para escolher a métrica para o gráfico de pizza
            selected_metric = st.selectbox("Selecione o filtro de análise:", ["Medicamento", "Gênero", "Burnout","Cargo","Setor","Nine Box","DISC"])
            
            


            import plotly.express as px
            # Criar gráfico de pizza
           # Seção para a contagem de membros
            st.subheader("Análise segmentada da equipe: ")

            if selected_metric == "Medicamento":
                fig_pie = px.pie(df_processed, names='Medicamento', title='Distribuição de membros por uso de medicamento', hole=0.5)

            elif selected_metric == "Gênero":
                fig_pie = px.pie(df_processed, names='Gênero', title='Distribuição de membros por Gênero', hole=0.5)

            elif selected_metric == "Burnout":
                fig_pie = px.pie(df_processed, names='Burnout', title='Distribuição de membros por Burnout', hole=0.5)
                
            elif selected_metric == "Cargo":
                fig_pie = px.pie(df_processed, names='Cargo', title='Distribuição de membros por Cargo', hole=0.5)

            elif selected_metric == "Setor":
                fig_pie = px.pie(df_processed, names='Setor', title='Distribuição de membros por Setor', hole=0.5)
            
            elif selected_metric == "Nine Box":
                fig_pie = px.pie(df_processed, names='Nine Box', title='Distribuição de membros por Nine Box', hole=0.5)
            
            elif selected_metric == "DISC":
                fig_pie = px.pie(df_processed, names='DISC', title='Distribuição de membros por perfil DISC', hole=0.5)

            # Exibir o gráfico de pizza
            st.plotly_chart(fig_pie)

            # Métricas específicas para o filtro selecionado
            if selected_metric == "Medicamento":
                filter_values = df_processed['Medicamento'].unique()
                filter_column = 'Medicamento'

            elif selected_metric == "Gênero":
                filter_values = df_processed['Gênero'].unique()
                filter_column = 'Gênero'

            elif selected_metric == "Burnout":
                filter_values = df_processed['Burnout'].unique()
                filter_column = 'Burnout'

            elif selected_metric == "Cargo":
                filter_values = df_processed['Cargo'].unique()
                filter_column = 'Cargo'

            elif selected_metric == "Setor":
                filter_values = df_processed['Setor'].unique()
                filter_column = 'Setor'
            
            elif selected_metric == "Nine Box":
                filter_values = df_processed['Nine Box'].unique()
                filter_column = 'Nine Box'
            
            elif selected_metric == "DISC":
                filter_values = df_processed['DISC'].unique()
                filter_column = 'DISC'


            num_columns = 3  # Defina o número desejado de colunas antes de pular para a próxima linha
            metrics_column = st.columns(num_columns)

            for i, value in enumerate(filter_values):
                filtered_df = df_processed[df_processed[filter_column] == value]

                # Exibir métricas específicas
                with metrics_column[i % num_columns]:  # Use o operador % para lidar com a mudança para a próxima linha
                    st.subheader(f"{value}")
                    
                    # Criar uma tabela com as métricas
                    metrics_table = pd.DataFrame({
                        'Métrica': ['Depressão', 'Estresse', 'Ansiedade', 'Bem Estar','Engajamento','QualiVida','IMC','Idade'],
                        'Média': [
                            filtered_df['Depressão'].mean(),
                            filtered_df['Estresse'].mean(),
                            filtered_df['Ansiedade'].mean(),
                            filtered_df['Bem Estar'].mean(),
                            filtered_df['Engajamento'].mean()*10,
                            filtered_df['QualiVida'].mean(),
                            filtered_df['IMC'].mean(),
                            filtered_df['Idade'].mean()


                        ],
                        'Desvio Padrão': [
                            filtered_df['Depressão'].std(),
                            filtered_df['Estresse'].std(),
                            filtered_df['Ansiedade'].std(),
                            filtered_df['Bem Estar'].std(),
                            filtered_df['Engajamento'].std(),
                            filtered_df['QualiVida'].std(),
                            filtered_df['IMC'].std(),
                            filtered_df['Idade'].std()                             
                        ]
                    })

                    metrics_table.set_index('Métrica', inplace=True)
                    st.table(metrics_table)

                    dif_dep = abs(df['Depressão'].mean() - filtered_df['Depressão'].mean())
                    dif_est = abs(df['Estresse'].mean() - filtered_df['Estresse'].mean())
                    dif_ans = abs(df['Ansiedade'].mean() - filtered_df['Ansiedade'].mean())
                    dif_best = abs(df['Bem Estar'].mean() - filtered_df['Bem Estar'].mean())
                    dif_eng = abs(df['Engajamento'].mean() - filtered_df['Engajamento'].mean())
                    dif_quavi = abs(df['QualiVida'].mean() - filtered_df['QualiVida'].mean())

                    difs = ([dif_dep, dif_est, dif_ans, dif_best, dif_eng, dif_quavi])

             

                    # Encontrar o índice do maior valor na lista
                    indice_maior_valor = difs.index(max(difs))

                    # Mapear o índice para o nome correspondente
                    maior_valor_nome = {
                        0: 'Depressão',
                        1: 'Estresse',
                        2: 'Ansiedade',
                        3: 'Bem Estar',
                        4: 'Engajamento',
                        5: 'Qualidade de Vida'
                    }

                    # Obter o nome correspondente ao maior valor
                    nome_maior_valor = maior_valor_nome[indice_maior_valor]

                    # Obter o valor correspondente ao maior valor
                    maior_valor = difs[indice_maior_valor]

                    st.write(f'O atributo que mais se difere do global é o de {nome_maior_valor}.')
        




def clima_org():
    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    import pandas as pd
    import json
    import requests

    if not st.session_state.get("logged_in"):
        st.warning("You need to login first.")
        return
    



    # Display content based on the access level
    if st.session_state.access_level == "admin":

            #Notion credentials
        NOTION_TOKEN = "secret_BL3kRZyHDQKu0tHNn0lHiHdl7ExPYO3Rq3dOmwaKgS7"
        DATABASE_ID = "15adc73306234c918ec9884d5da6f738"

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

        # Supondo que você já tenha o DataFrame df e a coluna 'Date' no formato fornecido
        data = {'Date': {'id': '%3EXob',
                        'type': 'date',
                        'date': {'start': '2024-02-04', 'end': None, 'time_zone': None}}}

        # Extraindo a data do formato fornecido
        start_date = data['Date']['date']['start']
        # Initialize an empty list to store row data
        rows_data = []

        # Iterate through each page using the index
        for i in range(len(pages)):
            page = pages[i]
            row_data = {
                'Name': page['properties']['Name']['title'][0]['plain_text'] if 'Name' in page['properties'] and 'title' in page['properties']['Name'] and page['properties']['Name']['title'] else None,
                'compTranquilidade': page['properties']['compTranquilidade']['number'] if 'compTranquilidade' in page['properties'] and 'number' in page['properties']['compTranquilidade'] else None,
                'compAlegria': page['properties']['compAlegria']['number'] if 'compAlegria' in page['properties'] and 'number' in page['properties']['compAlegria'] else None,
                'crencaTranquilidade': page['properties']['crencaTranquilidade']['number'] if 'crencaTranquilidade' in page['properties'] and 'number' in page['properties']['crencaTranquilidade'] else None,
                'crencaAlegria': page['properties']['crencaAlegria']['number'] if 'crencaAlegria' in page['properties'] and 'number' in page['properties']['crencaAlegria'] else None,
                'valorTranquilidade': page['properties']['valorTranquilidade']['number'] if 'valorTranquilidade' in page['properties'] and 'number' in page['properties']['valorTranquilidade'] else None,
                'valorAlegria': page['properties']['valorAlegria']['number'] if 'valorAlegria' in page['properties'] and 'number' in page['properties']['valorAlegria'] else None,
                'missaoTranquilidade': page['properties']['missaoTranquilidade']['number'] if 'missaoTranquilidade' in page['properties'] and 'number' in page['properties']['missaoTranquilidade'] else None,
                'missaoAlegria': page['properties']['missaoAlegria']['number'] if 'missaoAlegria' in page['properties'] and 'number' in page['properties']['missaoAlegria'] else None
                
            }
            rows_data.append(row_data)
        
        df = pd.DataFrame(rows_data)
        df.dropna(inplace=True)
        resultado_df = pd.DataFrame(columns=['elemento', 'tranquilidade', 'alegria'])
        
        # Adicionar linhas ao DataFrame resultante com os dados organizados
        nova_linha_missao = pd.DataFrame({'elemento': ['Missão'], 'tranquilidade': [df['missaoTranquilidade'].mean()-5], 'alegria': [df['missaoAlegria'].mean()-5]})
        resultado_df = pd.concat([resultado_df, nova_linha_missao], ignore_index=True)
        
        nova_linha_valores = pd.DataFrame({'elemento': ['Valores'], 'tranquilidade': [df['valorTranquilidade'].mean()-5], 'alegria': [df['valorAlegria'].mean()-5]})
        resultado_df = pd.concat([resultado_df, nova_linha_valores], ignore_index=True)
        
        nova_linha_visao = pd.DataFrame({'elemento': ['Visão'], 'tranquilidade': [df['crencaTranquilidade'].mean()-5], 'alegria': [df['crencaAlegria'].mean()-5]})
        resultado_df = pd.concat([resultado_df, nova_linha_visao], ignore_index=True)
        
        nova_linha_politica = pd.DataFrame({'elemento': ['Política de qualidade'], 'tranquilidade': [df['compTranquilidade'].mean()-5], 'alegria': [df['compAlegria'].mean()-5]})
        resultado_df = pd.concat([resultado_df, nova_linha_politica], ignore_index=True)

            # Leitura do CSV
            # Carregar JSON
        with open('elementos.json', 'r') as file:
                json_data = file.read()

        # Carregar JSON
        st.title('Hipolabor')
        data = json.loads(json_data)

            # Salvar elementos em variáveis
        missao = data["empresa"]["missao"]
        visao = data["empresa"]["visao"]
        valores = data["empresa"]["valores"]
        politica_qualidade = data["empresa"]["politica_qualidade"]



        st.subheader(f'Missão: ')
        st.write(f'{missao}')
        st.subheader(f'Valores: ')
        st.write(f'{valores}')
        st.subheader(f'Visão: ')
        st.write(f'{visao}')
        st.subheader(f'Política de qualidade: ')
        st.write(f'{politica_qualidade}')


            # Verificar se as colunas necessárias existem
        required_columns = ['elemento', 'tranquilidade', 'alegria']
        if all(column in resultado_df.columns for column in required_columns):
                # Criar um gráfico de dispersão com tamanho reduzido
                fig, ax = plt.subplots(figsize=(3, 2))  # Ajuste o tamanho conforme necessário
                st.title('Clima Organizacional - Tranquilidade x Alegria')

                for elemento in resultado_df['elemento'].unique():
                    subset = resultado_df[resultado_df['elemento'] == elemento]

                    # Use seaborn para o gráfico de dispersão
                    sns.scatterplot(x='tranquilidade', y='alegria', data=subset, label=elemento, s=75)

                # Definir limites dos eixos x e y
                plt.xlim(-5, 5)
                plt.ylim(-5, 5)

                # Adicionar linhas dos eixos no centro
                plt.axhline(0, color='black', linewidth=2.5)
                plt.axvline(0, color='black', linewidth=2.5)

                plt.grid(True)

                # Posicione a legenda à direita do gráfico
                plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize=6)

                # Pass the figure to st.pyplot()
                st.pyplot(fig)

        else:
                st.write("As colunas necessárias não existem no DataFrame.")
            

            

        st.header('Assessoramento do Clima Organizacional da Empresa')

            # Assessoramento para cada elemento


        # Lista para armazenar os detalhes de cada elemento
        detalhes_elementos = []

        # Iterar sobre as linhas do DataFrame
        for index, row in resultado_df.iterrows():
            elemento = row['elemento']
            tranquilidade = row['tranquilidade']
            alegria = row['alegria']

            if tranquilidade > 0 and alegria > 0:
                mensagem = f"O clima organizacional em relação ao elemento {elemento} indica tranquilidade e alegria. Isso sugere que a equipe está alinhada com o propósito e valores da empresa."
            elif tranquilidade > 0 and alegria <= 0:
                mensagem = f"Embora o clima organizacional em relação ao elemento {elemento} indique tranquilidade, a equipe não expressa um alto nível de alegria. Isso sugere que, apesar da falta de ansiedade ou insegurança, a satisfação pode ser melhorada."
            elif tranquilidade <= 0 and alegria > 0:
                mensagem = f"Embora haja alegria em relação ao elemento {elemento}, a tranquilidade não está em um bom índice. Isso sugere que a equipe pode sentir um certo anseio e insegurança em relação aos valores da empresa."
            else:
                mensagem = f"O clima organizacional em relação ao elemento {elemento} indica tanto falta de tranquilidade quanto alegria. A equipe pode estar insatisfeita e sentir anseio em relação a esse elemento."

            detalhes_elementos.append({'Elemento': elemento, 'Tranquilidade': tranquilidade, 'Alegria': alegria, 'Assessoramento': mensagem})

        # Criar um DataFrame com os detalhes
        df_detalhes = pd.DataFrame(detalhes_elementos)
        df_detalhes.set_index('Elemento', inplace=True)

        # Exibir a tabela no Streamlit
        st.table(df_detalhes)

    # Calcular e exibir a distância euclidiana à origem para cada elemento em cada linha

        st.header('Tabela de Intensidade de Emoções')
        st.write('O coeficiente de intensidade de emoções é um valor que ocila de 0 a 1. Com 0 representando intensidade nula e 1 representando intensidade máxima.')
        table_data = []

        # Iterate through the DataFrame and add data to the table
        for index, row in resultado_df.iterrows():
            elemento = row['elemento']
            distancia = np.sqrt(row['tranquilidade']**2 + row['alegria']**2) / 7.0710678118654755
            table_data.append({'Elemento': f'{elemento}', 'Coeficiente de Intensidade': f'{distancia:.4f}'})

        # Display the table
            
        st.table(table_data)

        st.header('Alinhamento de emoções')
        st.write('O alinhamento de emoções é um valor que ocila de 0 a 1. Com 0 representando alinhamento nulo e 1 representando alinhamento máxima.')

        # Função para calcular a similaridade de cosseno
        def calcular_similaridade_cosseno(vetor_referencia, vetor):
            dot_product = np.dot(vetor_referencia, vetor)
            norm_a = np.linalg.norm(vetor_referencia)
            norm_b = np.linalg.norm(vetor)
            cosine_similarity = dot_product / (norm_a * norm_b)
            return abs(cosine_similarity)

        # Criar uma lista para armazenar todos os vetores
        vetores = []

        # Ler todos os vetores e elementos do DataFrame df
        for index, row in resultado_df.iterrows():
            elemento = row['elemento']
            vetor = np.array([row['tranquilidade'], row['alegria']])
            vetores.append((elemento, vetor))

        # Calcular a similaridade de cosseno entre cada par de vetores
        resultados_similaridade = []
        for i, (elemento_ref, vetor_ref) in enumerate(vetores):
            row = {'Elemento de Referência': elemento_ref}
            for j, (elemento, vetor) in enumerate(vetores):
                if i != j:
                    similarity = calcular_similaridade_cosseno(vetor_ref, vetor)
                    row[elemento] = similarity
            resultados_similaridade.append(row)

        # Criar um DataFrame para os resultados
        df_resultados = pd.DataFrame(resultados_similaridade)
        df_resultados.set_index('Elemento de Referência', inplace=True)

        # Exibir o heatmap com Seaborn e Streamlit
        plt.figure(figsize=(5, 3))
        sns.heatmap(df_resultados, cmap='YlGnBu', annot=True, fmt=".2f", linewidths=.5)
        st.pyplot(plt)





                        


  

if __name__ == '__main__':
    main()
