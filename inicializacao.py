import os

def cria_configs(path_configs):
    existe_arquivo = os.path.isfile(path_configs)
    if not existe_arquivo:
        conteudo_json = '{"Credenciais":{"Ana":{"Identificador":"", "Senha":""}}}'
        arquivo = open(path_configs, 'w')
        arquivo.write(conteudo_json)
        arquivo.close()
    
def cria_dir_resultados(path_resultados):
    """Cria pasta 'resultados'"""
    os.makedirs(path_resultados, exist_ok=True)    

def cria_estacoes(path_estacoes):
    existe_arquivo = os.path.isfile(path_estacoes)
    if not existe_arquivo:
        arquivo = open(path_estacoes, 'w')
        arquivo.close()

def inicializacao_basico(path_configs, path_resultados, path_estacoes):
    cria_configs(path_configs)
    cria_dir_resultados(path_resultados)
    cria_estacoes(path_estacoes)
    