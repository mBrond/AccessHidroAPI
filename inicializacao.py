import os

def criaConfigs(pathConfigs):
    existeArq =os.path.isfile(pathConfigs)
    if(not existeArq):
        conteudoJson = '{"Credenciais":{"Ana":{"Identificador":"", "Senha":""}}}'

        arq = open(pathConfigs, 'w')
        arq.write(conteudoJson)

        arq.close()
    
def criaDirResultados():
    try:
        os.mkdir('resultados')
    except:
        pass

def criaArqEstacoes(pathEstacoes):
    existeArq = os.path.isfile(pathEstacoes)
    if(not existeArq):
        pass

def inicializacaoBasico(pathConfigs):
    criaConfigs(pathConfigs)
    criaDirResultados()
