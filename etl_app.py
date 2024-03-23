from src import config
from src import coletar_nomes_frequentes
from src import coletar_dados_cemiterio
from src import pre_processamento
from src import armazenar_dados

# deinir configuracoes antes de rodar
ANO = config.ANO
COLETAR_NOMES_FREQUENTES = config.COLETAR_NOMES_FREQUENTES
COLETAR_DADOS_CEMITERIO = config.COLETAR_DADOS_CEMITERIO
PRE_PROCESSAR_DADOS = config.PRE_PROCESSAR_DADOS
ARMAZENAR_DADOS = config.ARMAZENAR_DADOS

if COLETAR_NOMES_FREQUENTES == True:
    # coletar nomes frequentes no Brasil
    coletar_nomes_frequentes.coletar_nomes_frequentes()
    print('nomes frequentes coletados, app funcionando')

if COLETAR_DADOS_CEMITERIO == True:
    # coletar dados de um ano específico
    # coletar dados de cemiterios
    coletar_dados_cemiterio.coletar_dados_cemit(ANO)

if PRE_PROCESSAR_DADOS == True:
    # tratar dados coletados
    pre_processamento.tratar_dados()
    print('Dados pre processados')

if ARMAZENAR_DADOS == True:
    # armazenar dados tratados
    armazenar_dados.carregar_dados_bd()
    print('Dados carregados no banco de dados com sucesso')


