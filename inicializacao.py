import os

def cria_configs(pathConfigs):
    existeArq =os.path.isfile(pathConfigs)
    if(not existeArq):
        conteudoJson = '{"Credenciais":{"Ana":{"Identificador":"", "Senha":""}}}'

        arq = open(pathConfigs, 'w')
        arq.write(conteudoJson)

        arq.close()
    
def cria_dir_resultados(pathResultados):
    """Cria pasta 'resultados'"""
    os.makedirs(pathResultados, exist_ok=True)


# def cria_arq_estacoes(pathEstacoes): # em utilização ?????
#     existeArq = os.path.isfile(pathEstacoes)
#     if(not existeArq):
#         file = open(pathEstacoes, 'w')
#         file.close()
        

def inicializacao_basico(pathConfigs, pathResultados):
    cria_configs(pathConfigs)
    cria_dir_resultados(pathResultados)
