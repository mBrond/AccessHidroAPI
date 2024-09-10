import json
import os
import datetime
import inicializacao
from acess import Acess
from interfaces import *
from manipulacaoArquivos import *

def decodeRequestDetalhada(request):
    content = json.loads(request.content)
    itens = content['items']
    listaOrdenada = list()
    for item in itens:
        dicionarioDiario = dict()
        dicionarioDiario["Hora_medicao"] = item['Data_Hora_Medicao']
        dicionarioDiario["Chuva_Acumulada"] = item["Chuva_Acumulada"]
        dicionarioDiario["Chuva_Adotada"] = item["Chuva_Adotada"]
        dicionarioDiario["Cota_Adotada"] = item["Cota_Adotada"]
        dicionarioDiario["Cota_Sensor"] = item["Cota_Sensor"]
        dicionarioDiario["Vazao_Adotada"] = item["Vazao_Adotada"]
        listaOrdenada.append(dicionarioDiario)
    return listaOrdenada

def decodeRequestAdotada(request):
    content = json.loads(request.content)
    itens = content['items']
    listaOrdenada = list()
    for item in itens:
        dicionarioDiario = dict()
        dicionarioDiario["Hora_Medicao"] = item["Data_Hora_Medicao"]
        dicionarioDiario["Chuva_Adotada"] = item["Chuva_Adotada"]
        dicionarioDiario["Cota_Adotada"] = item["Cota_Adotada"]
        dicionarioDiario["Vazao_Adotada"] = item["Vazao_Adotada"]
        listaOrdenada.append(dicionarioDiario)
    return listaOrdenada

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

def solicitarEstacaoDetalhada(dataAtual, pathEstacoes):
    acess = Acess()
    acess.lerCredenciais()

    f = open(pathEstacoes, 'r')
    estacoes = f.read().split('\n')
    estacoes.remove('')
    f.close()

    token = acess.forceRequestToken()
    for estacao in estacoes:
        try:
            request = acess.requestTelemetricaDetalhada(int(estacao), dataAtual, token)
        except:
            token = acess.forceRequestToken()
            request = acess.requestTelemetricaDetalhada(int(estacao), dataAtual, token)
        novoArquivo = 'resultados\\{}-Detalhada.txt'.format(estacao)
        cria_detalhada(novoArquivo)
        dados = decodeRequestDetalhada(request)
        atualiza_detalhada(novoArquivo, dados)
        # atualiza_detalhada(novoArquivo, dados)

def solicitarEstacaoAdotada(dataAtual, pathEstacoes):
    acess = Acess()
    acess.lerCredenciais()

    f = open(pathEstacoes, 'r')
    estacoes = f.read().split('\n')
    estacoes.remove('')
    f.close()

    token = acess.forceRequestToken()
    for estacao in estacoes:
        try:
            request = acess.requestTelemetricaAdotada(int(estacao), dataAtual, token)
        except:
            token = acess.forceRequestToken()
            request = acess.requestTelemetricaAdotada(int(estacao), dataAtual, token)
        novoArquivo = 'resultados\\{}-Adotada.txt'.format(estacao)
        cria_adotada(novoArquivo)
        dados = decodeRequestAdotada(request)
        atualiza_adotada(novoArquivo, dados)

def solicitarPeriodoAdotada(dataComeco, dataFinal, pathEstacoes):
    acess = Acess()
    acess.lerCredenciais()

    f = open(pathEstacoes, 'r')
    estacoes = f.read().split('\n')
    estacoes.remove('')
    f.close()
    while(dataComeco != dataFinal):



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

        elif(entradaUser==3): #solicitar um dia para todas as estacoes (Detalhadas)
            dataComeco = unicaData()
            solicitarEstacaoDetalhada(dataComeco, pathEstacoes)
        elif(entradaUser==4):
            dataComeco = unicaData()
            solicitarEstacaoAdotada(dataComeco, pathEstacoes)

        elif(entradaUser==5):
            pass
        elif(entradaUser==6):
            pass
        else:
            pass
if __name__ == "__main__":
    main()