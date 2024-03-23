# imports
from src import config, coletar_nomes_frequentes

from selenium                               import webdriver
from webdriver_manager.chrome               import ChromeDriverManager
from selenium.webdriver.chrome.service      import Service
from selenium.webdriver.common.by           import By
from selenium.webdriver.chrome.options      import Options
from selenium.common.exceptions             import *
from selenium.webdriver.support.ui          import WebDriverWait
from selenium.webdriver.support             import expected_conditions as EC
from time                                   import sleep

import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# tempo de espera padrao
SLEEP = config.SLEEP

# importar diretorios
dir_raiz, dir_dados = coletar_nomes_frequentes.configurar_diretorios()


def driver_settings():
    # criar driver para web scraping com selenium
    # Set options
    options = Options()
    options.add_argument('start-maximized')
    options.add_argument('--disable-notifications')
    options.add_argument('--no-sandbox')
    options.add_argument('--verbose')

    # Run browser
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver


def consulta_ano_nome(driver, ano, abrev):
    # executa uam consulta por ano e nome abreviado
    try:
        # confere se os campos renderizaram
        WebDriverWait(driver, SLEEP).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/section/div/table/thead/tr[3]/th/input[3]'))
        )

        # inputa os dados
        driver.find_element(By.XPATH, '/html/body/section/div/table/thead/tr[3]/th/input[3]').send_keys(ano)
        driver.find_element(By.XPATH, '/html/body/section/div/table/thead/tr[3]/th/input[4]').send_keys(abrev)
        driver.find_element(By.XPATH, '/html/body/section/div/table/thead/tr[3]/th/button').click()

    except:
        print('nao foi possivel fazer a consulta')


def verificar_numero_registros(driver, ano, nome):
    # verifica quantos registros existem na pagina
    # primeira faz uma verificacao minima para ver se vale a pena analisar a pagina
    try:
        # procurar pelo primeiro registro renderizado
        WebDriverWait(driver, SLEEP).until(             
            EC.presence_of_element_located((By.XPATH, '/html/body/div/table/tbody/tr[1]/td[2]'))
        )
        presenca_registro = True

        # procurar o maior numero de registros
        if presenca_registro == True:
            for i in range(1, 1000):
                try:
                    driver.find_element(By.XPATH, f'/html/body/div/table/tbody/tr[{i}]/td[2]')
                    numero_registros = i
                except:        
                    numero_registros = i - 1
                    break  
    except:
        print(f"Ano: {ano} / Nome: {nome} / registro nao encontrado ou tempo limite excedido.")
        numero_registros = 0

    return numero_registros


def verificar_numero_paginas(driver, numero_registros):
    # verifica quantos paginas existem na pesquisa
    # casos com mais de uma pagina
    try:
        #procurar primeira pagina renderizada
        WebDriverWait(driver, SLEEP).until(
            EC.presence_of_element_located((By.XPATH, f'/html/body/div/table/tbody/tr[{numero_registros+1}]/th/a[1]'))
        )                                              

        presenca_paginas = True

        # procurar o maior numero de pagina
        if presenca_paginas == True:
            for i in range(1, 1000):
                try:
                    driver.find_element(By.XPATH, f'/html/body/div/table/tbody/tr[{numero_registros+1}]/th/a[{i}]')
                    numero_paginas = i
                except:        
                    numero_paginas = i - 1
                    break  
    except:
        # casos com uma pagina
        try:
            #procurar primeira pagina renderizada
            WebDriverWait(driver, SLEEP).until(
                EC.presence_of_element_located((By.XPATH, f'/html/body/div/table/tbody/tr[{numero_registros+1}]/th/a'))
            ) 
            numero_paginas = 1
        # casos com nenhuma pagina
        except:
            numero_paginas = 0 

    return numero_paginas


def coletar_dados_detalhados(driver, ano, nome):
    # coletar dados como lista
    novo_registro = []

    try:
        num_obtuario = WebDriverWait(driver, SLEEP).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/table/thead/tr/th/b'))
        ).text
        novo_registro.append(num_obtuario)

        cemiterio = WebDriverWait(driver, SLEEP).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/table/tbody[2]/tr[1]/td/b'))
        ).text
        novo_registro.append(cemiterio)

        falecido = WebDriverWait(driver, SLEEP).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/table/tbody[2]/tr[2]/td/b[1]'))
        ).text
        novo_registro.append(falecido)

        data_falecimento = WebDriverWait(driver, SLEEP).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/table/tbody[2]/tr[2]/td/b[2]'))
        ).text
        novo_registro.append(data_falecimento)

        sexo = WebDriverWait(driver, SLEEP).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/table/tbody[2]/tr[3]/td/b[1]'))
        ).text
        novo_registro.append(sexo)

        cor = WebDriverWait(driver, SLEEP).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/table/tbody[2]/tr[3]/td/b[2]'))
        ).text
        novo_registro.append(cor)

        data_nascimento = WebDriverWait(driver, SLEEP).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/table/tbody[2]/tr[3]/td/b[3]'))
        ).text
        novo_registro.append(data_nascimento)

        idade = WebDriverWait(driver, SLEEP).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/table/tbody[2]/tr[3]/td/b[4]'))
        ).text
        novo_registro.append(idade)

        try:
            localizacao = WebDriverWait(driver, SLEEP).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div/div/table/tbody[2]/tr[4]/th'))
            ).text
            novo_registro.append(localizacao)

            detalhes = WebDriverWait(driver, SLEEP).until(      
                EC.presence_of_element_located((By.XPATH, '/html/body/div/div/table/tbody[2]/tr[5]/td'))
            ).text
            novo_registro.append(detalhes)
        except:
            localizacao = ''
            novo_registro.append(localizacao)

            detalhes = ''
            novo_registro.append(detalhes)

    except:
        print(f"Ano: {ano} / Nome: {nome} / dados detalhados não encontrados ou tempo limite excedido.")

    return novo_registro


def coletar_linha(driver, df, registro, numero_registros, pagina, ano, nome):
    try:
        #procurar registro renderizado
        WebDriverWait(driver, SLEEP).until(
            EC.presence_of_element_located((By.XPATH, f'/html/body/div/table/tbody/tr[{registro}]/td[2]'))
        ).click()

        # coletar dados detalhados
        novo_registro = coletar_dados_detalhados(driver, ano, nome)
        df.loc[len(df)] = novo_registro

        # retornar para lsita de pesuqisa
        driver.find_element(By.XPATH, f'/html/body/section/div/table/thead/tr[3]/th/button').click()

        # verifica se encaminha para pagina correta na ordem de pesquisa
        try:
            # ir para proxima pagina
            WebDriverWait(driver, SLEEP).until(
                EC.presence_of_element_located((By.XPATH, f'/html/body/div/table/tbody/tr[{numero_registros+1}]/th/a[{pagina}]'))
            ).click()   

            # aguardar para evitar duplicidade
            sleep(SLEEP)
        except:
            pass
    except:
        pass

    return df


def web_scraping(df, driver, ano, nome_abrev):
    # realizar coleta de dados do site
    # fazer pesquisa por nome abreviado
    for nome in nome_abrev:
        # inicir pagina limpa
        url = 'https://funeraria.guarulhos.sp.gov.br/finados.php'
        driver.get(url)

        # inputar valores e pesquisar
        consulta_ano_nome(driver, ano, nome)

        # encontra numero de registros na pagina
        numero_registros = verificar_numero_registros(driver, ano, nome)

        if numero_registros > 0:
            # encontra numero de paginas na pesquisa
            numero_paginas = verificar_numero_paginas(driver, numero_registros)
        else:
            numero_paginas = 0

        if numero_paginas > 1:
            for pagina in range(1, numero_paginas+1):
                for registro in range(1, numero_registros+1):
                    df = coletar_linha(driver, df, registro, numero_registros, pagina, ano, nome)
        elif numero_paginas == 1:
            for registro in range(1, numero_registros+1):
                df = coletar_linha(driver, df, registro, numero_registros, 1, ano, nome)
        else:
            print(f'Ano: {ano} / Nome: {nome} / numero de paginas = 0')
            pass

    df = df.drop_duplicates()
    return df


def salvar_dados_cemit(df, dir_dados, ano):
    df.to_csv(f'{dir_dados}/df_{ano}.csv', sep=';', encoding='utf-8', index=False)


def coletar_dados_cemit(ano):
    # criar driver
    driver = driver_settings()

    # criar dataframe
    df = pd.DataFrame(columns=[
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

    nomes_frequentes = pd.read_csv(f'{dir_dados}/nomes_frequentes.csv', sep=';', encoding='utf-8')
    nome_abrev = list(nomes_frequentes['nome_abrev'])

    print(f'numero de nomes abreviados para pesquisa: {len(nome_abrev)}')
    print(f'Ano de pesquisa: {ano}')
    
    df = web_scraping(df, driver, ano, nome_abrev)

    salvar_dados_cemit(df, dir_dados, ano)