from src import armazenar_dados

import streamlit as st
import pandas as pd
import plotly.express as px

df = armazenar_dados.consultar_df_bd()
df = df.drop(columns='id')

st.sidebar.image('dados/logo_gru.png', width=200)

st.title('Imprimindo data frame com st.write')
st.write(df, index=False)

# Criando o gráfico de linhas com Plotly
# fig = px.line(data, x='Data', y='Quantidade_de_Mortes', title='Quantidade de Mortes ao longo do tempo')
# Exibindo o gráfico no Streamlit
# st.plotly_chart(fig)

x = st.sidebar.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

st.sidebar.text_input("Your name", key="name")
# You can access the value at any point with:
st.session_state.name

if st.sidebar.checkbox('Show dataframe'):
        st.write('show dataframe')

df2 = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.sidebar.selectbox(
    'Which number do you like best?',
    df2['first column'])

'You selected: ', option

df['data_falecimento'] = pd.to_datetime(df['data_falecimento'])
anos = set(df['data_falecimento'].dt.year)
st.markdown(f'Anos disponíveis para pesquisa: {anos}')

numero_registros = df.shape[0]
st.markdown(f'numero de registros no banco de dados: {numero_registros}')
