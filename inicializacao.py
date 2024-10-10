import os

def cria_configs(pathConfigs):
    existeArq =os.path.isfile(pathConfigs)
    if(not existeArq):
        conteudoJson = '{"Credenciais":{"Ana":{"Identificador":"", "Senha":""}}}'

        arq = open(pathConfigs, 'w')
        arq.write(conteudoJson)

        arq.close()
    
def cria_dir_resultados():
    """Cria pasta 'resultados'"""
    try:
        os.mkdir('resultados')
    except:
        pass

def cria_arq_estacoes(pathEstacoes):
    existeArq = os.path.isfile(pathEstacoes)
    if(not existeArq):
        pass

def inicializacao_basico(pathConfigs):
    cria_configs(pathConfigs)
    cria_dir_resultados()
