import json
import os
from interfaces import *


def criaConfigs(pathConfigs):
    existeArq =os.path.isfile(pathConfigs)
    if(not existeArq):
        conteudoJson = '{"Credenciais":{"Ana":{"Identificador":"", "Senha":""}}}'

        arq = open(pathConfigs, 'w')
        arq.write(conteudoJson)

        arq.close()

def atualizaCredenciaisAna(pathConfigs):
    novosDadosDict = interfaceCredenciais()
    
    arq = open(pathConfigs, 'r+')
     
    dataArqStr = arq.read()
    dataJson = json.loads(dataArqStr)
    
    dataJson.update({"Credenciais":{"Ana":{"Identificador":novosDadosDict['id'], "Senha":novosDadosDict['senha']}}})

    #arq.read() faz o ponteiro ir para o final do arquivo, e sendo necessário voltar pro começo para sobre-escrever as modificações
    arq.seek(0)

    arq.write(json.dumps(dataJson))

    arq.close()


def main():
    pathConfigs = 'configs.json'
    criaConfigs(pathConfigs)
    interfaceMenu()
    entradaUser = input()
    if(entradaUser==1):
        atualizaCredenciaisAna(pathConfigs)
    elif():
        pass
if __name__ == "__main__":
    main()