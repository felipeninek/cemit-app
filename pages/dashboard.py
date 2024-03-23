from src import armazenar_dados

import streamlit as st
import pandas as pd

df = armazenar_dados.consultar_df_bd()

st.title('Dados coletados do site da prefeitura')
st.write(df, index=False)

df['data_falecimento'] = pd.to_datetime(df['data_falecimento'])
anos = set(df['data_falecimento'].dt.year)
st.markdown(f'Anos disponíveis para pesquisa: {anos}')

numero_registros = df.shape[0]
st.markdown(f'numero de registros no banco de dados: {numero_registros}')
