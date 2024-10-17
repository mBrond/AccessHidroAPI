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

def solicitar_atualizacao_credenciais_ana(pathConfigs):
    novosDadosDict = interfaceCredenciais()
    atualiza_credenciais_ana(pathConfigs, novosDadosDict)

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
        novoArquivo = 'resultados\\{}-Detalhada-{}.txt'.format(estacao, dataAtual)
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
        novoArquivo = 'resultados\\{}-Adotada-{}.txt'.format(estacao, dataAtual)
        cria_adotada(novoArquivo)
        dados = decodeRequestAdotada(request.content)
        atualiza_adotada(novoArquivo, dados)

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

def solicitar_leitura_credenciais_ana(pathConfigs):
    credenciaisAna = le_credenciais_ana(pathConfigs)['Credenciais']['Ana']
    print(f'\nId:{credenciaisAna['Identificador']}\nSenha: {credenciaisAna['Senha']}')

def main():
    pathConfigs = 'configs.json'
    pathResultados = 'resultados'
    inicializacao.inicializacao_basico(pathConfigs, pathResultados)

    interfaceVersao()

    pathEstacoes = 'estacoes.txt'
    
    entradaUser = 9
    while(entradaUser!=0):
        interfaceMenu()
        entradaUser = int(input())
        if(entradaUser==1):
            solicitar_atualizacao_credenciais_ana(pathConfigs)

        elif(entradaUser==2):
            operacao = interfaceOperacaoEstacao()
            escreverEstacoes(pathEstacoes, operacao, estacoes=interfaceSolicitarEstacoes())

        elif(entradaUser==3): #solicitar um dia para todas as estacoes (Detalhadas)
            stringComeco = unicaData()
            if(stringComeco):
                solicitarEstacaoDetalhada(stringComeco, pathEstacoes)
            else:
                interfaceDataInvalida()

        elif(entradaUser==4):
            stringComeco = unicaData()
            if(stringComeco):
                solicitarEstacaoAdotada(stringComeco, pathEstacoes)
            else:
                interfaceDataInvalida()

        elif(entradaUser==5):
            stringComeco, stringFinal = datasComecoFinal()
            solicitarPeriodoAsyncDetalhada(stringComeco, stringFinal, pathEstacoes)

        elif(entradaUser==6):
            stringComeco, stringFinal = datasComecoFinal()
            solicitarPeriodoAsyncAdotada(stringComeco, stringFinal, pathEstacoes)
        
        elif(entradaUser==7):
            solicitar_leitura_credenciais_ana(pathConfigs)

        else:
            pass
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("HOUVE ERRO NA EXECUCAO DO SISTEMA")
        print(e)
        input()