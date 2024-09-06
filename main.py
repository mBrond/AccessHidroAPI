import json
import os
import inicializacao
from acess import Acess
from interfaces import *

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


def escreverEstacoes(pathEstacoes, operacao, estacoes:list):
    if(operacao == 1):
        f = open(pathEstacoes, 'w')
    else:
        f = open(pathEstacoes, 'a')

    for estacao in estacoes:
        f.write(estacao+'\n')

    f.close()

def escreverDados(pathResultados, dados, codigoEstacao):
    f = open(pathResultados+str(codigoEstacao)+'.txt', 'w')
    f.write(str(dados))
    f.close()

def solicitarEstacao(dataComeco, pathEstacoes):
    acess = Acess()
    acess.lerCredenciais()

    f = open(pathEstacoes, 'r')
    estacoes = f.read().split('\n')
    estacoes.remove('')
    f.close()

    dataAtual = dataComeco
    token = acess.forceRequestToken()
    for estacao in estacoes:
        dados = acess.requestTelemetricaAdotada(int(estacao), dataAtual, token)
        escreverDados('resultados\\', dados.content, estacao)

def main():
    pathConfigs = 'configs.json'
    inicializacao.criaConfigs(pathConfigs)

    pathEstacoes = 'estacoes.txt'

    
    entradaUser = 9
    while(entradaUser!=0):
        interfaceMenu()
        entradaUser = int(input())
        if(entradaUser==1):
            atualizaCredenciaisAna(pathConfigs)
        elif(entradaUser==2):
            operacao = interfaceOperacaoEstacao()
            escreverEstacoes(pathEstacoes, operacao, estacoes=interfaceSolicitarEstacoes())
        elif(entradaUser==3): #solicitar um dia para todas as estacoes
            dataComeco, dataFinal = datasComecoFinal()
            solicitarEstacao(dataComeco, pathEstacoes)
        else:
            pass
if __name__ == "__main__":
    main()