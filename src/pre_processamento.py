from src import coletar_nomes_frequentes

import os
import pandas as pd


# carregar caminhos
dir_raiz, dir_dados = coletar_nomes_frequentes.configurar_diretorios()

def ler_arquivos_cemit(dir_dados):
    # listar todos os arquivos da pasta
    arquivos = os.listdir(dir_dados)

    # ler arquivos csv dos cemiterios
    arquivos_csv_cemit = [arquivo for arquivo in arquivos if arquivo.startswith('df_')]

    # criar dataframe
    df_agrupado = pd.DataFrame(columns=[
        'num_obtuario',
        'cemiterio',
        'falecido',
        'data_falecimento',
        'sexo',
        'cor',
        'data_nascimento',
        'idade',
        'localizacao',
        'detalhes'
        ])

    # Loop através dos arquivos CSV
    for arquivo_csv in arquivos_csv_cemit:
        caminho_arquivo = os.path.join(dir_dados, arquivo_csv)
        
        # Lê o arquivo CSV como um DataFrame do Pandas
        df = pd.read_csv(caminho_arquivo, sep=';', encoding='utf-8')
        
        # adicionar ao dataframe
        df_agrupado = pd.concat([df_agrupado, df], ignore_index=True)

    # reset index
    df_agrupado = df_agrupado.reset_index(drop=True)

    return df_agrupado


def tratar_duplicados(df):
    # visualizar dados duplicados
    df_duplicados = df.loc[df.duplicated(),:]
    print('Quantidade de dados duplicados: ',df_duplicados.shape[0])

    if df_duplicados.shape[0] > 0:
        # retirar dados duplicados
        df = df.drop_duplicates()

        # resetar index
        df = df.reset_index(drop=True)

    return df


def tratar_nulos(df):
    # visualizar dados nulos
    df_nulos = df[df.isna().any(axis=1)]
    print('Quantidade de dados nulos:',df_nulos.shape[0])

    if df_nulos.shape[0] > 0:
        # retirar dados nulos e manter informações importantes
        df = df.dropna(subset=['num_obtuario',
                                'cemiterio',
                                'falecido',
                                'data_falecimento',
                                'sexo',
                                'cor',
                                'data_nascimento',
                                'idade'])

        # resetar index
        df = df.reset_index(drop=True)
    
    return df, df_nulos


def redefinir_formato(df):
    # melhorar nomes dos cemiterios
    df['cemiterio'] = df['cemiterio'].replace({'NECROPOLE DO CAMPO SANTO - GUARULHOS - SP':'Necrópole do Campo Santo',
                                               'SAO JUDAS TADEU - GUARULHOS - SP':'São Judas Tadeu',
                                               'NOSSA SENHORA DE BONSUCESSO - GUARULHOS - SP':'Nossa Senhora de Bonsucesso'})
    
    df['falecido'] = df['falecido'].str.title()

    df['sexo'] = df['sexo'].replace({'IGN':'Não informado'})
    df['sexo'] = df['sexo'].str.title()

    df['cor'] = df['cor'].replace({'IGN':'Não informado'})
    df['cor'] = df['cor'].str.title()

    # retirar idade pois é possivel conseguir o valor através do calculo de data_falecimento - data_nascimento
    df = df.drop(columns=['idade'])

    df['localizacao'] = df['localizacao'].str[13:]
    df['localizacao'] = df['localizacao'].str.title()

    df['detalhes'] = df['detalhes'].str.title()

    return df


def redefinir_tipagem(df):
    # redefinir tipagem
    df['num_obtuario'] = df['num_obtuario'].astype('int64')

    df['cemiterio'] = df['cemiterio'].astype('category')

    df['falecido'] = df['falecido'].astype('string')

    df['data_falecimento'] = pd.to_datetime(df['data_falecimento'], errors='coerce', dayfirst=True)

    df['sexo'] = df['sexo'].astype('string')

    df['cor'] = df['cor'].astype('string')

    df['data_nascimento'] = pd.to_datetime(df['data_nascimento'], errors='coerce', dayfirst=True)

    df['localizacao'] = df['localizacao'].astype('string')

    df['detalhes'] = df['detalhes'].astype('string')

    return df


def salvar_dados_tratados(df, dir_dados):
    df.to_csv(f'{dir_dados}/dados_tratados.csv', sep=';', encoding='utf-8', index=False)


def tratar_dados():
    df = ler_arquivos_cemit(dir_dados)
    df = tratar_duplicados(df)
    df, df_nulos = tratar_nulos(df)
    df = redefinir_formato(df)
    df = redefinir_tipagem(df)
    salvar_dados_tratados(df, dir_dados)