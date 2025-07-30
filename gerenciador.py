from hidroaccess.access import Access
from manipulacaoArquivos import *

def _lista_estacoes(pathEstacoes) -> list:
    arquivo = open(pathEstacoes, 'r')
    listaEstacoes = arquivo.read().split('\n')
    try:
        listaEstacoes.remove('')
    except:
        pass
    arquivo.close()
    return listaEstacoes

def solicitar_estacoes(stringComeco: str, stringFinal: str, pathEstacoes: str, pathConfigs: 
    str, tipo: str, qtdDownloadAsync: int, pathDownload: str):
    credenciais = le_credenciais_ana(pathConfigs)
    sessao = Access(credenciais[0], credenciais[1])
    estacoes = _lista_estacoes(pathEstacoes)

    for estacao in estacoes:
        caminhoArquivo = f'{pathDownload}\\{estacao}-{tipo}-{stringComeco}-{stringFinal}.txt'
        cria_arquivo_resultado(caminhoArquivo, tipo)

        token = sessao.safe_request_token()

        if tipo == 'Adotada' or tipo == 'Detalhada':
            listaDicionario = sessao.request_telemetrica(int(estacao), stringComeco, stringFinal, token, tipo, qtdDownloadAsync)    
        elif tipo == 'Cota':
            listaDicionario = sessao.request_cota(int(estacao), stringComeco, stringFinal, token, qtdDownloadAsync)
        elif tipo == 'Sedimentos':
            listaDicionario = sessao.request_sedimentos(int(estacao), stringComeco, stringFinal, token, qtdDownloadAsync)
        elif tipo == 'Chuva':
            listaDicionario = sessao.request_chuva(int(estacao), stringComeco, stringFinal, token, qtdDownloadAsync)

        atualizar_arquivo_resultado(caminhoArquivo, listaDicionario, tipo)