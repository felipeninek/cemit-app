# imports
from src import coletar_nomes_frequentes

import pandas as pd
import sqlite3
import os

# identificar diretorios de trabalho
dir_raiz, dir_dados = coletar_nomes_frequentes.configurar_diretorios()

# carregar dados
df = pd.read_csv(f'{dir_dados}/dados_tratados.csv', sep=';', encoding='utf-8')


def criar_bd(dir_dados):
    # verificar se o banco existe
    if os.path.exists(f'{dir_dados}/obituarios.db'):
        print('O banco já existe')
        return

    # Conectar ao banco de dados (criará o arquivo se não existir)
    conn = sqlite3.connect(f'{dir_dados}/obituarios.db')

    # Criar a tabela
    conn.execute('''
    CREATE TABLE obituarios (
        id INTEGER PRIMARY KEY,
        num_obtuario INTEGER,
        cemiterio TEXT,
        falecido TEXT,
        data_falecimento DATE,
        sexo TEXT,
        cor TEXT,
        data_nascimento DATE,
        localizacao TEXT,
        detalhes TEXT
    )
    ''')

    # Salvar as alterações e fechar a conexão
    conn.commit()
    conn.close()

    print("Banco de dados e tabela criados com sucesso.")


def inserir_dados_bd(df):
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(f'{dir_dados}/obituarios.db')

    # Inserir os dados do DataFrame na tabela SQLite
    df.to_sql('obituarios', conn, if_exists='append', index=False)

    # Fechar a conexão
    conn.close()

    print('Dados inseridos com sucesso')


def consultar_dados_bd():
    # funcao pode ser utilizada para verificar dados armazenados no banco
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(f'{dir_dados}/obituarios.db')

    # Criar um cursor para executar consultas SQL
    cursor = conn.cursor()

    # Executar uma consulta simples para selecionar todos os registros da tabela
    cursor.execute('SELECT * FROM obituarios')

    # Recuperar os resultados da consulta
    resultados = cursor.fetchall()

    # Exibir os resultados
    for row in resultados:
        print(row)

    # Fechar a conexão
    conn.close()

    return resultados


def consultar_df_bd():
    # fazer consulta em dataframe
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(f'{dir_dados}/obituarios.db')

    # Carregar os resultados da consulta SQL em um DataFrame
    df = pd.read_sql_query('SELECT * FROM obituarios', conn)

    # Fechar a conexão
    conn.close()

    # Exibir shape do DataFrame
    print(df.shape)

    return df


def carregar_dados_bd():
    criar_bd(dir_dados)
    inserir_dados_bd(df)