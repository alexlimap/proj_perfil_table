import streamlit as st
import pandas as pd
import base64
import logging

# Configuração básica do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(uploaded_file):
    # Verifica a extensão do arquivo e tenta carregar os dados apropriadamente
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file, sep=";",encoding="utf-8")
    elif uploaded_file.name.endswith('.xlsx'):
        data = pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith('.parquet'):
        data = pd.read_parquet(uploaded_file)
    else:
        st.error("Formato de arquivo não suportado!")
        return None
    return data

def analyze_data(data):
    # Análise de dados
    profile = pd.DataFrame({
        "Coluna": data.columns,
        "Tipos": data.dtypes,
        "Valores Únicos": [data[col].nunique() for col in data.columns],
        "Valores Nulos (%)": [data[col].isnull().mean() * 100 for col in data.columns],
        "Máx Caracteres": [data[col].astype(str).map(len).max() if data[col].dtype == 'object' else 'N/A' for col in data.columns]
    })
    return profile

def show_download_link(data):
    # Função para gerar link de download de um DataFrame
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data_profile.csv">Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)

# Interface
st.title('Análise de Dados com Streamlit')

uploaded_file = st.file_uploader("Carregue um arquivo CSV, Excel ou Parquet", type=['csv', 'xlsx', 'parquet'])

if uploaded_file is not None:
    data = load_data(uploaded_file)
    if data is not None:
        st.write("Visualizando as primeiras 100 linhas do dataset:")
        st.dataframe(data.head(100))

        profile = analyze_data(data)
        st.write("Perfil dos Dados:")
        st.dataframe(profile)

        show_download_link(profile)
