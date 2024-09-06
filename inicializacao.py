import os

def criaConfigs(pathConfigs):
    existeArq =os.path.isfile(pathConfigs)
    if(not existeArq):
        conteudoJson = '{"Credenciais":{"Ana":{"Identificador":"", "Senha":""}}}'

        arq = open(pathConfigs, 'w')
        arq.write(conteudoJson)

        arq.close()
    
def criaArqEstacoes(pathEstacoes):
    existeArq = os.path.isfile(pathEstacoes)
    if(not existeArq):
        pass