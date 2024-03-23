# neste arquivo estão resentes as funções necessárias para coletar, tratar e
# salvar nomes frequentes do Brasil. Dados obtidos na wikipedia

# imports
import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
from unidecode import unidecode


def configurar_diretorios():
    # configurar diretorios
    # encontrar diretorio raiz
    dir_raiz = os.getcwd()
    dir_raiz = dir_raiz.replace('\\', '/')
  

    # encontrar diretorio para armazenar dados, e, caso nao exista, sera criado
    dir_dados = os.path.join(dir_raiz, 'dados')
    dir_dados = dir_dados.replace('\\', '/')

    if not os.path.exists(dir_dados):
        os.makedirs(dir_dados)

    return dir_raiz, dir_dados


def coletar_nomes():
    # coletar dados de nomes frequentes da web
    # Cria lista para armazenar nomes coletados
    nomes = []
    # Fazer requisição da página
    url = 'https://pt.wikipedia.org/wiki/Lista_de_prenomes_mais_comuns_no_Brasil'

    # Fazendo uma requisição GET para obter o conteúdo da página
    response = requests.get(url)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Parseia o conteúdo HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontrando a tabela desejada pelo seu atributo 'class'
        tabela = soup.find('table', class_='wikitable')

        # Verificando se a tabela foi encontrada
        if tabela:
            # Itera sobre as linhas da tabela
            for linha in tabela.find_all('tr'):
                # Itera sobre as células de cada linha
                colunas = linha.find_all('td')
                if colunas:
                    # insere nomes na lista
                    registro = [coluna.text.strip() for coluna in colunas]
                    nomes.append(registro[1])
                    nomes.append(registro[6])             
        else:
            print("Tabela não encontrada.")
    else:
        print("Falha ao acessar a página.")

    # Cria DataFrame com nomes coletados
    df = pd.DataFrame({'nome':nomes})

    return df


def tratar_dados_coletados(df):
    # tratar dados para armazenamento adequado
    # selecionar 3 primeiros caracteres
    df['nome_abrev'] = df['nome'].str.slice(0,3)

    # retirar acentuação dos nome abreviados
    df['nome_abrev'] = df['nome_abrev'].apply(lambda x: unidecode(x))

    # remover dados nulos
    df = df.dropna()

    # remover abreviaçoes duplicadas
    df = df.drop_duplicates(subset='nome_abrev')

    return df


def salvar_nomes_frequentes(df, dir_dados):
    # salvar dados coletados no dir dados
    df.to_csv(f'{dir_dados}/nomes_frequentes.csv', sep=';', encoding='utf-8', index=False)


def coletar_nomes_frequentes():
    # executar todos os passos da coleta de nomes
    dir_raiz, dir_dados = configurar_diretorios()
    df = coletar_nomes()
    df = tratar_dados_coletados(df)
    salvar_nomes_frequentes(df, dir_dados)