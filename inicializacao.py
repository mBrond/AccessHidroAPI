import os
from error_handler import error_handler

def cria_configs(path_configs):
    def criar():
        existe_arquivo = os.path.isfile(path_configs)
        if not existe_arquivo:
            conteudo_json = '{"Credenciais":{"Ana":{"Identificador":"", "Senha":""}}}'
            arquivo = open(path_configs, 'w')
            arquivo.write(conteudo_json)
            arquivo.close()
    
    error_handler.safe_execute(
        criar,
        context="criação de arquivo de configurações",
        show_message=False
    )
    
def cria_dir_resultados(path_resultados):
    """Cria pasta 'resultados'"""
    def criar():
        os.makedirs(path_resultados, exist_ok=True)
    
    error_handler.safe_execute(
        criar,
        context="criação de diretório de resultados",
        show_message=False
    )    

def cria_estacoes(path_estacoes):
    def criar():
        existe_arquivo = os.path.isfile(path_estacoes)
        if not existe_arquivo:
            arquivo = open(path_estacoes, 'w')
            arquivo.close()
    
    error_handler.safe_execute(
        criar,
        context="criação de arquivo de estações",
        show_message=False
    )

def inicializacao_basico(path_configs, path_resultados, path_estacoes):
    def inicializar():
        cria_configs(path_configs)
        cria_dir_resultados(path_resultados)
        cria_estacoes(path_estacoes)
    
    error_handler.safe_execute(
        inicializar,
        context="inicialização básica do sistema",
        show_message=False
    )
    