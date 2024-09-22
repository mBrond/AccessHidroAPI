import json
import os
from datetime import datetime, timedelta
import inicializacao
from acess import *
from interfaces import *
from manipulacaoArquivos import *

def _listaEstacoes(pathEstacoes) -> list:
    f = open(pathEstacoes, 'r')
    estacoes = f.read().split('\n')
    try:
        estacoes.remove('')
    except:
        pass
    f.close()
    return estacoes

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
        dados = decodeRequestDetalhada(request.content)
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
        dados = decodeRequestAdotada(request.content)
        atualiza_adotada(novoArquivo, dados)

def solicitarPeriodoAdotada(dataComeco, dataFinal, pathEstacoes):
    acess = Acess()
    acess.lerCredenciais()

    estacoes = _listaEstacoes(pathEstacoes)

    for estacao in estacoes:
        novoArquivo = 'resultados\\{}-Adotada-{}-{}.txt'.format(estacao, dataComeco, dataFinal)
        cria_adotada(novoArquivo)
        
        token = acess.forceRequestToken()
        
        dataAtual = datetime.datetime.strptime(dataComeco, "%Y-%m-%d")
        dataFinal = datetime.datetime.strptime(dataFinal, "%Y-%m-%d")
        
        while(dataAtual != dataFinal):
            try:
                request = acess.requestTelemetricaAdotada(int(estacao), dataAtual, token)
            except:
                token = acess.forceRequestToken()
                request = acess.requestTelemetricaAdotada(int(estacao), dataAtual, token)
            dados = decodeRequestAdotada(request.content)
            atualiza_adotada(novoArquivo, dados)
            dataAtual = dataAtual + timedelta(days=1)

def solicitarPeriodoDetalhada(dataComeco, dataFinal, pathEstacoes):
    acess = Acess()
    acess.lerCredenciais()

    estacoes = _listaEstacoes(pathEstacoes)

    for estacao in estacoes:
        novoArquivo = 'resultados\\{}-Detalhada-{}-{}.txt'.format(estacao, dataComeco, dataFinal)
        cria_detalhada(novoArquivo)
        
        token = acess.forceRequestToken()
        
        dataAtual = datetime.datetime.strptime(dataComeco, "%Y-%m-%d")
        dataFinal = datetime.datetime.strptime(dataFinal, "%Y-%m-%d")
        
        while(dataAtual != dataFinal):
            try:
                request = acess.requestTelemetricaDetalhada(int(estacao), dataAtual, token)
            except:
                token = acess.forceRequestToken()
                request = acess.requestTelemetricaDetalhada(int(estacao), dataAtual, token)
            dados = decodeRequestAdotada(request.content)
            atualiza_adotada(novoArquivo, dados)
            dataAtual = dataAtual + timedelta(days=1)

def solicitarPeriodoAsyncAdotada(stringComeco: str, stringFinal: str, pathEstacoes):
    acess = Acess()
    acess.lerCredenciais()

    estacoes = _listaEstacoes(pathEstacoes)

    for estacao in estacoes:
        novoArquivo = 'resultados\\{}-Adotada-{}-{}.txt'.format(estacao, stringComeco, stringFinal)
        cria_adotada(novoArquivo)

        headers = {'Authorization': 'Bearer {}'.format(acess.forceRequestToken())}

        ListalistaRespostas = asyncio.run(acess.requestTelemetricaAdotadaAsync(int(estacao), stringComeco, stringFinal, headers))
    
        for listaResposta in ListalistaRespostas:
            for resposta in listaResposta:
                dado = decodeRequestAdotada(resposta)
                atualiza_adotada(novoArquivo, dado)

def solicitarPeriodoAsyncDetalhada(stringComeco: str, stringFinal: str, pathEstacoes):
    acess = Acess()
    acess.lerCredenciais()

    estacoes = _listaEstacoes(pathEstacoes)

    for estacao in estacoes:
        novoArquivo = 'resultados\\{}-Detalhada-{}-{}.txt'.format(estacao, stringComeco, stringFinal)
        cria_detalhada(novoArquivo)

        headers = {'Authorization': 'Bearer {}'.format(acess.forceRequestToken())}

        ListalistaRespostas = asyncio.run(acess.requestTelemetricaDetalhadaAsync(int(estacao), stringComeco, stringFinal, headers))
    
        for listaResposta in ListalistaRespostas:
            for resposta in listaResposta:
                dado = decodeRequestDetalhada(resposta)
                atualiza_detalhada(novoArquivo, dado)

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
            stringComeco = unicaData()
            solicitarEstacaoDetalhada(stringComeco, pathEstacoes)

        elif(entradaUser==4):
            stringComeco = unicaData()
            solicitarEstacaoAdotada(stringComeco, pathEstacoes)

        elif(entradaUser==5):
            stringComeco, stringFinal = datasComecoFinal()
            solicitarPeriodoAsyncDetalhada(stringComeco, stringFinal, pathEstacoes)

        elif(entradaUser==6):
            stringComeco, stringFinal = datasComecoFinal()
            solicitarPeriodoAsyncAdotada(stringComeco, stringFinal, pathEstacoes)

        else:
            pass
if __name__ == "__main__":
    main()